FROM nvidia/cuda:8.0-devel-ubuntu14.04
 
MAINTAINER Athanasios Tasoglou <tasoglou@gmail.com>

LABEL Description="ROS-Indigo-Desktop with CUDA 8 support (Ubuntu 14.04)" Vendor="TurluCode" Version="1.0"

# Install packages without prompting the user to answer any questions
# export DEBIAN_FRONTEND="noninteractive"
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
gdb valgrind

# Install GCC 4.9 !!!
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
apt-get update && \
apt-get install -y gcc-4.9 g++-4.9 gcc-4.8 g++-4.8
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.9
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
# check which one is set, and change back and forth using:
# sudo update-alternatives --config gcc


# Configure timezone and locale
#RUN echo "Europe/Amsterdam" > /etc/timezone && \
#	dpkg-reconfigure -f noninteractive tzdata
#RUN export LANGUAGE=en_US.UTF-8 && \
#	export LANG=en_US.UTF-8 && \
#	export LC_ALL=en_US.UTF-8 && \
#	locale-gen en_US.UTF-8 && \
#	DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales

# Locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# Install OhMyZSH
RUN apt-get install -y zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
#RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
RUN chsh -s /usr/bin/zsh root
RUN git clone https://github.com/sindresorhus/pure ~/.oh-my-zsh/custom/pure
RUN ln -s ~/.oh-my-zsh/custom/pure/pure.zsh-theme ~/.oh-my-zsh/custom/
RUN ln -s ~/.oh-my-zsh/custom/pure/async.zsh ~/.oh-my-zsh/custom/
RUN sed -i -e 's/robbyrussell/refined/g' ~/.zshrc

# Terminator Config
RUN mkdir -p /root/.config/terminator/
COPY assets/terminator_config /root/.config/terminator/config 
COPY assets/terminator_background.png /root/.config/terminator/background.png

# Install ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN apt-get update && apt-get install -y ros-indigo-desktop-full

# Configure ROS
RUN rosdep init && rosdep update 
RUN echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
RUN echo "source /opt/ros/indigo/setup.zsh" >> ~/.zshrc

# Clean-up
RUN rm -rf /var/lib/apt/lists/*

# Entry - run terminator
CMD ["terminator"]
