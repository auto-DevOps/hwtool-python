#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   nic.py
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


class NIC(BaseHardwareModel):

    NAME = 'network_interface_cards'

    FIELD_IFACE = 'iface'
    FIELD_BRAND = 'brand'
    FIELD_UP = 'up'
    FIELD_LINKED = 'linked'
    FIELD_MTU = 'mtu'
    FIELD_MAC = 'mac'
    FIELD_IPS = 'ips'
    FIELD_BUS = 'bus'
    FIELD_SPEED = 'speed'

    def _fetch_info_linux(self):
        from ethtool import (
            Ethtool,
        )
        from sysfs.bus.pci.device import(
            PCIDevice,
        )

        from procfs.net.dev import fetch as fetch_network_devices

        nics = []

        with Ethtool() as ethtool:
            for iface in fetch_network_devices():
                try:
                    drvinfo = ethtool.fetch_drvinfo(iface_name=iface)
                except:
                    continue

                bus_info = drvinfo.get('bus_info')
                if not bus_info or bus_info in ('N/A',):
                    continue

                pci = PCIDevice(bus_info)
                brand = '  '.join((
                    (pci.get('vendor') or '').strip(),
                    (pci.get('device') or '').strip(),
                ))

                try:
                    mtu = ethtool.fetch_mtu(iface_name=iface)
                except:
                    mtu = None

                try:
                    flags = ethtool.fetch_if_flags(iface_name=iface)
                    is_up = flags.is_up
                    is_running = flags.is_running
                except:
                    is_up = None
                    is_running = None

                try:
                    mac = ethtool.fetch_hardware_address(iface_name=iface)
                except:
                    mac = None

                try:
                    link_settings = ethtool.fetch_link_setttings(iface_name=iface)
                    speed = link_settings.get('speed', None)
                except:
                    try:
                        settings = ethtool.fetch_settings(iface_name=iface)
                        speed = settings['speed']
                    except:
                        speed = None

                try:
                    ip = ethtool.fetch_ip_address(iface_name=iface)
                except:
                    ip = None

                ips = [
                    ip
                    for ip in (ip,)
                    if ip
                ]

                if speed in (0xffff, 0xffffffff):
                    speed = None

                nic = OrderedDict([
                    (self.FIELD_IFACE, iface),
                    (self.FIELD_BRAND, brand),
                    (self.FIELD_BUS, bus_info),
                    (self.FIELD_SPEED, speed),
                    (self.FIELD_MAC, mac),
                    (self.FIELD_IPS, ips),
                    (self.FIELD_MTU, mtu),
                    (self.FIELD_UP, is_up),
                    (self.FIELD_LINKED, is_running),
                ])

                nics.append(nic)

        return nics
