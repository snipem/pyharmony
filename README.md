pyharmony
=========

Python library for connecting to and controlling the Logitech Harmony Link

Protocol
--------

As the harmony protocol is being worked out, notes are in PROTOCOL.md.

Status
------

* Authentication to Logitech's web service working.
* Authentication to harmony device working.
* Querying for entire device information
* Sending a simple command to harmony device working.

Usage
-----

To query your device's configuration state:

    PYTHONPATH="." python harmony --email user@example.com --password pass \
        --harmony_ip 192.168.0.1 show_config

It really helps to assign a static lease and hostname for your harmony
on your router interface, so you don't have to keep looking up the IP.

Some other commands you can invoke via command line:

    PYTHONPATH="." python harmony --email user@example.com --password pass \
        --harmony_ip my_hub_host start_activity 'watch movie'

    PYTHONPATH="." python harmony --email user@example.com --password pass \
        --harmony_ip my_hub_host sync

    PYTHONPATH="." python harmony --email user@example.com --password pass \
        --harmony_ip my_hub_host show_current_activity

For full argument information on the command-line tool:

    PYTHONPATH="." python harmony --help

TODO
----

* Figure out how to detect when the session token expires so we can get a new
  one.
* Figure out a good way of sending commands based on sync state.
* Is it possible to update device configuration?
