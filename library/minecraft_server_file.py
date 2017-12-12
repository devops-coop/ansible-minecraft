#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Generate Minecraft server files (ACLs and server.properties).
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
SERVER_FILE_CHOICES = [
    'banned-ips',
    'banned-players',
    'ops',
    'server-properties',
    'whitelist',
]
DEFAULT_BAN_EXPIRES = 'forever'
DEFAULT_BAN_REASON = 'Banned by an operator.'
MINECRAFT_OP_CODE = 4


class BadValuesTypeException(Exception):

    def __init__(self, expected_type, actual_type):
        super(BadValuesTypeException, self).__init__(
            'expected "values" to be {} but got {}'.format(
                expected_type, actual_type))


class MissingArgsException(Exception):

    def __init__(self, missing_args):
        super(MissingArgsException, self).__init__(
            'missing required arguments: {}'.format(', '.join(missing_args)))


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
        self.mode = module.params['mode'] if module.params['mode'] else 0o644

    @property
    def changed(self):
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

    def update(self):
        self.module.set_owner_if_different(self.path, self.owner, False)
        self.module.set_group_if_different(self.path, self.group, False)
        self.module.set_mode_if_different(self.path, self.mode, False)


class ServerFile(object):
    """
    Abstract class representing any server file.
    """

    # Override this with the expected type of the 'values' parameter.
    VALUES_TYPE = list

    def __init__(self, module):
        self.module = module
        self.values = self.module.params['values']
        actual_values_type = type(self.values)
        if actual_values_type is not self.VALUES_TYPE:
            raise BadValuesTypeException(self.VALUES_TYPE, actual_values_type)
        self.stats = FileStats(module)

    @property
    def content(self):
        """
        Return content in its native format (e.g. dict).
        """
        raise NotImplementedError

    def as_str(self):
        """
        Return content as a string, for saving to a file.
        """
        return self.content

    @property
    def changed(self):
        """
        Indicates whether the content changed or not.
        """
        raise NotImplementedError


class ServerProperties(ServerFile):
    """
    The Minecraft server.properties file.

    The module "values" argument should be a dictionary of property names and
    values.
    """
    VALUES_TYPE = dict

    def __init__(self, module):
        super(ServerProperties, self).__init__(module)
        self._content_changed = False
        self.newlines = []
        properties = self.values.copy()

        # Convert all values to strings.  The default booleans in
        # server.properties are represented by "true" and "false" instead of
        # Python's "True" and "False", so convert them explicitly.
        for name, value in properties.iteritems():
            properties[name] = str(value).lower() if isinstance(value, bool) else str(value)

        with open(self.stats.path) as filein:
            for line in filein:
                if line.startswith('#'):
                    self.newlines.append(line)
                    continue

                name, eq, val = [x.strip() for x
                                 in line.strip().partition('=')]
                if eq and name in properties:
                    self.newlines.append('{0}={1}\n'.format(name, properties[name]))
                    current = properties.pop(name)
                    if current != val:
                        self._content_changed = True
                else:
                    self.newlines.append(line)

        for name, value in properties.iteritems():
            self.newlines.append('{0}={1}\n'.format(name, value))
            self._content_changed = True

    @property
    def content(self):
        return ''.join(self.newlines)

    @property
    def changed(self):
        return self._content_changed


class ACL(ServerFile):
    """
    A Minecraft ACL.
    """
    def __init__(self, module):
        super(ACL, self).__init__(module)
        self.acl = []

    @property
    def changed(self):
        try:
            with open(self.stats.path, 'r') as f:
                current_acl = json.load(f)
        except (IOError, OSError):
            current_acl = []

        return current_acl != self.acl

    @property
    def content(self):
        return self.acl

    def as_str(self):
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
                required=True,
                type='raw',
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
        module.fail_json(msg=e)
    except BadValuesTypeException as e:
        module.fail_json(msg=e)

    changed = server_file.stats.changed or server_file.changed

    if module.check_mode:
        module.exit_json(content=server_file.content,
                         path=server_file.stats.path,
                         changed=changed)
        return

    if changed:
        # Write to temporary file; let Ansible clean it up.
        tmp = tempfile.NamedTemporaryFile(delete=False)
        module.add_cleanup_file(tmp.name)
        with open(tmp.name, 'w') as f:
            f.write(server_file.as_str())

        module.atomic_move(tmp.name, server_file.stats.path)
        server_file.stats.update()

    module.exit_json(content=server_file.content,
                     path=server_file.stats.path,
                     changed=changed)


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
