from pytest import mark

from data import name_user, headers, repository
from helpers.assertions import Assertions
from libs.api import ApiService

wrong_user_name = "my_wrong_user_23"
wrong_branch_name = "wrong_branch"
wrong_repository = "my_wrong_repository"

expected_repositories = ['amadeus_test', 'at.info-knowledge-base', 'ATE', 'AutomationProjects-24-server-',
                         'awesome-computer-vision', 'booking_test', 'BoxingTime', 'ChatBot', 'data', 'dogecodes-repo',
                         'FinalProject', 'Final_project_python_selenium', 'GBSFO_test_task', 'git-demo',
                         'git-repo-geekbrains', 'git-repo-geekbrains2', 'HomeTask', 'ironpython_training',
                         'java_ptf', 'LearnQA_PythonAPI', 'mastering-pycharm-course', 'MyHometaskForGoJava',
                         'MyWorkProjects', 'pikabu', 'pomodoro', 'pyTest', 'python_api_training', 'Python_training',
                         'Python_training_mantis', 'SeleniumTest1', 'Spoon-Knife', 'stepic_automation_python_course',
                         'TestForYandex', 'TestGIT', 'testing-python-apps', 'TestPrestashopSite', 'TestRepository',
                         'TestSeleniumUI', 'TM', 'UserBrowsermobProxy', 'VictorKazankov2', 'Winium', 'WorkProjects']

expected_branches = ["main", "test_branch1", "test_branch2"]


class TestRepositories:

    def test_get_all_repositories(self):
        endpoint = f"/users/{name_user}/repos?per_page=100" # here display 100 repositories on page

        response = ApiService.get(endpoint=endpoint, headers=headers)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_name_repositories(response, expected_repositories)

    def test_get_all_branches_from_repository(self):
        endpoint = f"/repos/{name_user}/{repository}/branches"

        response = ApiService.get(endpoint=endpoint, headers=headers)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_name_branches(response, expected_branches)

    @mark.parametrize("incorrect_repository_name", [f"{wrong_repository}", ""],
                      ids=["wrong_repository", "empty_repository"])
    def test_get_all_branches_from_repository_with_incorrect_repository_name(self, incorrect_repository_name):
        endpoint = f"/repos/{name_user}/{incorrect_repository_name}/branches"

        response = ApiService.get(endpoint=endpoint, headers=headers)

        Assertions.assert_code_status(response, 404)
        Assertions.assert_message_response(response, 'Not Found')
