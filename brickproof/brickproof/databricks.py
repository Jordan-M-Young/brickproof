import requests
import brickproof.constants as c


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

    def make_directory(self, workspace_path: str):
        url = f"{self.workspace_url}/{c.CREATE_WORKSPACE_DIR_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def check_for_git_folder(self, workspace_path: str) -> requests.Response:
        # TODO functionality not completely flushed out yet. fix that!

        url = f"{self.url}/{c.GET_REPOS_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def create_git_folder(self, git_payload: dict) -> requests.Response:
        url = f"{self.url}/{c.CREATE_REPO_ENDPOINT}"
        response = requests.post(url=url, data=git_payload, headers=self.headers)
        return response

    def remove_git_folder(self, repo_id: str) -> requests.Response:
        url = f"{self.workspace_url}/{c.CREATE_REPO_ENDPOINT}/{repo_id}"
        response = requests.delete(url=url, headers=self.headers)
        return response

    def create_job(self, job_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.CREATE_JOB_ENDPOINT}"
        response = requests.post(url=url, data=job_payload, headers=self.headers)
        return response

    def trigger_job(self):

        pass

    def check_job(self):
        pass

    def remove_job(self):
        pass

    def upload_runner(self, upload_payload: dict) -> requests.Response:
        url = f"{self.workspace_url}/{c.UPLOAD_FILE_ENDPOINT}"
        response = requests.post(url=url, data=upload_payload, headers=self.headers)
        return response


    def one_off_submission(self, payload: dict) -> requests.Response:
        #Experimental, could be helpful!
        url = f"{self.workspace_url}/{c.ONE_OFF_SUBMISSION}"
        response = requests.post(url=url,data=payload,headers=self.headers)
        return response