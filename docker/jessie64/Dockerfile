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
    && apt-get --no-install-recommends install -y \
      gcc \
      python-dev \
      libffi-dev \
      libssl-dev \
      python-pip \
      net-tools \
      ruby \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U setuptools

# A newish version of ansible is required, so install from pip instead of from
# the old Debian package.
RUN pip install ansible

RUN gem install serverspec
