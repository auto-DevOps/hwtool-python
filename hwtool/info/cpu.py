#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   cpu.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from collections import (
    OrderedDict,
)

from dmi.parser.type import (
    DMIType,
)

from .base import (
    BaseHardwareModel,
)


class CPU(BaseHardwareModel):

    NAME = 'cpu'

    FIELD_MODEL = 'model'
    FIELD_FREQUENCY = 'frequency'
    FIELD_CPU_COUNT = 'cpu_count'
    FIELD_CORE_COUNT = 'core_count'
    FIELD_THREAD_COUNT = 'thread_count'
    FIELD_HT = 'hyper_threading'

    def _fetch_freq_from_dmi(self):
        for item in self.DMI_MAPPING[DMIType.TYPE_PROCESSOR]:
            current_speed = int(item['current_speed'] or 0)
            if current_speed:
                return current_speed

    def _fetch_info_linux(self):
        from procfs.cpuinfo import (
            get_cpuinfos,
        )

        cpuinfos = get_cpuinfos()
        if not cpuinfos:
            return

        item_count = len(cpuinfos)
        first_item = cpuinfos[0]

        freq = self._fetch_freq_from_dmi()

        cpu = OrderedDict([
            (self.FIELD_MODEL, first_item['model_name'],),
            (self.FIELD_FREQUENCY, freq),
            (self.FIELD_CPU_COUNT, item_count,),
            (self.FIELD_CORE_COUNT, item_count,),
            (self.FIELD_THREAD_COUNT, item_count,),
        ])

        if 'physical_id' in first_item:
            cpu[self.FIELD_CPU_COUNT] = len(set([
                cpuinfo['physical_id']
                for cpuinfo in cpuinfos
            ]))

            cpu[self.FIELD_CORE_COUNT] = len(set([
                (cpuinfo['physical_id'], cpuinfo['core_id'])
                for cpuinfo in cpuinfos
            ]))

        return cpu

    def _fetch_info(self):
        cpu = super(CPU, self)._fetch_info()
        if not cpu:
            return

        cpu[self.FIELD_HT] = cpu[self.FIELD_CORE_COUNT] < cpu[self.FIELD_THREAD_COUNT]
        return cpu
