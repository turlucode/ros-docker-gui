import importlib.resources
from typing import Any

import yaml
from loguru import logger


def load_yaml_file(file_path: str) -> dict:
    """
    Load and parse a YAML file.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The parsed YAML data as a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
            return yaml_data
    except IsADirectoryError as e:
        logger.error(f"Provided path '{file_path}' is not YAML file but a directory. Error: {e}")
        raise
    except FileNotFoundError as e:
        logger.error(f"Could not find YAML file '{file_path}'. Error: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{file_path}'. Error: {e}")
        raise


def load_packaged_yaml(package: str, yaml_file: str) -> dict[str, Any]:
    """
    Load a YAML file packaged in a module.

    Parameters:
        package (str): The name of the module containing the YAML file.
        yaml_file (str): The name of the YAML file to load.

    Returns:
        dict[str, Any]: The parsed YAML data as a dictionary.
    """
    try:
        with importlib.resources.open_text(package, yaml_file) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"The file '{yaml_file}' was not found.")
        raise
    except yaml.YAMLError as exc:
        logger.error(f"Error parsing YAML file: {exc}")
        raise


def load_cuda_config() -> dict[str, Any]:
    """
    Load the YAML from our module that contains the supported CUDA configurations

    Returns:
        dict[str, Any]: The parsed YAML containing the supported CUDA configurations
    """
    return load_packaged_yaml("turludock.assets.config_files", "nvidia_cuda.yaml")


def load_cudnn_config() -> dict[str, Any]:
    """
    Load the YAML from our module that contains the supported cuDNN configurations

    Returns:
        dict[str, Any]: The parsed YAML containing the supported cuDNN configurations
    """
    return load_packaged_yaml("turludock.assets.config_files", "nvidia_cudnn.yaml")


def load_default_image_configuration(yaml_filename: str) -> dict[str, Any]:
    """
    Load the YAML from our module that contains the Dockerfile configuration

    Parameters:
        yaml_filename (str): The name of the YAML file configuration to load.

    Returns:
        dict[str, Any]: The parsed YAML configuration
    """
    yaml_config = load_packaged_yaml(
        package="turludock.assets.default_image_configurations",
        yaml_file=yaml_filename,
    )
    yaml_config.update({"filename": yaml_filename})
    return yaml_config
