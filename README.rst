
Radar plugins
=============

This repository contains (currently) only one plugin and a plugin template (which
you can use as a starting point to develop a plugin) :

    * Email-Notifier.
    * Plugin-Template.


Documentation
-------------

    * Email-Notifier includes two files that can be configured to adjust an email
      notification. The email-notifier.yml file allows you to set different SMTP
      parameters while the email-template file contains a plain text with the
      notification details that you'll receive each time a contact is notified.
      This simple plugin will notify your contacts whenever the current or
      previous status of a check is not OK.
    
    * Plugin-Template includes just a Python plugin template that you can use to
      start playing around with Radar plugin development. It contains all the
      details you need to know to effectively implement a plugins without any
      problems.
        

Installation
------------

Manually copy the plugins (which are contained in the plugins directory) you want
to add to your Radar client's plugins directory.


Tests
-----

Radar plugins uses `Tox <http://codespeak.net/tox/>` to run its tests. To install
Tox, from the command line run :

.. code-block:: bash
    
    pip install tox


To run tests, clone the this repository and run Tox.

.. code-block:: bash

    git clone https://github.com/lliendo/Radar-Plugins.git
    cd Radar-Plugins
    tox


License
-------

Radar plugins are distributed under the LGPL v3 license.


Contact
-------

If you find this software useful you can drop me a line. Bug reporting,
suggestions, missing documentation and critics of any kind are always welcome !


Authors
-------

    * Lucas Liendo.
