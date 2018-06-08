FROM turlucode/ros-indigo:cuda8

MAINTAINER Athanasios Tasoglou <tasoglou@gmail.com>
LABEL Description="ROS-Indigo-Desktop with CUDA 8 support and OpenCV v3.3.1 (Ubuntu 14.04)" Vendor="TurluCode" Version="2.0"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

# Install OpenCV3
## Install dependencies
RUN apt-get update && apt-get install -y \
build-essential \
checkinstall \
pkg-config \
yasm \
gfortran \
libjpeg8-dev \
libjasper-dev \
libpng12-dev \
libtiff4-dev \
libprotobuf-dev \
protobuf-compiler \
libgoogle-glog-dev \
libgflags-dev \
libgphoto2-dev \
libeigen3-dev \
libhdf5-dev \
doxygen \
python3-dev python3-pip && \
apt-get clean && rm -rf /var/lib/apt/lists/*

RUN /usr/bin/yes | pip3 install --upgrade pip numpy

## Get OpenCV
RUN git clone https://github.com/opencv/opencv.git && cd opencv && git checkout 3.3.1 && cd .. && \
git clone https://github.com/opencv/opencv_contrib.git && cd opencv_contrib && git checkout 3.3.1 && cd .. && \
cd opencv && mkdir build && cd build && \
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D WITH_CUBLAS=1 \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON \
      -D CUDA_CUDA_LIBRARY=/usr/local/cuda-8.0/targets/x86_64-linux/lib/stubs/libcuda.so .. && \
make -j8 && make install && cd ../.. && \
rm -rf /opencv && rm -rf /opencv_contrib

RUN sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf' && ldconfig

# --- turlucode/ros-indigo:cuda8 will launch terminator
CMD ["true"]