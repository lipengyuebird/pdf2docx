# ./venv/Scipts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/1/12 10:24 AM
# @Author   : Perye(Li Pengyu)
# @FileName : create_db.py
# @Software : PyCharm

import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect('../pdf2docx')
    connection.execute("""
    CREATE TABLE file(
       id             INTEGER        PRIMARY KEY     AUTOINCREMENT     NOT NULL,
       task_id        CHAR(36)                                         NOT NULL,
       name           VARCHAR(255)                                     NOT NULL,
       user_id        CHAR(36)                                         NOT NULL,
       output_format  CHAR(5)                                          NOT NULL,
       time           DATETIME                                         NOT NULL,
       status         INTEGER                                          NOT NULL
    );""")
    connection.commit()
    connection.close()
