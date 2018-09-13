配置新网站
========

## 需要安装的包：

* SCL
* Python 3.6
* nginx
* Git
* pip
* virtualenv

以 CentOS 为例，可以执行下面的命令安装：

    sudo yum install centos-release-scl
    sudo yum install rh-python36
    sudo yum groupinstall 'Development Tools'

    yum -y update
    yum install epel-release
    yum install nginx

## 配置 Nginx 虚拟主机

* 参考 nginx.template.conf
* 把 SITENAME 替换成所需的域名，例如 staging.my-domain.com

## Upstar 任务

* 参考 gunicorn-upstart.template.conf
* 把 SITENAME 替换成所需的域名，例如 staging.my-domain.com

## 文件夹结构：

假设有用户账户，Home 目录为 /home/username

    /home/username 
     └─ sites
        └─ SITENAME
            ├─ database
            ├─ source 
            ├─ static 
            └─ virtualenv

