# vim: set ft=dockerfile:

# Requires Ansible 1.8+ from jessie-backports.
FROM debian:jessie-backports

# Colour output.
ENV TERM=xterm

# Defaults to graphical.target.
RUN systemctl set-default multi-user.target

RUN apt-get update -y \
    && apt-get -t jessie-backports install -y ansible \
    && apt-get install -y \
      net-tools \
      ruby \
    && rm -rf /var/lib/apt/lists/*

RUN gem install serverspec
