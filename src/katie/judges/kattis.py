from bs4 import BeautifulSoup
import collections
import zipfile
import configparser
import re
import io
import logging
import pathlib
from urllib.parse import urljoin
import requests
import requests.exceptions
import typing

from .. import errors

_DEBUG = logging.getLogger(__name__).debug
_WARNING = logging.getLogger(__name__).warning


class Problem:
    _HEADERS = {"User-Agent": "kattis-cli-submit"}
    _LANGUAGES = [
        "C",
        "C++",
        "C#",
        "COBOL",
        "F#",
        "Go",
        "Haskell",
        "Java",
        "JavaScript",
        "Kotlin",
        "Common Lisp",
        "Objective-C",
        "OCaml",
        "Pascal",
        "PHP",
        "Prolog",
        "Python 2",
        "Python 3",
        "Ruby",
        "Rust",
        "Scala",
    ]
    _HTTP_TIMEOUT = 10  # seconds

    def __init__(self, url: str):
        m = re.fullmatch(r"https://[^/]+\.kattis\.com/.*problems/([^/]+)/*", url)
        if m:
            self._url = url
            self._id = m.group(1)
        else:
            raise ValueError

    def tests(self) -> zipfile.ZipFile:
        # Since we're making more than one HTTP(S) request, start a session.
        # According to https://requests.readthedocs.io/en/v0.8.2/user/advanced/#keep-alive,
        # this automatically sets Keep-Alive, which saves us the overhead of starting each
        # connection from scratch.
        session = requests.session()
        
        response = session.get(
            self._url, headers=self._HEADERS, timeout=self._HTTP_TIMEOUT
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        test_links = soup.find_all("a", string="Sample data files", limit=2)
        if not test_links:
            raise ValueError("No download URL")
        elif len(test_links) > 1:
            _WARNING("Found more than one download link, so I'm picking the first one I see.")

        _DEBUG("Downloading tests from `{")
        response = session.get(
            urljoin(self._url, test_links[0]["href"]),
            headers=self._HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )
        response.raise_for_status()
        return zipfile.ZipFile(io.BytesIO(response.content))

    def submit(
        self,
        certificate: str,
        files: typing.Iterable[pathlib.Path],
        language: str,
        main_class: str,
        **kwargs,
    ) -> str:
        """:return: a URL to the submission page where the results of the
        solution's judgement may be viewed
        """
        if language not in self._LANGUAGES:
            raise ValueError(f"'{language}' is not a supported language.")

        secrets = configparser.ConfigParser()
        with open(certificate) as f:
            secrets.read_file(f)

        data = {"user": secrets["user"]["username"], "script": "true"}

        # This session will save the freshly baked cookies from a
        # successful login so we can submit using the same connection.
        session = requests.session()

        # Certificate must either provide...
        if "password" in secrets["user"]:
            # a password or...
            data["password"] = secrets["user"]["password"]
        elif "token" in secrets["user"]:
            # token.
            data["token"] = secrets["user"]["token"]
        else:
            raise errors.LoginError("Missing password or token")

        _DEBUG(
            "Logging in to `%s` as `%s`", secrets["kattis"]["loginurl"], data["user"]
        )
        response = session.post(
            secrets["kattis"]["loginurl"],
            data=data,
            headers=self._HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )
        response.raise_for_status()

        data = {
            "submit": "true",
            "submit_ctr": 2,
            "language": language,
            "mainclass": main_class or "",
            "problem": self._id,
            "tag": "",  # Kattis developers probably use this for something internally.
            "script": "true",
        }
        files = [
            ("sub_file[]", (file.name, file.read_bytes(), "application/octet-stream"))
            for file in files
        ]

        response = session.post(
            # secrets["kattis"]["submissionurl"],
            self._url + "/submit",
            data=data,
            files=files,
            headers=self._HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )
        response.raise_for_status()
        content = response.content.decode("UTF-8")
        match = re.search(r"Submission ID: (\d+)", content)
        if match:
            return "/".join([secrets["kattis"]["submissionsurl"], match.group(1)])
        else:
            # If the response does not contain a submission ID,
            # it is almost certainly not good news.
            raise errors.SubmissionError(f"Kattis says '{content}'")
