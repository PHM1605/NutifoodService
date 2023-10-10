import requests
from typing import Optional
from functools import partial

from requests.sessions import Session

# # Tenant Mangement URL
# HTTP URL
# BASE_URL = "http://13.76.182.208:9200"
# PORT = 9200


class HttpHelper(Session):

    def __init__(self, baseUrl: str = None, authorization: str = None) -> None:
        self.baseUrl = baseUrl
        self.authorization = authorization

    resq = requests.Session()

    def get(self, apiPath: str, params: Optional[object] = {}):
        self.resq.headers = {
            "Content-Type": "application/json",
            "Authorization":  self.authorization
        }
        try:
            resquest = self.resq.get(
                url=self.baseUrl + apiPath,
                params=params
            )

            res = resquest.json()

            return res
        except requests.exceptions.HTTPError as http_err:
            # TODO: Handler HTTPError here ...
            return
        except requests.exceptions.RequestException as e:
            # TODO: Handler RequestException here ...
            return e
