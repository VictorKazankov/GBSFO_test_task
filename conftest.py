from pytest import fixture

from user_data import repository, headers, name_user
from helpers.utils import random_string, json_to_python_object
from libs.api import ApiService


@fixture
def create_branch_with_commit():
    # getting sha for main branch
    endpoint_get = f'/repos/{name_user}/{repository}/git/refs/heads/main'
    response_get = ApiService.get(endpoint=endpoint_get, headers=headers)
    master_branch_sha = json_to_python_object(response_get)["object"]["sha"]

    # create commit mode tree based of tree pattern
    endpoint_post_tree = f"/repos/{name_user}/{repository}/git/trees"
    tree_pattern = "4316b68b11ab431307510b4c4169e097058b2267"  # lib folder sha
    tree_data = {"tree": [{"path": "new_submodule", "mode": "160000", "type": "commit", "sha": f"{tree_pattern}"}]}
    response_post_tree = ApiService.post(endpoint=endpoint_post_tree, headers=headers, data=tree_data)
    sha_tree = json_to_python_object(response_post_tree)["sha"]

    # create commit
    endpoint_post_commit = f"/repos/{name_user}/{repository}/git/commits"
    commit_data = {"message": "My new commit message",
                   "author": {"name": "Victor Kazankov", "email": "sadovnichi@mail.ru"},
                   "parents": [f"{master_branch_sha}"],
                   "tree": f'{sha_tree}'}
    response_post_commit = ApiService.post(endpoint=endpoint_post_commit, headers=headers, data=commit_data)
    sha_commit = json_to_python_object(response_post_commit)["sha"]

    # create new branch with commit
    new_branch = f'new_branch_{random_string}'

    endpoint_post_branch = f"/repos/{name_user}/{repository}/git/refs"
    branch_data = {
        "ref": f'refs/heads/{new_branch}',
        "sha": f'{sha_commit}'
    }
    ApiService.post(endpoint=endpoint_post_branch, headers=headers, data=branch_data)

    yield new_branch

    # delete branch

    endpoint_del_branch = f"/repos/{name_user}/{repository}/git/refs/heads/{new_branch}"
    ApiService.delete(endpoint=endpoint_del_branch, headers=headers)


@fixture()
def create_pull_request(create_branch_with_commit):
    new_branch_name = create_branch_with_commit
    pull_request_data = {
        'title': f'New_PR_{random_string}',
        'body': 'Please pull this in!',
        'head': f'{new_branch_name}',
        'base': 'main'
    }
    endpoint = f"/repos/{name_user}/{repository}/pulls"
    response_post = ApiService.post(endpoint=endpoint, headers=headers, data=pull_request_data)
    response_text = json_to_python_object(response_post)
    yield response_text["number"]  # return PR number
