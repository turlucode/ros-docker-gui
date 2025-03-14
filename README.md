# `turludock` - Robot Operating System (ROS) Docker Containers with X11 and Wayland support for Linux
[![N|Solid](http://turlucode.com/wp-content/uploads/2017/10/turlucode_.png)](http://turlucode.com/)

`turludock` aims to provide different versions of ROS as Docker containers, but with GUI 
support for both X11 and Wayland!
This means your local OS is no more bound to the version of ROS you are using! 
You can use _any_ version of ROS with _any_ Linux distribution, thanks to the amazing 
power of Docker!

# TL;DR
## Install tool - Python >= 3.9
```
pip install turludock
```

## Build image
```sh
# Build ROS image from presets (turludock which presets)
turludock build -e noetic_mesa
# Build using a custom configuration
turludock build -c custom.yaml --tag custom_tag

# Check supported versions
turludock which ros
turludock which cuda ROS_CODENAME
```
All commands have a `--help` support.
> [Example YAML config](https://github.com/turlucode/ros-docker-gui/blob/master/examples/noetic_nvidia_custom.yaml)

## Run container
[See "Running the image (as current user)"](#running-the-image-as-current-user) on how to run a container.

# Getting Started
The idea is to have HW accelerated GUIs with Docker. Generally it has proven that this is 
a challenging task. Graphics card companies like NVIDIA, already provide 
solutions for their platform. Running X11 applications within a Docker container is proven for
the last years. However, Wayland support remains still a bit challenging, but at least for
our ROS containers we can assume it is supported :cake:.

## Install `turludock`
```sh
pip install turludock
```

## Supported tool functionality
This tool has two main functionalities:
  1. **Build** ROS images which result in ready-to-use containers.
  2. **Generate** Dockerfile and required assets for *manually building* the Docker images with `docker build`.

Some more details with:
```sh
turludock --help
```

## Supported GPU drivers
Currently this project supports all HW accelerated containers, assuming your GPU is supported by
either [`mesa`](https://www.mesa3d.org/) or NVIDIA drivers.
> For older Ubuntu versions that need support for state-of-the-art GPUs like the Radeon RX 7 series,
we rely on the [`ppa:kisak/kisak-mesa`](https://launchpad.net/~kisak/+archive/ubuntu/turtle)
repository.

### NVIDIA GPU
Both the NVIDIA drivers and the [nvidia-container-toolkit] are required to be installed and working.

You test this by making sure `nvidia-smi` works:
```sh
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

### Known Wayland limitations

ROS related GUI programs seem to working fine. Other programs like `meld` or `vscode` also seem to be working fine. There might be cases where some GUIs do not work as expected. Feel free to open a ticket so we can look into it.

For example, we know RViz is not ready for Wayland; hence we will need to use the `xcb` (X11) plugin instead of the one for Wayland and therefore we will use `QT_QPA_PLATFORM=xcb` for all QT applications. More info in section ["RViz Wayland known issues"](#rviz-wayland-known-issues).

## Supported ROS Images

The idea is to try and support all currently ROS versions that are not End-of-Life (EOL).
Below you can check all ROS1 and ROS2 distributions and their EOL status:
- [ROS 1 distributions](http://wiki.ros.org/Distributions)
- [ROS 2 distributions](https://docs.ros.org/en/rolling/Releases.html)

> Even if ROS 1 Noetic becomes EOL we will try to support it for longer time since many people might
still be relying on it :sunglasses:

To check which versions are actually supported use:
```sh
turludock which ros
```
This will output ROS versions with their codename.

## Supported CUDA and cuDNN versions

To see the supported versions of CUDA/cuDDN for a specific ROS version use:
```sh
turludock which cuda ROS_CODENAME
```
`ROS_CODENAME` could be `noetic` for example.

# Build desired Docker Image

*Hint: For more details and supported arguments*
```sh
turludock build --help
# Or
turludock generate --help
```

## Tool is based on YAML configurations
This tool uses a specific `.yaml` configuration to generate Dockerfiles or build Docker images.

You can find a [typical configuration](https://github.com/turlucode/ros-docker-gui/blob/master/examples/noetic_nvidia_custom.yaml) in the examples folder.

### Build or generate from presets
This tool already provides preconfigured `.yaml` files that can be used directly to generate
Dockerfiles or build Docker images. This is what we call a list of *presets*: you might like
them and use them; or hate them and create your own :wink:.

For a list of available presets run:
```sh
turludock which presets
```
This will show the underlying ROS version, the GPU driver assumed, the CUDA/cuDNN version (if applicable) 
and some preinstalled packages that are part of the preset.

To build a Docker image from the presets use:
```sh
turludock build -e noetic_mesa
```
Or if you want to generate the Dockerfile and its required assets for manual build use:
```sh
turludock generate -e noetic_mesa FOLDER_PATH
```
The `FOLDER_PATH` now contains all necessary files to run a custom `docker build` command.
So you can just invoke `docker build FOLDER_PATH` for example.

### Build or generate from custom YAML configuration
OK, so you don't like the existing presets and you would like to build a Docker image using
your own custom configuration... 

No problemo, use:
```sh
turludock build -c custom.yaml --tag CUSTOM_TAG
```
> How to create a custom yaml configuration? [Check the example.](https://github.com/turlucode/ros-docker-gui/blob/master/examples/noetic_nvidia_custom.yaml)

Or if you want to generate the Dockerfile and its required assets for manual build use:
```sh
turludock generate -c custom.yaml FOLDER_PATH
```
The `FOLDER_PATH` now contains all necessary files to run a custom `docker build` command.

# Running the image (as current user)
## Mesa
> :pineapple: **Important:** Make sure your YAML configuration uses: [`gpu_driver: mesa`](https://github.com/turlucode/ros-docker-gui/blob/master/examples/noetic_nvidia_custom.yaml#L15)

### X11
To run the ROS Docker container with X11 support use:
```sh
docker run --rm -it --privileged --net=host --ipc=host \
--device=/dev/dri:/dev/dri \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-noetic:mesa-cmake-tmux-llvm-meld
```

_Important Remarks_: 

- The `DOCKER_USER_*` variables are used to run the container as the current user.
- Please note that you need to pass the `Xauthority` to the correct user's home directory.
- You may need to run `xhost si:localuser:$USER` or worst case `xhost local:root` if get errors like `Error: cannot open display`.
- See also section ["Other options"](#other-options) for other options.

### Wayland
> **NOTE:** Wayland support is still a bit experimental! See section ["Known Wayland limitations"](#known-wayland-limitations).

ROS GUI on Wayland is still problematic and that is why we are going to use [`xwayland`](https://wayland.freedesktop.org/xserver.html).
Make sure you have installed `xhost`.
Make also sure the user has the rights to draw to the display; more info in section ["X11: Error: cannot open display"](#x11-error-cannot-open-display).

To run the ROS Docker container with Wayland support use:

```sh
docker run --rm -it --security-opt seccomp=unconfined \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-e XDG_RUNTIME_DIR=/run/user/$(id -u) \
-e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
-v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/run/user/$(id -u)/$WAYLAND_DISPLAY \
--device /dev/dri \
--group-add video \
-e QT_QPA_PLATFORM=xcb \
-e XDG_SESSION_TYPE=wayland \
-e GDK_BACKEND=wayland \
-e CLUTTER_BACKEND=wayland \
-e SDL_VIDEODRIVER=wayland \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-noetic:mesa-cmake-tmux-llvm-meld dbus-launch terminator
```

Or for Ubuntu 24.04 and up, `dbus-launch terminator` is not needed, just use:

```sh
docker run [...] turlucode/ros-jazzy:mesa-cmake-tmux-llvm-meld
```

_Important Remarks_: 

- The `DOCKER_USER_*` variables are used to run the container as the current user.
- We need to start `terminator` with `dbus-launch` for Ubuntu versions less than 24.04, i.e. for versions < `jazzy`.
- The `QT_QPA_PLATFORM=xcb` is for now intentionally as discussed.
For this reason also the `qtwayland5` package is not installed in our Docker images.
- See also section ["Other options"](#other-options) for other options.

## NVIDIA GPU
> :pineapple: **Important:** Make sure your YAML configuration uses: [`gpu_driver: nvidia`](https://github.com/turlucode/ros-docker-gui/blob/master/examples/noetic_nvidia_custom.yaml#L15)

For machines that are using NVIDIA graphics cards we need to have the [nvidia-container-toolkit] installed.

### X11

To run the ROS Docker container with X11 support use:
````sh
docker run --rm -it --runtime=nvidia --gpus all --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-noetic:nvidia-cmake-tmux-llvm-meld
````

_Important Remarks_: 

- The `DOCKER_USER_*` variables are used to run the container as the current user.
- Please note that you need to pass the `Xauthority` to the correct user's home directory.
- You may need to run `xhost si:localuser:$USER` or worst case `xhost local:root` if get errors like `Error: cannot open display`
- Adapt `--gpus all` to your needs
- See also section ["Other options"](#other-options) for other options.

### Wayland
> **NOTE:** Wayland support is still a bit experimental! See section ["Known Wayland limitations"](#known-wayland-limitations).

ROS GUI on Wayland is still problematic and that is why we are going to use [`xwayland`](https://wayland.freedesktop.org/xserver.html).
Make sure you have installed `xhost`.
Make also sure the user has the rights to draw to the display; more info in section ["X11: Error: cannot open display"](#x11-error-cannot-open-display).

To run the ROS Docker container with X11 support use:
````sh
docker run --rm -it --runtime=nvidia --gpus all --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-e XDG_RUNTIME_DIR=/run/user/$(id -u) \
-e WAYLAND_DISPLAY=$WAYLAND_DISPLAY \
-v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/run/user/$(id -u)/$WAYLAND_DISPLAY \
-e QT_QPA_PLATFORM=xcb \
-e XDG_SESSION_TYPE=wayland \
-e GDK_BACKEND=wayland \
-e CLUTTER_BACKEND=wayland \
-e SDL_VIDEODRIVER=wayland \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
turlucode/ros-noetic:nvidia-cmake-tmux-llvm-meld dbus-launch terminator
````

Or for Ubuntu 24.04 and up, `dbus-launch terminator` is not needed, just use:

```sh
docker run [...] turlucode/ros-jazzy:nvidia-cmake-tmux-llvm-meld
```

- The `DOCKER_USER_*` variables are used to run the container as the current user.
- We need to now start `terminator` with `dbus-launch`
- The `QT_QPA_PLATFORM=xcb` is for now intentionally as discussed.
For this reason also the `qtwayland5` package is not installed in our Docker images.
- Please note that you need to pass the `Xauthority` to the correct user's home directory.
- You may need to run `xhost si:localuser:$USER` or worst case `xhost local:root` if get errors like `Error: cannot open display`
- Adapt `--gpus all` to your needs
- See also section ["Other options"](#other-options) for other options.

## Other options
### Mount your ssh-keys
For both root and custom user use:

```sh
-v $HOME/.ssh:/root/.ssh
```
For the custom-user the container will make sure to copy them to the right location.

### Mount your local catkin_ws

To mount your local `catkin_ws` you can just use the following Docker feature:
```sh
# for root user
-v $HOME/<some_path>/catkin_ws:/root/catkin_ws
# for local user
-v $HOME/<some_path>/catkin_ws:/home/$(id -un)/catkin_ws
```

### Passing a camera device
If you have a virtual device node like `/dev/video0`, e.g. a compatible usb camera, you pass this to the Docker container like this:
```sh
--device /dev/video0
```

# References
## Wayland in Docker references

- [mviereck/x11docker](https://github.com/mviereck/x11docker/wiki/How-to-provide-Wayland-socket-to-docker-container)
- [stackexchange: How can I run a graphical application in a container under Wayland?](https://unix.stackexchange.com/a/359244/189868)
- [rso2/RViz:  Wayland Support #847 ](https://github.com/ros2/rviz/issues/847#issuecomment-1506502560)
- [github ticket: wayland libGL error](https://github.com/pygame/pygame/issues/3405#issuecomment-1221266709)
- [archlinux: Wayland](https://wiki.archlinux.org/title/wayland)

## RViz Wayland known issues

- https://github.com/ros-visualization/rviz/issues/1442#issuecomment-553946698
- https://github.com/ros2/rviz/issues/672#issuecomment-2041508267
- https://github.com/ros2/rviz/issues/847#issuecomment-1503892696

## OpenGL NVIDIA

- https://gitlab.com/nvidia/container-images/opengl/-/tree/ubuntu22.04?ref_type=heads

# Troubleshooting
## Container eating up too much memory
Is even a simple command inside Docker eating up crazy a lot of memory? This happens especially in arch-linux.
Chances are you have a "miss-configured" `LimitNOFILE`. See [here](https://github.com/containerd/containerd/issues/3201#issue-431539379),
[here](https://github.com/moby/moby/issues/44547#issuecomment-1334125338), [here](https://bugs.archlinux.org/task/77548) for the reported issue.
```sh
# This is what is configured
cat /usr/lib/systemd/system/containerd.service | grep LimitNOFILE
# This is what is actually being used
systemctl show containerd | grep LimitNOFILE
```
If `containerd.service` uses `infinity` better bound it with systemd with a new `.conf` file:
```sh
# /etc/systemd/system/containerd.service.d/30-override.conf
[Service]
LimitNOFILE=1048576
```
If the folder `docker.service.d` doesn't exist, create it.
Now reload service with:
```sh
sudo systemctl restart containerd && sudo systemctl daemon-reload
```
And you are good to go! The container feels also "snappier" now.

## X11: Error: cannot open display
Assuming `xhost` is installed and running on your host, you may need to run `xhost si:localuser:$USER` or worst case `xhost local:root`.

### Docker security risks

Are you worried about the security risks when exposing your X-server to the
container? Normally you should be! :smiley:

There are some nice articles that explain what is going on and what might be some extra
steps you can do, in order to be less exposed.

1. [Docker Security Risks: GUIs + Xorg](https://nicroland.wordpress.com/2016/02/27/docker-security-risks-guis-xorg/)
2. [Running a Graphical Application from a Docker Container - Simply and Securely](https://blog.artis3nal.com/blog/container-gui-app-pgmodeler/)
3. Feel free to google/gpt the matter yourself. :wink:

Most importantly you can also review the [template files](turludock/assets/dockerfile_templates/) in order to be absolutely sure you like what is being installed in the images when using the `turludock` tool.

## Vscode crashes

Try adding `--shm-size=8G` to your docker command.

# Issues and Contributing
  - Please let us know by [filing a new 
issue](https://github.com/turlucode/ros-docker-gui/issues/new).
  - You can contribute by [opening a pull 
request](https://github.com/turlucode/ros-docker-gui/compare).

## Base images
### NVIDIA
The images on this repository are based on the following work:

  - [nvidia-opengl](https://gitlab.com/nvidia/samples/blob/master/opengl/ubuntu14.04/glxgears/Dockerfile)
  - [nvidia-cuda](https://gitlab.com/nvidia/cuda) - Hierarchy is base->runtime->devel

## For developers - a quick how to

This project uses [`poetry`](https://python-poetry.org/) for packaging and dependency management.
After [installing poetry](https://python-poetry.org/docs/#installation) you can basically create a [python virtual environment ](https://docs.python.org/3/library/venv.html) for one of the supported python versions, >=3.9, and inside that new environment just install the dependencies with
```sh
poetry install 
```
After that, you are good to go!
> Hint: You can [install pynev](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation) if you want to check multiple python versions.
### Coding style enforcement
Check and enforce the coding style with static analysis:
```sh
poetry run isort turludock && poetry run black turludock && poetry run pflake8 turludock
```

   [nvidia-docker]: https://github.com/NVIDIA/nvidia-docker
   [nvidia-container-toolkit]: 
https://github.com/NVIDIA/nvidia-container-toolkit
