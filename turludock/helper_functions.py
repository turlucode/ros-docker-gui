import importlib.metadata
import importlib.resources
import multiprocessing
import os
import re
import subprocess
from typing import List

import requests
import urllib3
from loguru import logger
from packaging.version import InvalidVersion, Version

import turludock.constants as constants


def get_module_name() -> str:
    """Returns the name of the module.

    Returns:
        str: The name of the module
    """
    # TODO(ATA): Maybe use: from utils import get_module_name
    return "turludock"


def check_if_remote_tag_exists(remote_url: str, tag_name: str) -> bool:
    """Check if a specific tag exists in a remote repository.

    Args:
        remote_url (str): The URL of the remote repository.
        tag_name (str): The name of the tag to check.

    Returns:
        bool: True if the tag exists, False otherwise.

    Raises:
        Exception: If a general exception occurs while checking the tag.
    """
    try:
        # Run the git command to list remote tags
        result = subprocess.run(
            ["git", "ls-remote", "--tags", remote_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Check if the command was successful
        if result.returncode != 0:
            logger.error(f"Git command not successful: {result.stderr}")
            return False

        # Check if the tag exists in the remote repository
        tags = result.stdout
        if f"refs/tags/{tag_name}" in tags:
            logger.debug(f"Tag '{tag_name}' exists in remote")
            return True
        else:
            logger.error(f"Tag {tag_name} not found in remote! Check provided tag!")
            return False
    except Exception as e:
        logger.error(f"Could not check if remote-tag in remote exists: {e}")
        return False


def get_github_latest_version_tag(owner: str, repo: str) -> str:
    """Fetches the latest version tag from a GitHub repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Raises:
        ValueError: In case we get stats 200 from github API - unsuccessful request
        ValueError: Or if there are no valid versions found

    Returns:
        str: The latest version tag or None if no valid tags are found.
    """
    logger.debug(f"Trying to get latest version-tag from github for {owner}/{repo}...")

    # GitHub API URL for fetching tags of the repository
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    response = requests.get(url, timeout=10)

    # Check if the request was successful
    if response.status_code != 200:
        raise ValueError(f"Cannot determine tag-version: Error fetching tags: {response.status_code}")

    # Parse the JSON response to get the list of tags
    tags = response.json()

    # Iterate over each tag to check if it follows semantic versioning
    valid_versions = []
    for tag in tags:
        tag_name = tag["name"]
        try:
            version = Version(tag_name.lstrip("v"))  # Remove 'v' prefix if present
            valid_versions.append((version, tag_name))
        except InvalidVersion:
            continue

    # Check if there are any valid versions found
    if not valid_versions:
        raise ValueError(f"Cannot determine tag-version: No valid versions found for {owner}/{repo} on github.")

    latest_version = max(valid_versions, key=lambda v: v[0])
    logger.debug(f"Latest version found for {owner}/{repo} is {latest_version[1]}")
    return latest_version[1]


def get_llvm_supported_versions() -> List[int]:
    """Fetches a list of supported LLVM versions from the official LLVM APT repository.

    The function fetches the content of the URL ``https://apt.llvm.org/llvm.sh`` and
    uses a regular expression to extract the supported LLVM version numbers from the
    content.

    Returns:
        List[int]: A list of integers representing the supported LLVM version numbers
    """
    # Get LLVM install script which contains info about the supported versions
    url = "https://apt.llvm.org/llvm.sh"
    try:
        # fixes warning: InsecureRequestWarning: Unverified HTTPS request is being made to host 'apt.llvm.org'
        # when using verify=False in requests.get()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Get the content of the URL
        response = requests.get(url, timeout=10, verify=False)
    except Exception as e:
        logger.error(f"Could not get supported LLVM versions. Requests.get() error: {e}")
        raise

    # Check if the request was successful
    if response.status_code != 200:
        response.raise_for_status()

    # Define the regex pattern to match lines with LLVM_VERSION_PATTERNS[version]="-(version)"
    # the ="-(version)" is important so we can capture the group and extract the version integer
    pattern = re.compile(r'LLVM_VERSION_PATTERNS\[\d+\]="-(\d+)"')

    # Split content into lines and search for the pattern
    supported_versions = list()
    lines = response.text.splitlines()
    for line in lines:
        match = pattern.search(line)
        if match:
            version_number_int = int(match.group(1))  # Extract the number - this is still a int
            supported_versions.append(version_number_int)

    if len(supported_versions) == 0:
        raise ValueError(
            "No supported llvm could be extracted from https://apt.llvm.org/llvm.sh. "
            "Versioning might have changed, contact developers of this tool."
        )

    return supported_versions


def get_llvm_latest_version() -> int:
    """Fetches the latest supported LLVM version number.

    The function returns the maximum of the supported LLVM version numbers as returned by
    'get_llvm_supported_versions'.

    Returns:
        int: The latest supported LLVM version number
    """
    return max(get_llvm_supported_versions())


def list_yaml_files(directory: str) -> List[str]:
    """Walk through a directory and returns a list of all YAML files.

    Args:
        directory (str): The directory to start searching from.

    Returns:
        List[str]: A list of paths to YAML files.
    """
    yaml_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml"):
                # file_dict = {'filename': file,
                #              'full_path': os.path.join(root, file)}
                # yaml_files.append(file_dict)
                yaml_files.append(os.path.join(root, file))
    return yaml_files


def list_packaged_yaml_files(asset_folder: str) -> List[str]:
    """List all YAML files from a package.

    Args:
        asset_folder (str): The folder name of where the YAML files are located.

    Returns:
        List[str]: A list of paths to YAML files inside the package
    """
    # ref = importlib.resources.files(package)
    ref = importlib.resources.files(get_module_name())
    with importlib.resources.as_file(ref) as resource_path:
        try:
            asset_path = os.path.join(resource_path, asset_folder)
            return list_yaml_files(asset_path)
        except Exception as e:
            logger.error(f"Could not list yaml files in asset folder {asset_folder}: {e}")
            raise


def get_cpu_count_for_build() -> int:
    """Get the number of CPUs available for a build.

    These are usually being used by make, e.g. make -j<num_of_cpu>
    The idea is to help speed up the build process of the Dockerfile.

    Returns:
        int: The number of CPUs available for the build.
    """
    no_of_cpu = multiprocessing.cpu_count()
    no_of_cpu_for_build = no_of_cpu - 2

    if no_of_cpu_for_build <= 0:
        no_of_cpu_for_build = 1

    return no_of_cpu_for_build


def get_ubuntu_version(ros_version_codename: str) -> dict:
    """Creates a mapper that maps the ROS codename to the Ubuntu version

    The ROS codename is assumed to be checked already with the config_sanity.py

    Args:
        ros_version_codename (str): The ROS distribution codename

    Returns:
        dict: The corresponding Ubuntu version
    """
    if is_ros_version_supported(ros_version_codename):
        version_map = {
            "noetic": {"flat": "ubuntu2004", "semantic": "20.04"},
            "humble": {"flat": "ubuntu2204", "semantic": "22.04"},
            "iron": {"flat": "ubuntu2204", "semantic": "22.04"},
            "jazzy": {"flat": "ubuntu2404", "semantic": "24.04"},
        }
        return version_map[ros_version_codename]
    else:
        raise ValueError(f"Error mapping ROS '{ros_version_codename}' to Ubuntu version.")


def get_ros_major_version(ros_version_codename: str) -> int:
    """Creates a mapper that maps the ROS codename to the ROS major version

    The ROS codename is assumed to be checked already with the config_sanity.py

    Args:
        ros_version_codename (str): The ROS distribution codename

    Returns:
        int: The corresponding major ROS version, i.e. 1 or 2
    """
    version_map = constants.ROS_VERSION_MAP

    return version_map[ros_version_codename]


def is_ros_version_supported(ros_version_codename: str) -> bool:
    """Checks if a given ROS version is supported.

    Args:
        ros_version_codename (str): The codename of the ROS distribution.

    Returns:
        bool: True if the ROS version is supported, False otherwise.
    """
    try:
        ros_major_version = get_ros_major_version(ros_version_codename)
        logger.debug(f"ROS {ros_major_version} '{ros_version_codename}' version supported.")
        return True
    except KeyError:
        logger.error(f"Unsupported ROS version: {ros_version_codename}")
        return False


def is_version_lower(version_to_check: str, reference_version: str) -> bool:
    """Checks if a given version is lower than a reference version.

    Args:
        version_to_check (str): The version to check.
        reference_version (str): The reference version.

    Returns:
        bool: True if the version is lower than the reference version, False otherwise.
    """
    version = Version(version_to_check)
    reference = Version(reference_version)
    return version < reference


def is_version_greater(version_to_check: str, reference_version: str) -> bool:
    """Checks if a given version is greater than a reference version.

    Args:
        version_to_check (str): The version to check.
        reference_version (str): The reference version.

    Returns:
        bool: True if the version is greater than the reference version, False otherwise.
    """
    version = Version(version_to_check)
    reference = Version(reference_version)
    return version > reference


def get_program_version() -> str:
    """Gets the program version.

    See pyproject.toml

    Returns:
        str: The version
    """
    return importlib.metadata.version("turludock")
