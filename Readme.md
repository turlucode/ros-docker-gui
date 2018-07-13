# Robot Operating System (ROS) Docker Containers with X11 support [Linux]
[![N|Solid](http://turlucode.com/wp-content/uploads/2017/10/turlucode_.png)](http://turlucode.com/)

This project aims to bring different versions of ROS as docker containers with GUI 
support! This means your local OS is no more bound the version of ROS you are using! 
You can use _any_ version of ROS with _any_ Linux distribution, thanks to the amazing 
power of docker!

More info in [this blog post](http://turlucode.com/ros-docker-container-gui-support/).

# Getting Started
The idea is to have HW accelerated GUIs on docker. Generally it has proven that this is 
a challenging task. However graphics card companies like NVIDIA, already provide 
solutions for their platform. To make this work, the idea is to share the host’s X11 
socket with the container as an external volume.

## Current Support
Currently this project supports HW accelerated containers for:

 - NVIDIA (via [nvidia-docker])

Support for other grahics cards will follow!

## NVIDIA Graphics Card
For machines that are using NVIDIA graphics cards we need to have the [nvidia-docker-plugin].

__IMPORTANT:__ This repo supports only `nvidia-docker` version 1!!! 

### Install nvidia-docker-plugin 
Assuming the NVIDIA drivers and Docker® Engine are properly installed (see 
[installation](https://github.com/NVIDIA/nvidia-docker/wiki/Installation))

#### _Ubuntu distributions_
```sh
# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1-1_amd64.deb && \
sudo dpkg -i /tmp/nvidia-docker*.deb && rm /tmp/nvidia-docker*.deb

# Test nvidia-smi
nvidia-docker run --rm nvidia/cuda nvidia-smi
```

#### _CentOS distributions_
```sh
# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker-1.0.1-1.x86_64.rpm && \
sudo rpm -i /tmp/nvidia-docker*.rpm && rm /tmp/nvidia-docker*.rpm && \
sudo systemctl start nvidia-docker

# Test nvidia-smi
nvidia-docker run --rm nvidia/cuda nvidia-smi
```

#### _Other distributions_
```sh
# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1_amd64.tar.xz && \
sudo tar --strip-components=1 -C /usr/bin -xvf /tmp/nvidia-docker*.tar.xz && rm /tmp/nvidia-docker*.tar.xz

# Run nvidia-docker-plugin
sudo -b nohup nvidia-docker-plugin > /tmp/nvidia-docker.log

# Test nvidia-smi
nvidia-docker run --rm nvidia/cuda nvidia-smi
```
If the `nvidia-smi` test was successful you may proceed. Otherwise please visit the 
[official NVIDIA support](https://github.com/NVIDIA/nvidia-docker).

### Build desired Docker Image

You can either browse to directory of the version you want to install and issue 
manually a `docker build` command or just use the makefile:
````
# Prints Help
make
# E.g. Build ROS Indigo with CUDA 8 and OpenCV3 support
make nvidia_ros_indigo_cuda8_opencv3
````
_Note:_ The build process takes a while.

### Running the image (as root)
Once the container has been built, you can issue the following command to run it:
````
nvidia-docker run --rm -it --privileged --net=host \ 
--ipc=host \               
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/root/.Xauthority -e XAUTHORITY=/root/.Xauthority \
-v <PATH_TO_YOUR_CATKIN_WS>:/root/catkin_ws \
-e ROS_IP=<HOST_IP or HOSTNAME> \
turlucode/ros-indigo:cuda8
````
A terminator window will pop-up and the rest you know it! :)

_Important Remark_: This will launch the container as root. This might have unwanted effects! If you want to run it as the current user, see next section.

### Running the image (as current user)
You can also run the script as the current linux-user by passing the `DOCKER_USER_*` variables like this:
````
nvidia-docker run --rm -it --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=localhost \
turlucode/ros-indigo:cuda8
````

_Important Remark_: Please note that you need to pass the `Xauthority` to the correct user's home directory.

## Other options

### Mount your ssh-keys
For both root and custom user use:

```
-v $HOME/.ssh:/root/.ssh
```
For the custom-user the container will make sure to copy them to the right location.

### Mount your local catkin_ws

To mount your local `catkin_ws` you can just use the following docker feature:
````
# for root user
-v $HOME/<some_path>/catkin_ws:/root/catkin_ws
# for local user
-v $HOME/<some_path>/catkin_ws:/home/$(id -un)/catkin_ws
````

### Passing a camera device
If you have a virtual device node like `/dev/video0`, e.g. a compatible usb camera, you pass this to the docker container like this:
````
--device /dev/video0
````

# Issues and Contributing
  - Please let us know by [filing a new 
issue](https://github.com/turlucode/ros-docker-gui/issues/new).
  - You can contribute by [opening a pull 
request](https://github.com/turlucode/ros-docker-gui/compare).


   [nvidia-docker]: https://github.com/NVIDIA/nvidia-docker
   [nvidia-docker-plugin]: 
https://github.com/NVIDIA/nvidia-docker/wiki/nvidia-docker-plugin

