from urllib.parse import urljoin

import requests

from .exceptions import normalize_network_error, APIError


class Client:
    """
    API doc: https://www.juhe.cn/docs/api/id/213
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.session()
        self.timeout = (5, 10)

    @staticmethod
    def _assert_call_success(error_code):
        if error_code != 0:
            raise APIError(
                "Unexpected error from server, the code is %s"
                % error_code
            )


class ValidateBankCard4(Client):

    @normalize_network_error
    def validate(self, real_name, id_card, bank_card, mobile) -> bool:
        args = {
            'realname': real_name,
            'idcard': id_card,
            'bankcard': bank_card,
            'mobile': mobile,
            'key': self.api_key,
        }
        url = 'https://v.juhe.cn/verifybankcard4/query.php'
        resp = self.session.get(
            url=url,
            params=args,
            timeout=self.timeout,
        )
        data = resp.json()
        if data['error_code'] != 0:
            return False
        return int(data['result']['res']) == 1


class ValidateBankCard3(Client):

    @normalize_network_error
    def validate(self, real_name, id_card, bank_card) -> bool:
        args = {
            'realname': real_name,
            'idcard': id_card,
            'bankcard': bank_card,
            'key': self.api_key,
        }
        url = 'https://v.juhe.cn/verifybankcard3/query'
        resp = self.session.get(
            url=url,
            params=args,
            timeout=self.timeout,
        )
        data = resp.json()
        self._assert_call_success(data['error_code'])
        return int(data['result']['res']) == 1


class CardInfoClient(Client):

    @normalize_network_error
    def get(self, bank_card) -> None or dict:
        args = {
            'cardid': bank_card,
            'key': self.api_key,
        }
        url = 'http://detectionBankCard.api.juhe.cn/bankCard'
        resp = self.session.get(
            url=url,
            params=args,
            timeout=self.timeout,
        )
        data = resp.json()
        error_code = data['error_code']
        if int(error_code) == 305402:
            return
        self._assert_call_success(error_code)
        return data['result']
