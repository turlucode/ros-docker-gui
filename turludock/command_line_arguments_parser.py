import argparse
import os
from typing import Tuple

from loguru import logger

from turludock.helper_functions import get_program_version


class PrintVersionAction(argparse.Action):
    """Action class to print the version of the program."""

    def __call__(self, parser, namespace, values, option_string=None):
        """The actual call to the action."""
        logger.info(f"turludock v{get_program_version()}")
        parser.exit()


def print_command_help(args: argparse.Namespace, parser: dict) -> None:
    """Print help message for the command specified by the user.

    Args:
        args (argparse.Namespace): The parsed command line arguments.
        parser (dict): Dictionary containing the command line arguments parsers.
    """
    if args.command == "build":
        parser["build"].print_help()
    elif args.command == "generate":
        parser["gen"].print_help()
    elif args.command == "which":
        if args.which is None:
            parser["which"].print_help()
        else:
            if args.which == "presets":
                parser["wpre"].print_help()
            elif args.which == "ros":
                parser["wros"].print_help()
            elif args.which == "cuda":
                parser["wnv"].print_help()
    else:
        parser.print_help()


def check_arguments(args: argparse.Namespace) -> None:
    """Check if the command line arguments are valid.

    Checks the arguments depending on the command.

    Args:
        args (argparse.Namespace): The parsed command line arguments.

    Raises:
        ValueError: If the arguments are invalid.
    """
    if args.command == "build":
        if args.e and args.c:
            raise ValueError("Provide either argument '-c' or argument '-e'\n")
        if not args.e and not args.c:
            raise ValueError("Provide either argument '-c' or argument '-e'\n")
    elif args.command == "generate":
        if args.e and args.c:
            raise ValueError("Provide either argument '-c' or argument '-e'\n")
        if not args.e and not args.c:
            raise ValueError("Provide either argument '-c' or argument '-e'\n")
        if not args.path:
            raise ValueError("The following arguments are required: path\n")
        if not os.path.isdir(args.path):
            raise ValueError(f"The path '{args.path}' is not a valid directory.\n")
    elif args.command == "which":
        if args.which is None:
            raise ValueError("You need to provide one of the following sub-commands: presets, ros, cuda\n")
        if args.which == "presets":
            pass
        elif args.which == "ros":
            pass
        elif args.which == "cuda":
            pass
        else:
            raise ValueError("Only the following sub-commands are supported: presets, ros, cuda\n")
    else:
        raise ValueError(f"Unknown command '{args.command}'.\n")


def parse_command_line_args() -> Tuple[argparse.Namespace, bool]:
    """Parse the command line arguments.

    Returns:
        Tuple[argparse.Namespace, bool]: A tuple containing the parsed command line arguments as
        an argparse.Namespace object, and a boolean indicating whether the arguments are valid or not.
    """
    parser = dict()
    parser["main"] = argparse.ArgumentParser(
        description="ROS docker container generator " + f"| turludock v{get_program_version()} | TurluCode"
    )
    parser["main"].add_argument(
        "--version", action=PrintVersionAction, nargs=0, help="Show the program version and exit"
    )

    subparsers = parser["main"].add_subparsers(title="Commands", description="", help="additional help", dest="command")
    subparsers.required = True  # Ensure that a sub-command is required

    # Sub-command 'build'
    parser["build"] = subparsers.add_parser("build", help="Generates and also builds the image using 'docker build'")
    parser["build"].add_argument(
        "-c", type=str, metavar="YAML_CONFIG", help="Provide the Dockerfile configuration .yaml file"
    )
    parser["build"].add_argument(
        "-e",
        type=str,
        metavar="CONFIG_NAME",
        help='Choose an existing pre-configuration. Check with "turludock which presets"',
    )
    parser["build"].add_argument(
        "--tag", type=str, metavar="TAG", help='Name and optionally a tag (format: "name:tag")'
    )
    parser["build"].add_argument(
        "--no-cache", action="store_true", default=False, help="Do not use cache when building the image"
    )
    parser["build"].add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Shows the complete docker build output"
    )
    parser["build"].add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug mode")

    # Sub-command 'generate'
    parser["gen"] = subparsers.add_parser(
        "generate",
        help="Generates the Dockerfile and the required assets for manual build. " "Overwrites existing files!",
    )
    parser["gen"].add_argument(
        "-c", type=str, metavar="YAML_CONFIG", help="Provide the Dockerfile configuration .yaml file"
    )
    parser["gen"].add_argument(
        "-e",
        type=str,
        metavar="CONFIG_NAME",
        help='Choose an existing pre-configuration. Check with "turludock which presets"',
    )
    parser["gen"].add_argument(
        "path",
        type=str,
        help="The directory path where the Dockerfile and its assets should be generated. "
        "Contents will be overwritten!",
    )
    parser["gen"].add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug mode")

    # Sub-command 'which'
    parser["which"] = subparsers.add_parser("which", help="List available pre-configurations for generating ROS images")

    which_parsers = parser["which"].add_subparsers(dest="which")

    # Sub-command 'which presets'
    parser["wpre"] = which_parsers.add_parser(
        "presets", help="List available pre-configurations for directly generating ROS images"
    )
    parser["wpre"].add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug mode")
    # Sub-command 'which ros'
    parser["wros"] = which_parsers.add_parser("ros", help="List supported ROS versions")
    parser["wros"].add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug mode")
    # Sub-command 'which cuda'
    parser["wnv"] = which_parsers.add_parser("cuda", help="List supported CUDA/cuDNN versions for a given ROS version")
    parser["wnv"].add_argument("ros_codename", type=str, help="ROS codename string, e.g. noetic")
    parser["wnv"].add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug mode")

    # Parse arguments
    args = parser["main"].parse_args()

    # Check them before returning
    try:
        check_arguments(args)
        return args, True
    except ValueError as e:
        logger.error(f"{e}")
        print_command_help(args, parser)
        return args, False
