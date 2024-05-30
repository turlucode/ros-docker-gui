import os

from turludock.config_parser import get_config_filename, get_config_name
from turludock.helper_functions import list_packaged_yaml_files
from turludock.yaml_load import load_default_image_configuration


def configuration_exists(config_name: str) -> bool:
    """Check if a configuration with the given name exists as asset in our module.

    See 'turludock/assets/default_image_configurations' for supported configurations.

    Args:
        config_name (str): The name of the configuration to check.

    Returns:
        bool: True if the configuration exists, False otherwise.
    """
    yaml_config_files = list_packaged_yaml_files(os.path.join("assets", "default_image_configurations"))
    for yaml_config in yaml_config_files:
        valid_config_name = get_config_name(yaml_config)
        if config_name == valid_config_name:
            return True
    return False


def get_yaml_config(config_name: str) -> dict:
    """Get YAML configuration file based on the given configuration name.

    Args:
        config_name (str): The name of the configuration to retrieve.

    Returns:
        dict: The configuration loaded from the YAML file.

    Raises:
        ValueError: If the provided configuration name does not exist.
    """
    yaml_config_files = list_packaged_yaml_files(os.path.join("assets", "default_image_configurations"))
    yaml_config = None
    for yaml_config_full_path in yaml_config_files:
        if config_name == get_config_name(yaml_config_full_path):
            yaml_filename = get_config_filename(yaml_config_full_path)
            yaml_config = load_default_image_configuration(yaml_filename)
            return yaml_config
    if yaml_config is None:
        raise ValueError(
            f"Provided pre-configuration '{config_name}' doesn't exist! "
            + "List available with 'turludock which preset'"
        )
