# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:20
# @Author   : Perye(Li Pengyu)
# @FileName : task_service.py
# @Software : PyCharm
import sys
sys.path.append("../")

import os
from datetime import datetime
import pyrqlite.dbapi2 as dbapi2

from werkzeug.datastructures import ImmutableMultiDict, FileStorage

from constant import PDF_DIR, DB_HOST, Status
from db_support import dict_factory

connection = dbapi2.connect(host=DB_HOST)


def create_a_task(
        task_id: str,
        file_dict: ImmutableMultiDict,
        user_id: str,
        output_format: str
) -> str:
    task_time = datetime.now()
    cursor = connection.cursor()
    os.mkdir(f'{PDF_DIR}/{task_id}')
    file_list = [file for key in file_dict.keys() for file in file_dict.getlist(key)]
    print(file_list)
    for file in file_list:
        file.save(f'{PDF_DIR}/{task_id}/{file.filename}')
    cursor.executemany(
        'INSERT INTO file (task_id, name, user_id, output_format, time, status, '
        '                  consumed_by_converter, consumed_by_compressor, ) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        [(task_id, file.filename, user_id, output_format, task_time, Status.TO_BE_CONVERTED,
          False, False) for file in file_list]
    )
    return task_id


def find_task_list_by_user_id(user_id: str):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT *, count(1) as file_amount, min(status), max(status) as task_status FROM file '
        'WHERE user_id = ? GROUP BY task_id ORDER BY time DESC, name DESC',
        (user_id,)
    )
    result = [
        {**task, 'description': _format_filename(task['name'], task['file_amount'])}
        for task in cursor.fetchall()
    ]
    return result


def find_latest_unconverted_file_list(limit: int):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM file '
        'WHERE status = ? and consumed_by_converter = false ORDER BY time DESC LIMIT ?',
        (Status.TO_BE_CONVERTED, limit)
    )
    result = cursor.fetchall()
    cursor.executemany(
        'UPDATE file SET consumed_by_converter = true '
        'WHERE id = ?',
        [(file['id'], ) for file in result]
    )
    return result


def update_file_status_by_file_id(file_id: int, status: int):
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE file SET status = ?'
        'WHERE id = ?',
        (status, file_id)
    )


def find_latest_uncompressed_task_list(limit):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM ('
        '   SELECT *, min(status) as min_status '
        '   FROM file '
        '   WHERE status != ? and consumed_by_compressor = false GROUP BY task_id ORDER BY time DESC'
        ') WHERE min_status = 2 LIMIT ?',
        (Status.FAILED, limit)
    )
    result = cursor.fetchall()
    cursor.executemany(
        'UPDATE file SET consumed_by_compressor = true '
        'WHERE task_id = ?',
        [(file['task_id'],) for file in result]
    )
    return result


def update_file_status_by_task_id(task_id: str, status: int):
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE file SET status = ?'
        'WHERE task_id = ?',
        (status, task_id)
    )


def _format_filename(filename, file_num):
    if file_num == 1:
        return filename if len(filename) <= 50 else filename[:47] + '...'
    elif file_num == 2:
        if len(filename) > 39:
            filename = filename[:36]
        return f'{filename}... and 1 file'
    else:
        if len(filename) > 38:
            filename = filename[:35]
        return f'{filename}... and {file_num - 1} files'


def _get_task_status(min_file_status: int, max_file_status: int):
    if min_file_status == Status.CONVERTED:
        return Status.CONVERTED
    elif max_file_status == Status.FAILED:
        return Status.FAILED
    else:
        return max_file_status


def find_task_status_by_task_id(task_id: str, user_id: str):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT max(status) as task_status FROM file '
        'WHERE task_id = ? AND user_id = ?',
        (task_id, user_id)
    )
    result = cursor.fetchone()
    return result['task_status'] if result else None


def find_task_node_by_task_id(task_id: str):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT node FROM file '
        'WHERE task_id = ?',
        (task_id,)
    )
    result = cursor.fetchone()
    return result['node'] if result else None


if __name__ == '__main__':
    print(find_latest_uncompressed_task_list(5))
