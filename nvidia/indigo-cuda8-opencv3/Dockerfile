FROM nvidia/cuda:8.0-devel-ubuntu14.04

MAINTAINER Athanasios Tasoglou <tasoglou@gmail.com>

LABEL Description="ROS-Indigo-Desktop with CUDA 8 support and OpenCV v3.3.1 (Ubuntu 14.04)" Vendor="TurluCode" Version="1.1"

# Install packages without prompting the user to answer any questions
ENV DEBIAN_FRONTEND noninteractive 

# Install packages
RUN apt-get update && apt-get install -y \
lsb-release \
mesa-utils \
git \
subversion \
nano \
terminator \
wget \
curl \
htop \
software-properties-common python-software-properties \
gdb valgrind && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Install GCC 4.9 !!!
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
apt-get update && \
apt-get install -y gcc-4.9 g++-4.9 gcc-4.8 g++-4.8 && \
apt-get clean && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.9
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
# check which one is set, and change back and forth using:
# sudo update-alternatives --config gcc

# Install new paramiko (solves ssh issues)
RUN apt-add-repository universe
RUN apt-get update && apt-get install -y python-pip python build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN /usr/bin/yes | pip install --upgrade pip
RUN /usr/bin/yes | pip install --upgrade virtualenv
RUN /usr/bin/yes | pip install --upgrade paramiko

# Locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# Install OhMyZSH
RUN apt-get update && apt-get install -y zsh && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
#RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
RUN chsh -s /usr/bin/zsh root
RUN git clone https://github.com/sindresorhus/pure /root/.oh-my-zsh/custom/pure
RUN ln -s /root/.oh-my-zsh/custom/pure/pure.zsh-theme /root/.oh-my-zsh/custom/
RUN ln -s /root/.oh-my-zsh/custom/pure/async.zsh /root/.oh-my-zsh/custom/
RUN sed -i -e 's/robbyrussell/refined/g' /root/.zshrc

# Terminator Config
RUN mkdir -p /root/.config/terminator/
COPY assets/terminator_config /root/.config/terminator/config 
COPY assets/terminator_background.png /root/.config/terminator/background.png

# Install ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN apt-get update && apt-get install -y \
gstreamer1.0-tools libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev \
ros-indigo-desktop-full \
ros-indigo-geodesy && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure ROS
RUN rosdep init && rosdep update 
RUN echo "source /opt/ros/indigo/setup.bash" >> /root/.bashrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.bashrc
RUN echo "source /opt/ros/indigo/setup.zsh" >> /root/.zshrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.zshrc

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
make -j8 && make install && cd ../.. \
rm -rf /opencv && rm -rf /opencv_contrib

RUN sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf' && ldconfig

# Run terminator
CMD ["terminator"]
