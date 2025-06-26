from pydantic import BaseModel
from enum import Enum


class GitProviders(Enum):
    GITHUB = "gitHub"
    GITLAB = "gitLab"
    BITBUCKET_CLOUD = "bitbucketCloud"
    GITHUB_ENTERPRISE = "gitHubEnterprise"
    BITBUCKET_SERVER = "bitbucketServer"
    AZURE_DEVOPS = "azureDevOpsServices"
    AWS_CODE_COMMIT = "awsCodeCommit"
    GITLAB_ENTERPRISE = "gitLabEnterpriseEdition"


class RepoConfig(BaseModel):
    name: str
    workspace_path: str
    git_provider: GitProviders
    git_repo: str
    branch: str


class JobConfig(BaseModel):
    job_name: str
    task_key: str
    dependencies: list[str]
    runner: str


class Config(BaseModel):
    repo: RepoConfig
    job: JobConfig

    def write_to_toml(self):
        toml_string = f"""[repo]
name = "{self.repo.name}"
workspace_path = "{self.repo.workspace_path}"
git_provider = "{self.repo.git_provider.value}"
git_repo = "{self.repo.git_repo}"
branch = "{self.repo.branch}"

[job]
job_name = "{self.job.job_name}"
task_key = "{self.job.task_key}"
dependencies = [{",".join([f'"{dependecy}"' for dependecy in self.job.dependencies])}]
runner = "{self.job.runner}"
"""
        with open("./brickproof.toml", "w") as tfile:
            tfile.write(toml_string)
