FROM 10.110.17.138:5000/centos:6.7
MAINTAINER DamonWang
USER root
WORKDIR /root/
COPY files/yum.repos.d /etc/yum.repos.d/
RUN yum clean all; \
    yum makecache;\
	yum install -y openssh-server openssh-clients tar zip unzip which python-pip ambari-server ; \
    yum clean all
COPY files/ambari.properties /etc/ambari-server/conf/ambari.properties
COPY files/serverSetup.py /usr/lib/python2.6/site-packages/ambari_server/serverSetup.py
RUN ambari-server setup -s
COPY files/start.sh /usr/local/bin/
RUN chmod 750 /usr/local/bin/start.sh