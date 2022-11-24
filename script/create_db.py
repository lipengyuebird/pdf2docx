# ./venv/Scipts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/1/12 10:24 AM
# @Author   : Perye(Li Pengyu)
# @FileName : create_db.py
# @Software : PyCharm
import sys
sys.path.append('/usr/local/pdf2docx')

import pyrqlite.dbapi2 as dbapi2

from constant import DB_HOST


if __name__ == '__main__':
    connection = dbapi2.connect(host=DB_HOST)
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
       consumed_by_compressor          BOOLEAN                         NOT NULL,
       node           CHAR(21)                                         NOT NULL
    );""")
    connection.commit()
    connection.close()
