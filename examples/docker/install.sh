#!/bin/bash
#
# Script to Install
# Linux System Tools and
# Basic Python Components
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
# GENERAL LINUX

# https://opsx.alibaba.com/mirror
# 使用阿里云镜像地址。修改debian apt 更新地址，pip 地址，设置时区。
# echo  "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n
# deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n
# deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n
# deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n
# deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n
# deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n" > /etc/apt/sources.list && echo /etc/apt/sources.list && \
# echo "[global]\n
# trusted-host=mirrors.aliyun.com\n
# index-url=http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf && \
# ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
#     echo "Asia/Shanghai" > /etc/timezone

apt-get update  # updates the package index cache
apt-get upgrade -y  # updates packages
# installs system tools
apt-get install -y bzip2 gcc git  # system tools
apt-get install -y htop screen vim wget  # system tools
apt-get upgrade -y bash  # upgrades bash if necessary
apt-get clean  # cleans up the package index cache

# INSTALL MINICONDA
# downloads Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.12.0-Linux-x86_64.sh -O Miniconda.sh
bash Miniconda.sh -b  # installs it
rm -rf Miniconda.sh  # removes the installer
export PATH="/root/miniconda3/bin:$PATH"  # prepends the new path

# 添加 conda 国内镜像源 TUNA 清华源
# conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
# 设置搜索时显示通道地址
# conda config --set show_channel_urls yes

# INSTALL PYTHON LIBRARIES
conda install -y pandas  # installs pandas
conda install -y ipython  # installs IPython shell

# CUSTOMIZATION
cd /root/
wget http://hilpisch.com/.vimrc  # Vim configuration	
