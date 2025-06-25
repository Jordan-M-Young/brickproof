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
