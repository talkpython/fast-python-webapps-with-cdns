from pathlib import Path
from typing import Optional

import flask
from flask import Request

from infrastructure import request_dict, cache_buster

root_folder = Path(__file__).parent.parent.parent
file_hashes = {}


def build_cache_id(resource_file: str) -> str:
    if not resource_file:
        return "ERROR_NO_FILE_PROVIDED"

    return cache_buster.build_cache_id(resource_file, False, file_hashes, root_folder.as_posix(), True)


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')
        self.is_htmx_request = 'HX-Request' in flask.request.headers

        self.error: Optional[str] = None
        self.view_model = self.to_dict()
        self.build_cache_id = build_cache_id

    def to_dict(self):
        return self.__dict__
