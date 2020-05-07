import argparse
import configparser
import importlib
import logging
import pathlib
import sys
import textwrap
import typing
import webbrowser

from . import utility


def main():
    parser = argparse.ArgumentParser(
        description="Download static tests from `url` to `directory`.",
        parents=[utility.common_options],
    )
    parser.add_argument(
        "-o",
        default=pathlib.Path.cwd(),
        dest="dest",
        metavar="directory",
        type=pathlib.Path,
        help="destination folder (defaults to current working directory)",
    )
    parser.add_argument("url")

    args = parser.parse_args()
    utility.init_root_logger(args.logging_level)

    problem = utility.identify_problem(args.url)
    problem.download_tests().extractall(args.dest)
