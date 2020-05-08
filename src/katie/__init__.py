import importlib
import logging
import pkgutil

from . import judges

_DEBUG = logging.getLogger(__name__).debug


def identify_problem(url: str):
    # Save us from repeating the URL in every log message.
    _DEBUG("Identifying URL `%s`", url)
    for module_info in pkgutil.iter_modules(
        judges.__path__, prefix=judges.__name__ + "."
    ):
        try:
            module = importlib.import_module(module_info.name)
            return module.Problem(url)
        except (AttributeError, ValueError):
            _DEBUG("`%s` did not recognize the URL.", module_info.name, exc_info=True)
    raise ValueError(f"No judge recognized the URL `{url}`.")


__all__ = ["identify_problem"]
