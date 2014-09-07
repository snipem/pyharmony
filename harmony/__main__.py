#!/usr/bin/env python2

"""Command line utility for querying the Logitech Harmony."""

import argparse
import logging
import json
import sys

from harmony import auth
from harmony import client as harmony_client

LOGGER = logging.getLogger(__name__)

def login_to_logitech(args):
    """Logs in to the Logitech service.

    Args:
      args: argparse arguments needed to login.

    Returns:
      Session token that can be used to log in to the Harmony device.
    """
    token = auth.login(args.email, args.password)
    if not token:
        sys.exit('Could not get token from Logitech server.')

    session_token = auth.swap_auth_token(
        args.harmony_ip, args.harmony_port, token)
    if not session_token:
        sys.exit('Could not swap login token for session token.')

    return session_token

def pprint(obj):
    """Pretty JSON dump of an object."""
    print(json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')))

def get_client(args):
    """Connect to the Harmony and return a Client instance."""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    return client

def show_config(args):
    """Connects to the Harmony and prints its configuration."""
    client = get_client(args)
    pprint(client.get_config())
    client.disconnect(send_close=True)
    return 0

def show_current_activity(args):
    """Connects to the Harmony and prints the current activity block
    from the config."""
    client = get_client(args)
    config = client.get_config()
    current_activity_id = client.get_current_activity()

    activity = [x for x in config['activity'] if int(x['id']) == current_activity_id][0]

    pprint(activity)

    client.disconnect(send_close=True)
    return 0

def sync(args):
    """Connects to the Harmony and syncs it.
    """
    client = get_client(args)

    client.sync()

    client.disconnect(send_close=True)
    return 0

def get_current_activity_name(args):
    """Get current activity and print its name"""
    token = login_to_logitech(args)
    client = harmony_client.create_and_connect_client(
        args.harmony_ip, args.harmony_port, token)
    activities = client.get_config()['activity']
    current_activity_id = client.get_current_activity()

    for t in activities:
        if int(t['id']) == int(current_activity_id):
            print t['label']

    client.disconnect(send_close=True)
    return 0

def start_activity(args):
    """Connects to the Harmony and switches to a different activity,
    specified as an id or label."""
    client = get_client(args)

    config = client.get_config()

    activity = [x for x in config['activity']
        if (args.activity.isdigit() and int(x['id']) == int(args.activity))
            or x['label'].lower() == args.activity.lower()
    ]

    if not activity:
        LOGGER.error('could not find activity: ' + args.activity)
        client.disconnect(send_close=True)
        return 1

    activity = activity[0]

    client.start_activity(activity['id'])

    LOGGER.info("started activity: '%s' of id: '%s'"%(activity['label'], activity['id']))

    client.disconnect(send_close=True)
    return 0

def main():
    """Main method for the script."""
    parser = argparse.ArgumentParser(
        description='pyharmony utility script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Required flags go here.
    required_flags = parser.add_argument_group('required arguments')
    required_flags.add_argument('--email', required=True, help=(
        'Logitech username in the form of an email address.'))
    required_flags.add_argument(
        '--password', required=True, help='Logitech password.')
    required_flags.add_argument(
        '--harmony_ip', required=True, help='IP Address of the Harmony device.')

    # Flags with defaults go here.
    parser.add_argument('--harmony_port', default=5222, type=int, help=(
        'Network port that the Harmony is listening on.'))
    loglevels = dict((logging.getLevelName(level), level)
                     for level in [10, 20, 30, 40, 50])
    parser.add_argument('--loglevel', default='INFO', choices=loglevels.keys(),
        help='Logging level to print to the console.')

    subparsers = parser.add_subparsers()

    show_config_parser = subparsers.add_parser(
        'show_config', help='Print the Harmony device configuration.')
    show_config_parser.set_defaults(func=show_config)

    show_activity_parser = subparsers.add_parser(
        'show_current_activity', help='Print the current activity config.')
    show_activity_parser.set_defaults(func=show_current_activity)

    start_activity_parser = subparsers.add_parser(
        'start_activity', help='Switch to a different activity.')

    start_activity_parser.add_argument(
        'activity', help='Activity to switch to, id or label.')

    start_activity_parser.set_defaults(func=start_activity)

    sync_parser = subparsers.add_parser(
        'sync', help='Sync the harmony.')

    sync_parser.set_defaults(func=sync)

    get_current_activity_name_parser = subparsers.add_parser(
        'get_current_activity_name', help='Print the Harmony device configuration.')
    get_current_activity_name_parser.set_defaults(func=get_current_activity_name)
    

    args = parser.parse_args()

    logging.basicConfig(
        level=loglevels[args.loglevel],
        format='%(levelname)s:\t%(name)s\t%(message)s')

    sys.exit(args.func(args))

if __name__ == '__main__':
    main()
