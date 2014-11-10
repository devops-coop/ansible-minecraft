#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate Minecraft ACLs.
"""

# This script is designed for non-Pythonistas. It must:
#
#   1. be completely self-contained.
#   2. not depend on any third-party libraries.
#
# TODO: Classes should probably be abstracted to collections of single
# resources (e.g., BannedPlayer, WhitelistedPlayer, etc.). But the current
# design works.

from __future__ import print_function

import argparse
import json
import sys
import urllib2
import uuid

from datetime import datetime

MINECRAFT_API_URL = 'https://api.mojang.com/profiles/minecraft'
ACL_CHOICES = ('ops', 'whitelist', 'banned-players', 'banned-ips')
DEFAULT_ACL = 'whitelist'
DEFAULT_BAN_EXPIRES = 'forever'
DEFAULT_BAN_REASON = 'Banned by an operator.'


class ACL(object):
    """
    A Minecraft ACL.
    """
    def __init__(self):
        self.acl = []

    def json(self):
        """
        Returns a pretty-printed JSON representation of the ACL.
        """
        return json.dumps(self.acl, sort_keys=True, indent=2)


class Banlist(ACL):
    """
    A generic Minecraft banlist.
    """
    def __init__(self, created=None, expires=None, reason=None):
        super(Banlist, self).__init__()
        self.created = created if created else datetime.utcnow()
        self.expires = expires if expires else DEFAULT_BAN_EXPIRES
        self.reason = reason if reason else DEFAULT_BAN_REASON
        self.template = {
            # datetime.utcnow() creates a naive datetime object. Since we know
            # the time is in UTC, we will specify the offset explicitly.
            'created': self.created.strftime('%Y-%m-%d %H:%M:%S +0000'),
            'source': 'Server',
            'expires': self.expires,
            'reason': self.reason,
        }


class BannedPlayers(Banlist):
    """
    A list of banned players.
    """
    def __init__(self, usernames):
        super(BannedPlayers, self).__init__()
        uuids = get_uuids(usernames)
        for username, u in uuids.items():
            entry = self.template
            entry['name'] = username
            entry['uuid'] = u
            self.acl.append(entry)


class BannedIPs(Banlist):
    """
    A list of banned IPs.
    """
    def __init__(self, ips):
        super(BannedIPs, self).__init__()
        for ip in ips:
            entry = self.template
            entry['ip'] = ip
            self.acl.append(entry)


class Whitelist(ACL):
    """
    A Minecraft whitelist.
    """
    def __init__(self, usernames):
        """
        Generate a Minecraft whitelist from a list of usernames.
        """
        super(Whitelist, self).__init__()
        uuids = get_uuids(usernames)
        for username, u in uuids.items():
            self.acl.append({'name': username, 'uuid': u})


class Oplist(Whitelist):
    """
    A Minecraft oplist (list of server operators).
    """
    def __init__(self, usernames):
        """
        Generate a Minecraft oplist from a list of usernames.
        """
        super(Oplist, self).__init__(usernames)
        for entry in self.acl:
            entry['level'] = 4


def get_uuids(usernames, url=None):
    """
    Query the Mojang API to return the UUIDs of the given users.

    Args:
        usernames: A list of usernames.
        url: URL of Minecraft API (optional, defaults to MINECRAFT_API_URL).

    Returns:
        A dict mapping Minecraft usernames to UUIDs.
    """
    url = url if url else MINECRAFT_API_URL
    payload = json.dumps(usernames)
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url, data=payload, headers=headers)
    response = urllib2.urlopen(request)
    profiles = json.loads(response.read())
    # The API provides UUIDs without dashes. Convert the provided IDs into
    # the canonical format so Minecraft can load them.
    return dict((p['name'], str(uuid.UUID(p['id']))) for p in profiles)


def parse_args(argv):
    """
    Parse command-line arguments.

    Args:
        argv: A list of command-line arguments (e.g., from sys.argv[1:].
    Returns:
        An argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-l', '--acl', choices=ACL_CHOICES, default=DEFAULT_ACL, metavar='',
        help='ACL to generate. Choose from: {1} (default: {0}).'.format(
            DEFAULT_ACL, ', '.join(ACL_CHOICES)
        ),
    )
    parser.add_argument('items', nargs='+', help='Usernames or IP addresses.')
    return parser.parse_args(argv)


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]
    args = parse_args(argv)
    dispatch = {
        'whitelist': Whitelist,
        'ops': Oplist,
        'banned-players': BannedPlayers,
        'banned-ips': BannedIPs,
    }
    acl = dispatch[args.acl](args.items)
    print(acl.json())

if __name__ == '__main__':
    sys.exit(main())
