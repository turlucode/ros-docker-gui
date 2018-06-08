FROM turlucode/ros-indigo:cuda8-cudnn6

MAINTAINER Athanasios Tasoglou <tasoglou@gmail.com>
LABEL Description="ROS-Indigo-Desktop with CUDA 8 support, cuDNN 6 and OpenCV v3.4.1 (Ubuntu 14.04)" Vendor="TurluCode" Version="2.0"

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
libtbb2 libtbb-dev \
doxygen \
python3-dev python3-pip && \
apt-get clean && rm -rf /var/lib/apt/lists/*

RUN /usr/bin/yes | pip3 install --upgrade pip numpy

## Get OpenCV
# for opencv 3.4.1 use BUILD_EXAMPLES=OFF (https://github.com/opencv/opencv/issues/11117) OR detele driver_api_multi.cpp and driver_api_stereo_multi.cpp
# True? Using WITH_OPENMP=ON has no sense if TBB is used (lower priority).
RUN git clone https://github.com/opencv/opencv.git && cd opencv && git checkout 3.4.1 && cd .. && \
git clone https://github.com/opencv/opencv_contrib.git && cd opencv_contrib && git checkout 3.4.1 && cd .. && \
rm opencv/samples/gpu/driver_api_multi.cpp opencv/samples/gpu/driver_api_stereo_multi.cpp && \
cd opencv && mkdir build && cd build && \
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D WITH_CUBLAS=1 \
      -D WITH_TBB=ON \
      -D WITH_OPENMP=ON \
      -D WITH_CUDA=ON \
      -D ENABLE_PRECOMPILED_HEADERS=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=OFF \
      -D CUDA_CUDA_LIBRARY=/usr/local/cuda-8.0/targets/x86_64-linux/lib/stubs/libcuda.so .. && \
make -j8 && make install && cd ../.. && \
rm -rf /opencv && rm -rf /opencv_contrib

RUN sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf' && ldconfig

# --- turlucode/ros-indigo:cuda8-cudnn6 will launch terminator
CMD ["true"]