import pytest

from katie.judges import kattis

@pytest.mark.parametrize("url", [
    "https://open.kattis.com/problems/2048",
    "https://maps20.kattis.com/problems/buriedtreasure/",
    "https://maps20.kattis.com/problems/maps20.schoolspirit",
    "https://maps20.kattis.com/problems/maps20.schoolspirit/",
    "https://open.kattis.com/contests/t7oaz3/problems/r2",
])
def test_recognized_urls(url: str):
    assert kattis.Problem(url)

@pytest.mark.parametrize("url", [
    "https://open.kattis.com/problems",
    "https://maps20.kattis.com/download/kattisrc",
    "https://maps20.kattis.com/problems/buriedtreasure/submit",
    "https://open.kattis.com/contests",
])
def test_unrecognized_urls(url: str):
    with pytest.raises(ValueError):
        kattis.Problem(url)