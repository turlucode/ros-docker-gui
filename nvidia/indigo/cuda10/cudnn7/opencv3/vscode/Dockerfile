FROM turlucode/ros-indigo:cuda10-cudnn7-opencv3

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Indigo-Desktop with CUDA 10, cuDNN 7, OpenCV v3.4.7 and VS Code support (Ubuntu 14.04)" Vendor="TurluCode" Version="1.4"
LABEL com.turlucode.ros.opencv="3.4.7"

## Install dependencies
RUN apt-get update && apt-get install -y \
software-properties-common \
apt-transport-https \
wget && \
apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -

RUN sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

## Install VS Code
RUN apt-get update && apt-get install -y \
code && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Launch terminator
CMD ["terminator"]
