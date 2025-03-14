from typing import Any, Dict, List

from loguru import logger

from turludock.helper_functions import check_if_remote_tag_exists, get_llvm_supported_versions, get_ubuntu_version
from turludock.yaml_load import load_cuda_config, load_cudnn_config


def check_if_cmake_version_exists(version: str) -> None:
    """Checks if a given CMake version exists in the remote repository.

    Args:
        version (str): The version of CMake to check.

    Raises:
        ValueError: If the given version of CMake is not found in the remote repository.
    """
    if not check_if_remote_tag_exists("https://github.com/Kitware/CMake.git", version):
        raise ValueError("CMake tag not found in remote. Check your configuration.")


def check_if_tmux_version_exists(version: str) -> None:
    """Checks if a given Tmux version exists in the remote repository.

    Args:
        version (str): The version of Tmux to check.

    Raises:
        ValueError: If the given version of Tmux is not found in the remote repository.
    """
    if not check_if_remote_tag_exists("https://github.com/tmux/tmux.git", version):
        raise ValueError("Tmux tag not found in remote. Check your configuration.")


def check_if_llvm_version_exists(version: str) -> None:
    """Checks if a given LLVM version exists in the remote repository.

    Args:
        version (str): The version of LLVM to check.

    Raises:
        ValueError: If the given version of LLVM is not found in the remote repository.
    """
    # Get supported LLVM versions
    supported_versions = get_llvm_supported_versions()

    # Check if version is supported
    version_is_supported = False
    for supported_version in supported_versions:
        try:
            if int(version) == int(supported_version):
                version_is_supported = True
        except Exception as e:
            logger.error(f"LLVM version not supported - check your configuration. Error: {e}")
            raise
    if not version_is_supported:
        raise ValueError(f"LLVM version {version} not supported. Supported are: {supported_versions}")


def check_against_known_list(config: Dict[str, Any], dict_key: str, supported_values: List[str]) -> None:
    """Checks if a given YAML key is in a list of supported values.

    In case of the extra packages, besides checking if we support the package, we also check if
    we support the version as well.

    Args:
        config (Dict[str, Any]): The configuration dictionary
        dict_key (str): The key in the configuration dictionary to check
        supported_values (list): The list of supported values for the given key

    Raises:
        ValueError: If the given value is not in the supported list of values
    """
    # In case the key points to a list
    if isinstance(config[dict_key], list):
        # Check each item of the config-list if it is a known configuration, e.g. a supported by us "package"
        for item in config[dict_key]:
            # If item is a dictionary we assume a version has been specified
            if isinstance(item, dict):
                if len(item.keys()) != 1:
                    raise ValueError(f"'{dict_key}: - {item}' cannot be a list. Specify only one version.")
                if "cmake" in item.keys():
                    package_name = "cmake"
                    check_if_cmake_version_exists(item[package_name])
                if "tmux" in item.keys():
                    package_name = "tmux"
                    check_if_tmux_version_exists(item[package_name])
                if "llvm" in item.keys():
                    package_name = "llvm"
                    check_if_llvm_version_exists(item[package_name])
            # Else no version has be specified and we just need to install "latest" available version
            else:
                package_name = item

            if package_name not in supported_values:
                raise ValueError(f"'{dict_key}: - {item}' not supported. Supported are {supported_values}")
    # Else if it is a single value
    else:
        if config[dict_key] not in supported_values:
            raise ValueError(f"'{dict_key}: {config[dict_key]}' not supported. Supported are {supported_values}")


def check_supported_ros_version(config: Dict[str, Any]) -> None:
    """Checks if a given ROS version is supported.

    Args:
        config (Dict[str, Any]): The configuration dictionary

    Raises:
        ValueError: If the ROS version is not supported
    """
    dict_key = "ros_version"
    supported_ros1_values = ["noetic"]
    supported_ros2_values = ["humble", "iron", "jazzy"]
    supported_values = supported_ros1_values + supported_ros2_values
    check_against_known_list(config, dict_key, supported_values)


def check_supported_gpu_drivers(config: Dict[str, Any]) -> None:
    """Checks if a given GPU driver is supported.

    Args:
        config (Dict[str, Any]): The configuration dictionary

    Raises:
        ValueError: If the given GPU drive is not supported
    """
    dict_key = "gpu_driver"
    supported_values = ["nvidia", "mesa"]
    check_against_known_list(config, dict_key, supported_values)


def check_extra_packages(config: Dict[str, Any]) -> None:
    """Checks the 'extra packages' YAML configuration.

    Args:
        config (Dict[str, Any]): The configuration dictionary

    Raises:
        ValueError: If the given GPU drive is not supported
    """
    dict_key = "extra_packages"
    # It can happen that no extra packages have been configured
    if dict_key not in config:
        logger.debug("No extra_packages have been configured in the .yaml file.")
        return
    supported_by_default = ["cmake"]
    supported_values = ["tmux", "llvm", "vscode", "conan", "meld", "cpplint"]
    supported_values += supported_by_default
    check_against_known_list(config, dict_key, supported_values)


