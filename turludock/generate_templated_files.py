import importlib.resources
from string import Template
from typing import Any, Dict, List

from loguru import logger

from turludock.config_sanity import (
    check_if_cmake_version_exists,
    check_if_llvm_version_exists,
    check_if_tmux_version_exists,
)
from turludock.helper_functions import (
    get_cpu_count_for_build,
    get_ros_major_version,
    get_ubuntu_version,
    is_ros_version_supported,
    is_version_greater,
    is_version_lower,
)


def populate_templated_file(mapping: Dict[str, str], templated_file: str) -> str:
    """Populates a templated file with the provided mapping and returns it as generated string

    Args:
        mapping (Dict[str, str]): The mapping of template variables to their values.
        templated_file (str): The name of the templated file.

    Returns:
        str: The populated templated file.
    """
    with importlib.resources.open_text("turludock.assets.dockerfile_templates", templated_file) as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output


def _get_ubuntu_base_image(version: str, nvidia: bool) -> str:
    """Get the base image for the Docker build. It is used in "FROM <base_image>".

    Args:
        version (str): The semantic version of Ubuntu
        nvidia (bool): Whether the NVIDIA GPU driver is being used

    Returns:
        str: The Docker image name to use as the base image.
    """
    if nvidia:
        if is_version_lower(version, "16.04"):
            raise ValueError(f"Ubuntu version lower than 16.04 is not supported. You provided: {version}")

        # TODO(ATA): Not sure nvidia/opengl is really needed. Can we not just use 'ubuntu' with nvidia-docker-v2?
        return f"nvidia/opengl:1.2-glvnd-runtime-ubuntu{version}"
    else:
        return f"ubuntu:{version}"


def _get_base_image(yaml_config: Dict[str, Any]) -> str:
    """Return the supported base image name.

    This is used in the "FROM " part of the Dockerfile. See "from.txt" template.

    Args:
        yaml_config (dict): The configuration of the image to be built.

    Returns:
        str: The base image name.
    """
    ubuntu_version = get_ubuntu_version(yaml_config["ros_version"])
    if yaml_config["gpu_driver"] == "nvidia":
        uses_nvidia = True
        # Temp fix until nvidia releases nvidia/opengl for Ubuntu 24.04
        if is_version_greater(ubuntu_version["semantic"], "23.04"):
            uses_nvidia = False
            logger.warning(
                "'nvidia/opengl:1.2-glvnd-runtime' does not exist yet for Ubuntu 24.04. "
                + "Using 'ubuntu:20.04' as base image instead. This is experimental. "
                + "Please report any issues faced."
            )
    else:
        uses_nvidia = False
    return _get_ubuntu_base_image(ubuntu_version["semantic"], uses_nvidia)


def generate_from(yaml_config: Dict[str, Any]) -> str:
    """Generates the 'from.txt' templated file.

    Args:
        from_str (str): The value to be used for the 'From' template variable.

    Returns:
        yaml_config (dict): The image configuration in yaml format.
    """
    # Map the template variables
    base_image = _get_base_image(yaml_config)
    mapping = {"from": base_image}

    # Pick template based on ubuntu version
    ubuntu_version = get_ubuntu_version(yaml_config["ros_version"])
    if is_version_greater(ubuntu_version["semantic"], "23.04"):
        logger.debug(f"Generate 'from_2404.txt'. Input: {base_image}")
        return populate_templated_file(mapping, "from_2404.txt")
    else:
        logger.debug(f"Generate 'from.txt'. Input: {base_image}")
        return populate_templated_file(mapping, "from.txt")


