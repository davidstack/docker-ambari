#!/bin/bash
#config shmmax
kernel_version=$(uname -r)
echo $kernel_version
if [ "$kernel_version" \< "3.16.0" ]; then
   echo 1073741824 > /proc/sys/kernel/shmmax
fi

service sshd start
sed s/AMBARI_SERVER_HOSTNAME/$AMBARI_SERVER_HOSTNAME/ /etc/ambari-agent/conf/ambari-agent.ini.template > /etc/ambari-agent/conf/ambari-agent.ini
ambari-agent start >>/dev/null
while true; do sleep 1000; done
