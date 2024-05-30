from typing import Dict, Any

from loguru import logger

from turludock.config_parser import print_configuration
from turludock.generate_templated_files import (
    generate_from,
    generate_header_info,
    generate_cmake,
    generate_llvm,
    generate_tmux,
    generate_ros,
    generate_extra_packages_label,
)
from turludock.generate_non_templated_files import (
    generate_common_env_config,
    generate_install_common_packages,
    generate_mesa,
    generate_locale,
    generate_terminator,
    generate_ohmyzsh,
    generate_conan,
    generate_vscode,
    generate_entrypoint,
    generate_cmd,
    generate_meld,
    generate_cpplint,
)
from turludock.generate_nvidia_templated_files import (
    generate_cuda_base,
    generate_cuda_devel,
    generate_cuda_runtime,
    generate_cudnn_devel,
    generate_cudnn_runtime,
)
from turludock.helper_functions import (
    is_version_lower,
    is_version_greater,
    get_ubuntu_version,
    get_ros_major_version,
    get_github_latest_version_tag,
    get_llvm_latest_version,
)


def _get_item_from_extra_packages(extra_packages: list, package_name: str):
    """Get the dict or the str of a given package name

    Since the yaml list can contain either dictionaries or strings, here were trying to find the dictionary
    or the string that matches the given package_name.

    If a dict is found, return that dict. If a str is found, return that str. Otherwise return None.

    Args:
        extra_packages (List[Union[dict, str]]): A list of extra packages which could be either
            dictionaries or str.
        package_name (str): The name of the package to search for.

    Returns:
        Optional[dict]: If a dict which matches the package_name was found, return that dict. If a str
            which matches the package_name was found, return that str. Otherwise return None.
    """
    for item in extra_packages:
        if isinstance(item, dict) and package_name in item:
            return item
        if isinstance(item, str) and item == package_name:
            return item
        return None


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
    else:
        uses_nvidia = False
    return _get_ubuntu_base_image(ubuntu_version["semantic"], uses_nvidia)


def _generate_description(yaml_config: Dict[str, Any]) -> str:
    """Generate a description to be using in the "LABEL Description=" of the Dockerfile.

    See "header_info.txt" template

    Args:
        yaml_config (dict): The image configuration in yaml format.

    Returns:
        str: The generated description
    """
    ros_version = yaml_config["ros_version"]
    ros_version_str = f"ROS {get_ros_major_version(ros_version)} {ros_version.capitalize()}"

    # Ubuntu version
    ubuntu_version = get_ubuntu_version(ros_version)
    ubuntu_version_str = f"Ubuntu {ubuntu_version['semantic']}"

    # GPU driver
    gpu_driver_str = f"{yaml_config['gpu_driver']}"

    return f"{ros_version_str} | {ubuntu_version_str} | {gpu_driver_str}"


def _get_package_version(yaml_config: dict, package_name: str) -> str:
    """Get the version of a package from the yaml config or get the latest version by looking usually online.

    If the package is configured explicitly in the 'extra_packages' list, use the version
    specified there. Otherwise, infer that the latest version should be used.

    Args:
        yaml_config (dict): The parsed yaml config
        package_name (str): The name of the package to get the version of

    Returns:
        str: The version of the package

    Raises:
        ValueError: If the package is not known or the latest version cannot be determined
    """
    # Check if we even have key 'extra_packages'
    if "extra_packages" in yaml_config:
        item = _get_item_from_extra_packages(yaml_config["extra_packages"], package_name)
        if isinstance(item, dict):
            get_latest = False
        else:
            get_latest = True
    # If package not configured explicitly, always pick the latest version
    # This is only applicable for the default packages and never happens to the extra-packages
    else:
        get_latest = True

    # Infer and get the 'latest' version
    if get_latest:
        if package_name == "cmake":
            return get_github_latest_version_tag("Kitware", "CMake")
        elif package_name == "tmux":
            return get_github_latest_version_tag("tmux", "tmux")
        elif package_name == "llvm":
            return str(get_llvm_latest_version())
        else:
            raise ValueError(f"get_package_version() unknown package: {package_name}")
    # Get the version as defined in the .yaml
    else:
        return item[package_name]


