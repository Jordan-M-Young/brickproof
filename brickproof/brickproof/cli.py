import getpass
from brickproof.constants import WORKSPACE_PROMPT, TOKEN_PROMPT, PROFILE_PROMPT
from brickproof.utils import write_profile, get_profile, write_toml
from brickproof.databricks import DatabricksHandler
import os

def version():
    print("brickproof-v0.0.0")
    
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


def run(profile: str, file_path: str):

    config = get_profile(file_path=file_path, profile=profile)

    handler = DatabricksHandler(
        workspace_url=config["workspace"], access_token=config["token"]
    )

    handler.check_for_git_folder()
