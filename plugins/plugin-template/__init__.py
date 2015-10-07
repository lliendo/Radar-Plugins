# -*- coding: utf-8 -*-

"""
Adjust this file to fit your needs. You must set at least the PLUGIN_NAME
class attribute, otherwise your plugin may not work at all !

Optionally you may want to :
----------------------------

    - Set the version of this plugin through the PLUGIN_VERSION class
      attribute, otherwise it will default to 0.0.1.

    - Set a YAML configuration file through the PLUGIN_CONFIG_FILE class
      attribute to let your users configure this plugin.

    - Set the DEFAULT_CONFIG class attribute to a Python dictionary containing
      default values provided users don't set certain parameters in the
      configuration file.

    - Use the log() method to register any activity to the Radar's log file.

If you're using a YAML configuration file you can read those values from the
self.config dictionary.


Also remember that you can read checks and contacts attributes.

Check attributes :
------------------

    - name : This is a string holding name of the check that was defined in a
      check file.

    - path : This is a string that holds the check's path.

    - args : This is a string containing the check's arguments. It can be
      an empty string if the check does not use command line arguments.

    - details : Should be a string but depends on the check's implementation.
      This string may be empty if the check does not reply any details at all.

    - data : Should be a Python dictionary but depends on the check's
      implementation. This dictionary may be empty if the check does not reply
      any data at all.

    - current_status : This is an integer value that indicates the current
      status of a check.

    - previous_status : This is an integer value that indicates the previous
      status of a check.

Contact attributes :
--------------------

    - name : This is a string containing the name of the contact that was
      defined in a contact file.

    - email : This attribute holds the email of the contact that was defined
      in a contact file.

    - phone : Contains a string of the contact's phone number. It may be
      empty if it wasn't defined in the contact's definition.


To convert the numerical value of current_status or previous_status attributes
from the Check class you should use the Check.get_status() static method
available from the radar.check module. To use simply add this import :

    from radar.check import Check

to your plugin's code.

"""


from radar.plugin import ServerPlugin


class PluginTemplate(ServerPlugin):

    PLUGIN_NAME = ''
    PLUGIN_CONFIG_FILE = ServerPlugin.get_path(__file__, '')
    DEFAULT_CONFIG = {}

    def on_start(self):
        pass

    def on_check_reply(self, address, port, checks, contacts):
        """ Implement me. """
        pass

    def on_shutdown(self):
        pass
