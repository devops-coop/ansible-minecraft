FROM centos:7

ENV TERM=xterm

RUN yum install -y epel-release \
    && yum install -y \
      ansible \
      git \
      iproute \
      java-1.8.0-openjdk \
      ruby \
      sudo \
      tar \
    && yum clean all

RUN gem install serverspec
