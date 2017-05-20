FROM centos:7

ENV TERM=xterm

COPY chef.asc /tmp/chef.asc
COPY chef-stable.repo /etc/yum.repos.d/chef-stable.repo

RUN rpm --import /tmp/chef.asc \
    && yum install -y epel-release \
    && yum install -y \
      ansible \
      inspec-1.25.0-1.el7 \
      wget \
      coreutils \
      net-tools \
    && yum clean all
