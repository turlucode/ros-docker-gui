
First get the nvidia-docker and the nvidia-docker-plugin. Especially the nvidia-docker-plugin is very important to us. From https://github.com/NVIDIA/nvidia-docker:

# Install nvidia-docker and nvidia-docker-plugin
wget -P /tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.1/nvidia-docker_1.0.1_amd64.tar.xz
sudo tar --strip-components=1 -C /usr/bin -xvf /tmp/nvidia-docker*.tar.xz && rm /tmp/nvidia-docker*.tar.xz

# Run nvidia-docker-plugin
sudo -b nohup nvidia-docker-plugin > /tmp/nvidia-docker.log

# Test nvidia-smi
nvidia-docker run --rm nvidia/cuda nvidia-smi

If the test is successfull, things look promising! :)

# Install xhost

Authorise only user starting the container:
xhost +si:localuser:$USER
Avoid using xhost +.

# Check also https://github.com/mviereck/x11docker

Issue when using --net host and glxgears black screen: https://github.com/NVIDIA/nvidia-docker/issues/327

nvidia-docker run --rm -it --privileged --net=host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY turlucode/ros-indigo

Make sure nvidia plugin is running
# Run nvidia-docker-plugin
sudo -b nohup nvidia-docker-plugin > /tmp/nvidia-docker.log

nvidia-docker run --rm -it --privileged --net=host \
--ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \
-v $HOME/.Xauthority:/root/.Xauthority -e XAUTHORITY=/root/.Xauthority \
-v $HOME/Workspace/DrivePX/ROS/catkin_ws:/root/catkin_ws \
-e ROS_IP=cookie.2gt.lan \
turlucode/ros-indigo

# See https://github.com/osrf/docker_images/issues/21
# -env QT_X11_NO_MITSHM=1 (The MIT-SHM is an extension to the X server which allows faster transactions by using shared memory. Docker isolation probably blocks it. Docker isolation probably blocks it. https://en.wikipedia.org/wiki/MIT-SHM)

# alternative solution is to pass --ipc host and take advantage of MIT-SHM performance


