# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/29 21:07
# @Author   : Perye(Li Pengyu)
# @FileName : compressor.py
# @Software : PyCharm
import sys
sys.path.append('/usr/local/pdf2docx')

import threading
import shutil
import time
import traceback

from constant import CONVERTED_DIR, OUTPUT_DIR, Status
from service import task_service

task_queue = []
task_queue_lock = threading.Lock()


def compress(task_id):
    shutil.make_archive(f'{OUTPUT_DIR}/{task_id}', 'zip', f'{CONVERTED_DIR}/{task_id}')


def maintain_task_queue():
    while len(task_queue) <= 10:
        try:
            task_queue_lock.acquire(blocking=True)
            task_queue.extend(task_service.find_latest_uncompressed_task_list(5))
            print(task_queue)
        except:
            traceback.print_exc()
        finally:
            task_queue_lock.release()
            time.sleep(10)


if __name__ == '__main__':
    threading.Thread(target=maintain_task_queue).start()
    while True:
        print(task_queue)
        if not task_queue:
            time.sleep(10)
            continue
        task_queue_lock.acquire(blocking=True)
        task = task_queue.pop()
        task_queue_lock.release()
        try:
            compress(task.get('task_id'))
            task_service.update_file_status_by_task_id(task.get('task_id'), int(Status.CONVERTED))
        except:
            pass
            # task_service.update_file_status_by_task_id(task.get('task_id'), int(Status.FAILED))
