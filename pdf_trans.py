# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/14 14:36
# @Author   : Perye(Li Pengyu)
# @FileName : pdf_trans.py
# @Software : PyCharm

import threading

from pdf2docx import Converter

from constant import PDF_DIRECTORY, CONVERTED_DIRECTORY, OutputFormat, Status
from service import task_service

file_queue = []
file_queue_lock = threading.Lock()


def trans(filename, output_format):
    if output_format not in OutputFormat.list():
        raise TypeError
    # convert pdf to docx
    cv = Converter(f'{PDF_DIRECTORY}/{filename}')
    cv.convert(f'{CONVERTED_DIRECTORY}/{filename.replace(".pdf", ".docx")}')
    cv.close()


def push_task_queue():
    while len(file_queue) <= 10:
        file_queue_lock.acquire(blocking=True)
        file_queue.extend(task_service.find_latest_unconverted_file_list(5))
        file_queue_lock.release()


threading.Thread(target=push_task_queue()).run()


while True:
    file_queue_lock.acquire(blocking=True)
    file = file_queue.pop()
    file_queue_lock.release()
    try:
        trans(file.get('filename'), file.get('output_format'))
        task_service.update_file_status_by_file_id(file.get('file_id'), Status.TO_BE_COMPRESSED)
    except:
        task_service.update_file_status_by_file_id(file.get('file_id'), Status.FAILED)



