FROM turlucode/ros-melodic:cuda10

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Melodic-Desktop with CUDA 10 and cuDNN 7 support (Ubuntu 18.04)" Vendor="TurluCode" Version="1.1"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

ENV CUDNN_VERSION 7.6.5.32
LABEL com.turlucode.ros.cudnn="${CUDNN_VERSION}"

## CUDNN Runtime-packages
RUN wget -q https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb \
    && echo "a7e21448181bf69b2f4b9fb3e8c8bdfd962e327b1716d34608488641b4199bb2 libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb" | sha256sum -c - \
    && dpkg -i libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb \
    && rm -f libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb \
    && apt-mark hold libcudnn7

## CUDNN Devel-packages
RUN wget -q https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libcudnn7-dev_7.6.5.32-1+cuda10.0_amd64.deb \
    && echo "2a9a15089040ea53c5ed224f39a5d9d43319d6db7c499716e7d222acf3cb3427 libcudnn7-dev_7.6.5.32-1+cuda10.0_amd64.deb" | sha256sum -c - \
    && dpkg -i libcudnn7-dev_7.6.5.32-1+cuda10.0_amd64.deb \
    && rm -f libcudnn7-dev_7.6.5.32-1+cuda10.0_amd64.deb \
    && apt-mark hold libcudnn7

# Launch terminator
CMD ["terminator"]