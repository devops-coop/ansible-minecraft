#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Generate Minecraft ACLs.
"""

import grp
import json
import os
import pwd
import stat
import tempfile
import uuid

from datetime import datetime as dt

MINECRAFT_API_URL = 'https://api.mojang.com/profiles/minecraft'
ACL_CHOICES = ['ops', 'whitelist', 'banned-players', 'banned-ips']
DEFAULT_ACL = 'whitelist'
DEFAULT_BAN_EXPIRES = 'forever'
DEFAULT_BAN_REASON = 'Banned by an operator.'
MINECRAFT_OP_CODE = 4


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
        self.created = created if created else dt.utcnow()
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
            entry = self.template.copy()
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
            entry = self.template.copy()
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
            entry['level'] = MINECRAFT_OP_CODE


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
    response = open_url(url, data=payload, headers=headers)
    profiles = json.loads(response.read())
    # The API provides UUIDs without dashes. Convert the provided IDs into
    # the canonical format so Minecraft can load them.
    return dict((p['name'], str(uuid.UUID(p['id']))) for p in profiles)


def main(argv=None):
    module = AnsibleModule(
        argument_spec=dict(
            acl=dict(
                default=DEFAULT_ACL,
                choices=ACL_CHOICES,
                type='str',
            ),
            path=dict(
                required=True,
                type='str',
            ),
            values=dict(
                type='list',
            )
        ),
        add_file_common_args=True,
        supports_check_mode=True,
    )

    # Check required file parameters.
    required_args = ['owner', 'group']
    missing_args = [x for x in required_args if not module.params[x]]
    if missing_args:
        module.fail_json(msg='missing required arguments: {}'.format(', '.join(missing_args)))

    path = os.path.expanduser(module.params['path'])
    owner = module.params['owner']
    group = module.params['group']
    mode = module.params['mode'] if module.params['mode'] else 0644

    # Generate appropriate ACL.
    dispatch = {
        'whitelist': Whitelist,
        'ops': Oplist,
        'banned-players': BannedPlayers,
        'banned-ips': BannedIPs,
    }
    acl = dispatch[module.params['acl']](module.params['values'])

    # Compare ACL against existing ACL.
    try:
        with open(path, 'r') as f:
            current_acl = json.load(f)
        st = os.stat(path)
        current_mode = st.st_mode & stat.S_IMODE(st.st_mode)
        # We cannot look up non-existant uids and gids when we compare the
        # current state to desired state. Instead, get the usernames and groups
        # now to make comparison easier.
        current_uid, current_gid = module.user_and_group(path)
        current_user = pwd.getpwuid(current_uid).pw_name
        current_group = grp.getgrgid(current_gid).gr_name
    # Cannot read the file or the file does not exist.
    except (IOError, OSError):
        current_acl = []
        current_user, current_group, current_mode = None, None, None

    changed = any([
        acl.acl != current_acl,
        owner != current_user,
        group != current_group,
        mode != current_mode,
    ])

    if module.check_mode:
        module.exit_json(content=acl.acl, path=path, changed=changed)
        return

    # Write ACL to temporary file; let Ansible clean it up.
    tmp = tempfile.NamedTemporaryFile(delete=False)
    module.add_cleanup_file(tmp.name)
    with open(tmp.name, 'w') as f:
        f.write(acl.json())

    module.atomic_move(tmp.name, path)

    changed = any([
        changed,
        module.set_owner_if_different(path, owner, False),
        module.set_group_if_different(path, group, False),
        module.set_mode_if_different(path, mode, False),
    ])

    module.exit_json(content=acl.acl, path=path, changed=changed)

# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
