# ansible-minecraft changelog

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
