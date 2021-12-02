#!/usr/bin/python
# -*- coding: UTF-8 -*-

from crawler import JiangXianLi
from crawler import KuaiDaiLi
from crawler import XiLaDaiLi

print("======== Start ========")
JiangXianLi.spider()
KuaiDaiLi.spider()
XiLaDaiLi.spider()
print("======== Done! ========")
