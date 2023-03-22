from typing import List

from pydantic import BaseModel

from import_models.video_model import Video


class Category(BaseModel):
    category: str
    image: str
    videos: List[Video]