def generate_header_info(docker_label_description: str, ros_version_short: str) -> str:
    """Generates the 'header_info.txt' templated file.

    Args:
        docker_label_description (str): The text for the "LABEL Description =" field
        ros_version_short (str): The ROS codename used in "LABEL com.turlucode.ros.version="

    Returns:
        str: The populated 'header_info.txt' file as a string.

    Raises:
        ValueError: If the provided ROS version is not supported.
    """
    logger.debug(f"Generate 'header_info.txt'. Input: {docker_label_description}, {ros_version_short}")

    # Check if provided version is supported
    if not is_ros_version_supported(ros_version_short):
        raise ValueError(f"ROS version '{ros_version_short}' not supported. Check your configuration.")

    # Map the template variables
    mapping = {
        "docker_label_description": docker_label_description,
        "ros_version_short": ros_version_short,
    }

    # Populate the templated file
    return populate_templated_file(mapping, "header_info.txt")


def generate_cmake(version: str) -> str:
    """Generates the 'cmake.txt' templated file.

    Args:
        version (str): The version of CMake to be used.

    Returns:
        str: The populated 'cmake.txt' file as a string.
    """
    logger.debug(f"Generate 'cmake.txt'. Input: {version}")

    # Check if provided version exists in remote
    check_if_cmake_version_exists(version)

    # Map the template variables
    mapping = {"cmake_version": version, "num_of_cpu": get_cpu_count_for_build()}

    # Populate the templated file
    return populate_templated_file(mapping, "cmake.txt")


def generate_tmux(version: str) -> str:
    """Generates the 'tmux.txt' templated file.

    Args:
        version (str): The version of tmux to be used.

    Returns:
        str: The populated 'tmux.txt' file as a string.
    """
    logger.debug(f"Generate 'tmux.txt'. Input: {version}'")

    # Check if provided version exists in remote
    check_if_tmux_version_exists(version)

    # Map the template variables
    mapping = {"tmux_version": version, "num_of_cpu": get_cpu_count_for_build()}

    # Populate the templated file
    return populate_templated_file(mapping, "tmux.txt")


def generate_llvm(version: str) -> str:
    """Generates the 'llvm.txt' templated file.

    Args:
        version (str): The version of LLVM to be used.

    Returns:
        str: The populated 'llvm.txt' file as a string.
    """
    logger.debug(f"Generate 'llvm.txt'. Input: {version}")

    # Check if provided version is supported
    check_if_llvm_version_exists(version)

    # Map the template variables
    mapping = {"llvm_version": version}

    # Populate the templated file
    return populate_templated_file(mapping, "llvm.txt")


def generate_ros(ros_version_codename: str) -> str:
    """Generates the 'ros1.txt' or 'ros2.txt' templated file, which is responsible for installing ROS 1 or 2

    The selection of ROS 1 or 2 is based on the provided ROS codename.

    Args:
        ros_version_codename (str): The ROS version as codename.

    Returns:
        str: The populated 'ros1.txt' file as a string.

    Raises:
        ValueError: If the provided ROS version is not supported.
    """
    # Determine if it ROS1 or ROS2
    if get_ros_major_version(ros_version_codename) == 1:
        template_file = "ros1.txt"
    else:
        template_file = "ros2.txt"

    logger.debug(f"Generate '{template_file}'. Input: {ros_version_codename}")

    # Check if provided version is supported
    if not is_ros_version_supported(ros_version_codename):
        raise ValueError("ROS version not supported. Check your configuration.")

    # Map the template variables
    mapping = {"ros_version_short": ros_version_codename}

    # Populate the templated file
    return populate_templated_file(mapping, template_file)


def generate_extra_packages_label(extra_packages_list: List[str]) -> str:
    """Generates the 'extra_packages_label.txt' templated file

    This file is used to add extra packages to the image.

    Args:
        extra_packages_list (List[str]): The list of extra packages to be installed in the docker image

    Returns:
        str: The populated 'extra_packages_label.txt' file as a string.
    """
    logger.debug(f"Generate 'extra_packages_label.txt'. Input: {extra_packages_list}")

    # Map the template variables
    list_as_str = " ".join(extra_packages_list)
    mapping = {"extra_packages_list": list_as_str}

    # Populate the templated file
    return populate_templated_file(mapping, "extra_packages_label.txt")
