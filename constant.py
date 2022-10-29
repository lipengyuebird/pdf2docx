# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/10/28 22:32
# @Author   : Perye(Li Pengyu)
# @FileName : constant.py
# @Software : PyCharm

from enum import Enum, IntEnum, StrEnum

PDF_DIRECTORY = 'cache/pdf'
CONVERTED_DIRECTORY = 'cache/converted'
OUTPUT_DIRECTORY = 'cache/output'


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


class OutputFormat(StrEnum, ExtendedEnum):
    DOCX = 'DOCX'
    JPG = 'JPG'


if __name__ == '__main__':
    print(Status.list())

