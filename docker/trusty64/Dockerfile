# vim: set ft=dockerfile:

FROM ubuntu:trusty

# Colour output.
ENV TERM=xterm

RUN apt-get install -y software-properties-common \
    && apt-add-repository ppa:ansible/ansible \
    && apt-get update -y \
    && apt-get --no-install-recommends install -y \
      ansible \
      net-tools \
      ruby2.0 \
    && rm -rf /var/lib/apt/lists/*

RUN gem2.0 install serverspec
