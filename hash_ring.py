# ./venv/Scripts/python
# _*_ coding: utf-8 _*_
# @Time     : 2022/11/21 12:29
# @Author   : Perye(Li Pengyu)
# @FileName : hash_ring.py
# @Software : PyCharm
from __future__ import print_function

from uhashring import HashRing

import sys
sys.path.append("../")
from pysyncobj import SyncObj, SyncObjConf, replicated


class DistributedHashRing(SyncObj):
    def __init__(self, self_address, partner_addrs):
        cfg = SyncObjConf(dynamicMembershipChange=True)
        super(DistributedHashRing, self).__init__(self_address, partner_addrs, cfg)
        self.__hashring = HashRing(nodes=[self_address, *partner_addrs])

    @replicated
    def add_node(self, address):
        self.__hashring.add_node(address)

    @replicated
    def remove_node(self, address):
        self.__hashring.remove_node(address)

    def get_node(self, key):
        return self.__hashring.get_node(key)


