#!/bin/bash

set -e;

# Install Python 3.7
wget https://www.python.org/ftp/python/3.7.12/Python-3.7.12.tar.xz;

tar -xf Python-3.7.12.tar.xz;
mv Python-3.7.12 /opt/Python-3.7.12

apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev -y;

cd /opt/Python-3.7.12;
./configure --enable-optimizations --enable-shared;
make -j 4;
make altinstall;
ldconfig /opt/Python-3.7.12;

# Install pip for Python 3.7
wget https://bootstrap.pypa.io/get-pip.py;
python3.7 get-pip.py;
python3.7 -m pip install --upgrade pip

# Install a couple of libraries through pip
python3.7 -m pip install protobuf pyparsing