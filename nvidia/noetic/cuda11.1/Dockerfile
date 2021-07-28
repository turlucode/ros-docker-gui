FROM turlucode/ros-noetic:nvidia

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Noetic-Desktop with CUDA 11.1 support (Ubuntu 20.04)" Vendor="TurluCode" Version="1.1"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

# CUDA Base-packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu2004/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl \
    && rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 11.1.0
ENV CUDA_PKG_VERSION 11-1=11.1.74-1
LABEL com.turlucode.ros.cuda="${CUDA_VERSION}"

## For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
        cuda-compat-11-1 && \
    ln -s cuda-11.1 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

## nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
#ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.1 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 brand=tesla,driver>=450,driver<451"


# CUDA Runtime-packages
ENV NCCL_VERSION 2.7.8
LABEL com.turlucode.ros.nccl="${NCCL_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-1=11.1.0-1 \
    libnpp-11-1=11.1.1.269-1 \
    cuda-nvtx-11-1=11.1.74-1 \
    libcublas-11-1=11.2.1.74-1 \
    libnccl2=$NCCL_VERSION-1+cuda11.1 \
    && apt-mark hold libnccl2 \
    && rm -rf /var/lib/apt/lists/*


# CUDA Devel-packages
RUN apt-get update && apt-get install -y --no-install-recommends --allow-downgrades \
    cuda-nvml-dev-11-1=11.1.74-1 \
    cuda-command-line-tools-11-1=11.1.0-1 \
    cuda-nvprof-11-1=11.1.69-1 \
    libnpp-dev-11-1=11.1.1.269-1 \
    cuda-libraries-dev-11-1=11.1.0-1 \
    cuda-minimal-build-11-1=11.1.0-1 \
    libnccl-dev=2.7.8-1+cuda11.1 \
    libcublas-dev-11-1=11.2.1.74-1 \
    libcusparse-11-1=11.2.0.275-1 \
    libcusparse-dev-11-1=11.2.0.275-1 \
    && apt-mark hold libnccl-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs


# Launch terminator
CMD ["terminator"]
