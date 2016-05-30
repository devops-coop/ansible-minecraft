# ansible-minecraft

[![Build Status](https://travis-ci.org/benwebber/ansible-minecraft.svg?branch=master)](https://travis-ci.org/benwebber/ansible-minecraft)

This role installs vanilla [Minecraft](https://minecraft.net/) and configures it to run under [systemd](https://wiki.freedesktop.org/www/Software/systemd/) or [Supervisor](http://supervisord.org/).

## Requirements

* Python 2.7 on the Ansible control machine to generate user ACLs
* **Optional:** Ansible 2.0.2+, `httplib2`, or `curl` on the control machine to fetch the latest Minecraft version

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

## Versioning

This project follows [semantic versioning](http://semver.org/).

In the context of semantic versioning, consider the role contract to be defined by the role variables.

* Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
* Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
* Bug fixes will increase the **patch** version.

### Upcoming changes

#### Change to default server version

In the next major release (3), the default server version (`minecraft_version`) will change from `1.9` to `latest`. The role will query the [launcher API](https://launchermeta.mojang.com/mc/game/version_manifest.json) to determine the latest release.

## Role variables

The following variable defaults are defined in `defaults/main.yml`.

* `minecraft_version`

    Minecraft version to install (default: `1.9`)

    **N.B.** The default behaviour is to install the latest available minor release in a major release series (e.g., `1.8.x`). Override this default to install a specific minor release (e.g., `1.8.8`).

    To install the latest stable release, set `minecraft_version: latest`.

    To install a snapshot, use the snapshot version: `minecraft_version: 16w21a`.

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

2. Run tests with `make`. See `make help` for more information.

    ```
    make jessie64 test
    ```

## License

Apache 2.0

## Disclaimer

To automate the installation, this role automatically accepts the [Minecraft EULA](https://account.mojang.com/documents/minecraft_eula). Be aware that by using this role, you implicitly accept the same EULA.
