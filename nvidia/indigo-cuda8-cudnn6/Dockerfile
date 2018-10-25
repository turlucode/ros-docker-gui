FROM turlucode/ros-indigo:cuda8

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Indigo-Desktop with CUDA 8 and cuDNN 6 support (Ubuntu 14.04)" Vendor="TurluCode" Version="3.0"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

ENV CUDNN_VERSION 6.0.21
LABEL com.turlucode.ros.cudnn="${CUDNN_VERSION}"

RUN echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1404/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn6=$CUDNN_VERSION-1+cuda8.0 \
            libcudnn6-dev=$CUDNN_VERSION-1+cuda8.0 && \
    rm -rf /var/lib/apt/lists/*

# Launch terminator
CMD ["terminator"]