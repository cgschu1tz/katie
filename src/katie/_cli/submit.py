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
        description="Submit `files` to `url`.",
        parents=[utility.common_options]
    )
    parser.add_argument(
        "-c",
        "--certificate",
        default=pathlib.Path.home() / pathlib.Path(".kattisrc"),
        help="a file that some some judges (Kattis) require to login (defaults to `~/.kattisrc`)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Don't prompt before submission.",
    )
    parser.add_argument("-l", "--language")
    parser.add_argument("-m", "--main-class")
    parser.add_argument("url")
    parser.add_argument("files", metavar="file", nargs="+", type=pathlib.Path)

    args = parser.parse_args()
    kwargs = vars(args)
    utility.init_root_logger(args.logging_level)
    positive_replies = ["y", "yes"]
    problem = utility.identify_problem(args.url)
    if args.force or input("Submit? [yN] ").lower() in positive_replies:
        verdict = problem.submit(**kwargs)
        print(verdict)
        webbrowser.open(verdict)
