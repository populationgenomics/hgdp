FROM google/cloud-sdk:361.0.0-slim

# Aspera doesn't install for the root user.
RUN useradd -m aspera
USER aspera
WORKDIR /home/aspera

RUN curl https://d3gcli72yxqn2z.cloudfront.net/connect_latest/v4/bin/ibm-aspera-connect_4.1.0.46-linux_x86_64.tar.gz | tar xz && \
    ./ibm-aspera-connect_4.1.0.46-linux_x86_64.sh && \
    rm ibm-aspera-connect_4.1.0.46-linux_x86_64.sh

# Allow Hail Batch to create files in /io.
USER root
