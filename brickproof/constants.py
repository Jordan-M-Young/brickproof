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
dependencies = []
runner = "default"
"""


RUNNER_DEF = """# Databricks notebook source
!pip install pytest
!pip install tomlkit
# COMMAND ----------

dbutils.library.restartPython()


# COMMAND ----------

import pytest
import os
import sys

# COMMAND ----------

# Run all tests in the repository root.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))
os.chdir(f'/Workspace/{repo_root}')
%pwd

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main(["-p", "no:cacheprovider"])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'

# COMMAND ----------
#Exits notebook run with a value we can use for determining success or failure.
dbutils.notebook.exit(retcode)"""
