# ./venv/Scipts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/1/12 10:39 AM
# @Author   : Perye(Li Pengyu)
# @FileName : db_support.py
# @Software : PyCharm


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
