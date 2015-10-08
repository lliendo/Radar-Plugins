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


class ProxyPlugin(ServerPlugin):

        PLUGIN_NAME = 'Proxy plugin'
        PLUGIN_CONFIG_FILE = ServerPlugin.get_path(__file__, 'udp-proxy.yml')

        def _create_socket(self):
            fd = None

            try:
                fd = socket(AF_INET, SOCK_DGRAM)
            except Exception, e:
                self.log('Error - Couldn\'t create UDP socket. Details : {:}.', e)

            return fd

        def _disconnect(self):
            self._fd.close()

        def on_start(self):
            self._fd = self._create_socket()

        def _forward(self, address, checks, contacts):
            serialized = {
                'address': address,
                'checks': [c.to_dict() for c in checks],
                'contacts': [c.to_dict() for c in contacts],
            }

            self._fd.sendto(dumps(serialized) + '\n', (self.config['forward']['to'], self.config['forward']['port']))

        def on_check_reply(self, address, port, checks, contacts):
            try:
                self._forward(address, checks, contacts)
            except Exception, e:
                self.log('Error - Couldn\'t send data. Details : {:}.'.format(e))

        def on_shutdown(self):
            self._disconnect()
