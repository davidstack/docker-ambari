# docker--ambari
#Containerization of ambari

 将ambari-server 和ambari-agent 容器化，并利用ambari提供的blueprint，自动完成hadoop集群搭建。此项目可以用于测试ambari 功能，只需要简单更新安装源就可以

##0. 环境初始化
    0.1 搭建本地的安装源包括ambari和ambari的依赖包
    0.2 下载源码，在目录images中可以获取制作ambari-server 和ambari-agent镜像的源码，只需要更新镜像仓库地址
    0.3 docker build 分别制作ambari-server 和ambari-agent镜像
    0.4 创建docker overlay 网络：docker network create --driver overlay --subnet 172.18.0.0/24 overlay （若不使用swarmkit，需要先配置kv存储）
    0.5 测试场景下，可以不搭建DNS，使用配置hosts文件方式（可以通过卷挂载方式，多容器共享hosts文件）


##1. ambari 集群节点创建
     docker run -itd --name ambari-server.test.com --hostname ambari-server.test.com --ip 172.18.0.2 --net overlay -v /root/ambari/hosts:/etc/hosts --privileged=true 10.110.17.138:5000/iop/ambari-server:v2.0 /usr/local/bin/start.sh
     docker run -itd --name emr-master1.test.com --hostname emr-master1.test.com --ip 172.18.0.3 --net overlay --env AMBARI_SERVER_HOSTNAME=ambari-server.test.com -v /root/ambari/hosts:/etc/hosts --memory 2G   --privileged=true 10.110.17.138:5000/iop/ambari-agent:v2.0 /usr/local/bin/start.sh
     docker run -itd --name emr-master2.test.com --hostname emr-master2.test.com --ip 172.18.0.4 --net overlay --env AMBARI_SERVER_HOSTNAME=ambari-server.test.com -v /root/ambari/hosts:/etc/hosts  --memory 2G      --privileged=true 10.110.17.138:5000/iop/ambari-agent:v2.0 /usr/local/bin/start.sh
     docker run -itd --name emr-edge.test.com --hostname emr-edge.test.com --ip 172.18.0.5 --net overlay --env AMBARI_SERVER_HOSTNAME=ambari-server.test.com -v /root/ambari/hosts:/etc/hosts --memory 2G    --privileged=true  10.110.17.138:5000/iop/ambari-agent:v2.0 /usr/local/bin/start.sh
     docker run -itd --name emr-worker1.test.com --hostname emr-worker1.test.com --ip 172.18.0.6 --net overlay --env AMBARI_SERVER_HOSTNAME=ambari-server.test.com -v /root/ambari/hosts:/etc/hosts  --memory 2G  --privileged=true 10.110.17.138:5000/iop/ambari-agent:v2.0 /usr/local/bin/start.sh
     docker run -itd --name emr-worker2.test.com --hostname emr-worker2.test.com --ip 172.18.0.7 --net overlay --env AMBARI_SERVER_HOSTNAME=ambari-server.test.com -v /root/ambari/hosts:/etc/hosts  --memory 2G   --privileged=true 10.110.17.138:5000/iop/ambari-agent:v2.0 /usr/local/bin/start.sh


##2.ambari 集群创建
     在可以访问ambari-server 容器的服务器上执行 python service_init.py （需要安装python依赖requests）


##3.ambari集群访问
     http://172.18.0.2:8080  也可以做端口映射或者走haproxy代理，使用主机IP访问

##已知Bug：

    1、由于安装hdfs组件时需要切换到hdfs用户，ambari代码应该限制了hdfs用户的切换（参考文件/etc/security/limits.d/hdfs.conf），所以创建容器需要增加 --privileged=true 参数
    2、创建容器时，虽然限制了容器内存，但是ambari manager界面查看到的节点内存仍为宿主机内存
   
