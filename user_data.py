name_user = "VictorKazankov"
token_user = "<your token for 1-th user>"  # main user
headers = {"Authorization": f"Bearer {token_user}", "Accept": "application/vnd.github+json"}
repository = "LearnQA_PythonAPI"

another_user_token = "<your token for 2-th user>"  # use for approve
headers_for_another_user = {"Authorization": f"Bearer {another_user_token}", "Accept": "application/vnd.github+json"}
