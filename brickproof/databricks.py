import requests
import constants as c


class DatabricksHandler:
    def __init__(self, workspace_url: str = None, access_token: str = None):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        self.workspace_url = workspace_url

    def list_files(self, workspace_path: str):
        url = f"{self.workspace_url}{c.LIST_WORKSPACE_FILES_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def make_directory(self, workspace_path: str):
        url = f"{self.workspace_url}/{c.CREATE_WORKSPACE_DIR_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def check_for_git_folder(self, workspace_path: str):
        #TODO functionality not completely flushed out yet. fix that!

        url = f"{self.url}/{c.GET_REPOS_ENDPOINT}"
        params = {"path": workspace_path}
        response = requests.get(url=url, params=params, headers=self.headers)

        return response

    def create_git_folder(self, git_payload: dict):
        url = f"{self.url}/{c.CREATE_REPO_ENDPOINT}"
        response = requests.post(url=url,data=git_payload,headers=self.headers)
        return response

    def remove_git_folder(self, repo_id: str):

        url = f"{self.workspace_url}/{c.CREATE_REPO_ENDPOINT}/{repo_id}"
        response = requests.delete(url=url, headers=self.headers)
        return response

    def create_job(self):
        pass

    def run_job(self):
        pass

    def check_job(self):
        pass

    def remove_job(self):
        pass
