import pytest

from katie.judges import kattis
from urls import Tag, URLS


@pytest.mark.parametrize("url", URLS[Tag.is_problem])
def test_recognized_urls(url: str):
    assert kattis.Problem(url)


@pytest.mark.parametrize("url", URLS[Tag.all] - URLS[Tag.is_problem])
def test_unrecognized_urls(url: str):
    with pytest.raises(ValueError):
        kattis.Problem(url)
