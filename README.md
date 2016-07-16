# ansible-minecraft

[![Build Status](https://travis-ci.org/benwebber/ansible-minecraft.svg?branch=master)](https://travis-ci.org/benwebber/ansible-minecraft)

This role installs vanilla [Minecraft](https://minecraft.net/) and configures it to run under [systemd](https://wiki.freedesktop.org/www/Software/systemd/) or [Supervisor](http://supervisord.org/).

**If you're viewing this at https://github.com/benwebber/ansible-minecraft/, you're reading the documentation for the master branch.
[View documentation for the latest release
 (3.0.0).](https://github.com/benwebber/ansible-minecraft/tree/v3.0.0#ansible-minecraft)**

## Requirements

* **Optional:** Python 2.7 on the Ansible control machine to generate user ACLs
* **Optional:** Ansible 2.0.2+ or `curl` on the control machine to fetch the latest Minecraft version

## Features

* supports Debian 8, Ubuntu 14.04, and RHEL/CentOS 7
* supports different process supervisors on different platforms

    | OS           | Supervisor | systemd |
    |--------------|:----------:|:-------:|
    | Debian 8     | ✓          | ✓       |
    | Ubuntu 14.04 | ✓          |         |
    | CentOS 7     |            | ✓       |

* safely stops the server using [`stop`](http://minecraft.gamepedia.com/Commands#stop) when running under **systemd**
* uses [Docker](https://www.docker.com/) and [Serverspec](http://serverspec.org/) to run integration tests
* manages user ACLs
* manages `server.properties`
* hooks: include arbitrary tasks at specific stages during execution

## Versioning

This project follows [semantic versioning](http://semver.org/).

In the context of semantic versioning, consider the role contract to be defined by the role variables.

* Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
* Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
* Bug fixes will increase the **patch** version.

Refer to the [change log](CHANGELOG.md) for upcoming changes.

## Role variables

The following variable defaults are defined in `defaults/main.yml`.

* `minecraft_version`

    Minecraft version to install (default: `latest`)

    Examples:

    ```yaml
    minecraft_version: latest
    minecraft_version: 1.10
    minecraft_version: 1.9.1
    minecraft_version: 16w21a
    ```

* `minecraft_url`

    Minecraft download URL (default: `https://s3.amazonaws.com/Minecraft.Download/versions`)

* `minecraft_user`

    system user Minecraft runs as (default: `minecraft`)

* `minecraft_group`

    system group Minecraft runs as (default: `minecraft`)

* `minecraft_home`

    directory to install Minecraft to (default: `/srv/minecraft`)

* `minecraft_max_memory`

    Java max memory (`-Xmx`) to allocate (default: `1024M`)

* `minecraft_initial_memory`

    Java initial memory (`-Xms`) to allocate (default: `1024M`)

* `minecraft_supervisor_name`

    Supervisor program name (default: `minecraft`)

* `minecraft_process_control`

    Choose between `systemd` and `supervisor` (default: `systemd`).

* `minecraft_whitelist`

    list of Minecraft usernames to whitelist (default: `[]`)

* `minecraft_ops`

    list of Minecraft usernames to make server ops (default: `[]`)

* `minecraft_banned_players`

    list of Minecraft usernames to ban (default: `[]`)

* `minecraft_banned_ips`

    list of IP addresses to ban (default: `[]`)

* `minecraft_server_properties`

    dictionary of server.properties entries (e.g. `server-port: 25565`) to set (default: `{}`)

## Hooks and run stages

**ansible-minecraft** organizes execution into a number of run stages:

* `setup`
    * install prerequisites (e.g., Java)
    * create Minecraft user and group
* `download`
    * fetch the latest version of from the launcher API
    * download Minecraft
* `install`
    * symlink version to `minecraft_server.jar`
    * agree to EULA
* `acl`
    * configure server ACLs (whitelist, banned players, etc.)
* `configure`
    * set `server.properties`
* `start`
    * (re)start server

You can execute custom tasks before or after specific stages. Simply specify a [task include file](https://docs.ansible.com/ansible/playbooks_roles.html#task-include-files-and-encouraging-reuse) using the relevant role variable:

```yaml
- hosts: minecraft
  roles:
    - role: benwebber.minecraft
      minecraft_hook_before_start: "{{ playbook_dir }}/download-world-from-s3.yml"
```

The available hooks are:

* `minecraft_hook_before_setup`

    run before `setup` tasks

* `minecraft_hook_after_setup`

    run after `setup` tasks

* `minecraft_hook_before_download`

    run before `download` tasks

* `minecraft_hook_after_download`

    run after `download` tasks

* `minecraft_hook_before_install`

    run before `install` tasks

* `minecraft_hook_after_install`

    run after `install` tasks

* `minecraft_hook_before_start`

    run before `start` tasks

* `minecraft_hook_after_start`

    run after `start` tasks

## Example

```yaml
- hosts: minecraft
  roles:
     - { role: benwebber.minecraft, minecraft_whitelist: ["jeb_", "dinnerbone"]}
```

## Contributing

Pull requests are welcome. Among other features, this role lacks support for custom Minecraft servers.

### Testing

This role includes a Docker-based test harness for integration testing.

1. Install [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/).

2. Run tests with `make`.
    ```
    make jessie64 test
    ```

Integration tests use **systemd** by default. Set `PROCESS_CONTROL` to
change this:

```
make trusty64 test PROCESS_CONTROL=supervisor
```

See `make help` for more information.

## License

Apache 2.0

## Disclaimer

To automate the installation, this role automatically accepts the [Minecraft EULA](https://account.mojang.com/documents/minecraft_eula). Be aware that by using this role, you implicitly accept the same EULA.
