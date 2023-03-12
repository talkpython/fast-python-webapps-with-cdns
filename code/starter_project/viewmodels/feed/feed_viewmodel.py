from typing import List

from models.video_model import Video
from services import video_service
from viewmodels.shared.viewmodelbase import ViewModelBase


class FeedViewModel(ViewModelBase):
    def __init__(self, page_size: int, page: int = 1):
        super().__init__()

        self.page_size = page_size
        self.page = page

        count = video_service.video_count()
        start = (page - 1) * page_size
        end = start + page_size

        self.videos: List[Video] = video_service.all_videos(page, page_size)
        self.has_more_videos = count > end
