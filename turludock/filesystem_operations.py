import importlib.resources
import os
import shutil

from loguru import logger


def get_package_permissions(package: str, resource: str) -> int:
    """Get the linux file-permissions of a resource from a package.

    Args:
        package (str): The name of the package the resource belongs to.
        resource (str): The name of the resource to get the permissions of.

    Returns:
        int: The permissions of the resource.

    Raises:
        Exception: If an error occurs while getting the permissions of the resource.
    """
    try:
        with importlib.resources.path(package, resource) as resource_path:
            return os.stat(resource_path).st_mode
    except Exception as e:
        logger.error(f"Could not get permissions of package resource {package}/{resource}: {e}")
        raise


def copy_file(src: str, dst: str) -> None:
    """Copy a file from a source to a destination.

    Args:
        src (str): The source file to copy.
        dst (str): The destination file path.

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If the program does not have sufficient permissions to copy the source to the destination.
        Exception: Catch-all for any other unexpected errors.
    """
    try:
        shutil.copy(src, dst)
        logger.debug(f"File copied successfully from {src} to {dst}.")
    except FileNotFoundError:
        logger.error(f"File {src} not found.")
    except PermissionError:
        logger.error(f"Permission denied to copy {src} to {dst}.")
    except Exception as e:
        logger.error(f"File copy: An error occurred: {e}")


def get_filename_from_path(full_path: str) -> str:
    """Returns the filename from a given full path.

    Args:
        full_path (str): The full path.

    Returns:
        str: The filename.
    """
    return os.path.basename(full_path)


def copy_resource(package: str, resource_name: str, destination_path: str) -> None:
    """
    Copies a resource file from the specified module to the destination path.

    Args:
    - resource_name: The name of the resource file to copy.
    - destination_path: The file path where the resource should be copied.
    """
    ref = importlib.resources.files(package) / resource_name
    with importlib.resources.as_file(ref) as resource_path:
        try:
            shutil.copy(resource_path, destination_path)
            logger.debug(f"Successfully copied '{resource_path}' to '{destination_path}'.")
        except FileNotFoundError:
            logger.error(f"File {resource_name} not found.")
        except PermissionError:
            logger.error(f"Permission denied to copy {resource_path} to {destination_path}.")
        except Exception as e:
            logger.error(f"File copy: An error occurred: {e}")


def create_clean_directory(dir_path: str):
    """Creates a directory at the specified path, ensuring it is empty by deleting it first if it already exists.

    Parameters:
        dir_path (str): The path to the directory to be created or cleaned.

    Raises:
        PermissionError: If the program does not have sufficient permissions to delete or create directories.
        Exception: Catch-all for any other unexpected errors.
    """
    try:
        # Check if the directory exists
        if os.path.exists(dir_path):
            # If it exists, delete it
            shutil.rmtree(dir_path)
        # Create the directory
        os.makedirs(dir_path)
    except PermissionError as e:
        logger.error(f"Could not create a clean directory in {dir_path}. Permission error: {e}")
    except Exception as e:
        # Catch-all for any other exceptions
        logger.error(f"Could not create a clean directory in {dir_path}. An unexpected error occurred: {e}")


def to_absolute_path(path: str) -> str:
    """Checks if a path is absolute or relative. If it's relative, converts it to an absolute path.

    Parameters:
        path (str): The path to be checked and converted.

    Returns:
        str: The absolute path.
    """
    if os.path.isabs(path):
        # If path is already absolute, return it as it is
        return path
    else:
        # If path is relative, convert it to absolute
        return os.path.abspath(path)
