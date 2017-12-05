.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# [NVIDIA] Build ROS Indigo Container
nvidia_ros_indigo: ## [NVIDIA] Build ROS Indigo Container | (CUDA 8 - no CUDNN)
	docker build -t turlucode/ros-indigo:latest nvidia/indigo
	@printf "\n\033[92mDocker Image: turlucode/ros-indigo:latest\033[0m\n"

# [NVIDIA] Build ROS Indigo Container with OpenCV 3.3 support
nvidia_ros_indigo_opencv3: ## [NVIDIA] Build ROS Indigo Container | (CUDA 8 - no CUDNN) | OpenCV 3.3
	docker build -t turlucode/ros-indigo-opencv3:latest nvidia/indigo-opencv3
	@printf "\n\033[92mDocker Image: turlucode/ros-indigo-opencv3:latest\033[0m\n"

# [NVIDIA] Build ROS Kinetic Container
nvidia_ros_kinetic: ## [NVIDIA] Build ROS Kinetic Container | (CUDA 8 - no CUDNN)
	docker build -t turlucode/ros-kinetic:latest nvidia/kinetic
	@printf "\n\033[92mDocker Image: turlucode/ros-kinetic:latest\033[0m\n"

# [NVIDIA] Build ROS Kinetic Container with OpenCV 3.3 support
nvidia_ros_kinetic_opencv3: ## [NVIDIA] Build ROS Kinetic Container | (CUDA 8 - no CUDNN) | OpenCV 3.3
	docker build -t turlucode/ros-kinetic-opencv3:latest nvidia/kinetic-opencv3
	@printf "\n\033[92mDocker Image: turlucode/ros-kinetic-opencv3:latest\033[0m\n"

# Helper TASKS
nvidia_run_help: ## [NVIDIA] Prints help and hints on how to run an NVIDIA-based image
	 @printf "  - Make sure the nvidia-docker-plugin (Test it with: nvidia-docker run --rm nvidia/cuda nvidia-smi)\n  - Command example:\nnvidia-docker run --rm -it --privileged --net=host \\ \n--ipc=host \\ \n-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \\ \n-v $HOME/.Xauthority:/root/.Xauthority -e XAUTHORITY=/root/.Xauthority \\ \n-v <PATH_TO_YOUR_CATKIN_WS>:/root/catkin_ws \\ \n-e ROS_IP=<HOST_IP or HOSTNAME> \\ \nturlucode/ros-indigo\n"
