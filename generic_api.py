import json

import requests


class APIInterface:
    @staticmethod
    def get_request(url: str, params: dict):
        get_response = requests.get(url, params)
        print(get_response.url)
        response = json.loads(get_response.text)
        return response

    @staticmethod
    def post_request(url: str, data: dict):
        response = requests.post(url, data).text
        return response
