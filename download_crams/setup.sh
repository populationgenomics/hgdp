#!/bin/bash

set -ex

sudo apt update
sudo apt install -y gcsfuse stackdriver-agent python3-pip

pip3 install click

curl https://d3gcli72yxqn2z.cloudfront.net/connect_latest/v4/bin/ibm-aspera-connect_4.1.0.46-linux_x86_64.tar.gz | tar xz
bash ibm-aspera-connect_4.1.0.46-linux_x86_64.sh

mkdir $HOME/data
