import json

from pytest import mark

from credentials import name_user, token_user
from libs.api import ApiService

wrong_user_name = "my_wrong_user_23"
wrong_branch_name = "wrong_branch"

repository = "python_api_training"
wrong_repository = "my_wrong_repository"

headers = {"Authorization": f"Bearer {token_user}", "Accept": "application/vnd.github+json"}

expected_repositories = ['amadeus_test', 'at.info-knowledge-base', 'ATE', 'AutomationProjects-24-server-',
                         'awesome-computer-vision', 'booking_test', 'BoxingTime', 'ChatBot', 'data', 'dogecodes-repo',
                         'FinalProject', 'Final_project_python_selenium', 'GBSFO_test_task', 'git-demo',
                         'git-repo-geekbrains', 'git-repo-geekbrains2', 'HomeTask', 'ironpython_training', 'java_ptf',
                         'LearnQA_PythonAPI', 'mastering-pycharm-course', 'MyHometaskForGoJava', 'MyWorkProjects',
                         'pikabu', 'pomodoro', 'pyTest', 'python_api_training', 'Python_training',
                         'Python_training_mantis', 'SeleniumTest1']

expected_branches = ["master", "2-th_version_framework", "test_branch1"]


class TestRepositories:

    def test_get_all_repositories(self):
        response = ApiService.get(endpoint=f"/users/{name_user}/repos", headers=headers)
        message = json.loads(response.text)
        name_repositories = [rep["name"] for rep in message]
        assert sorted(name_repositories) == sorted(expected_repositories)

    @mark.parametrize("incorrect_user_name", [f"{wrong_user_name}", ""], ids=["wrong_user", "empty_user"])
    def test_get_all_repositories_with_incorrect_user_name(self, incorrect_user_name):
        response = ApiService.get(endpoint=f"/users/{incorrect_user_name}/repos", headers=headers, expected_status=404)
        message = json.loads(response.text)
        assert message["message"] == 'Not Found'

    def test_get_all_branches_from_repository(self):
        response = ApiService.get(endpoint=f"/repos/{name_user}/{repository}/branches", headers=headers)
        message = json.loads(response.text)
        name_branches = [br["name"] for br in message]
        assert sorted(name_branches) == sorted(expected_branches)

    @mark.parametrize("incorrect_user_name", [f"{wrong_user_name}", ""], ids=["wrong_user", "empty_user"])
    def test_get_all_branches_from_repository_with_incorrect_user_name(self, incorrect_user_name):
        response = ApiService.get(endpoint=f"/repos/{incorrect_user_name}/{repository}/branches", headers=headers,
                                  expected_status=404)
        message = json.loads(response.text)
        assert message["message"] == 'Not Found'

    @mark.parametrize("incorrect_repository_name", [f"{wrong_repository}", ""],
                      ids=["wrong_repository", "empty_repository"])
    def test_get_all_branches_from_repository_with_incorrect_repository_name(self, incorrect_repository_name):
        response = ApiService.get(endpoint=f"/repos/{name_user}/{incorrect_repository_name}/branches", headers=headers,
                                  expected_status=404)
        message = json.loads(response.text)
        assert message["message"] == 'Not Found'
