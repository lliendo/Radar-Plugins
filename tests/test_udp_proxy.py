# -*- coding: utf-8 -*-

"""
This file is part of Radar.

Radar is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Radar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with Radar. If not, see <http://www.gnu.org/licenses/>.

Copyright 2015 Lucas Liendo.
"""


from unittest import TestCase
from nose.tools import raises
from mock import MagicMock
from json import loads
from radar.check import Check
from radar.contact import Contact
from plugins.udp_proxy import UDPProxyPlugin


class TestUDDProxyPlugin(TestCase):
    def setUp(self):
        self.udp_proxy = UDPProxyPlugin()
        self.udp_proxy.log = MagicMock()

        self.checks = [
            Check(
                name='Disk usage',
                path='disk-usage.py',
                args='-p / -O 0,8 -W 8,10 -u gib',
                details='Total : 18.21, in use : 7.87, free : 9.39'
            ),
            Check(
                name='Uptime',
                path='uptime.py',
                args='-S 300',
                details='0 days 4 hours 47 minutes'
            ),
            Check(
                name='Ram usage',
                path='ram-usage.py',
                args='-O 0,1000 -W 1000,1900',
                details='Total : 1984.06, in use : 1811.91, available : 847.33'
            ),
        ]

        self.contacts = [
            Contact(name='Hernan', email='hernan@invader'),
            Contact(name='Lucas', email='lucas@invader'),
        ]

    @raises(Exception)
    def test_create_socket_raises_error(self):
        self.udp_proxy._create_docket = MagicMock(side_effect=Exception)
        self.udp_proxy.on_start()
        self.assertTrue(self.udp_proxy.log.called)

    @raises(Exception)
    def test_forward_raises_error(self):
        self.udp_proxy._create_docket = MagicMock(side_effect=Exception)
        self.assertTrue(self.udp_proxy.log.called)

    def test_forward_payload_format(self):
        self.udp_proxy._fd = MagicMock()
        payload = self.udp_proxy._forward('10.0.0.1', self.checks, self.contacts)
        self.assertEqual(type(loads(payload.strip('\n'))), dict)
