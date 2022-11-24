# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/6 13:45
# @Author   : Perye(Li Pengyu)
# @FileName : client.py
# @Software : PyCharm
import os
import time

import requests

f_list = []

for i in range(11):
    for filename in os.listdir('C:\\Users\\lipen\\Downloads\\master-gdc-gdcdatasets-2020445568-2020445568\\lcwa_gov_pdf_data\\data')[100*i: min(100*(i+1), 1002)]:
        f = open('C:\\Users\\lipen\\Downloads\\master-gdc-gdcdatasets-2020445568-2020445568\\lcwa_gov_pdf_data\\data\\' + filename, 'rb')
        f_list.append(('file', (filename, f, "multipart/form-data")))

    while 1:
        try:
            task_id = requests.get('http://127.0.0.1:5001/task_id').text
            r = requests.post('http://127.0.0.1:5001/upload', files=f_list,
                              params={'output_format': 'docx', 'task_id': task_id})
            break
        except:
            time.sleep(20)
            pass
    print(f_list)
    f_list = []
    time.sleep(20)


task_id = requests.get('http://127.0.0.1:5001/task_id').text
r = requests.post('http://127.0.0.1:5001/upload', files=f_list, params={'output_format': 'docx', 'task_id': task_id})
# print(r.text)
# print(r.headers)
#
# print(requests.get('http://127.0.0.1:5000/history', headers={'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJQZXJ5ZSIsInN1YiI6IjBkZjExNDZjNTgxOTExZWQ4MWQ4MDBlMDRjMjM5OTg3IiwiZXhwIjoyMjcxOTEwMDE0LCJpYXQiOjE2NjcxMTAwMTR9.eNhEqjFMLguLY5YdrfXe2LL4_w3r8il05iXMvrY75LcbkPsXkzZ86QYyJ5HtDnU_vGdhPGJCSnfs_fDwYPXFmID-uZ3kym5powOGmN-IIaf87Bb7p7sJk7jXw-UPpkdvm_yWT-J5TQqjVgpaDhKRxubpT2UhPl2q_QeU1H9S4DQ'}).text)
