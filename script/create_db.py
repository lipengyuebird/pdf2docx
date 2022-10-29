# ./venv/Scipts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/1/12 10:24 AM
# @Author   : Perye(Li Pengyu)
# @FileName : create_db.py
# @Software : PyCharm

import sqlite3

from constant import DB_DIR

if __name__ == '__main__':
    connection = sqlite3.connect(f'{DB_DIR}')
    connection.execute("""
    CREATE TABLE file(
       id             INTEGER        PRIMARY KEY     AUTOINCREMENT     NOT NULL,
       task_id        CHAR(36)                                         NOT NULL,
       name           VARCHAR(255)                                     NOT NULL,
       user_id        CHAR(36)                                         NOT NULL,
       output_format  CHAR(5)                                          NOT NULL,
       time           DATETIME                                         NOT NULL,
       status         INTEGER                                          NOT NULL,
       consumed_by_converter           BOOLEAN                         NOT NULL,
       consumed_by_compressor          BOOLEAN                         NOT NULL 
    );""")
    connection.commit()
    connection.close()
