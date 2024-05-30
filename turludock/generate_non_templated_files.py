import importlib.resources

from loguru import logger


def get_non_templated_file(templated_file: str) -> str:
    """Generates a non-templated txt file, which basically only appending the text from the file

    Args:
        templated_file (str): The name of the templated file located in the assets

    Returns:
        str: The contents of the non-templated text file
    """
    logger.debug(f"Generate '{templated_file}'")
    with importlib.resources.open_text("turludock.assets.dockerfile_templates", templated_file) as f:
        str_output = f.read()
    str_output += "\n\n"
    return str_output


def generate_entrypoint() -> str:
    """Get entrypoint.txt as a string

    Returns:
        str: The entrypoint.txt as a string
    """
    return get_non_templated_file("entrypoint.txt")


def generate_cmd() -> str:
    """Get cmd.txt as a string

    Returns:
        str: The cmd.txt as a string
    """
    return get_non_templated_file("cmd.txt")


def generate_common_env_config() -> str:
    """Get common_env_config.txt as a string

    Returns:
        str: The common_env_config.txt as a string
    """
    return get_non_templated_file("common_env_config.txt")


def generate_install_common_packages() -> str:
    """Get install_common_packages.txt as a string

    Returns:
        str: The install_common_packages.txt as a string
    """
    return get_non_templated_file("install_common_packages.txt")


def generate_locale() -> str:
    """Get locale.txt as a string

    Returns:
        str: The locale.txt as a string
    """
    return get_non_templated_file("locale.txt")


def generate_ohmyzsh() -> str:
    """Get oh_my_zsh.txt as a string

    Returns:
        str: The oh_my_zsh.txt as a string
    """
    return get_non_templated_file("oh_my_zsh.txt")


def generate_terminator() -> str:
    """Get terminator.txt as a string

    Returns:
        str: The terminator.txt as a string
    """
    return get_non_templated_file("terminator.txt")


def generate_conan() -> str:
    """Get conan.txt as a string

    Returns:
        str: The conan.txt as a string
    """
    return get_non_templated_file("conan.txt")


def generate_vscode() -> str:
    """Get vscode.txt as a string

    Returns:
        str: The vscode.txt as a string
    """
    return get_non_templated_file("vscode.txt")


def generate_meld() -> str:
    """Get meld.txt as a string

    Returns:
        str: The meld.txt as a string
    """
    return get_non_templated_file("meld.txt")


def generate_cpplint() -> str:
    """Get cpplint.txt as a string

    Returns:
        str: The cpplint.txt as a string
    """
    return get_non_templated_file("cpplint.txt")


def generate_mesa(use_latest: bool = True) -> str:
    """Get the mesa install command as a string

    Args:
        use_latest (bool, optional): Whether to use the latest mesa version. Defaults to True.

    Returns:
        str: The mesa Dockerfile instructions as a string
    """
    if use_latest:
        filename = "mesa_latest.txt"
    else:
        filename = "mesa.txt"
    return get_non_templated_file(filename)
