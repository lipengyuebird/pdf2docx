# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/14 14:36
# @Author   : Perye(Li Pengyu)
# @FileName : converter.py
# @Software : PyCharm
import sys
sys.path.append('/usr/local/pdf2docx')

import os.path
import threading
import time
import traceback

import aspose.words as aw
from pdf2image import convert_from_path

from constant import PDF_DIR, CONVERTED_DIR, OutputFormat, Status
from service import task_service

file_queue = []
file_queue_lock = threading.Lock()


def trans(task_id: str, filename: str, output_format: str):
    if output_format.upper() not in OutputFormat.list():
        raise TypeError
    if not os.path.exists(f'{CONVERTED_DIR}/{task_id}'):
        os.mkdir(f'{CONVERTED_DIR}/{task_id}')
    if output_format.upper() == OutputFormat.JPG:
        convert_from_path(f'{PDF_DIR}/{task_id}/{filename}', output_folder=f'{CONVERTED_DIR}/{task_id}/{filename.replace(".pdf", "")}')
    else:
        doc = aw.Document(f'{PDF_DIR}/{task_id}/{filename}')
        doc.save(f'{CONVERTED_DIR}/{task_id}/{filename.replace(".pdf", "." + output_format.lower())}')


def maintain_file_queue():
    while True:
        if len(file_queue) >= 10:
            time.sleep(5)
            continue
        print(file_queue)
        try:
            file_queue_lock.acquire(blocking=True)
            file_queue.extend(task_service.find_latest_unconverted_file_list(5))
        except:
            traceback.print_exc()
        finally:
            file_queue_lock.release()
            time.sleep(5)


if __name__ == '__main__':
    threading.Thread(target=maintain_file_queue).start()
    flag = False
    while True:
        if not file_queue:
            if flag:
                with open('time1.txt', 'a') as f:
                    f.write('END\n')
                    f.write(str(time.time()))
                    f.write('\n')
                flag = False
            time.sleep(10)
            continue

        if not flag:
            with open('time1.txt', 'a') as f:
                f.write('START\n')
                f.write(str(time.time()))
                f.write('\n')
            flag = True

        file_queue_lock.acquire(blocking=True)
        file = file_queue.pop()
        file_queue_lock.release()
        try:
            trans(file.get('task_id'), file.get('name'), file.get('output_format'))
            task_service.update_file_status_by_file_id(file.get('id'), int(Status.TO_BE_COMPRESSED))
        except:
            traceback.print_exc()
            task_service.update_file_status_by_file_id(file.get('id'), int(Status.FAILED))
