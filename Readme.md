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
solutions for their platform. To make this work, the idea is to share the host's X11 
socket with the container as an external volume.

## Current Support
Currently this project supports HW accelerated containers for:

 - [Integraded GPU](#integraded-gpu) (e.g. Intel)
 - [NVIDIA](#nvidia-graphics-card) (via [nvidia-docker])

Support for other grahics cards will follow!

### Supported ROS Images

| ROS Distribution | Integrated Graphics |                            NVIDIA Graphics                           |                 OpenCV                 |
|:----------------:|:-------------------:|:--------------------------------------------------------------------:|:--------------------------------------:|
|      Indigo      |         yes         | - CUDA 8 (cuDNN 6,7)<br>- CUDA 10 (cuDNN 7)<br>- CUDA 10.1 (cuDNN 7) | - OpenCV 2.x (default)<br>- OpenCV 3.x |
|      Kinetic     |         yes         | - CUDA 8 (cuDNN 6)<br>- CUDA 10 (cuDNN 7)<br>- CUDA 10.1 (cuDNN 7)   | - OpenCV 2.x (default)<br>- OpenCV 3.x |
|      Melodic     |         yes         | - CUDA 10 (cuDNN 7)<br>- CUDA 10.1 (cuDNN 7)                         | - OpenCV 3.x (default)                 |
|      Noetic      |         yes         |                             coming soon!                             | - OpenCV 4.x (default)                 |
|   Bouncy (ROS2)  |         yes         |                            no support yet                            | - OpenCV 3.x (Ubuntu 18.04)            |

You can also see the complete list by running:

```sh
make
```

## Integraded GPU
This repository supports ROS docker images that rely their integrated GPU of the CPU for Graphics. 


### Build desired Docker Image
You can use the docker images labeled with `[CPU]` to get support for your integraded GPU:

```sh
# Prints Help
make

# E.g. Build ROS Indigo
make cpu_ros_indigo
```

### Running the image (as root)
Once the container has been built, you can issue the following command to run it:
````sh
docker run --rm -it --privileged --net=host --ipc=host \
--device=/dev/dri:/dev/dri \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e ROS_IP=127.0.0.1 \
turlucode/ros-indigo:cpu
````
A terminator window will pop-up and the rest you know it! :)

_Important Remark_: This will launch the container as root. This might have unwanted effects! If you want to run it as the current user, see next section.

- See also [this section](#other-options) for other options.

### Running the image (as current user)
You can also run the script as the current linux-user by passing the `DOCKER_USER_*` variables like this:
````sh
docker run --rm -it --privileged --net=host --ipc=host \
--device=/dev/dri:/dev/dri \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-indigo:cpu
````

_Important Remark_: 

- Please note that you need to pass the `Xauthority` to the correct user's home directory.
- You may need to run `xhost si:localuser:$USER` or worst case `xhost local:root` if get errors like `Error: cannot open display`

- See also [this section](#other-options) for other options.

## NVIDIA Graphics Card
For machines that are using NVIDIA graphics cards we need to have the [nvidia-docker-plugin].

__IMPORTANT:__ This repo supports `nvidia-docker` version `2.x`!!!

> For `nvidia-docker-v1.0` support, [check the corresponding branch](https://github.com/turlucode/ros-docker-gui/tree/nvidia-docker-v1.0)

### Install nvidia-docker-plugin 
Assuming the NVIDIA drivers and Docker® Engine are properly installed (see 
[installation](https://github.com/NVIDIA/nvidia-docker/wiki/Installation))

#### _Ubuntu 14.04/16.04/18.04, Debian Jessie/Stretch_
```sh
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge -y nvidia-docker

# Add the package repositories
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
```

#### _CentOS 7 (docker-ce), RHEL 7.4/7.5 (docker-ce), Amazon Linux 1/2_

If you are __not__ using the official `docker-ce` package on CentOS/RHEL, use the next section.

```sh
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo yum remove nvidia-docker

# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo yum install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
```

If `yum` reports a conflict on `/etc/docker/daemon.json` with the `docker` package, you need to use the next section instead.

For `docker-ce` on `ppc64le`, look at the [FAQ](https://github.com/nvidia/nvidia-docker/wiki/Frequently-Asked-Questions#do-you-support-powerpc64-ppc64le).

#### _Arch-linux_
```sh
# Install nvidia-docker and nvidia-docker-plugin
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f

sudo rm /usr/bin/nvidia-docker /usr/bin/nvidia-docker-plugin

# Install nvidia-docker2 from AUR and reload the Docker daemon configuration
yaourt -S aur/nvidia-docker
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi
```

#### Proceed only if `nvidia-smi` works

If the `nvidia-smi` test was successful you may proceed. Otherwise please visit the 
[official NVIDIA support](https://github.com/NVIDIA/nvidia-docker).

#### Remarks & Troubleshooting

- If your nvidia-driver is `4.10.x` and greater, you need to choose CUDA 10 images.

### Build desired Docker Image

You can either browse to directory of the version you want to install and issue 
manually a `docker build` command or just use the makefile:
````sh
# Prints Help
make

# E.g. Build ROS Indigo
make nvidia_ros_indigo
````
_Note:_ The build process takes a while.

> For nvidia-driver `>= 4.10.x` you need to build CUDA10 images for compatibility!

### Running the image (as root)
Once the container has been built, you can issue the following command to run it:
````sh
docker run --rm -it --runtime=nvidia --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/root/.Xauthority -e XAUTHORITY=/root/.Xauthority \
-v <PATH_TO_YOUR_CATKIN_WS>:/root/catkin_ws \
-e ROS_IP=<HOST_IP or HOSTNAME> \
turlucode/ros-indigo:nvidia
````
A terminator window will pop-up and the rest you know it! :)

_Important Remark_: This will launch the container as root. This might have unwanted effects! If you want to run it as the current user, see next section.

### Running the image (as current user)
You can also run the script as the current linux-user by passing the `DOCKER_USER_*` variables like this:
````sh
docker run --rm -it --runtime=nvidia --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-indigo:nvidia
````

_Important Remark_: 

- Please note that you need to pass the `Xauthority` to the correct user's home directory.
- You may need to run `xhost si:localuser:$USER` or worst case `xhost local:root` if get errors like `Error: cannot open display`

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
# Tools

# Visual Studio Code

You can have the option to create a new container that contais [Visual Studio Code](https://code.visualstudio.com/). This allows to use Visual Studio Code wihtin the ROS docker image and in turn use it for development and debugging.

## Create image

To create the new image run:
```sh
make tools_vscode <existing_ros_docker_image>

# E.g.
make tools_vscode turlucode/ros-indigo:cuda10.1-cudnn7-opencv3
# which creates the image turlucode/ros-indigo:cuda10.1-cudnn7-opencv3-vscode
```

This will create a new docker image that uses as base `<existing_ros_docker_image>` with the name `<existing_ros_docker_image>-vscode`. If the image doesn't exist, the command will terminate with an error, so make sure you build the ros-docker-image first, before you use it as a base-image to install Visual Studio Code.

## Run image

You can run the newly created image as you were running the rest of the ROS images. If you want to keep the Visual Studio Code configuration consistent then you need to mount `.vscode`, e.g.:

```sh
# Mount argument for the docker run command:
- v <local_path_to_store_configuration>:/home/$(id -un)/.vscode
```

If you are running the images as `root` then you need to follow the Visual Studio Code recommendations, which state:
```
You are trying to start vscode as a super user which is not recommended. If you really want to, you must specify an alternate user data directory using the --user-data-dir argument.
```

So act accordingly.

# Base images

## NVIDIA
The images on this repository are based on the following work:

  - [nvidia-opengl](https://gitlab.com/nvidia/samples/blob/master/opengl/ubuntu14.04/glxgears/Dockerfile)
  - [nvidia-cuda](https://gitlab.com/nvidia/cuda) - Hierarchy is base->runtime->devel

# OpenCV Build References

  - [Official documentation](https://docs.opencv.org/3.4.7/d7/d9f/tutorial_linux_install.html)
  - [learnopencv.com](https://www.learnopencv.com/install-opencv-3-4-4-on-ubuntu-16-04/)

# Issues and Contributing
  - Please let us know by [filing a new 
issue](https://github.com/turlucode/ros-docker-gui/issues/new).
  - You can contribute by [opening a pull 
request](https://github.com/turlucode/ros-docker-gui/compare).


   [nvidia-docker]: https://github.com/NVIDIA/nvidia-docker
   [nvidia-docker-plugin]: 
https://github.com/NVIDIA/nvidia-docker/wiki/nvidia-docker-plugin

