# databricks endpoints
LIST_WORKSPACE_FILES_ENDPOINT = "/api/2.0/workspace/list"
CREATE_WORKSPACE_DIR_ENDPOINT = "/api/2.0/workspace/mkdirs"
GET_REPOS_ENDPOINT = "/api/2.0/repos"
CREATE_REPO_ENDPOINT = "/api/2.0/repos"
UPLOAD_FILE_ENDPOINT = "/api/2.0/workspace/import"
CREATE_JOB_ENDPOINT = "/api/2.2/jobs/create"
TRIGGER_JOB_ENDPOINT = "/api/2.2/jobs/run-now"
GET_RUN_ENDPOINT = "/api/2.2/jobs/runs/get"
GET_RUN_OUTPUT = "/api/2.2/jobs/runs/get-output"
ONE_OFF_SUBMISSION = "/api/2.2/jobs/runs/submit"
REMOVE_JOB_RUN_ENDPOINT = "/api/2.2/jobs/runs/delete"
REMOVE_JOB_ENDPOINT = "/api/2.2/jobs/delete"


# cli constants
WORKSPACE_PROMPT = "Please enter your workspace url like: https://XXX-XXXXXXXX-XXXX.cloud.databricks.com: "
TOKEN_PROMPT = "Please enter your Personal Access Token (PAT): "
PROFILE_PROMPT = (
    "Please enter a profile name, if not input provided 'default' will be selected: "
)


# databricks workspace constants
TESTING_DIRECTORY = ".brickproof_testing"


# bprc
TOKEN_PREFIX = "token="
WORKSPACE_PREFIX = "workspace="


# brickproof toml
TOML_TEMPLATE = """[repo]
name = "test"
workspace_path = ""
git_provider = ""
git_repo = ""
branch = ""


[job]
notebook_path = ""
job_name = ""
task_key = ""
dependencies = []"""
