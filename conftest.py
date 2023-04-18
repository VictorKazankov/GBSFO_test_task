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

    # create commit
    libs_folder_tree_sha = "9d1dcfdaf1a6857c5f83dc27019c7600e1ffaff8"
    endpoint_post_commit = f"/repos/{name_user}/{repository}/git/commits"
    commit_data = {"message": "My new commit message",
                   "author": {"name": "Victor Kazankov", "email": "sadovnichi@mail.ru"},
                   "parents": [f"{master_branch_sha}"],
                   "tree": f'{libs_folder_tree_sha}'}
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
