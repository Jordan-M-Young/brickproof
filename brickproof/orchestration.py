from brickproof.databricks import DatabricksHandler
from brickproof.utils import (
    get_profile,
    load_config,
    get_runner_bytes,
    format_pytest_result,
)
import brickproof.constants as c
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class RunOrchestrator:
    def __init__(self, config_file_path: str, profile: str, verbose: bool = False):
        self.db_config = get_profile(file_path=config_file_path, profile=profile)
        self.project_config = load_config()

        # initialize databricks client
        self.handler = DatabricksHandler(
            workspace_url=self.db_config["workspace"],
            access_token=self.db_config["token"],
        )
        self.verbose = verbose

        if self.verbose:
            logger.setLevel(logging.INFO)

        self.repo_path = f"{self.project_config.repo.workspace_path}/{c.TESTING_DIRECTORY}/{self.project_config.repo.name}"

    def get_repos(self) -> dict:
        # check for git repo in brickproof testing directory
        logger.info(self.repo_path)
        r = self.handler.check_for_git_folder(self.repo_path)
        repos = r.json()
        return repos

    def check_for_repo(self, repos: dict) -> tuple[bool, str]:
        # check if the configured git repo exists in databricks
        git_repo_exists = False
        repo_id = ""
        for repo in repos.get("repos", []):
            logger.info(self.repo_path, f"/Workspace{repo['path']}")

            # if it does, grab it's id.
            if f"/Workspace{repo['path']}" == self.repo_path:
                git_repo_exists = True
                repo_id = repo["id"]

                break

        return git_repo_exists, repo_id

    def clone_repo(self) -> str:
        git_payload = {
            "branch": self.project_config.repo.branch,
            "path": self.repo_path,
            "provider": self.project_config.repo.git_provider.value,
            "url": self.project_config.repo.git_repo,
        }
        r = self.handler.create_git_folder(git_payload=git_payload)
        git_data = r.json()
        repo_id = git_data["id"]
        return repo_id

    def checkout_branch(self, repo_id: str):
        checkout_payload = {"branch": self.project_config.repo.branch}
        r = self.handler.checkout_branch(
            checkout_payload=checkout_payload, repo_id=repo_id
        )
        logger.info("CHECKOUT", r.text)

    def delete_repo(self, repo_id: str):
        # delete repo
        r = self.handler.remove_git_folder(repo_id=repo_id)
        logger.info("REMOVE", r.text)

    def create_job(self) -> str:
        runner_upload_path = f"{self.repo_path}/brickproof_runner.py"

        # create job
        job_payload = {
            "environments": [
                {
                    "environment_key": "default_python",
                    "spec": {
                        "client": "1",
                        "dependencies": self.project_config.job.dependencies,
                    },
                }
            ],
            "format": "SINGLE_TASK",
            "max_concurrent_runs": 1,
            "name": f"{self.project_config.repo.name}-Tests",
            "tasks": [
                {
                    "notebook_task": {"notebook_path": runner_upload_path},
                    "task_key": f"{self.project_config.job.task_key}-Unittests",
                }
            ],
        }
        r = self.handler.create_job(job_payload=job_payload)
        job = r.json()
        job_id = job["job_id"]

        return job_id

    def trigger_job(self, job_id: str) -> str:
        job_payload = {"job_id": job_id}
        r = self.handler.trigger_job(job_payload=job_payload)
        job_run = r.json()
        run_id = job_run["run_id"]
        logger.info(job_run)

        return run_id

    def monitor_run(self, run_id: str):
        start = time.time()
        success = False
        while True:
            # monitor job
            query_params = {
                "run_id": run_id,
            }
            r = self.handler.check_job(query_params=query_params)
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

        logger.info("SUCCESS", success)
        logger.info(state)

        return state

    def final_job_check(self, run_id: str) -> str:
        query_params = {
            "run_id": run_id,
        }

        r = self.handler.check_job(query_params=query_params)
        status = r.json()
        logger.info("FINAL", status)
        tasks = status["tasks"]
        task = tasks[0]
        task_id = task["run_id"]

        return task_id

    def get_job_result(self, task_id: str) -> int:
        query_params = {"run_id": task_id}
        r = self.handler.get_job_output(query_params=query_params)
        output = r.json()
        logger.info("OUPUT", output)
        if output.get("notebook_output", {}).get("result"):
            exit_message = output["notebook_output"]["result"]
            exit_code, test_report = format_pytest_result(exit_message)
            print(int(exit_code.split("=")[-1]))
            print(test_report)
            exit_code = int(exit_code.split("=")[-1])
        else:
            print("Notebook Output not found... check runner ")
            exit_code = 1

        return exit_code

    def delete_job(self, job_id: str):
        # delete job
        delete_payload = {"job_id": job_id}

        r = self.handler.remove_job(delete_payload=delete_payload)
        logger.info(r.text)

    def get_workspace_files(self) -> list:
        r = self.handler.list_files(
            workspace_path=self.project_config.repo.workspace_path
        )
        files = r.json()["objects"]
        return files

    def find_brickproof_dir(self, files: list) -> bool:
        # check for a brickproof testing directory in databricks workspace
        brickproof_testing_dir_exists = False
        for file in files:
            object_name = file["path"].replace(
                self.project_config.repo.workspace_path, ""
            )
            if file["object_type"] == "DIRECTORY" and object_name == ".brickproof-cicd":
                brickproof_testing_dir_exists = True
                break
        return brickproof_testing_dir_exists

    def make_brickproof_dir(self):
        # create brickproof testing directory if it doesnt exist
        brick_proof_testing_dir = f"{self.db_config['workspace']}/{c.TESTING_DIRECTORY}"
        r = self.handler.make_directory(directory_path=brick_proof_testing_dir)
        logger.info(r.text)

    def check_for_runner(self) -> bool:
        # check for runner
        r = self.handler.list_files(workspace_path=self.repo_path)
        repo_objects = r.json()
        runner_exists = False
        for object in repo_objects.get("objects", []):
            if object["path"] == f"{self.repo_path}/brickproof_runner.py":
                runner_exists = True
                break
        return runner_exists

    def upload_runner(self):
        runner_upload_path = f"{self.repo_path}/brickproof_runner.py"

        content = get_runner_bytes(self.project_config.job.runner)
        upload_paylod = {
            "content": content,
            "format": "SOURCE",
            "language": "PYTHON",
            "overwrite": "true",
            "path": runner_upload_path,
        }
        r = self.handler.upload_file(upload_payload=upload_paylod)
        logger.info(r.text)
