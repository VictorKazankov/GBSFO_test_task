import json

from pytest import mark
import requests

from libs.api import ApiService

api_url = "https://api.github.com"
token = "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"
wrong_token = "ghp_01010101010101010101001001101"


class TestUserAuth:
    def test_user_authorization_with_correct_token(self):
        headers = {"Authorization": f"Bearer {token}"}
        response = ApiService.get(endpoint="/octocat", headers=headers)

    @mark.parametrize("incorrect_token", [f"{wrong_token}", ""], ids=["wrong_token", "empty_token"])
    def test_user_authorization_with_incorrect_tokens(self, incorrect_token):
        headers = {"Authorization": f"Bearer {wrong_token}"}
        response = ApiService.get(endpoint="/octocat", headers=headers, expected_status=401)
        message = json.loads(response.text)
        assert message["message"] == 'Bad credentials'

