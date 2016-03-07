FROM centos:7

ENV TERM=xterm

RUN yum install -y epel-release \
    && yum install -y \
      ansible \
      iproute \
      ruby \
      sudo \
    && yum clean all

RUN gem install serverspec
