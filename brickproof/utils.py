from brickproof.constants import (
    WORKSPACE_PREFIX,
    TOKEN_PREFIX,
    TOML_TEMPLATE,
    RUNNER_DEF,
)
import tomlkit
import base64


def write_toml(file_path: str):
    with open(file_path, "w") as toml_file:
        toml_file.write(TOML_TEMPLATE)


def read_toml(file_path: str = "./brickproof.toml") -> tomlkit.TOMLDocument:
    with open(file_path, "r") as toml_file:
        return tomlkit.load(fp=toml_file)


def write_profile(file_path: str, profile: str, token: str, workspace: str):
    with open(file_path, "a") as bprc_file:
        bprc_file.write(f"[{profile}]\n")
        bprc_file.write(f"{WORKSPACE_PREFIX}{workspace}\n")
        bprc_file.write(f"{TOKEN_PREFIX}{token}\n")
        bprc_file.write("\n")


def get_profile(file_path: str, profile: str) -> dict:
    with open(file_path, "r") as bprc_file:
        data = bprc_file.readlines()

    for idx, line in enumerate(data):
        if line == f"[{profile}]\n":
            workspace = data[idx + 1].replace("\n", "").replace(WORKSPACE_PREFIX, "")
            token = data[idx + 2].replace("\n", "").replace(TOKEN_PREFIX, "")
            return {"profile": profile, "workspace": workspace, "token": token}

    return {}


def get_runner_bytes(runner: str) -> str:
    if runner == "default":
        runner_bytes = RUNNER_DEF.encode()

    else:
        with open("./brickproof_runner.py", "rb") as runner_file:
            runner_bytes = runner_file.read()

    base64_encoded_data = base64.b64encode(runner_bytes)
    base64_output = base64_encoded_data.decode("utf-8")

    return base64_output