def generate_dockerfile(yaml_config: Dict[str, Any]) -> str:
    """Generate the actual Dockerfile from a given yaml configuration.

    Based on YAML configuration we populate all templates to finally generate the Dockerfile.

    Args:
        yaml_config (dict): The image configuration in yaml format.

    Returns:
        str: The generated Dockerfile.
    """
    # Print configuration
    print("")
    logger.info("Configuration:")
    print_configuration(yaml_config)

    # Generate Dockerfile
    dockerfile = ""

    # Base image
    base_image = _get_base_image(yaml_config)
    dockerfile += generate_from(base_image)

    # Meta data
    dockerfile += generate_header_info(_generate_description(yaml_config), yaml_config["ros_version"])

    # Common configuration for all images
    dockerfile += generate_common_env_config()
    dockerfile += generate_install_common_packages()
    dockerfile += generate_locale()
    dockerfile += generate_cmake(_get_package_version(yaml_config, "cmake"))
    dockerfile += generate_terminator()
    dockerfile += generate_ohmyzsh()

    # GPU driver
    ubuntu_version = get_ubuntu_version(yaml_config["ros_version"])
    if yaml_config["gpu_driver"] == "mesa":
        if is_version_lower(ubuntu_version["semantic"], "20.04"):
            logger.warning(
                "Using mesa driver. However latest mesa drivers cannot be installed for "
                + f"Ubuntu {ubuntu_version['semantic']}. This means if you use laster Intel/AMD GPU "
                + "you most likely not going to get HW acceleration and programs like RViZ will use "
                + "software rendering. For more info check ppa:kisak/kisak-mesa"
            )
            # use mesa from default ubuntu repos
            dockerfile += generate_mesa(False)
        elif is_version_greater(ubuntu_version["semantic"], "22.04"):
            # use mesa from default ubuntu repos - those should be the latest
            dockerfile += generate_mesa(False)
        else:
            # use latest mesa provided by custom ppa
            dockerfile += generate_mesa(True)
    else:
        # no need to install something for NVIDIA
        pass

    # Add CUDA/cuDNN
    ubuntu_version = get_ubuntu_version(yaml_config["ros_version"])
    if "cuda_version" in yaml_config:
        dockerfile += generate_cuda_base(yaml_config["cuda_version"], ubuntu_version["flat"])
        dockerfile += generate_cuda_devel(yaml_config["cuda_version"], ubuntu_version["flat"])
        dockerfile += generate_cuda_runtime(yaml_config["cuda_version"], ubuntu_version["flat"])
        if "cudnn_version" in yaml_config:
            dockerfile += generate_cudnn_devel(
                yaml_config["cuda_version"], yaml_config["cudnn_version"], ubuntu_version["flat"]
            )
            # TODO(ATA): Devel already contains what runtime has. So it redundant.
            # But is it the case for cuDNN implementation?
            dockerfile += generate_cudnn_runtime(
                yaml_config["cuda_version"], yaml_config["cudnn_version"], ubuntu_version["flat"]
            )

    # Add ROS
    dockerfile += generate_ros(yaml_config["ros_version"])

    # Add the extra-packages
    extra_packages_label_list = list()
    if "extra_packages" in yaml_config:
        for item in yaml_config["extra_packages"]:
            if isinstance(item, dict):
                package_name = next(iter(item), None)
            elif isinstance(item, str):
                package_name = item

            if package_name == "tmux":
                dockerfile += generate_tmux(_get_package_version(yaml_config, package_name))
            if package_name == "llvm":
                dockerfile += generate_llvm(_get_package_version(yaml_config, package_name))
            if package_name == "meld":
                dockerfile += generate_meld()
            if package_name == "cpplint":
                dockerfile += generate_cpplint()
            if package_name == "conan":
                dockerfile += generate_conan()
            if package_name == "vscode":
                dockerfile += generate_vscode()

            extra_packages_label_list.append(package_name)
    else:
        extra_packages_label_list.append("")
        logger.debug("Warning: generate_dockerfile(): No extra packages have been configured.")
    dockerfile += generate_extra_packages_label(extra_packages_label_list)

    # Finally, add the entrypoint and cmd parts
    dockerfile += generate_entrypoint()
    dockerfile += generate_cmd()

    # print(dockerfile)
    return dockerfile