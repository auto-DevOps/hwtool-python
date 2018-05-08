#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   memory.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from collections import (
    defaultdict,
    OrderedDict,
)

from dmi.parser.type import (
    DMIType,
)

from .base import (
    BaseHardwareModel,
)


class Memory(BaseHardwareModel):

    NAME = 'memory'

    FIELD_SIZE = 'size'
    FIELD_SLOTS = 'slots'
    FIELD_SLOTS_USED = 'slots_used'
    FIELD_DIVICE_BRIEF = 'device_brief'
    FIELD_DEVICES = 'devices'
    FIELD_OS_TOTAL = 'os_total'

    FIELD_DEVICE_SIZE = 'size'
    FIELD_DEVICE_MANUFACTUER = 'manufacturer'
    FIELD_DEVICE_SPEED = 'speed'

    def _fetch_info_bios(self):
        dmi_memory_device = self.DMI_MAPPING[DMIType.TYPE_MEMORY_DEVICE]
        slots = len(dmi_memory_device)

        devices = []
        total_size = 0
        size_count = defaultdict(lambda: 0)

        for item in dmi_memory_device:
            size = item['size']
            if not size:
                continue

            speed = item['speed'] or None
            manufacturer = item['manufacturer']

            devices.append(OrderedDict([
                (self.FIELD_DEVICE_MANUFACTUER, manufacturer),
                (self.FIELD_DEVICE_SIZE, size),
                (self.FIELD_DEVICE_SPEED, speed),
            ]))

            total_size += size

            size_count[size] += 1

        slots_used = len(devices)

        device_brief = ' '.join(
            '{size}*{count}'.format(size=size, count=count)
            for size, count in sorted(size_count.items())
        )

        memory = OrderedDict([
            (self.FIELD_SIZE, total_size),
            (self.FIELD_SLOTS, slots),
            (self.FIELD_SLOTS_USED, slots_used),
            (self.FIELD_DIVICE_BRIEF, device_brief),
            (self.FIELD_DEVICES, devices),
        ])

        return memory

    def _fetch_info_linux(self):
        memory = self._fetch_info_bios()
        return memory

    def _fetch_info_windows(self):
        memory = self._fetch_info_bios()

        system = None
        for system in self.wmi.Win32_ComputerSystem():
            pass

        if system:
            os_total = system.TotalPhysicalMemory
            if os_total:
                os_total = int(os_total)
            memory[self.FIELD_OS_TOTAL] = os_total

        return memory
