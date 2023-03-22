from pathlib import Path
from typing import Optional

import flask
from flask import Request

from infrastructure import request_dict, cache_buster

root_folder = Path(__file__).parent.parent.parent
use_cdn = True


def build_cache_id(resource_file: str) -> str:
    return cache_buster.build_cache_id(resource_file, False, root_folder.as_posix(), True)


class ViewModelBase:
    def __init__(self):
        self.request: Request = flask.request
        self.request_dict = request_dict.create('')
        self.is_htmx_request = 'HX-Request' in flask.request.headers

        self.error: Optional[str] = None
        self.view_model = self.to_dict()
        self.build_cache_id = build_cache_id
        self.cdn_prefix = '' if not use_cdn else 'https://video-collector.b-cdn.net'

    def to_dict(self):
        return self.__dict__
