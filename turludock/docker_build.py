import os
import tempfile
from typing import Any, Dict

import docker
from loguru import logger

import turludock.default_image_config as default_image_config
from turludock.build_progress import BuildProgress
from turludock.config_parser import check_dockerfile_config
from turludock.filesystem_operations import copy_resource, get_filename_from_path
from turludock.generate_dockerfile import generate_dockerfile
from turludock.yaml_load import load_yaml_file


def _generate_image_tag(yaml_config: Dict[str, Any]) -> str:
    """
    Generate the docker image tag based on the given configuration.

    Args:
        yaml_config (dict): The image configuration in yaml format.

    Returns:
        str: The generated docker image tag.
    """
    tag_name = "turlucode/"

    ros_version = yaml_config["ros_version"]
    tag_name += f"ros-{ros_version.lower()}"
    tag_name += f':{yaml_config["gpu_driver"].lower()}'

    if "cuda_version" in yaml_config:
        tag_name += f'-cuda{yaml_config["cuda_version"]}'
    if "cudnn_version" in yaml_config:
        tag_name += f'-cudnn{yaml_config["cudnn_version"]}'

    if "extra_packages" in yaml_config:
        for item in yaml_config["extra_packages"]:
            if isinstance(item, dict):
                package_name = next(iter(item), None)
            elif isinstance(item, str):
                package_name = item
            tag_name += f"-{package_name}"

    return tag_name


def build_image(docker_image_path: str, build_args: dict) -> None:
    """Build a Docker image using docker api

    Args:
        docker_image_path (str): The path to the Dockerfile to build.
        build_args (dict): The build arguments to use.
    """
    try:
        # Initialize the progress bar if needed
        if not build_args["verbose"]:
            build_progress = BuildProgress()

        # Connect to the Docker daemon
        client = docker.from_env()

        # Build the Docker image
        # Not using client.images.build so we can monitor the progress in real-time
        # See also: https://github.com/docker/docker-py/issues/376#issue-46825714
        response = client.api.build(
            path=docker_image_path,
            rm=True,  # Remove intermediate containers after a successful build
            tag=build_args["tag"],
            decode=True,  # The returned stream will be decoded into dicts on the fly
            nocache=build_args["no_cache"],  # Don't use the cache
        )

        # Process and print build logs in real-time
        try:
            for chunk in response:
                if "stream" in chunk:
                    if build_args["verbose"]:
                        print(chunk["stream"], end="", flush=True)
                    else:
                        build_progress.advance(chunk["stream"])
                elif "errorDetail" in chunk:
                    if build_args["verbose"]:
                        print(chunk["errorDetail"]["message"], end="", flush=True)
                    raise RuntimeError(f"Docker build error: {chunk['errorDetail']['message']}")
        except Exception as e:
            logger.error(f"client.api.build Error: {e}")
            raise

        if not build_args["verbose"]:
            build_progress.finish()

        # Print the ID of the built image
        image = client.images.get(build_args["tag"])
        print("")
        logger.info(f"Built image: '{build_args['tag']}' ({image.id})")
    except Exception as e:
        logger.error(f"Could not build image. Error: {e}")
        raise


def build_image_from_yaml_config(yaml_config: dict, build_args: dict) -> None:
    """Build a Docker image whose Dockerfile generation is based on the provided YAML config

    Args:
        yaml_config (dict): The YAML configuration for the auto-generation of the Dockerfile
        build_args (dict): The build arguments for 'docker build' command
    """
    # Check Dockerfile .yaml configuration
    check_dockerfile_config(yaml_config)

    # Generate Dockerfile based on configuration
    dockerfile = generate_dockerfile(yaml_config)

    if build_args["tag"] is None:
        build_args["tag"] = _generate_image_tag(yaml_config)

    # Create a temporary directory where we store the generated Dockerfile and its assets.
    # Important: when TemporaryDirectory() goes out of scope it deletes it.
    # So everything needs to happen within 'tempfile.TemporaryDirectory()'
    with tempfile.TemporaryDirectory() as temp_dir:
        # print(f"Temporary directory created at: {temp_dir}")

        # Store generated Dockerfile in tmp directory
        dockerfile_path = os.path.join(temp_dir, "Dockerfile")
        with open(dockerfile_path, "w", encoding="utf-8") as file:
            file.write(dockerfile)

        # Copy over Dockerfile assets
        copy_resource("turludock.assets.dockerfile_assets", "entrypoint_setup.sh", temp_dir)
        copy_resource("turludock.assets.dockerfile_assets", "terminator_config", temp_dir)

        # Build image
        build_image(temp_dir, build_args)


def build_pre_configured_image(config_name: str, build_args: dict) -> None:
    """Build an image given a provided by us configuration, a.k.a. pre-configuration

    All the pre-configuration are located in 'assets/default_image_configurations' and
    these are the ones we support basically.

    Args:
        config_name (str): The name of the pre-configured image to build
        build_args (dict): The build arguments for 'docker build' command
    """
    try:
        yaml_config = default_image_config.get_yaml_config(config_name)
        build_image_from_yaml_config(yaml_config, build_args)
    except Exception as e:
        logger.error(f"Could not build pre-configured image. {e}")
        raise


def build_custom_image(yaml_config_path: str, build_args: dict) -> None:
    """Build a Docker image based on a provided/custom YAML configuration

    Args:
        yaml_config_path (str): The path to the YAML configuration
        build_args (dict): The build arguments for the 'docker build' command
    """
    try:
        # Load .yaml file
        yaml_config = load_yaml_file(yaml_config_path)
        yaml_config.update({"filename": get_filename_from_path(yaml_config_path)})
        # Build custom-image
        build_image_from_yaml_config(yaml_config, build_args)
    except Exception:
        logger.error("Could not build custom-image")
        raise
