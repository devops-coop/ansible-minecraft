# vim: set ft=dockerfile:

FROM debian:jessie

# Colour output.
ENV TERM=xterm

RUN apt-get update -y \
    && apt-get install -y apt-transport-https software-properties-common

COPY chef.asc /tmp/chef.asc
COPY chef-stable.list /etc/apt/sources.list.d/chef-stable.list

RUN echo deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main >> /etc/apt/sources.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 \
    && apt-key add /tmp/chef.asc \
    && apt-get update -y \
    && apt-get --no-install-recommends install -y \
      software-properties-common \
      ansible \
      inspec=1.25.0-1 \
      wget \
      coreutils \
      net-tools \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
