Radar plugins
=============

This repository contains a few demonstrative plugins for Radar :

* Email-Notifier.
* UDP-Proxy.
* Plugin-Template.


Documentation
-------------

* Email-Notifier includes two files that can be configured to adjust an email
  notification. The email-notifier.yml file allows you to set different SMTP
  parameters while the email-template file contains a plain text with the
  notification details that you'll receive each time a contact is notified.
  This simple plugin will notify your contacts whenever the current or
  previous status of a check is not OK.

* UDP-Proxy is a very small plugin that allows you to forward check replies to
  a UDP socket. It might not be really useful but it has been included here as
  an example to show you how to read a configuration from a YAML using the
  Radar's plugin API.

* Plugin-Template includes just a Python plugin template that you can use to
  start playing around with Radar plugin development. It contains all the
  details you need to know to effectively implement a plugin without going
  into trouble.
        

Installation
------------

Clone this repository to a temporary directory using `GIT <https://git-scm.com/>`_ (or alternatively download
as `.zip <https://github.com/lliendo/Radar-Plugins/archive/master.zip>`_).

Now manually copy the plugins (which are contained in the plugins directory) you
want to add to your Radar server's plugins directory.


Tests
-----

You'll need to have `Radar <https://github.com/lliendo/Radar>`_ installed on your system to run these tests.

Radar-Plugins uses `Nose <https://nose.readthedocs.org/en/latest/>`_ to run its tests.
To install Nose, from the command line run :

.. code-block:: bash
    
    pip install nose

To run the tests, clone the this repository and run Nose.

.. code-block:: bash

    git clone https://github.com/lliendo/Radar-Plugins.git
    cd Radar-Plugins
    nosetests


License
-------

Radar plugins are distributed under the `GNU LGPLv3 <https://www.gnu.org/licenses/lgpl.txt>`_ license.


Authors
-------

* Lucas Liendo.
