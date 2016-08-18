FROM 10.110.17.138:5000/centos:6.7
MAINTAINER DamonWang
USER root
WORKDIR /root/
COPY files/yum.repos.d /etc/yum.repos.d/
RUN yum clean all; \
    yum makecache;\
	yum install -y openssh-server openssh-clients tar zip unzip which python-pip ambari-agent; \
    yum clean all
COPY files/ambari-agent.ini.template  /etc/ambari-agent/conf
RUN chmod 755 /etc/ambari-agent/conf/ambari-agent.ini.template
COPY files/start.sh /usr/local/bin/
RUN chmod 750 /usr/local/bin/start.sh