#/bin/bash
xhost +
docker run -it --runtime=nvidia --privileged --net=host --ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/home/$(id -un)/.Xauthority -e XAUTHORITY=/home/$(id -un)/.Xauthority \
-e DOCKER_USER_NAME=$(id -un) \
-e DOCKER_USER_ID=$(id -u) \
-e DOCKER_USER_GROUP_NAME=$(id -gn) \
-e DOCKER_USER_GROUP_ID=$(id -g) \
-e ROS_IP=127.0.0.1 \
--name melodic-vscode \
-v $HOME/.vscode:/home/$(id -un)/.vscode \
-v $HOME/docker:/home/$(id -un)/docker \
turlucode/ros-melodic:cuda10.1-cudnn7-vscode