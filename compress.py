# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/29 21:07
# @Author   : Perye(Li Pengyu)
# @FileName : compress.py
# @Software : PyCharm

import threading

from pdf2docx import Converter

from constant import PDF_DIRECTORY, CONVERTED_DIRECTORY, OutputFormat, Status
from service import task_service

task_queue = []
task_queue_lock = threading.Lock()


def compress(task_id):
    pass


def push_task_queue():
    pass


threading.Thread(target=push_task_queue()).run()


while True:
    task_queue_lock.acquire(blocking=True)
    task = task_queue.pop()
    task_queue_lock.release()
    try:
        compress(task.get('task_id'))
        task_service.update_file_status_by_task_id(task.get('task_id'), Status.CONVERTED)
    except:
        task_service.update_file_status_by_task_id(task.get('task_id'), Status.FAILED)
