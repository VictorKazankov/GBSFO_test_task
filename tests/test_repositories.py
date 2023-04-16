from pytest import mark

from credentials import name_user, token_user
from helpers.assertions import Assertions
from helpers.base_case import BaseCase

headers = {"Authorization": f"Bearer {token_user}", "Accept": "application/vnd.github+json"}

repository = "python_api_training"

wrong_user_name = "my_wrong_user_23"
wrong_branch_name = "wrong_branch"
wrong_repository = "my_wrong_repository"

expected_repositories = ['amadeus_test', 'at.info-knowledge-base', 'ATE', 'AutomationProjects-24-server-',
                         'awesome-computer-vision', 'booking_test', 'BoxingTime', 'ChatBot', 'data', 'dogecodes-repo',
                         'FinalProject', 'Final_project_python_selenium', 'GBSFO_test_task', 'git-demo',
                         'git-repo-geekbrains', 'git-repo-geekbrains2', 'HomeTask', 'ironpython_training', 'java_ptf',
                         'LearnQA_PythonAPI', 'mastering-pycharm-course', 'MyHometaskForGoJava', 'MyWorkProjects',
                         'pikabu', 'pomodoro', 'pyTest', 'python_api_training', 'Python_training',
                         'Python_training_mantis', 'SeleniumTest1']

expected_branches = ["master", "2-th_version_framework", "test_branch1"]


class TestRepositories(BaseCase):

    def test_get_all_repositories(self):
        endpoint = f"/users/{name_user}/repos"

        response = self.perform_request(endpoint, headers)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_name_repositories(response, expected_repositories)

    def test_get_all_branches_from_repository(self):

        endpoint = f"/repos/{name_user}/{repository}/branches"

        response = self.perform_request(endpoint, headers)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_name_branches(response, expected_branches)

    @mark.parametrize("incorrect_repository_name", [f"{wrong_repository}", ""],
                      ids=["wrong_repository", "empty_repository"])
    def test_get_all_branches_from_repository_with_incorrect_repository_name(self, incorrect_repository_name):

        endpoint = f"/repos/{name_user}/{incorrect_repository_name}/branches"

        response = self.perform_request(endpoint, headers)

        Assertions.assert_code_status(response, 404)
        Assertions.assert_message_response(response, 'Not Found')

