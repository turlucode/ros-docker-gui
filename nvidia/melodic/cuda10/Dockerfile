FROM turlucode/ros-melodic:nvidia

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Melodic-Desktop with CUDA 10 support (Ubuntu 18.04)" Vendor="TurluCode" Version="1.1"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

# CUDA Base-packages
RUN wget -nv https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb && \
    dpkg -i cuda-keyring_1.0-1_all.deb && \
    rm cuda-keyring_1.0-1_all.deb

ENV CUDA_VERSION 10.0.130
ENV CUDA_PKG_VERSION 10-0=$CUDA_VERSION-1
LABEL com.turlucode.ros.cuda="${CUDA_VERSION}"

## For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION \
        cuda-compat-10-0 && \
    ln -s cuda-10.0 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*


ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

## nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
# ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.0 brand=tesla,driver>=384,driver<385 brand=tesla,driver>=410,driver<411"


# CUDA Runtime-packages
ENV NCCL_VERSION 2.6.4

RUN wget -q https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libnccl2_2.6.4-1+cuda10.0_amd64.deb \
    && echo "f92759e2ab0e36a1c9887f080f7283a774a7c971e352203db4d94d99c44f1028 libnccl2_2.6.4-1+cuda10.0_amd64.deb" | sha256sum -c --strict - \
    && dpkg -i libnccl2_2.6.4-1+cuda10.0_amd64.deb \
    && rm -f libnccl2_2.6.4-1+cuda10.0_amd64.deb

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
    cuda-npp-$CUDA_PKG_VERSION \
    cuda-nvtx-$CUDA_PKG_VERSION \
    cuda-cublas-10-0=10.0.130-1 \
    && apt-mark hold libnccl2 \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold cuda-cublas-10-0


# CUDA Devel-packages
RUN wget -q https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libnccl2_2.6.4-1+cuda10.0_amd64.deb \
    && echo "f92759e2ab0e36a1c9887f080f7283a774a7c971e352203db4d94d99c44f1028 libnccl2_2.6.4-1+cuda10.0_amd64.deb" | sha256sum -c --strict - \
    && dpkg -i libnccl2_2.6.4-1+cuda10.0_amd64.deb \
    && rm -f libnccl2_2.6.4-1+cuda10.0_amd64.deb

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-nvml-dev-$CUDA_PKG_VERSION \
    cuda-command-line-tools-$CUDA_PKG_VERSION \
    cuda-nvprof-$CUDA_PKG_VERSION \
    cuda-npp-dev-$CUDA_PKG_VERSION \
    cuda-libraries-dev-$CUDA_PKG_VERSION \
    cuda-minimal-build-$CUDA_PKG_VERSION \
    cuda-cublas-dev-10-0=10.0.130-1 \
    && apt-mark hold libnccl-dev \
    && rm -rf /var/lib/apt/lists/*

# apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold libnccl2 cuda-cublas-dev-10-0

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs


# Launch terminator
CMD ["terminator"]