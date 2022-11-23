# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/11/21 13:44
# @Author   : Perye(Li Pengyu)
# @FileName : node_management.py
# @Software : PyCharm

import os
import pysftp

from uhashring import HashRing
import pyrqlite.dbapi2 as dbapi2


def add_node(hash_ring, local_address, partner_address):
    os.system(f'syncobj_admin -conn {partner_address} -add {local_address}')
    hash_ring.add_node(local_address)


def remove_node(hash_ring, local_address, sample_key):
    new_address = HashRing(hash_ring.get_nodes().pop(local_address)).get_node(sample_key)
    with pysftp.Connection(new_address, username='root') as sftp:
        with sftp.cd('~/pdf2docx/cache'):
            sftp.put('~/pdf2docx/cache')

    hash_ring.remove_node(local_address)
    os.system(f'syncobj_admin -conn {new_address} -remove {local_address}')


