import argparse
import configparser
import importlib
import logging
import pathlib
import sys
import textwrap
import typing
import webbrowser

from . import cli
from . import utility


def main():
    parser = argparse.ArgumentParser(
        description="Download tests from URL.", parents=[cli.common_options]
    )
    parser.add_argument(
        "-o",
        default=pathlib.Path.cwd(),
        dest="destination",
        type=pathlib.Path,
        help="destination folder (defaults to current working directory)",
    )
    parser.add_argument("url")

    try:
        args = parser.parse_args()

        logging.basicConfig(level=args.log_level)
        # stderr_handler = logging.StreamHandler(sys.stderr)
        # stderr_handler.setFormatter(logging.Formatter("[%(level)s] %(message)s"))
        # stderr_handler.setLevel(args.log_level)
        # root_logger.addHandler(stderr_handler)

        kwargs = vars(args)
        problem = utility.identify_problem(args.url)
        problem.download_tests().extractall(args.destination)
    except FileNotFoundError as err:
        raise
