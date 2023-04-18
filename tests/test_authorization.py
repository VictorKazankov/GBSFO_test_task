from pytest import mark

from data import token_user
from helpers.assertions import Assertions
from libs.api import ApiService

endpoint = "/octocat"
wrong_token = "ghp_01010101010101010101001001101"


class TestUserAuth:
    def test_user_authorization_with_correct_token(self):
        headers = {"Authorization": f"Bearer {token_user}", "Accept": "application/vnd.github+json"}
        response = ApiService.get(endpoint=endpoint, headers=headers)
        Assertions.assert_code_status(response, 200)

    @mark.parametrize("incorrect_token", [f"{wrong_token}", ""], ids=["wrong_token", "empty_token"])
    def test_user_authorization_with_incorrect_tokens(self, incorrect_token):
        headers = {"Authorization": f"Bearer {wrong_token}", "Accept": "application/vnd.github+json"}
        response = ApiService.get(endpoint=endpoint, headers=headers)
        Assertions.assert_code_status(response, 401)
        Assertions.assert_message_response(response, 'Bad credentials')
