#!/bin/bash

set -ex

# gcsfuse
echo "deb http://packages.cloud.google.com/apt gcsfuse-focal main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# stackdriver-agent
curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh
sudo bash add-monitoring-agent-repo.sh

apt update
apt install -y gcsfuse stackdriver-agent

service stackdriver-agent start

curl https://d3gcli72yxqn2z.cloudfront.net/connect_latest/v4/bin/ibm-aspera-connect_4.1.0.46-linux_x86_64.tar.gz | tar xz
bash ibm-aspera-connect_4.1.0.46-linux_x86_64.sh

mkdir $HOME/data
gcsfuse cpg-hgdp-main $HOME/data
