# from brickproof.databricks import DatabricksHandler
# from brickproof.utils import load_config, get_profile


# def test_list_files():
#     db_config = get_profile(file_path="./.bprc", profile="default")
#     project_config = load_config()

#     handler = DatabricksHandler(
#         workspace_url=db_config["workspace"], access_token=db_config["token"]
#     )

#     response = handler.list_files(project_config.repo.workspace_path)
#     response_paylod = response.json()

#     assert isinstance(response_paylod, dict)


# def test_list_files_fail():
#     db_config = get_profile(file_path="./.bprc", profile="default")
#     project_config = load_config()

#     handler = DatabricksHandler(
#         workspace_url=db_config["workspace"], access_token=db_config["token"]
#     )

#     response = handler.list_files("/workspace/doesnt/exist")
#     assert response.status_code == 404
