# ansible-minecraft

This role installs vanilla [Minecraft](https://minecraft.net/) and configures it to run under [systemd](https://wiki.freedesktop.org/www/Software/systemd/) or [Supervisor](http://supervisord.org/).

## Requirements

* Python 2.7 on the Ansible control machine to generate user ACLs

## Features

* supports Debian 8, Ubuntu 14.04, and RHEL/CentOS 7
* supports different process supervisors on different platforms

    | OS           | Supervisor | systemd |
    |--------------|:----------:|:-------:|
    | Debian 8     | ✓          | ✓       |
    | Ubuntu 14.04 | ✓          |         |
    | CentOS 7     |            | ✓       |

* safely stops the server using [`stop`](http://minecraft.gamepedia.com/Commands#stop) when running under **systemd**
* uses [Vagrant](http://vagrantup.com/) and [Serverspec](http://serverspec.org/) to run integration tests
* manages user ACLs

## Versioning

This project follows [semantic versioning](http://semver.org/).

In the context of semantic versioning, consider the role contract to be defined by the role variables.

* Changes that require user intervention will increase the **major** version. This includes changing the default value of a role variable.
* Changes that do not require user intervention, but add backwards-compatible features, will increase the **minor** version.
* Bug fixes will increase the **patch** version.

## Role variables

The following variable defaults are defined in `defaults/main.yml`.

* `minecraft_version`

    Minecraft version to install (default: `1.9`)

    **N.B.** The default behaviour is to install the latest available minor release in a major release series (e.g., `1.8.x`). Override this default to install a specific minor release (e.g., `1.8.8`).

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

This role includes a `Vagrantfile` to set up the development/testing environment using [Vagrant](http://vagrantup.com).

1. Install [Vagrant](http://vagrantup.com/).
2. Install [vagrant-serverspec](https://github.com/jvoorhis/vagrant-serverspec) to run RSpec tests. [Serverspec](http://serverspec.org/) is a declarative testing framework for server configuration.

    ```
    vagrant plugin install vagrant-serverspec
    ```

3. Run tests with `make`. See `make help` for more information.

    ```
    make jessie64 test
    ```

## License

Apache 2.0

## Disclaimer

To automate the installation, this role automatically accepts the [Minecraft EULA](https://account.mojang.com/documents/minecraft_eula). Be aware that by using this role, you implicitly accept the same EULA.
