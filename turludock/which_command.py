import os

from loguru import logger
from termcolor import colored

import turludock.constants as constants
from turludock.config_parser import check_dockerfile_config, get_config_filename, print_configuration
from turludock.helper_functions import get_ubuntu_version, is_ros_version_supported, list_packaged_yaml_files
from turludock.yaml_load import load_cuda_config, load_cudnn_config, load_default_image_configuration


def _explain_default_image_config(yaml_filename: str) -> None:
    """Explains with one line in the terminal the current configuration

    Args:
        yaml_filename (str): The name of the YAML file configuration to explain.
    """
    # Load yaml configuration file
    yaml_config = load_default_image_configuration(yaml_filename)

    # Check if config is valid
    # TODO(ATA): Do we really need this check? It is slowing down the command
    check_dockerfile_config(yaml_config)

    # Print configuration to terminal
    print_configuration(yaml_config)


def _sort_file_list_based_on_release_date(config_files: list) -> list:
    """Short the list of config files based on their release date and then alphabetically

    Important!!! For this to work all presets need to start with "<ros_codename>_"!
    Otherwise this is not able to infer the release date and in turn sort those.

    Args:
        config_files (list): The file list

    Returns:
        list: The input list sorted
    """

    def get_ros_codename(string: str) -> str:
        """Get the ROS code name from the string using ROS_VERSION_RELEASE_DATE_MAP

        Args:
            string (str): Input string

        Returns:
            str: The ROS codename
        """
        for key, _ in constants.ROS_VERSION_RELEASE_DATE_MAP.items():
            if key in string:
                return key

    # Function to extract the sorting key
    def sort_key(string: str) -> tuple:
        """Provide the sorting key

        - Fist key is the release date since epoch
        - Second key is what ever is after "codename_" and sorted alphabetically

        Args:
            string (str): The filepath of the .yaml file

        Returns:
            tuple: The sorting tuple
        """
        # Split the string on the last part after the last '/'
        last_part = string.rsplit("/", 1)[-1]
        # Split the last part on the first '_'
        first_part, rest = last_part.split("_", 1)
        return (constants.ROS_VERSION_RELEASE_DATE_MAP[get_ros_codename(first_part)], rest)

    # Sort the list using the custom key
    sorted_list = sorted(config_files, key=sort_key)
    return sorted_list


def list_pre_configs() -> None:
    """List in the terminal available image pre-configurations as provided by our module."""
    print("")
    logger.info("Available pre-configurations:")
    yaml_config_files = list_packaged_yaml_files(os.path.join("assets", "default_image_configurations"))
    sorted_yaml_config_files = _sort_file_list_based_on_release_date(yaml_config_files)

    for yaml_config_full_path in sorted_yaml_config_files:
        yaml_filename: str = get_config_filename(yaml_config_full_path)
        _explain_default_image_config(yaml_filename)

    config_name: str = "CONFIG_NAME"
    cmd_example: str = colored(f"turludock build -e {config_name}", attrs=["bold"])
    print("")
    print(f"> You can directly build a default docker image with: {cmd_example}")


def list_supported_ros_versions() -> None:
    """List in the terminal all supported ROS distributions."""
    print("")
    ros1 = [version for version, ros_version in constants.ROS_VERSION_MAP.items() if ros_version == 1]
    ros2 = [version for version, ros_version in constants.ROS_VERSION_MAP.items() if ros_version == 2]
    logger.info("Supported ROS Versions")
    logger.info(f"ROS 1: {ros1}")
    logger.info(f"ROS 2: {ros2}")


def list_cuda_support(ros_codename: str) -> None:
    """Lists all supported CUDA/cuDNN versions for a given ROS distribution.

    Args:
        ros_codename (str): ROS codename
    """
    ros_codename = ros_codename.lower()
    try:
        # Check if we even support this ROS version
        if not is_ros_version_supported(ros_codename):
            return

        # Load CUDA and cuDNN configs
        cuda_config = load_cuda_config()
        cudnn_config = load_cudnn_config()

        # Find which ones we support
        found_supported = False
        ubuntu_version = get_ubuntu_version(ros_codename)
        print("")
        logger.info(f"Supported versions for Ubuntu {ubuntu_version['semantic']} ({ros_codename}):")
        for cuda_version in cuda_config:
            if ubuntu_version["flat"] in cuda_config[cuda_version]:
                logger.info(f"*CUDA: {cuda_version}")
                found_supported = True
                for cudnn_version in cudnn_config:
                    if ubuntu_version["flat"] in cudnn_config[cudnn_version]:
                        if cudnn_config[cudnn_version][ubuntu_version["flat"]]:
                            logger.info(f"*CUDA: {cuda_version} | cuDNN: {cudnn_version}")
        if not found_supported:
            logger.warning(f"No supported CUDA/cuDNN version for ROS {ros_codename.capitalize()} at this point.")
    except Exception:
        logger.error("Could not run 'list-cuda-support' command. Exit.")
        raise
