# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/29 23:10
# @Author   : Perye(Li Pengyu)
# @FileName : test_user_service.py
from unittest import TestCase
from service.user_service import *


# @Software : PyCharm
class Test(TestCase):
    user_id = None
    token = None

    def test_generate_user_id(self):
        self.user_id = generate_user_id()

    def test_encrypt_token(self):
        self.token = encrypt_token(self.user_id)

    def test_decrypt_token(self):
        assert self.user_id == decrypt_token(self.token)

    def test_renewed_header(self):
        assert self.user_id == decrypt_token(renewed_header(self.user_id)[0][1])
