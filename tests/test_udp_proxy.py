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


from nose.tools import raises
from mock import MagicMock
from json import loads
from plugins.udp_proxy import UDPProxyPlugin
from . import TestPlugin


class TestUDDProxyPlugin(TestPlugin):
    def setUp(self):
        self.udp_proxy = UDPProxyPlugin()
        self.udp_proxy.log = MagicMock()
        self.checks = self._get_test_checks()
        self.contacts = self._get_test_contacts()

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
