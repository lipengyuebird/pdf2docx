# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/11/24 14:09
# @Author   : Perye(Li Pengyu)
# @FileName : clean_db.py
# @Software : PyCharm
import sys
sys.path.append('/usr/local/pdf2docx')

import pyrqlite.dbapi2 as dbapi2

from constant import DB_HOST

if __name__ == '__main__':
    connection = dbapi2.connect(host=DB_HOST)
    connection.execute("""
    DELETE FROM file where status != -2
    """)
    connection.commit()
    connection.close()