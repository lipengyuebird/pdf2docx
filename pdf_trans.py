# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/14 14:36
# @Author   : Perye(Li Pengyu)
# @FileName : pdf_trans.py
# @Software : PyCharm
import os
import time

from pdf2docx import Converter


def trans(record_id):
    # convert pdf to docx
    cv = Converter(f'cache/pdf/{record_id}' + '.pdf')
    cv.convert(f'cache/docx/{record_id}' + '.docx')
    cv.close()
    os.remove(f'cache/pdf/{record_id}' + '.pdf')


while True:
    time.sleep(3)
    file_queue = [filename for filename in sorted(os.listdir('cache/pdf')) if filename.endswith('.pdf')]
    if file_queue:
        trans(file_queue[0].replace('.pdf', ''))
