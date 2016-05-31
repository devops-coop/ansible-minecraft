# ansible-minecraft changelog

## 2.2.0 (2016-05-30)

* It is now possible to install the latest major release of Minecraft using `minecraft_version: latest`. This will be the default behaviour in the next major version of this role (3).
* Only generate ACL JSON files if the variables (e.g., `minecraft_ops`) are non-empty.

## 2.1.1 (2016-03-08)

* Notify Galaxy on successful build.

## 2.1.0 (2016-03-08)

### Changes

* Fix minimum Ansible version (requires Ansible 1.8+).
* Replace Vagrant test environments with Docker test harness.
* Integrate Travis CI for automated integration testing.

## 2.0.0 (2016-03-01)

### Changes

* Install latest 1.9 release by default.
* Change default process supervisor (`minecraft_process_control`) from `supervisor` to `systemd`.
