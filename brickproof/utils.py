from brickproof.constants import (
    WORKSPACE_PREFIX,
    TOKEN_PREFIX,
    TOML_TEMPLATE,
    RUNNER_DEF,
)

from brickproof.config import Config

import tomlkit
import base64
import os


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
    profile_exists = False
    if os.path.isfile(file_path):
        with open(file_path, "r") as bprc_file:
            data = bprc_file.readlines()
            for idx, line in enumerate(data):
                print(line)
                if line == f"[{profile}]\n":
                    profile_exists = True
                    data[idx + 1] = f"{WORKSPACE_PREFIX}{workspace}\n"
                    data[idx + 2] = f"{TOKEN_PREFIX}{token}\n"
                    break

    if not profile_exists:
        with open(file_path, "a") as bprc_file:
            bprc_file.write(f"[{profile}]\n")
            bprc_file.write(f"{WORKSPACE_PREFIX}{workspace}\n")
            bprc_file.write(f"{TOKEN_PREFIX}{token}\n")
            bprc_file.write("\n")
    else:
        with open(file_path, "w") as bprc_file:
            bprc_file.writelines(data)


def get_profile(file_path: str, profile: str) -> dict:
    with open(file_path, "r") as bprc_file:
        data = bprc_file.readlines()

    for idx, line in enumerate(data):
        if line == f"[{profile}]\n":
            workspace = data[idx + 1].replace("\n", "").replace(WORKSPACE_PREFIX, "")
            token = data[idx + 2].replace("\n", "").replace(TOKEN_PREFIX, "")
            return {"profile": profile, "workspace": workspace, "token": token}

    return {}


def insert_ignore_statement(runner_str: str, ignore: list[str], repo_name: str) -> str:
    ignore_statement = ""
    if ignore:

        ignore_statement = [f'"--ignore={item.replace(".",repo_name,1)}"' for item in ignore]
        ignore_statement = "," + ",".join(ignore_statement)

    runner_str = runner_str.replace("{ignore}", ignore_statement)

    return runner_str


def insert_dependencies(runner_str: str, requirements: list[str]) -> str:
    requirements_statement = ""
    if requirements:
        requirements_statement = [item for item in requirements]
        requirements_statement = "!pip install pytest " + " ".join(requirements_statement)

    runner_str = runner_str.replace("{requirements}", requirements_statement)

    return runner_str


def get_runner_bytes(runner: str, ignore: list[str], requirements: list[str], repo_name: str) -> str:
    if runner == "default":
        runner_str = RUNNER_DEF
        runner_str = insert_ignore_statement(runner_str, ignore, repo_name)
        runner_str = insert_dependencies(runner_str, requirements)
        runner_bytes = runner_str.encode()

    else:
        with open("./brickproof_runner.py", "r") as runner_file:
            runner_str = runner_file.read()
            runner_str = insert_ignore_statement(runner_str, ignore, repo_name)
            runner_str = insert_dependencies(runner_str, requirements)

            runner_bytes = runner_str.encode()

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
