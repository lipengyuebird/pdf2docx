# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:45
# @Author   : Perye(Li Pengyu)
# @FileName : client.py
# @Software : PyCharm

import requests

# files = {}
filename = 'a1.pdf'
with open(filename, 'rb') as f:
    files = {'file': (filename, f, "multipart/form-data")}
    requests.post('http://127.0.0.1:5000/upload', files=files)
