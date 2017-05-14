FROM centos:7

ENV TERM=xterm

RUN yum install -y epel-release \
    && yum install -y \
      ansible \
      wget \
      coreutils \
      net-tools \
    && yum clean all

## https://downloads.chef.io/inspec/1.24.0
RUN wget -q https://packages.chef.io/files/stable/inspec/1.24.0/el/7/inspec-1.24.0-1.el7.x86_64.rpm \
  && echo "c3b739f4262a56ad1626a4c46465a9905d3ab2d36514c4cfdc998cd2dae24f90  inspec-1.24.0-1.el7.x86_64.rpm" \
  | sha256sum -c \
  && yum install -y inspec-1.24.0-1.el7.x86_64.rpm \
  && rm inspec-1.24.0-1.el7.x86_64.rpm