def is_cuda_version_supported(cuda_version: str, ubuntu_version: str) -> bool:
    """Checks if the given CUDA version is supported for the given Ubuntu version.

    Args:
        cuda_version (str): CUDA version to check against the ubuntu_version
        ubuntu_version (str): The 'flat' Ubuntu version to check, e.g. 'ubuntu2204'

    Returns:
        bool: True if CUDA version is supported for the given Ubuntu version, False otherwise
    """
    cuda_config = load_cuda_config()
    if cuda_version in cuda_config:
        if ubuntu_version in cuda_config[cuda_version]:
            logger.debug(f"Found supported cuda-{cuda_version}-{ubuntu_version}")
            return True
        else:
            logger.error(f"Did not find supported ubuntu version '{ubuntu_version}' for cuda-{cuda_version}")
            supported_cuda_versions = list()
            for cuda_version in cuda_config:
                if ubuntu_version["flat"] in cuda_config[cuda_version]:
                    supported_cuda_versions.append(cuda_version)
            if len(supported_cuda_versions) == 0:
                logger.error(f"'cuda_version: {cuda_config['cuda_version']}' not supported at all!")
            else:
                logger.error(
                    f"cuda_version: {cuda_config['cuda_version']}' not supported. Supported are "
                    + f"{supported_cuda_versions} for Ubuntu {ubuntu_version['semantic']}"
                )
            return False
    else:
        logger.error(f"Did not find supported cuda version '{cuda_version}'")
        return False


def check_cuda_version(config: dict):
    """Check if the provided CUDA version is supported.

    Args:
        config (dict): The configuration dictionary

    Raises:
        ValueError: If the given CUDA version is not in the supported
    """
    ubuntu_version = get_ubuntu_version(config["ros_version"])
    if not is_cuda_version_supported(config["cuda_version"], ubuntu_version["flat"]):
        raise ValueError("CUDA version not supported.")


def is_cuda_cudnn_version_combination_supported(cuda_version: str, cudnn_version: str, ubuntu_version: str) -> bool:
    """Checks if the given cuDNN version is supported.

    A cuDNN version is always coupled to a CUDA version. Not all cuDNN/CUDA combinations are supported.
    And of course not all CUDA versions are supported by each Ubuntu version.
    So an Ubuntu version dictates which CUDA versions are supported and in turn each CUDA version
    dictates which cuDNN versions are supported.

    Args:
        cuda_version (str): the CUDA version to check
        cudnn_version (str): cuDNN version to check
        ubuntu_version (str): Ubuntu version to check

    Returns:
        bool: True if the CUDA and cuDNN version combination is supported for the given Ubuntu version, False otherwise
    """
    cudnn_config = load_cudnn_config()
    if cudnn_version in cudnn_config:
        if ubuntu_version in cudnn_config[cudnn_version]:
            if cuda_version in cudnn_config[cudnn_version][ubuntu_version]["cuda_version"]:
                return True
            else:
                logger.error(
                    f"Did not find supported cuDNN version '{cudnn_version}' "
                    + f"for cuda-{cuda_version} and Ubuntu '{ubuntu_version}'"
                )
                return False
        else:
            logger.error(f"Did not find supported Ubuntu version '{ubuntu_version}' for cuDNN {cudnn_version}")
            return False
    else:
        logger.error(f"Did not find supported cuDNN version '{cudnn_version}'")
        return False


def check_cudnn_version(config: dict):
    """Check if the provided cuDNN version is supported.

    Args:
        config (dict): The configuration dictionary

    Raises:
        ValueError: If the given cuDNN version is not in the supported
    """
    ubuntu_version = get_ubuntu_version(config["ros_version"])
    if not is_cuda_cudnn_version_combination_supported(
        config["cuda_version"], config["cudnn_version"], ubuntu_version["flat"]
    ):
        raise ValueError("cuDNN version not supported.")


def check_required_fields(config: dict):
    """Check if the configuration dictionary contains the required fields.

    Args:
        config (dict): The configuration dictionary

    Raises:
        ValueError: If the key 'ros_version' is missing in the YAML file
        ValueError: If the key 'gpu_driver' is missing in the YAML file
    """
    if "ros_version" not in config:
        raise ValueError("Please a ROS version, e.g. 'ros_version: noetic'")

    if "gpu_driver" not in config:
        raise ValueError("Please a GPU driver, e.g. 'gpu_driver: mesa'")


def check_nvidia_config(config: dict):
    """Check the CUDA/cuDNN configuration.

    Args:
        config (dict): The configuration dictionary

    Raises:
        ValueError: If the is a miss-configuration in the CUDA/cuDNN keys
    """
    try:
        # CUDNN only works with CUDA. So CUDA must be present
        if "cudnn_version" in config and "cuda_version" not in config:
            raise ValueError(
                "CUDNN version was configured, but not the CUDA version. Please configure also CUDA version."
            )

        # It doesn't make sense to install CUDA/CUDNN if the NVIDIA drivers are not present.
        if config["gpu_driver"] == "mesa":
            if "cuda_version" in config:
                logger.warning(
                    "CUDA has been configured although 'gpu_driver: mesa'. Did you mean 'gpu_driver: nvidia' ?"
                )
            if "cudnn_version" in config:
                logger.warning(
                    "CUDNN has been configured although 'gpu_driver: mesa'. Did you mean 'gpu_driver: nvidia' ?"
                )

        # Also show a warning in debug mode if nvidia has been selected but no CUDA or CUDNN version is set
        if config["gpu_driver"] == "nvidia":
            if "cuda_version" not in config:
                logger.debug("Warning: 'cuda_version' is not set in the yaml configuration file")
            else:
                if "cudnn_version" not in config:
                    logger.debug(
                        "Warning: 'cudnn_version' is not set in the yaml configuration file although "
                        + f"'cuda_version': '{config['cuda_version']}'"
                    )

        # Check CUDA version
        if "cuda_version" in config:
            check_cuda_version(config)
            # Check CUDNN version
            if "cudnn_version" in config:
                check_cudnn_version(config)
    except ValueError as e:
        logger.error(f"NVIDIA configuration error: {e}")
        raise
