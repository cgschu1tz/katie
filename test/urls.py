import enum


class Tag(enum.Enum):
    (all, is_problem) = range(2)


_URLS = {
    "https://open.kattis.com/problems": [],
    "https://maps20.kattis.com/download/kattisrc": [],
    "https://maps20.kattis.com/problems/buriedtreasure/submit": [],
    "https://open.kattis.com/contests": [],
    "https://open.kattis.com/problems/2048": [Tag.is_problem],
    "https://maps20.kattis.com/problems/buriedtreasure/": [Tag.is_problem],
    "https://maps20.kattis.com/problems/schoolspirit": [Tag.is_problem],
    "https://maps20.kattis.com/problems/schoolspirit/": [Tag.is_problem],
    "https://open.kattis.com/contests/t7oaz3/problems/r2": [Tag.is_problem],
}

URLS = {}
for tag in Tag:
    if tag == Tag.all:
        # Save us from having to tag every URL with ``Tag.all``.
        URLS[tag] = set(_URLS.keys())
    else:
        URLS[tag] = set(k for k, v in _URLS.items() if tag in v)

__all__ = ["Tag", "URLS"]
