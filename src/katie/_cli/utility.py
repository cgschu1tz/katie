import argparse
import configparser
import importlib
import logging
import pathlib
import pkgutil
import sys
import textwrap
import typing
import webbrowser

from .. import error
from .. import judges

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

def init_root_logger(logging_level: int, **kwargs):
    logging.basicConfig(level=logging_level)

def identify_problem(url: str):
    for module_info in pkgutil.iter_modules(
        judges.__path__, prefix=judges.__name__ + "."
    ):
        try:
            module = importlib.import_module(module_info.name)
            return module.Problem(url)
        except error.NotMyProblemError:
            pass
    raise ValueError


def nearest(pattern: str) -> typing.Optional[pathlib.Path]:
    """Search for a file in the current working directory and its 
    parent directories (traversed upwards).

    If multiple files match `pattern` in a single directory,
    only one is returned (essentially at random).

    :param pattern: a glob-style pattern
    :return: nearest file that matches `pattern`
    """
    search = pathlib.Path.cwd().resolve()

    while search.parent != search:
        for match in search.glob(pattern):
            return match
        search = search.parent

    # Don't forget the root directory.
    for match in search.glob(pattern):
        return match
