# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:20
# @Author   : Perye(Li Pengyu)
# @FileName : task_service.py
# @Software : PyCharm
import uuid
from datetime import datetime
import sqlite3

from werkzeug.datastructures import ImmutableMultiDict, FileStorage

from constant import PDF_DIRECTORY, Status
from db_support import dict_factory

connection = sqlite3.connect('../pdf2docx')
connection.row_factory = dict_factory


def create_a_task(
        file_dict,
        user_id: str,
        output_format: str
):
    task_time = datetime.now()
    task_id = uuid.uuid1().hex
    cursor = connection.cursor()
    for _k, file in file_dict:
        file.save(f'{PDF_DIRECTORY}/{task_id}/{file.filename}')
    cursor.executemany(
        """INSERT INTO file (task_id, name, user_id, output_format, time, status) VALUES (?, ?, ?, ?, ?, ?)""",
        [(task_id, file.filename, user_id, output_format, task_time, Status.TO_BE_CONVERTED) for k, file in file_dict]
    )
    cursor.close()
    return task_id


def find_task_list_by_user_id(user_id: str):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT *, count(1) as file_amount, min(status), max(status) as task_status FROM file '
        'WHERE user_id = ? GROUP BY task_id ORDER BY time DESC',
        (user_id,)
    )
    result = [
        {**task, 'description': _format_filename(task['name'], task['file_amount'])}
        for task in cursor.fetchall()
    ]
    cursor.close()
    return result


def find_latest_unconverted_file_list(limit: int):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM file '
        'WHERE status = ? ORDER BY time DESC LIMIT ?',
        (Status.TO_BE_CONVERTED, limit)
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def update_file_status_by_file_id(file_id: int, status: int):
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE file SET status = ?'
        'WHERE id = ?',
        (status, file_id)
    )
    cursor.close()


def find_latest_uncompressed_task_list(limit):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT *, max(status) as max_status, min(status) as min_status FROM file '
        'WHERE status = ? ORDER BY time DESC LIMIT ?',
        (Status.TO_BE_CONVERTED, limit)
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def update_file_status_by_task_id(task_id: str, status: int):
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE file SET status = ?'
        'WHERE task_id = ?',
        (status, task_id)
    )
    cursor.close()


def _format_filename(filename, file_num):
    if file_num == 1:
        return filename if len(filename) <= 50 else filename[:47] + '...'
    elif file_num == 2:
        return filename if len(filename) <= 39 else f'{filename[:36]}... and 1 file'
    else:
        return filename if len(filename) <= 38 else f'{filename[:35]}... and {file_num - 1} files'


def _get_task_status(min_file_status: int, max_file_status: int):
    if min_file_status == Status.CONVERTED:
        return Status.CONVERTED
    elif max_file_status == Status.FAILED:
        return Status.FAILED
    elif min_file_status == Status.COMPRESSING:
        return Status.COMPRESSING
    else:
        return Status.CONVERTING


def find_task_status_by_task_id(task_id: str, user_id: str):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT max(status) as task_status FROM file '
        'WHERE task_id = ? AND user_id = ?',
        (task_id, user_id)
    )
    result = cursor.fetchone()
    cursor.close()
    return result['task_status'] if result else None



if __name__ == '__main__':
    print(find_task_list_by_user_id('111'))
