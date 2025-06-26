from brickproof.constants import (
    WORKSPACE_PREFIX,
    TOKEN_PREFIX,
    TOML_TEMPLATE,
    RUNNER_DEF,
)

from brickproof.config import Config

import tomlkit
import base64


def load_config() -> Config:
    toml_doc = read_toml("./brickproof.toml")
    config = validate_toml(toml_doc)
    return config


def validate_toml(toml_data: tomlkit.TOMLDocument) -> Config:
    validated_config = Config(**toml_data)
    return validated_config


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


def parse_config_edits(vars: list):
    config = load_config()
    dumped_config = config.model_dump()

    for var in vars:
        key, val = var.split("=")
        section, key = key.split(".")
        if key == "dependencies":
            val = val.replace("]", "").replace("[", "").split(",")

        dumped_config[section][key] = val
    x = Config(**dumped_config)
    x.write_to_toml()


def format_pytest_result(result_str: str):
    exit, pytest_report = result_str.split("@@@")
    return exit, pytest_report
