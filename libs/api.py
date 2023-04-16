import requests

from libs.logger import Logger


class ApiService:
    @staticmethod
    def get(endpoint: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return ApiService._send(endpoint, data, headers, cookies, "GET")

    #################
    @staticmethod
    def _send(endpoint: str, data: dict, headers: dict, cookies: dict, method: str):

        endpoint_url = f"https://api.github.com{endpoint}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(endpoint_url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(endpoint_url, params=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
