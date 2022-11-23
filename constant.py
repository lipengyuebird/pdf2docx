# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:32
# @Author   : Perye(Li Pengyu)
# @FileName : constant.py
# @Software : PyCharm

from enum import Enum, IntEnum

BASE_DIR = '/usr/local/pdf2docx/'

PDF_DIR = BASE_DIR + 'cache/pdf'
CONVERTED_DIR = BASE_DIR + 'cache/converted'
OUTPUT_DIR = BASE_DIR + 'cache/output'
DB_HOST = 'test1'

ip_dict = {
        'test1': 'localhost:5001',
        'test2': 'localhost:5002',
        'test3': 'localhost:5003',
        'test4': 'localhost:5004',
        'test5': 'localhost:5005',
}


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Status(IntEnum, ExtendedEnum):
    FAILED = -1
    TO_BE_CONVERTED = 0
    CONVERTING = 1
    TO_BE_COMPRESSED = 2
    COMPRESSING = 3
    CONVERTED = 4
    CONVERTED_WITH_FAILURE = 5


class OutputFormat(ExtendedEnum):
    DOCX = 'DOCX'
    DOC = 'DOC'
    RTF = 'RTF'
    JPG = 'JPG'
    ODT = 'ODT'


if __name__ == '__main__':
    print(Status.list())

