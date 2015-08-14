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

from smtplib import SMTP, SMTP_SSL
from socket import setdefaulttimeout, getdefaulttimeout
from email.mime.text import MIMEText
from radar.plugin import ServerPlugin
from radar.check import Check


class EmailNotifier(ServerPlugin):

    PLUGIN_NAME = 'Email-Notifier'
    PLUGIN_CONFIG_FILE = ServerPlugin.get_path(__file__, 'email-notifier.yml')
    DEFAULT_CONFIG = {
        'connect': {
            'to': 'localhost',
            'port': 25,
            'secure': False,
            'timeout': 5,
        },

        'auth': {
            'username': '',
            'password': '',
        },

        'sender': 'radar@localhost',
    }

    def _smtp_connect(self):
        smtp_server = None

        if self.config['connect']['secure']:
            SMTPServer = SMTP_SSL
        else:
            SMTPServer = SMTP

        try:
            smtp_server = SMTPServer(self.config['connect']['to'], self.config['connect']['port'])
        except Exception, e:
            self.log('Error - Couldn\'t connect to {:}:{:}. Details : {:}'.format(
                self.config['connect']['to'], self.config['connect']['port'], e)
            )

        return smtp_server

    def _smtp_login(self, smtp_server):
        if (self.config['auth']['username'] != '') and (self.config['auth']['password'] != ''):
            try:
                smtp_server.login(self.config['auth']['username'], self.config['auth']['password'])
            except Exception, e:
                self.log('Error - Couldn\'t login to {:}:{:}. Details : {:}'.format(
                    self.config['connect']['to'], self.config['connect']['port'], e)
                )

    def _set_timeout(self):
        default_timeout = getdefaulttimeout()
        setdefaulttimeout(self.config['connect']['timeout'])

        return default_timeout

    def _restore_timeout(self, timeout):
        setdefaulttimeout(timeout)

    def _connect(self):
        default_timeout = self._set_timeout()
        smtp_server = self._smtp_connect()
        self._smtp_login(smtp_server)
        self._restore_timeout(default_timeout)

        return smtp_server

    def _disconnect(self):
        try:
            self._smtp_server.quit()
        except Exception, e:
            self.log('Error - Couldn\'t disconnect from {:}:{:}. Details : {:}'.format(
                self.config['connect']['to'], self.config['connect']['port'], e)
            )

        return None

    def _read_template(self):
        with open(ServerPlugin.get_path(__file__, 'email-template')) as fd:
            return fd.read()

    def _render_template(self, template, host, check):
        d = {
            'host': host,
            'path': check.path,
            'args': check.args,
            'details': check.details,
            'current status': Check.get_status(check.current_status),
            'previous status': Check.get_status(check.previous_status)
        }

        return template.format(**d)

    def _build_email(self, host, check, contacts):
        template = self._read_template()
        email = MIMEText(self._render_template(template, host, check))
        email['Subject'] = 'Radar notification : {:} - {:}'.format(check.name, host)
        email['From'] = self.config['sender']
        email['To'] = ', '.join([c.email for c in contacts])

        return email

    def _should_notify(self, check):
        return (check.current_status != Check.STATUS['OK']) or (check.previous_status != Check.STATUS['OK'])

    def _notify(self, host, checks, contacts):
        emails = [self._build_email(host, c, contacts) for c in checks if self._should_notify(c)]
        recipients = [c.email for c in contacts]

        try:
            [self._smtp_server.sendmail(self.config['sender'], recipients, e.as_string()) for e in emails]
        except Exception, e:
            self.log('Error - Couldn\'t send notifications. Details : {:}.'.format(e))

    def on_check_reply(self, address, port, checks, contacts):
        self._smtp_server = self._connect()
        self._notify(address, checks, contacts)
        self._smtp_server = self._disconnect()
