import os
import logging

from requests import Response

logger = logging.getLogger(__name__)


class Logger:
    @classmethod
    def add_log(cls, log):
        logger.info(log)

    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        testname = os.environ.get('PYTEST_CURRENT_TEST')

        data_to_add = f"\n-----\n"
        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Performing method:{method} request\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"

        logger.info(data_to_add)

    @classmethod
    def add_response(cls, response: Response):
        data_to_add = f"Response status code: {response.status_code}\n"
        data_to_add += f"Response data: {response.text}\n"
        data_to_add += f"Response headers: {response.headers}\n"
        data_to_add += f"Response cookies: {response.cookies}\n"
        data_to_add += "\n-----\n"

        logger.info(data_to_add)
