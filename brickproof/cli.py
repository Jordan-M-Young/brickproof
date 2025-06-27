import getpass
from brickproof.constants import (
    WORKSPACE_PROMPT,
    TOKEN_PROMPT,
    PROFILE_PROMPT,
)
from brickproof.utils import (
    write_profile,
    write_toml,
    parse_config_edits,
)

from brickproof.version import VERSION

from brickproof.orchestration import RunOrchestrator
import os
import logging


logger = logging.getLogger(__name__)


def version() -> str:
    return f"brickproof-{VERSION}"


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
    orchestrator = RunOrchestrator(
        config_file_path=file_path, profile=profile, verbose=verbose
    )

    files = orchestrator.get_workspace_files()

    brickproof_testing_dir_exists = orchestrator.find_brickproof_dir(files)

    # create brickproof testing directory if it doesnt exist
    if not brickproof_testing_dir_exists:
        orchestrator.make_brickproof_dir()

    # check for git repo in brickproof testing directory
    repos = orchestrator.get_repos()

    # check if the configured git repo exists in databricks
    git_repo_exists, repo_id = orchestrator.check_for_repo(repos)

    # if not, create git repo using config from brickproof.toml and get id.
    if not git_repo_exists:
        repo_id = orchestrator.clone_repo()

    # checkout branch
    orchestrator.checkout_branch(repo_id)

    # check for runner
    runner_exists = orchestrator.check_for_runner()

    # upload runner to git repo
    if not runner_exists:
        orchestrator.upload_runner()

    # create job
    job_id = orchestrator.create_job()

    # trigger job
    run_id = orchestrator.trigger_job(job_id=job_id)

    # monitor running job
    _state = orchestrator.monitor_run(run_id=run_id)

    # check finished job
    task_id = orchestrator.final_job_check(run_id=run_id)

    # get job result
    exit_code = orchestrator.get_job_result(task_id=task_id)

    if exit_code == 0:
        # delete job
        orchestrator.delete_job(job_id=job_id)

    # delete repo
    orchestrator.delete_repo(repo_id=repo_id)

    return exit_code


def edit(vars: list):
    parse_config_edits(vars)
    return 0
