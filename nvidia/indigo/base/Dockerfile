FROM nvidia/opengl:1.0-glvnd-runtime-ubuntu14.04

MAINTAINER Athanasios Tasoglou <athanasios@tasoglou.net>
LABEL Description="ROS-Indigo-Desktop (Ubuntu 14.04)" Vendor="TurluCode" Version="3.1"
LABEL com.turlucode.ros.version="indigo"

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
libssl-dev \
dbus-x11 \
python3 python3-dev python3-pip \
software-properties-common python-software-properties \
gdb valgrind && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Install latest git
RUN add-apt-repository ppa:git-core/ppa && apt-get update && apt-get install -y \
git && \
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

# Install cmake 3.15.5
RUN git clone https://gitlab.kitware.com/cmake/cmake.git && \
cd cmake && git checkout tags/v3.15.5 && ./bootstrap --parallel=8 && make -j8 && make install && \
cd .. && rm -rf cmake

# Install tmux 3.1
RUN apt-get update && apt-get install -y automake autoconf pkg-config libevent-dev libncurses5-dev bison && \
apt-get clean && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/tmux/tmux.git && \
cd tmux && git checkout tags/3.1 && ls -la && sh autogen.sh && ./configure && make -j8 && make install

# Install new paramiko (solves ssh issues)
RUN apt-add-repository universe
RUN apt-get update && apt-get install -y python-pip python build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN /usr/bin/yes | pip install --upgrade pip
RUN /usr/bin/yes | pip install --upgrade virtualenv --ignore-installed six
RUN /usr/bin/yes | pip install --upgrade paramiko
RUN /usr/bin/yes | pip install --ignore-installed --upgrade numpy protobuf
RUN /usr/bin/yes | pip3 install --upgrade pip
#RUN /usr/bin/yes | pip3 install --upgrade numpy

# Install Python 3.6 and pip3
# RUN add-apt-repository -y ppa:jonathonf/python-3.6 && apt-get update && apt-get install -y \
# python3 python3-dev python3.6 python3.6-dev && \
# apt-get clean && rm -rf /var/lib/apt/lists/* && \
# curl https://bootstrap.pypa.io/get-pip.py | python3.6 && \
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.4 1 && \
# update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
# RUN /usr/bin/yes | pip3 install --upgrade pip numpy

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
RUN sed -i '/plugins=(/c\plugins=(git git-flow adb pyenv tmux)' /root/.zshrc

# Terminator Config
RUN mkdir -p /root/.config/terminator/
COPY assets/terminator_config /root/.config/terminator/config 
COPY assets/terminator_background.png /root/.config/terminator/background.png

# Install ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN apt-get update && apt-get install -y --force-yes \
libpcap-dev \
gstreamer1.0-tools libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev \
ros-indigo-desktop-full \
ros-indigo-socketcan-bridge \
ros-indigo-geodesy && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure ROS
RUN rosdep init && rosdep update 
RUN echo "source /opt/ros/indigo/setup.bash" >> /root/.bashrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.bashrc
RUN echo "source /opt/ros/indigo/setup.zsh" >> /root/.zshrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.zshrc

# Force set fix
RUN update-alternatives --set gcc /usr/bin/gcc-4.9

# Entry script
COPY assets/entrypoint_setup.sh /
ENTRYPOINT ["/entrypoint_setup.sh"]

# Launch terminator
CMD ["terminator"]
