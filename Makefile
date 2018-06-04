.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# [NVIDIA] Build ROS Indigo Container
nvidia_ros_indigo_cuda8: ## [NVIDIA] Build ROS Indigo Container | (CUDA 8 - no cuDNN)
	docker build -t turlucode/ros-indigo:cuda8 nvidia/indigo-cuda8
	@printf "\n\033[92mDocker Image: turlucode/ros-indigo:cuda8\033[0m\n"

# [NVIDIA] Build ROS Indigo Container with OpenCV 3.3 support
nvidia_ros_indigo_cuda8_opencv3: ## [NVIDIA] Build ROS Indigo Container | (CUDA 8 - no cuDNN) | OpenCV 3.3
	docker build -t turlucode/ros-indigo:cuda8-opencv3 nvidia/indigo-opencv3
	@printf "\n\033[92mDocker Image: turlucode/ros-indigo:cuda8-opencv3\033[0m\n"

# [NVIDIA] Build ROS Indigo Container with OpenCV 3.3 support and cuDNN 6
nvidia_ros_indigo_cuda8_cudnn6_opencv3: ## [NVIDIA] Build ROS Indigo Container | (CUDA 8 - cuDNN 6) | OpenCV 3.3
	docker build -t turlucode/ros-indigo:cuda8-cudnn6-opencv3 nvidia/indigo-cuda8-cudnn6-opencv3
	@printf "\n\033[92mDocker Image: turlucode/ros-indigo:cuda8-cudnn6-opencv3\033[0m\n"

# [NVIDIA] Build ROS Kinetic Container
nvidia_ros_kinetic_cuda8: ## [NVIDIA] Build ROS Kinetic Container | (CUDA 8 - no cuDNN)
	docker build -t turlucode/ros-kinetic:cuda8 nvidia/kinetic
	@printf "\n\033[92mDocker Image: turlucode/ros-kinetic-cuda8:latest\033[0m\n"

# [NVIDIA] Build ROS Kinetic Container with OpenCV 3.3 support
nvidia_ros_kinetic_cuda8_opencv3: ## [NVIDIA] Build ROS Kinetic Container | (CUDA 8 - no cuDNN) | OpenCV 3.3
	docker build -t turlucode/ros-kinetic:cuda8-opencv3 nvidia/kinetic-opencv3
	@printf "\n\033[92mDocker Image: turlucode/ros-kinetic:cuda8-opencv3\033[0m\n"

# Helper TASKS
nvidia_run_help: ## [NVIDIA] Prints help and hints on how to run an NVIDIA-based image
	 @printf "  - Make sure the nvidia-docker-plugin (Test it with: nvidia-docker run --rm nvidia/cuda nvidia-smi)\n  - Command example:\nnvidia-docker run --rm -it --privileged --net=host \\ \n--ipc=host \\ \n-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY \\ \n-v $HOME/.Xauthority:/root/.Xauthority -e XAUTHORITY=/root/.Xauthority \\ \n-v <PATH_TO_YOUR_CATKIN_WS>:/root/catkin_ws \\ \n-e ROS_IP=<HOST_IP or HOSTNAME> \\ \nturlucode/ros-indigo:cuda8\n"
