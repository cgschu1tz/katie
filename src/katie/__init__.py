import importlib
import logging
import pkgutil

from . import judges

_DEBUG = logging.getLogger(__name__).debug


def identify_problem(url: str):
    """Identify a problem from its URL.

    >>> identify_problem("https://open.kattis.com/problems/2048")
    <katie.judges.kattis.Problem object at 0x...>

    If no judge recognizes ``url``, raise ``ValueError``.
    >>> identify_problem("https://not.a.problem")
    Traceback (most recent call last):
    ...
    ValueError: ...
    """
    for module_info in pkgutil.iter_modules(
        judges.__path__, prefix=judges.__name__ + "."
    ):
        try:
            module = importlib.import_module(module_info.name)
            return module.Problem(url)
        except (AttributeError, ValueError):
            _DEBUG(
                "`%s` did not recognize the URL `%s`.",
                module_info.name,
                url,
                exc_info=True,
            )
    raise ValueError(f"No judge recognized the URL `{url}`.")


__all__ = ["identify_problem"]
