#!/bin/bash
service sshd start
sed s/AMBARI_SERVER_HOSTNAME/$AMBARI_SERVER_HOSTNAME/ /etc/ambari-agent/conf/ambari-agent.ini.template > /etc/ambari-agent/conf/ambari-agent.ini
ambari-agent start >>/dev/null
while true; do sleep 1000; done