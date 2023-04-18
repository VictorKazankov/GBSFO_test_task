from user_data import name_user, repository, headers, headers_for_another_user
from helpers.assertions import Assertions
from helpers.utils import random_string, json_to_python_object
from libs.api import ApiService

expected_pull_requests = ["Created PR-1", "Created PR-2"]

main_endpoint = f"/repos/{name_user}/{repository}/pulls"


class TestPullRequests:
    def test_get_all_pull_requests(self):
        response = ApiService.get(endpoint=main_endpoint, headers=headers)
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
        response_post = ApiService.post(endpoint=main_endpoint, headers=headers, data=pull_request_data)
        Assertions.assert_code_status(response_post, 201)

        response_get = ApiService.get(endpoint=main_endpoint, headers=headers)  # for get all PRs
        Assertions.assert_present_pull_req_in_pull_req_list(response_get, response_post)

    def test_close_pull_request(self, create_pull_request):
        number_pr = create_pull_request
        endpoint_close = f"{main_endpoint}/{number_pr}"

        data = {"state": "closed"}

        response_patch = ApiService.patch(endpoint=endpoint_close, headers=headers, data=data)
        Assertions.assert_code_status(response_patch, 200)

        response_get = ApiService.get(endpoint=main_endpoint, headers=headers)  # for get all PRs
        Assertions.assert_not_present_pull_req_in_pull_req_list(response_get, response_patch)

    def test_approve_pull_request(self, create_pull_request):
        number_pr = create_pull_request
        endpoint_post = f"{main_endpoint}/{number_pr}/reviews"
        data = {"body": "This is close to perfect! Please address the suggested inline change.",
                "event": "APPROVE"}
        response_post = ApiService.post(endpoint=endpoint_post, headers=headers_for_another_user, data=data)
        Assertions.assert_code_status(response_post, 200)
        id_review = json_to_python_object(response_post)["id"]

        # assert that current pull request is approved
        endpoint_get = f"{main_endpoint}/{number_pr}/reviews/{id_review}"
        response_get = ApiService.get(endpoint=endpoint_get, headers=headers_for_another_user)
        Assertions.assert_review_has_approve_state(response_get)

    def test_merge_pull_request(self, create_pull_request):
        number_pr = create_pull_request
        endpoint_merge = f"{main_endpoint}/{number_pr}/merge"
        data = {"commit_title": "Merge_commit"}
        response_merge = ApiService.put(endpoint=endpoint_merge, headers=headers, data=data)
        Assertions.assert_code_status(response_merge, 200)

        # assert that current pull request is merged
        response_check_merge = ApiService.get(endpoint=endpoint_merge, headers=headers)
        Assertions.assert_code_status(response_check_merge, 204)
