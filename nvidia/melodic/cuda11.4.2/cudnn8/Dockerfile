FROM turlucode/ros-melodic:cuda11.4.2

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Melodic-Desktop with CUDA 11.4.2 and cuDNN 8 support (Ubuntu 18.04)" Vendor="TurluCode" Version="1.0"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

## CUDNN Runtime-packages
ENV NV_CUDNN_VERSION 8.2.4.15
ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda11.4"
LABEL com.turlucode.ros.cudnn="${NV_CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} && \
    rm -rf /var/lib/apt/lists/*

## CUDNN Devel-packages
ENV NV_CUDNN_PACKAGE_DEV "libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda11.4"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ${NV_CUDNN_PACKAGE} \
    ${NV_CUDNN_PACKAGE_DEV} && \
    rm -rf /var/lib/apt/lists/*

RUN apt-mark hold libcudnn8

# Launch terminator
CMD ["terminator"]
