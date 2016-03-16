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

from socket import socket, AF_INET, SOCK_DGRAM
from json import dumps
from radar.plugin import ServerPlugin


class UDPProxyPlugin(ServerPlugin):

    PLUGIN_NAME = 'UDP-Proxy'
    PLUGIN_CONFIG_FILE = ServerPlugin.get_path(__file__, 'udp-proxy.yml')
    DEFAULT_CONFIG = {
        'forward': {
            'to': '127.0.0.1',
            'port': 2000,
        }
    }

    def _create_socket(self):
        fd = None

        try:
            fd = socket(AF_INET, SOCK_DGRAM)
        except Exception as error:
            self.log('Error - Couldn\'t create UDP socket. Details : {:}.'.format(error))

        return fd

    def _disconnect(self):
        self._fd.close()

    def on_start(self):
        self._fd = self._create_socket()

    def _forward(self, address, checks, contacts):
        serialized = {
            'address': address,
            'checks': [check.to_dict() for check in checks],
            'contacts': [contact.to_dict() for contact in contacts],
        }

        payload = dumps(serialized) + '\n'
        self._fd.sendto(payload, (self.config['forward']['to'], self.config['forward']['port']))

        return payload

    def on_check_reply(self, address, port, checks, contacts):
        try:
            self._forward(address, checks, contacts)
        except Exception as error:
            self.log('Error - Couldn\'t forward data. Details : {:}.'.format(error))

    def on_shutdown(self):
        self._disconnect()
