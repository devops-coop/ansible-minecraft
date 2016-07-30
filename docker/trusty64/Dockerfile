# vim: set ft=dockerfile:

FROM ubuntu:trusty

# Colour output.
ENV TERM=xterm

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && apt-add-repository ppa:ansible/ansible \
    && apt-get update -y \
    && apt-get --no-install-recommends install -y \
      ansible \
      default-jdk \
      git \
      net-tools \
      ruby2.0 \
      sudo \
      tar \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN gem2.0 install serverspec
