import argparse
import importlib
import logging
import pkgutil
import typing

common_options = argparse.ArgumentParser(add_help=False)
common_options.add_argument(
    "-d",
    "--debug",
    action="store_const",
    const=logging.DEBUG,
    default=logging.INFO,
    dest="logging_level",
    help="print debugging information to standard error",
)


def init_root_logger(logging_level: int):
    logging.basicConfig(level=logging_level)
