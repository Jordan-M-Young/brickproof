import getpass
from brickproof.constants import (
    WORKSPACE_PROMPT,
    TOKEN_PROMPT,
    PROFILE_PROMPT,
    TESTING_DIRECTORY,
)
from brickproof.utils import (
    write_profile,
    get_profile,
    write_toml,
    get_runner_bytes,
    load_config,
    parse_config_edits,
    format_pytest_result
)

from brickproof.version import VERSION

from brickproof.databricks import DatabricksHandler
import os
import time
import logging


logger = logging.getLogger(__name__)


def version():
    print(f"brickproof-{VERSION}")


def configure():
    workspace = input(WORKSPACE_PROMPT)
    token = getpass.getpass(TOKEN_PROMPT)
    profile = input(PROFILE_PROMPT)

    if not profile:
        profile = "default"

    file_path = "./.bprc"
    write_profile(
        file_path=file_path, profile=profile, token=token, workspace=workspace
    )


def init(toml_path: str):
    if not os.path.isfile(toml_path):
        write_toml(toml_path)
    else:
        print("Project Already Initialized")


def run(profile: str, file_path: str, verbose: bool):
    # config loading

    db_config = get_profile(file_path=file_path, profile=profile)
    project_config = load_config()
    workspace_path = project_config.repo.workspace_path
    repo_name = project_config.repo.name
    runner = project_config.job.runner

    # if verbose flag passed, switch logging level to info
    if verbose:
        logger.setLevel(logging.INFO)

    # initialize databricks client
    handler = DatabricksHandler(
        workspace_url=db_config["workspace"], access_token=db_config["token"]
    )

    # get objects in databricks workspace path
    r = handler.list_files(workspace_path=workspace_path)
    files = r.json()["objects"]

    # check for a brickproof testing directory in databricks workspace
    brickproof_testing_dir_exists = False
    for file in files:
        object_name = file["path"].replace(workspace_path, "")
        if file["object_type"] == "DIRECTORY" and object_name == ".brickproof-cicd":
            brickproof_testing_dir_exists = True

            break

    # create brickproof testing directory if it doesnt exist
    if not brickproof_testing_dir_exists:
        brick_proof_testing_dir = f"{workspace_path}/{TESTING_DIRECTORY}"
        r = handler.make_directory(directory_path=brick_proof_testing_dir)

    # check for git repo in brickproof testing directory
    repo_path = f"{brick_proof_testing_dir}/{repo_name}"
    print(repo_path)
    r = handler.check_for_git_folder(brick_proof_testing_dir)
    repos = r.json()

    # check if the configured git repo exists in databricks
    git_repo_exists = False
    repo_id = None
    for repo in repos.get("repos", []):
        print(repo_path, f"/Workspace{repo['path']}")

        # if it does, grab it's id.
        if f"/Workspace{repo['path']}" == repo_path:
            git_repo_exists = True
            repo_id = repo["id"]

            break

    # if not, create git repo using config from brickproof.toml and get id.
    if not git_repo_exists:
        git_payload = {
            "branch": project_config.repo.branch,
            "path": repo_path,
            "provider": project_config.repo.git_provider.value,
            "url": project_config.repo.git_repo,
        }
        r = handler.create_git_folder(git_payload=git_payload)
        git_data = r.json()
        repo_id = git_data["id"]

    checkout_payload = {"branch":project_config.repo.branch}
    query_params = {"repo_id":repo_id}
    r = handler.checkout_branch(checkout_payload=checkout_payload,repo_id=repo_id)
    print("CHECKOUT", r.text)

    # check for runner
    r = handler.list_files(workspace_path=repo_path)
    repo_objects = r.json()
    runner_exists = False
    for object in repo_objects.get("objects", []):
        if object["path"] == f"{repo_path}/brickproof_runner.py":
            runner_exists = True
            break

    # upload runner to git repo
    runner_upload_path = f"{repo_path}/brickproof_runner.py"

    if not runner_exists:
        content = get_runner_bytes(runner)
        upload_paylod = {
            "content": content,
            "format": "SOURCE",
            "language": "PYTHON",
            "overwrite": "true",
            "path": runner_upload_path,
        }
        r = handler.upload_file(upload_payload=upload_paylod)

    # create job
    job_payload = {
        "environments": [
            {
                "environment_key": "default_python",
                "spec": {
                    "client": "1",
                    "dependencies": project_config.job.dependencies,
                },
            }
        ],
        "format": "SINGLE_TASK",
        "max_concurrent_runs": 1,
        "name": f"{repo_name}-Tests",
        "tasks": [
            {
                "notebook_task": {"notebook_path": runner_upload_path},
                "task_key": f"{repo_name}-Unittests",
            }
        ],
    }
    r = handler.create_job(job_payload=job_payload)
    job = r.json()
    job_id = job["job_id"]
    # trigger job

    job_payload = {"job_id": job_id}
    r = handler.trigger_job(job_payload=job_payload)
    job_run = r.json()
    run_id = job_run["run_id"]
    logger.info(job_run)
    start = time.time()
    success = False
    while True:
        # monitor job
        query_params = {
            "run_id": run_id,
        }
        r = handler.check_job(query_params=query_params)
        status = r.json()
        state = status["state"]
        print("CHECK", state)

        time.sleep(1)
        if time.time() - start > 100:
            break

        result_state = state.get("result_state")
        if not result_state:
            continue

        if result_state == "SUCCESS":
            success = True
        break

    print("SUCCESS", success)
    print(state)
    r = handler.check_job(query_params=query_params)
    status = r.json()
    print("FINAL",status)
    tasks = status['tasks']
    task = tasks[0]
    task_id = task["run_id"]



    query_params = {
        "run_id":task_id
    }
    r = handler.get_job_output(query_params=query_params)
    output = r.json()
    print("OUPUT",output)


    if output.get("notebook_output",{}).get("result"):
        exit_message = output['notebook_output']['result']
        exit_code, test_report = format_pytest_result(exit_message)
        print(int(exit_code.split("=")[-1]))
        print(test_report)
        exit_code = int(exit_code.split("=")[-1])
    else:
        print("Notebook Output not found... check runner ")
        exit_code = 1


    if exit_code == 0:
        # delete job
        delete_payload = {"job_id": job_id}

        r = handler.remove_job(delete_payload=delete_payload)
        print(r.text)


    # delete repo
    r = handler.remove_git_folder(repo_id=repo_id)
    print("REMOVE", r.text)

    return exit_code


def edit(vars: list):
    parse_config_edits(vars)
    return 0
