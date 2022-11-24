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

task_id = requests.get('http://127.0.0.1:5001/task_id').text
r = requests.post('http://127.0.0.1:5001/upload', files=f_list, params={'output_format': 'docx', 'task_id': task_id})
# print(r.text)
# print(r.headers)
#
# print(requests.get('http://127.0.0.1:5000/history', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJQZXJ5ZSIsInN1YiI6IjBkZjExNDZjNTgxOTExZWQ4MWQ4MDBlMDRjMjM5OTg3IiwiZXhwIjoyMjcxOTEwMDE0LCJpYXQiOjE2NjcxMTAwMTR9.eNhEqjFMLguLY5YdrfXe2LL4_w3r8il05iXMvrY75LcbkPsXkzZ86QYyJ5HtDnU_vGdhPGJCSnfs_fDwYPXFmID-uZ3kym5powOGmN-IIaf87Bb7p7sJk7jXw-UPpkdvm_yWT-J5TQqjVgpaDhKRxubpT2UhPl2q_QeU1H9S4DQ'}).text)
