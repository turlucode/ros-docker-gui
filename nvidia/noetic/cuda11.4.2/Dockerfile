FROM turlucode/ros-noetic:nvidia

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Noetic-Desktop with CUDA 11.4.2 support (Ubuntu 20.04)" Vendor="TurluCode" Version="1.0"

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

ENV NV_CUDA_LIB_VERSION 11.4.2-1
ENV NV_CUDA_CUDART_VERSION 11.4.108-1
ENV NV_CUDA_COMPAT_PACKAGE cuda-compat-11-4
LABEL com.turlucode.ros.cuda="${NV_CUDA_LIB_VERSION}"

## For libraries in the cuda-compat-* package: https://docs.nvidia.com/cuda/eula/index.html#attachment-a
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-cudart-11-4=${NV_CUDA_CUDART_VERSION} \
    ${NV_CUDA_COMPAT_PACKAGE} \
    && ln -s cuda-11.4 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

## Required for nvidia-docker v1
RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

## nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
#ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=11.4 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 driver>=450"


# CUDA Runtime-packages
ENV NV_NVTX_VERSION 11.4.120-1
ENV NV_LIBCUSPARSE_VERSION 11.6.0.120-1

ENV NV_LIBNPP_VERSION 11.4.0.110-1
ENV NV_LIBNPP_PACKAGE libnpp-11-4=${NV_LIBNPP_VERSION}

ENV NV_LIBCUBLAS_PACKAGE_NAME libcublas-11-4
ENV NV_LIBCUBLAS_VERSION 11.6.1.51-1
ENV NV_LIBCUBLAS_PACKAGE ${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}

ENV NV_LIBNCCL_PACKAGE_NAME libnccl2
ENV NV_LIBNCCL_PACKAGE_VERSION 2.11.4-1
ENV NCCL_VERSION 2.11.4-1
ENV NV_LIBNCCL_PACKAGE ${NV_LIBNCCL_PACKAGE_NAME}=${NV_LIBNCCL_PACKAGE_VERSION}+cuda11.4

LABEL com.turlucode.ros.nccl="${NV_LIBNCCL_PACKAGE_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-11-4=${NV_CUDA_LIB_VERSION} \
    ${NV_LIBNPP_PACKAGE} \
    cuda-nvtx-11-4=${NV_NVTX_VERSION} \
    libcusparse-11-4=${NV_LIBCUSPARSE_VERSION} \
    ${NV_LIBCUBLAS_PACKAGE} \
    ${NV_LIBNCCL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*
    
## Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_PACKAGE_NAME} ${NV_LIBNCCL_PACKAGE_NAME}


# CUDA Devel-packages
ENV NV_CUDA_CUDART_DEV_VERSION 11.4.108-1
ENV NV_NVML_DEV_VERSION 11.4.120-1
ENV NV_LIBCUSPARSE_DEV_VERSION 11.6.0.120-1

ENV NV_LIBNPP_DEV_VERSION 11.4.0.110-1
ENV NV_LIBNPP_DEV_PACKAGE libnpp-dev-11-4=${NV_LIBNPP_DEV_VERSION}

ENV NV_LIBCUBLAS_DEV_VERSION 11.6.1.51-1
ENV NV_LIBCUBLAS_DEV_PACKAGE_NAME libcublas-dev-11-4
ENV NV_LIBCUBLAS_DEV_PACKAGE ${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}

ENV NV_LIBNCCL_DEV_PACKAGE_NAME libnccl-dev
ENV NV_LIBNCCL_DEV_PACKAGE_VERSION 2.11.4-1
ENV NCCL_VERSION 2.11.4-1
ENV NV_LIBNCCL_DEV_PACKAGE ${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda11.4

RUN apt-get update && apt-get install -y --no-install-recommends \
    libtinfo5 libncursesw5 \
    cuda-cudart-dev-11-4=${NV_CUDA_CUDART_DEV_VERSION} \
    cuda-command-line-tools-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-minimal-build-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-libraries-dev-11-4=${NV_CUDA_LIB_VERSION} \
    cuda-nvml-dev-11-4=${NV_NVML_DEV_VERSION} \
    ${NV_LIBNPP_DEV_PACKAGE} \
    libcusparse-dev-11-4=${NV_LIBCUSPARSE_DEV_VERSION} \
    ${NV_LIBCUBLAS_DEV_PACKAGE} \
    ${NV_LIBNCCL_DEV_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

## Keep apt from auto upgrading the cublas and nccl packages. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
RUN apt-mark hold ${NV_LIBCUBLAS_DEV_PACKAGE_NAME} ${NV_LIBNCCL_DEV_PACKAGE_NAME}

ENV LIBRARY_PATH /usr/local/cuda/lib64/stubs


# Launch terminator
CMD ["terminator"]
