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
from radar.check import Check
from radar.contact import Contact


class TestPlugin(TestCase):
    def _get_test_checks(self):
        return [
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

    def _get_test_contacts(self):
        return [
            Contact(name='Hernan', email='hernan@invader'),
            Contact(name='Lucas', email='lucas@invader'),
        ]
