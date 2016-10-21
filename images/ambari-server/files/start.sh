#!/bin/bash
#config shmmax
kernel_version=$(uname -r)
echo $kernel_version
if [ "$kernel_version" \< "3.16.0" ]; then
   echo 1073741824 > /proc/sys/kernel/shmmax
fi
ambari-server start >>/dev/null
while true; do sleep 1000; done
