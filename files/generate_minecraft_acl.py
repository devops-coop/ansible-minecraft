#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate a Minecraft ACL from a list of usernames.
"""

import argparse
import json
import sys
import urllib2
import uuid

MINECRAFT_API_URL = 'https://api.mojang.com/profiles/minecraft'
ACL_CHOICES = ('ops', 'whitelist')
DEFAULT_ACL = 'whitelist'


def get_profiles(usernames, url=None):
    """
    Query the Mojang API to retrieve the profiles (including UUIDs) of the
    given users.
    """
    url = url if url else MINECRAFT_API_URL
    payload = json.dumps(usernames)
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url, data=payload, headers=headers)
    response = urllib2.urlopen(request)
    profiles = json.loads(response.read())
    # The API provides UUIDs without dashes. Convert the provided IDs into
    # the canonical format so Minecraft can load them.
    for profile in profiles:
        profile['uuid'] = str(uuid.UUID(profile['id']))
        profile.pop('id')
    return profiles


def generate_acl(usernames, acl):
    """
    Generate a Minecraft ACL from a list of usernames.
    """
    profiles = get_profiles(usernames)
    if not profiles:
        return
    keys = ('name', 'uuid', 'level')
    results = []
    for profile in profiles:
        profile = {k: profile[k] for k in keys if k in profile}
        if acl == 'ops':
            profile['level'] = 4
        results.append(profile)
    return results


def parse_args(argv):
    """
    Parse command-line arguments. Returns an argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-l', '--acl', choices=ACL_CHOICES, default=DEFAULT_ACL, metavar='',
        help='ACL to generate. Choose from: {1} (default: {0}).'.format(
            DEFAULT_ACL, ', '.join(ACL_CHOICES)
        ),
    )
    parser.add_argument('usernames', nargs='+')
    return parser.parse_args(argv)


def main(argv=None):
    if not argv:
        argv = sys.argv[1:]
    args = parse_args(argv)
    acl = generate_acl(args.usernames, args.acl)
    print json.dumps(acl)

if __name__ == '__main__':
    sys.exit(main())
