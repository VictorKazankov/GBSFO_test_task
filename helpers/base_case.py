from libs.api import ApiService


class BaseCase:
    @staticmethod
    def perform_request(endpoint, headers):
        return ApiService.get(endpoint=endpoint, headers=headers)
