# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:45
# @Author   : Perye(Li Pengyu)
# @FileName : client.py
# @Software : PyCharm
import os

import requests

f_list = []
files = {}

for filename in os.listdir('samples'):
    f = open('samples/' + filename, 'rb')
    f_list.append(('file', (filename, f, "multipart/form-data")))


requests.post('http://127.0.0.1:5000/upload', files=f_list, params={'output_format': 'docx'})
