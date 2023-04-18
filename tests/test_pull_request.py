from data import name_user, repository, headers
from helpers.assertions import Assertions
from helpers.utils import random_string
from libs.api import ApiService

expected_pull_requests = ["Created PR-1", "Created PR-2"]

endpoint = f"/repos/{name_user}/{repository}/pulls"


class TestPullRequests:
    def test_get_all_pull_requests(self):
        response = ApiService.get(endpoint=endpoint, headers=headers)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_name_pull_requests(response, expected_pull_requests)

    def test_create_pull_request(self, create_branch_with_commit):
        new_branch_name = create_branch_with_commit
        pull_request_data = {
            'title': f'New_PR_{random_string}',
            'body': 'Please pull this in!',
            'head': f'{new_branch_name}',
            'base': 'main'
        }
        response_post = ApiService.post(endpoint=endpoint, headers=headers, data=pull_request_data)
        Assertions.assert_code_status(response_post, 201)

        response_get = ApiService.get(endpoint=endpoint, headers=headers)  # for get all PRs
        Assertions.assert_present_pull_req_in_pull_req_list(response_get, response_post)

    def test_close_pull_request(self, create_pull_request):
        number_pr = create_pull_request
        endpoint_close = f"{endpoint}/{number_pr}"

        data = {"state": "closed"}

        response_patch = ApiService.patch(endpoint=endpoint_close, headers=headers, data=data)
        Assertions.assert_code_status(response_patch, 200)

        response_get = ApiService.get(endpoint=endpoint, headers=headers)  # for get all PRs
        Assertions.assert_not_present_pull_req_in_pull_req_list(response_get, response_patch)

    def test_merge_pull_request(self, create_pull_request):
        number_pr = create_pull_request
        endpoint_merge = f"{endpoint}/{number_pr}/merge"
        data = {"commit_title": f"Merge_commit_{random_string}"}
        response_merge = ApiService.put(endpoint=endpoint_merge, headers=headers, data=data)
        Assertions.assert_code_status(response_merge, 200)

        # assert that current pull request is merged
        response_check_merge = ApiService.get(endpoint=endpoint_merge, headers=headers)
        Assertions.assert_code_status(response_check_merge, 204)
