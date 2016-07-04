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
SERVER_FILE_CHOICES = ['ops', 'whitelist', 'banned-players', 'banned-ips',
                       'server-properties']
DEFAULT_BAN_EXPIRES = 'forever'
DEFAULT_BAN_REASON = 'Banned by an operator.'
MINECRAFT_OP_CODE = 4


class MissingArgsException(Exception):

    def __init__(self, missing_args):
        super(MissingArgsException, self).__init__(
            message='missing required arguments: {}'.format(
                ', '.join(missing_args)))


class BadValueException(Exception):

    def __init__(self, bad_value):
        super(BadValueException, self).__init__(
            message='bad value: {}'.format(bad_value))


class FileStats(object):
    """
    Compare and update file stats.
    """
    REQUIRED_ARGS = ['owner', 'group']

    def __init__(self, module):
        self.module = module
        missing_args = [x for x in self.REQUIRED_ARGS
                        if not self.module.params[x]]
        if missing_args:
            raise MissingArgsException(missing_args)

        self.path = os.path.expanduser(module.params['path'])
        self.owner = module.params['owner']
        self.group = module.params['group']
        self.mode = module.params['mode'] if module.params['mode'] else 0644

    def file_stats_changed(self):
        try:
            st = os.stat(self.path)
        except OSError:
            # If the file doesn't exist or isn't read, this is the same as
            # the stat values being wrong.
            return True

        current_mode = st.st_mode & stat.S_IMODE(st.st_mode)
        # We cannot look up non-existant uids and gids when we compare the
        # current state to desired state. Instead, get the usernames and
        # groups now to make comparison easier.
        current_uid, current_gid = self.module.user_and_group(self.path)
        current_user = pwd.getpwuid(current_uid).pw_name
        current_group = grp.getgrgid(current_gid).gr_name

        return any([
            self.owner != current_user,
            self.group != current_group,
            self.mode != current_mode,
        ])

    def correct_file_stats(self):
        self.module.set_owner_if_different(self.path, self.owner, False)
        self.module.set_group_if_different(self.path, self.group, False)
        self.module.set_mode_if_different(self.path, self.mode, False)


class ServerFile(object):
    """
    Abstract class representing any server file.
    """
    def __init__(self, module):
        self.module = module
        self.values = self.module.params['values']
        self.stats = FileStats(module)

    def content(self):
        """
        Return content in its native format (e.g. dict).
        """
        raise NotImplementedError

    def content_str(self):
        """
        Return content as a string, for saving to a file.
        """
        return self.content()

    def content_changed(self):
        """
        Indicates whether the content changed or not.
        """
        raise NotImplementedError


class ServerProperties(ServerFile):
    """
    The Minecraft server.properties file.

    The module "values" argument should be a list of strings in the format
    "<name>=<value>".
    """
    def __init__(self, module):
        super(ServerProperties, self).__init__(module)
        self._content_changed = False
        self.newlines = []
        properties = {}

        for a in self.values:
            name, eq, val = a.partition('=')
            if not eq:
                raise BadValueException(name)
            properties[name] = val

        filein = file(self.stats.path)

        for line in filein:
            if line.startswith('#'):
                self.newlines.append(line)
            else:
                name, eq, val = line.strip().partition('=')
                if eq and name in properties:
                    self.newlines.append('%s=%s\n' % (name, properties[name]))
                    if properties[name] != val:
                        self._content_changed = True
                    del properties[name]
                else:
                    self.newlines.append(line)

        for name, value in properties.iteritems():
            self.newlines.append('%s=%s\n' % (name, value))
            self._content_changed = True

    def content(self):
        return ''.join(self.newlines)

    def content_changed(self):
        return self._content_changed


class ACL(ServerFile):
    """
    A Minecraft ACL.
    """
    def __init__(self, module):
        super(ACL, self).__init__(module)
        self.acl = []

    def content_changed(self):
        try:
            with open(self.stats.path, 'r') as f:
                current_acl = json.load(f)
        except (IOError, OSError):
            current_acl = []

        return current_acl != self.acl

    def content(self):
        return self.acl

    def content_str(self):
        return self.json()

    def json(self):
        """
        Returns a pretty-printed JSON representation of the ACL.
        """
        return json.dumps(self.acl, sort_keys=True, indent=2)


class Banlist(ACL):
    """
    A generic Minecraft banlist.
    """
    def __init__(self, module, created=None, expires=None, reason=None):
        super(Banlist, self).__init__(module)
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

    The module "values" argument should be a list of usernames.
    """
    def __init__(self, module):
        super(BannedPlayers, self).__init__(module)
        uuids = get_uuids(self.values)
        for username, u in uuids.items():
            entry = self.template.copy()
            entry['name'] = username
            entry['uuid'] = u
            self.acl.append(entry)


class BannedIPs(Banlist):
    """
    A list of banned IPs.

    The module "values" argument should be a list of IP addresses.
    """
    def __init__(self, module):
        super(BannedIPs, self).__init__(module)
        for ip in self.values:
            entry = self.template.copy()
            entry['ip'] = ip
            self.acl.append(entry)


class Whitelist(ACL):
    """
    A Minecraft whitelist.

    The module "values" argument should be a list of usernames.
    """
    def __init__(self, module):
        """
        Generate a Minecraft whitelist from a list of usernames.
        """
        super(Whitelist, self).__init__(module)
        uuids = get_uuids(self.values)
        for username, u in uuids.items():
            self.acl.append({'name': username, 'uuid': u})


class Oplist(Whitelist):
    """
    A Minecraft oplist (list of server operators).

    The module "values" argument should be a list of usernames.
    """
    def __init__(self, module):
        """
        Generate a Minecraft oplist from a list of usernames.
        """
        super(Oplist, self).__init__(module)
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
            server_file=dict(
                required=True,
                choices=SERVER_FILE_CHOICES,
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

    # Generate appropriate ACL.
    dispatch = {
        'whitelist': Whitelist,
        'ops': Oplist,
        'banned-players': BannedPlayers,
        'banned-ips': BannedIPs,
        'server-properties': ServerProperties,
    }

    try:
        server_file = dispatch[module.params['server_file']](module)
    except MissingArgsException as e:
        module.fail_json(e.message)

    changed = (server_file.stats.file_stats_changed() or
               server_file.content_changed())

    if module.check_mode:
        module.exit_json(content=server_file.content(),
                         path=server_file.stats.path,
                         changed=changed)
        return

    if changed:
        # Write to temporary file; let Ansible clean it up.
        tmp = tempfile.NamedTemporaryFile(delete=False)
        module.add_cleanup_file(tmp.name)
        with open(tmp.name, 'w') as f:
            f.write(server_file.content_str())

        module.atomic_move(tmp.name, server_file.stats.path)
        server_file.stats.correct_file_stats()

    module.exit_json(content=server_file.content(),
                     path=server_file.stats.path,
                     changed=changed)


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
