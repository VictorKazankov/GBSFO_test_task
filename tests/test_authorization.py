import json

from pytest import mark

from data import token
from libs.api import ApiService

headers = {"Authorization": f"Bearer {token}"}

wrong_token = "ghp_01010101010101010101001001101"


class TestUserAuth:
    def test_user_authorization_with_correct_token(self):
        ApiService.get(endpoint="/octocat", headers=headers) # check status code in ApiService

    @mark.parametrize("incorrect_token", [f"{wrong_token}", ""], ids=["wrong_token", "empty_token"])
    def test_user_authorization_with_incorrect_tokens(self, incorrect_token):
        response = ApiService.get(endpoint="/octocat", headers=headers, expected_status=401)
        message = json.loads(response.text)
        assert message["message"] == 'Bad credentials'

