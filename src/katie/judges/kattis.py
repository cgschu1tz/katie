import collections
import configparser
import io
import logging
import pathlib
import re
import requests
import requests.exceptions
import typing
import zipfile

from .. import error

_DEBUG = logging.getLogger(__name__).debug

class Problem:
    # Use same headers as official CLI.
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
            raise error.NotMyProblemError

    def tests(self) -> zipfile.ZipFile:
        response = requests.get(
            self._url + "/file/statement/samples.zip",
            headers=self._HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )
        response.raise_for_status()
        return zipfile.ZipFile(io.BytesIO(response.content))

    def _login(self, secrets):
        """Login to Kattis.

        :return: freshly baked cookies
        """
        data = {"user": secrets["user"]["username"], "script": "true"}

        # Certificate must either provide...
        if "password" in secrets["user"]:
            # a password or...
            data["password"] = secrets["user"]["password"]
        elif "token" in secrets["user"]:
            # token.
            data["token"] = secrets["user"]["token"]
        else:
            raise error.LoginError("Missing password or token")

        _DEBUG(
            "Logging in to `%s` as `%s`", secrets["kattis"]["loginurl"], data["user"]
        )
        response = requests.post(
            secrets["kattis"]["loginurl"],
            data=data,
            headers=self._HEADERS,
            timeout=self._HTTP_TIMEOUT,
        )
        response.raise_for_status()
        _DEBUG(response.status_code)
        return response.cookies

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
        cookies = self._login(secrets)

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

        response = requests.post(
            # secrets["kattis"]["submissionurl"],
            self._url + "/submit",
            data=data,
            files=files,
            cookies=cookies,
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
            raise error.SubmissionError(f"Kattis says '{content}'")
