import os
from typing import Any, Dict

from termcolor import colored

import turludock.config_sanity as config_sanity
from turludock.helper_functions import get_ros_major_version, get_ubuntu_version


def get_config_filename(yaml_full_path: str) -> str:
    """Get the filename of the given YAML file.

    Args:
        yaml_full_path (str): The full path to the YAML file

    Returns:
        str: The filename of the given YAML file
    """
    return os.path.basename(yaml_full_path)


def get_config_name(yaml_full_path: str) -> str:
    """Infer the name of the given YAML file.

    For now this is the name of the file without its file extension

    Args:
        yaml_full_path (str): The full path to the YAML file

    Returns:
        str: The corresponding name of the YAML file
    """
    return get_config_filename(yaml_full_path).replace(".yaml", "")


def check_dockerfile_config(config: Dict[str, Any]) -> None:
    """Checks if the given Dockerfile configuration is valid.

    Checks the following:
        * The required fields are present.
        * The GPU driver is supported.
        * The NVIDIA configuration is valid.
        * The ROS version is supported.
        * The list of extra packages is valid.

    Args:
        config (dict): The Dockerfile configuration.
    """
    # First check if required fields are present
    config_sanity.check_required_fields(config)
    # Check GPU drivers
    config_sanity.check_supported_gpu_drivers(config)
    # Check NVIDIA configuration
    config_sanity.check_nvidia_config(config)
    # Check ROS version
    config_sanity.check_supported_ros_version(config)
    # Check the list of extra packages
    config_sanity.check_extra_packages(config)


def print_configuration(yaml_config: Dict[str, Any]) -> None:
    """Prints the given YAML configuration in a human readable format.

    Args:
        yaml_config (dict): The configuration file parsed as YAML.
    """
    # Config name
    config_name = get_config_name(yaml_config["filename"])
    config_name_str = colored(f"{config_name: <20}", "green", attrs=["bold"])

    # ROS version
    ros_version = yaml_config["ros_version"]
    ros_version_str = f"ROS {get_ros_major_version(ros_version)} {ros_version.capitalize()}"

    # Ubuntu version
    ubuntu_version = get_ubuntu_version(ros_version)
    ubuntu_version_str = f"Ubuntu {ubuntu_version['semantic']}"

    # GPU driver
    gpu_driver_str = "GPU: " + yaml_config["gpu_driver"]

    # CUDA/CUDNN
    if "cuda_version" in yaml_config:
        cuda_version_str = f"CUDA: {yaml_config['cuda_version']}"
    else:
        cuda_version_str = "CUDA: -"
    if "cudnn_version" in yaml_config:
        cudnn_version_str = f"cuDNN: {yaml_config['cudnn_version']}"
    else:
        cudnn_version_str = "cuDNN: -"

    # List of packages
    extra_packages_str = ""
    if "extra_packages" in yaml_config:
        extra_packages_str += "Extra packages:"
        for pkg in yaml_config["extra_packages"]:
            if isinstance(pkg, dict):
                package_name = next(iter(pkg), None)
                extra_packages_str += f" {package_name}-{pkg[package_name]}"
            elif isinstance(pkg, str):
                extra_packages_str += f" {pkg}"
    else:
        extra_packages_str = "No extra packages"

    print(
        f"{config_name_str} {ros_version_str: <13} | {ubuntu_version_str} | "
        + f"{gpu_driver_str: <11} | {cuda_version_str: <12} | {cudnn_version_str: <15} | {extra_packages_str}"
    )
