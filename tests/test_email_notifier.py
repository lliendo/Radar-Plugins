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
from mock import Mock, MagicMock
from radar.check import Check
from radar.contact import Contact
from plugins.email_notifier import EmailNotifier


class TestEmailNotifierPlugin(TestCase):
    def setUp(self):
        m = Mock()
        self.email_notifier = EmailNotifier()
        self.email_notifier._smtp_connect = MagicMock(return_value=m)
        self.email_notifier._disconnect = MagicMock(return_value=m)
        self.email_notifier.log = MagicMock()

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

    def test_no_need_to_notify(self):
        for c in self.checks:
            c.current_status = Check.STATUS['OK']
            c.previous_status = Check.STATUS['OK']

        self.email_notifier.on_check_reply('10.0.0.1', 45000, self.checks, self.contacts)
        self.assertFalse(self.email_notifier._smtp_server.sendmail.called)

    def test_need_to_notify(self):
        for c in self.checks:
            c.current_status = Check.STATUS['SEVERE']

        self.email_notifier.on_check_reply('10.0.0.1', 45000, self.checks, self.contacts)
        self.assertTrue(self.email_notifier._smtp_server.sendmail.called)

    def test_login_is_performed(self):
        self.email_notifier.config['auth']['username'] = 'username'
        self.email_notifier.config['auth']['password'] = 'password'
        self.email_notifier._smtp_login = MagicMock()
        self.email_notifier.on_check_reply('10.0.0.1', 45000, [], [])
        self.assertTrue(self.email_notifier._smtp_login.called)

    def test_login_is_not_performed(self):
        self.email_notifier._smtp_login = MagicMock()
        self.email_notifier.on_check_reply('10.0.0.1', 45000, [], [])
        self.assertFalse(self.email_notifier._smtp_login.called)

    @raises(Exception)
    def test_connect_raises_error(self):
        self.email_notifier._smtp_connect = MagicMock(side_effect=Exception)
        self.email_notifier.on_check_reply('10.0.0.1', 45000, [], [])
        self.assertTrue(self.email_notifier.log.called)

    @raises(Exception)
    def test_login_raises_error(self):
        self.email_notifier._smtp_login = MagicMock(side_effect=Exception)
        self.email_notifier.on_check_reply('10.0.0.1', 45000, [], [])
        self.assertTrue(self.email_notifier.log.called)

    @raises(Exception)
    def test_notify_raises_error(self):
        self.email_notifier._notify = MagicMock(side_effect=Exception)
        self.email_notifier.on_check_reply('10.0.0.1', 45000, [], [])
        self.assertTrue(self.email_notifier.log.called)

    def test_build_email(self):
        self.email_notifier.config['sender'] = 'unknown@localhost'
        email = self.email_notifier._build_email('10.0.0.1', self.checks[0], self.contacts)
        self.assertEqual(email['From'], self.email_notifier.config['sender'])
        self.assertEqual(len(email['To'].split(',')), 2)
