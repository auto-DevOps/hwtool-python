#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   __init__.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import json

from collections import (
    OrderedDict,
)

from .machine import Machine as module_machine
from ._os import OS as module_os
from .cpu import CPU as module_cpu
from .memory import Memory as module_memory
from .disk import Disk as module_disk
from .nic import NIC as module_nic

modules = [
    module_machine,
    module_os,
    module_cpu,
    module_memory,
    module_nic,
    module_disk,
]


def fetch_hardware(modules=modules):
    data = OrderedDict()

    for module in modules:
        module().saveto(data)

    return data


def print_hardware_jsonic():
    print(json.dumps(
        fetch_hardware(),
        ensure_ascii=False,
        indent=4,
        #default=lambda o: repr(o),
    ))
