import sys
import argparse

from loguru import logger

from turludock.logger import configure_logger
from turludock.command_line_arguments_parser import parse_command_line_args
from turludock.which_command import list_pre_configs, list_supported_ros_versions, list_cuda_support

from turludock.docker_build import build_pre_configured_image, build_custom_image
import turludock.generate_dockerfile_build_folder as generate_dockerfile_build_folder


def main(args: argparse.Namespace) -> int:
    """
    Main entry point for the command line interface of the turludock tool.

    Args:
        args: An object holding the command line arguments parsed by argparse.

    Returns:
        An integer indicating the exit status of the program. 0 indicates success,
        non-zero values indicate failure.
    """
    # Enable debug mode
    if args.debug:
        configure_logger(True)

    # which preset
    if args.command == "which":
        if args.which == "presets":
            list_pre_configs()
        elif args.which == "ros":
            list_supported_ros_versions()
        elif args.which == "cuda":
            list_cuda_support(args.ros_codename)
        return 0
    # build
    if args.command == "build":
        # Build from pre-configuration
        try:
            # Build image from pre-configuration
            if args.e:
                build_args = {"tag": args.tag, "no_cache": args.no_cache, "verbose": args.verbose}
                build_pre_configured_image(args.e, build_args)
            # Build custom-image using user's .yaml config file
            elif args.c:
                build_args = {"tag": args.tag, "no_cache": args.no_cache, "verbose": args.verbose}
                build_custom_image(args.c, build_args)
        except Exception:
            logger.error("Error running 'build' command. Exit.")
            return 1
    # generate
    if args.command == "generate":
        try:
            # Generate from pre-configuration
            if args.e:
                generate_dockerfile_build_folder.generate_from_pre_config(args.e, args.path)
            # Generate using user's .yaml config file
            elif args.c:
                generate_dockerfile_build_folder.generate_from_user_config(args.c, args.path)
        except Exception:
            logger.error("Error running 'generate' command. Exit.")
            return 1


if __name__ == "__main__":
    # Initialize the logger
    configure_logger()

    # Parse arguments
    args_, parse_ok_ = parse_command_line_args()

    # Run main if parsing successful
    if not parse_ok_:
        sys.exit(1)
    else:
        sys.exit(main(args_))
