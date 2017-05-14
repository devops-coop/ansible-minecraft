# vim: set ft=dockerfile:

FROM ubuntu:xenial

# Colour output.
ENV TERM=xterm

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && apt-add-repository ppa:ansible/ansible \
    && apt-get update -y \
    && apt-get --no-install-recommends install -y \
      ansible \
      wget \
      coreutils \
      net-tools \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## https://downloads.chef.io/inspec/1.24.0
RUN wget -q https://packages.chef.io/files/stable/inspec/1.24.0/ubuntu/16.04/inspec_1.24.0-1_amd64.deb \
  && echo "33e8ab3dd4ed7eb2285310ae9d0a32e0cc45d5b6d057a29541f93870c2f9e30a  inspec_1.24.0-1_amd64.deb" \
  | sha256sum -c \
  && dpkg -i inspec_1.24.0-1_amd64.deb \
  && rm inspec_1.24.0-1_amd64.deb
