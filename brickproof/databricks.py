import requests
import brickproof.constants as c
import json


class DatabricksHandler:
    def __init__(self, workspace_url: str = None, access_token: str = None):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        self.workspace_url = workspace_url

    def list_files(self, workspace_path: str) -> requests.Response:
        url = f"{self.workspace_url}{c.LIST_WORKSPACE_FILES_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def make_directory(self, directory_path: str):
        url = f"{self.workspace_url}/{c.CREATE_WORKSPACE_DIR_ENDPOINT}"
        params = {"path": directory_path}
        response = requests.post(url=url, data=json.dumps(params), headers=self.headers)

        return response

    def check_for_git_folder(self, git_folder_path: str) -> requests.Response:
        # TODO functionality not completely flushed out yet. fix that!

        url = f"{self.workspace_url}{c.GET_REPOS_ENDPOINT}"
        params = {"path_prefix": git_folder_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def create_git_folder(self, git_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.CREATE_REPO_ENDPOINT}"
        response = requests.post(
            url=url, data=json.dumps(git_payload), headers=self.headers
        )
        return response

    def checkout_branch(
        self, checkout_payload: dict, repo_id: str
    ) -> requests.Response:
        url = f"{self.workspace_url}/{c.CHECKOUT_ENDPOINT}/{repo_id}"
        response = requests.patch(
            url=url, data=json.dumps(checkout_payload), headers=self.headers
        )
        return response

    def remove_git_folder(self, repo_id: str) -> requests.Response:
        url = f"{self.workspace_url}/{c.CREATE_REPO_ENDPOINT}/{repo_id}"
        response = requests.delete(url=url, headers=self.headers)
        return response

    def create_job(self, job_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.CREATE_JOB_ENDPOINT}"
        response = requests.post(
            url=url, data=json.dumps(job_payload), headers=self.headers
        )
        return response

    def trigger_job(self, job_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.TRIGGER_JOB_ENDPOINT}"
        response = requests.post(
            url=url, data=json.dumps(job_payload), headers=self.headers
        )
        return response

    def check_job(self, query_params: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.GET_RUN_ENDPOINT}"
        response = requests.get(url=url, params=query_params, headers=self.headers)
        return response

    def get_job_output(self, query_params: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.GET_RUN_OUTPUT}"
        response = requests.get(url=url, params=query_params, headers=self.headers)
        return response

    def remove_job_run(self, delete_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.REMOVE_JOB_RUN_ENDPOINT}"
        response = requests.post(url=url, data=delete_payload, headers=self.headers)
        return response

    def remove_job(self, delete_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.REMOVE_JOB_ENDPOINT}"
        response = requests.post(
            url=url, data=json.dumps(delete_payload), headers=self.headers
        )
        return response

    def upload_file(self, upload_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.UPLOAD_FILE_ENDPOINT}"
        response = requests.post(
            url=url, data=json.dumps(upload_payload), headers=self.headers
        )
        return response

    def one_off_submission(self, payload: dict) -> requests.Response:
        # Experimental, could be helpful!
        url = f"{self.workspace_url}/{c.ONE_OFF_SUBMISSION}"
        response = requests.post(url=url, data=payload, headers=self.headers)
        return response
