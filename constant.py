# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:32
# @Author   : Perye(Li Pengyu)
# @FileName : constant.py
# @Software : PyCharm

from enum import Enum, IntEnum

BASE_DIR = 'C:\\Users\\lipen\\PycharmProjects\\pdf2docx\\'

PDF_DIR = BASE_DIR + 'cache/pdf'
CONVERTED_DIR = BASE_DIR + 'cache/converted'
OUTPUT_DIR = BASE_DIR + 'cache/output'
DB_DIR = BASE_DIR + 'pdf2docx'


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
    JPG = 'JPG'


if __name__ == '__main__':
    print(Status.list())

