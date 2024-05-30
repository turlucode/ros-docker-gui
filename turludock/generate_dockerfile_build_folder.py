import os

from loguru import logger

import turludock.default_image_config as default_image_config
from turludock.config_parser import check_dockerfile_config
from turludock.filesystem_operations import copy_resource, get_filename_from_path
from turludock.generate_dockerfile import generate_dockerfile
from turludock.yaml_load import load_yaml_file


def _populate_build_folder(yaml_config: dict, dir_path: str) -> None:
    """Populate the provided directory with the generated Dockerfile and its assets

    Args:
        yaml_config (dict): The configuration dictionary
        dir_path (str): The path of the directory where to populate the files
    """
    # Check Dockerfile .yaml configuration
    check_dockerfile_config(yaml_config)

    # Generate Dockerfile based on configuration
    dockerfile = generate_dockerfile(yaml_config)

    # Store generated Dockerfile in directory
    dockerfile_path = os.path.join(dir_path, "Dockerfile")
    with open(dockerfile_path, "w", encoding="utf-8") as file:
        file.write(dockerfile)
    logger.debug(f"Successfully copied generated Dockerfile in '{dir_path}'")

    # Copy over Dockerfile assets
    copy_resource("turludock.assets.dockerfile_assets", "entrypoint_setup.sh", dir_path)
    copy_resource("turludock.assets.dockerfile_assets", "terminator_config", dir_path)


def check_if_directory_path_is_valid(path: str) -> None:
    """Check if we have a valid path to a directory.

    Args:
        path (str): The directory path to check.

    Raises:
        ValueError: If the path is not a valid directory
        ValueError: If the directory does not exist or we do not have write access.
    """
    if not os.path.isdir(path):
        raise ValueError(f"The path '{path}' is not a valid directory.\n")
    if not os.access(path, os.W_OK):
        raise ValueError(f"We do not have write access to '{path}'\n")


def generate_from_pre_config(config_name: str, dir_path: str) -> None:
    """Populate the build folder with the Dockerfile and its assets using provided pre-configurations.

    See 'assets/default_image_configurations' for the list of supported pre-configurations.

    Args:
        config_name (str): The name of the pre-defined configuration to use.
        dir_path (str): The path to the directory where to store the generated Dockerfile and its assets

    Raises:
        Exception: If there is a problem populating the folder.
    """
    try:
        check_if_directory_path_is_valid(dir_path)
        yaml_config = default_image_config.get_yaml_config(config_name)
        _populate_build_folder(yaml_config, dir_path)

        print("")
        logger.info(f"Populated folder: '{dir_path}'")
    except Exception:
        logger.error(f"Could not populate build folder '{dir_path}'.")
        raise


def generate_from_user_config(yaml_config_path: str, dir_path: str):
    """Populate the build folder with the Dockerfile and its assets using the custom YAML configuration.

    Args:
        yaml_config_path (str): The path to the custom YAML configuration.
        dir_path (str): The path to the directory where to store the generated Dockerfile and its assets

    Raises:
        Exception: If there is a problem populating the folder.
    """
    try:
        check_if_directory_path_is_valid(dir_path)
        yaml_config = load_yaml_file(yaml_config_path)
        yaml_config.update({"filename": get_filename_from_path(yaml_config_path)})
        _populate_build_folder(yaml_config, dir_path)

        print("")
        logger.info(f"Populated folder: '{dir_path}'")
    except Exception:
        logger.error(f"Could not populate build folder '{dir_path}'.")
        raise
