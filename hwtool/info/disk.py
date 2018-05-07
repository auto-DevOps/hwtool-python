#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   disk.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from collections import (
    OrderedDict,
)

from .base import (
    BaseHardwareModel,
)


class Disk(BaseHardwareModel):

    NAME = 'disks'
    GB = 1024 * 1024 * 1024

    FIELD_NAME = 'name'
    FIELD_MODEL = 'model'
    FIELD_SIZE = 'size'
    FIELD_PARTITIONS = 'partitions'

    FIELD_PARTITION_NAME = 'name'
    FIELD_PARTITION_ID = 'id'
    FIELD_PARTITION_SIZE = 'size'

    @classmethod
    def bytes2GB(cls, bs):
        return round(1. * bs / cls.GB, 0)

    def _fetch_info_linux(self):
        from sysfs.block import (
            BlockDevice,
        )

        disks = []

        for device in BlockDevice.iter():
            if not device.has_device:
                continue

            partitions = []
            for partition in device.iter_partitions():
                partitions.append(OrderedDict([
                    (self.FIELD_PARTITION_NAME, partition.name),
                    (self.FIELD_PARTITION_ID, partition.partition),
                    (self.FIELD_PARTITION_SIZE, partition.size),
                ]))

            disks.append(OrderedDict([
                (self.FIELD_NAME, device.name),
                (self.FIELD_MODEL, device.model),
                (self.FIELD_SIZE, device.size),
                (self.FIELD_PARTITIONS, partitions),
            ]))

        return disks
