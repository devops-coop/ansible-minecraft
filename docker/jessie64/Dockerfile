# vim: set ft=dockerfile:

# Requires Ansible 1.8+ from jessie-backports.
FROM debian:jessie-backports

# Colour output.
ENV TERM=xterm

# Defaults to graphical.target.
RUN systemctl set-default multi-user.target

RUN grep -rl httpredir.debian.org /etc/apt/sources.list* \
    | xargs sed -i 's/httpredir.debian.org/ftp.us.debian.org/g'

RUN apt-get update -y \
    && apt-get -t jessie-backports install --no-install-recommends -y ansible \
    && apt-get --no-install-recommends install -y \
      net-tools \
      ruby \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN gem install serverspec
