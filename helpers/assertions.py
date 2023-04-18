import json

from requests import Response


class Assertions:
    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code!. Expected: {expected_status_code}.Actual: {response.status_code}," \
            f"Text: {response.text}"

    @staticmethod
    def assert_message_response(response: Response, expected_message):
        response_text = json.loads(response.text)
        assert response_text["message"] == expected_message

    @staticmethod
    def assert_name_repositories(response: Response, expected_repositories):
        response_text = json.loads(response.text)
        name_repositories = [rep["name"] for rep in response_text]
        assert sorted(name_repositories) == sorted(expected_repositories)

    @staticmethod
    def assert_name_branches(response: Response, expected_branches):
        response_text = json.loads(response.text)
        name_branches = [br["name"] for br in response_text]
        assert sorted(name_branches) == sorted(expected_branches)

    @staticmethod
    def assert_name_pull_requests(response: Response, expected_pull_requests):
        response_text = json.loads(response.text)
        name_pull_requests = [pr["title"] for pr in response_text]
        assert sorted(name_pull_requests) == sorted(expected_pull_requests)

    @staticmethod
    def assert_present_pull_req_in_pull_req_list(response_get, response_post):
        title_new_pr = json.loads(response_post.text)["title"]

        response_get_text = json.loads(response_get.text)
        all_pull_requests = [pr["title"] for pr in response_get_text]

        assert title_new_pr in all_pull_requests

    @staticmethod
    def assert_not_present_pull_req_in_pull_req_list(response_get, response_patch):
        title_new_pr = json.loads(response_patch.text)["title"]

        response_get_text = json.loads(response_get.text)
        all_pull_requests = [pr["title"] for pr in response_get_text]

        assert title_new_pr not in all_pull_requests