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
    is_version_greater,
)


def populate_templated_file(mapping: Dict[str, str], templated_file: str) -> str:
    """Populates a templated file with the provided mapping and returns it as generated string

    Args:
        mapping (Dict[str, str]): The mapping of template variables to their values.
        templated_file (str): The name of the templated file.

    Returns:
        str: The populated templated file.
    """
    try:
        with importlib.resources.open_text("turludock.assets.dockerfile_templates", templated_file) as f:
            src = Template(f.read())
            str_output = src.substitute(mapping)
        str_output += "\n\n"
        return str_output
    except FileNotFoundError:
        print(f"Template file '{templated_file}' not found.")
    except KeyError as e:
        print(f"Missing substitution key: {e}")
    except Exception as e:
        print(f"An unexpected error occurred at function `populate_templated_file`: {e}")


def _get_base_image(yaml_config: Dict[str, Any]) -> str:
    """Return the supported base image name.

    This is used in the "FROM " part of the Dockerfile. See "from.txt" template.

    Args:
        yaml_config (dict): The configuration of the image to be built.

    Returns:
        str: The base image name.
    """
    ubuntu_version = get_ubuntu_version(yaml_config["ros_version"])
    return f'ubuntu:{ubuntu_version["semantic"]}'


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
    """Generates the 'rosX.txt' templated file, which is responsible for installing ROS 1 or 2

    The selection of ROS 1 or 2 is based on the provided ROS codename.

    Args:
        ros_version_codename (str): The ROS version as codename.

    Returns:
        str: The populated 'rosX.txt' file as a string.
    """
    # Determine if it ROS1 or ROS2
    if get_ros_major_version(ros_version_codename) == 1:
        template_file = "ros1.txt"
    else:
        template_file = "ros2.txt"

    logger.debug(f"Generate '{template_file}'. Input: {ros_version_codename}")

    # Map the template variables
    mapping = {"ros_version_short": ros_version_codename}

    # Populate the templated file
    return populate_templated_file(mapping, template_file)


def generate_ros_extra(ros_version_codename: str) -> str:
    """Generates the 'rosX_extra.txt' templated file, which is responsible for installing extra ROS packages

    The selection of ROS 1 or 2 is based on the provided ROS codename.

    Args:
        ros_version_codename (str): The ROS version as codename.

    Returns:
        str: The populated 'rosX_extra.txt' file as a string.
    """
    # Determine if it ROS1 or ROS2
    if get_ros_major_version(ros_version_codename) == 1:
        # TODO
        return ""
    else:
        template_file = "ros2_extra.txt"

    logger.debug(f"Generate '{template_file}'. Input: {ros_version_codename}")

    # Map the template variables
    mapping = {"ros_version_short": ros_version_codename}

    # Populate the templated file
    return populate_templated_file(mapping, template_file)


def generate_ros_autocomplete_fix(ros_version_codename: str) -> str:
    """Generates the 'ros2_autocomplete_fix.txt' templated file as string

    This file is responsible for introducing a fix for zsh autocomplete.
    https://github.com/ros2/ros2cli/issues/534#issuecomment-957516107

    This has the hidden assumption that a ROS2 version is always coupled to a Ubuntu version.
    The fix should actually be on the Ubuntu version and not the ROS2 version.

    Args:
        ros_version_codename (str): The ROS version as codename.

    Returns:
        str: The populated 'ros2_autocomplete_fix.txt' file as a string.

    Raises:
        ValueError: If ROS version not supported / not yet added by this function
    """

    if get_ros_major_version(ros_version_codename) == 1:
        return ""

    template_file = "ros2_autocomplete_fix.txt"

    # Only apply for Humble
    if ros_version_codename == "humble" or ros_version_codename == "iron":
        mapping = {"python_argcomplete": "python-argcomplete3"}
    elif ros_version_codename == "jazzy":
        mapping = {"python_argcomplete": "python-argcomplete"}
    else:
        raise ValueError(
            f"ROS version {ros_version_codename} not yet supported by this function. "
            "Ask the developer to add support!"
        )

    logger.debug(f"Generate '{template_file}'. Input: {ros_version_codename}")
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
