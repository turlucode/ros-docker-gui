FROM turlucode/ros-indigo:cuda8

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Indigo-Desktop with CUDA 8 support and OpenCV v3.4.7 (Ubuntu 14.04)" Vendor="TurluCode" Version="2.2"
LABEL com.turlucode.ros.opencv="3.4.7"

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
qt5-default \
doxygen && \
apt-get clean && rm -rf /var/lib/apt/lists/*

## Get OpenCV
# True? Using WITH_OPENMP=ON has no sense if TBB is used (lower priority).
# Do we need QT5 support (-D WITH_QT=ON)? If not, remove also qt5-default.
ENV OPENCV_VERSION 3.4.7
RUN git clone https://github.com/opencv/opencv.git && cd opencv && git checkout $OPENCV_VERSION && cd .. && \
git clone https://github.com/opencv/opencv_contrib.git && cd opencv_contrib && git checkout $OPENCV_VERSION && cd .. && \
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
      .. && \
make -j8 && make install && cd ../.. && \
rm -rf /opencv && rm -rf /opencv_contrib

RUN sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf' && ldconfig

# Launch terminator
CMD ["terminator"]