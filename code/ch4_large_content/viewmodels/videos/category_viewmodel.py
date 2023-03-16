from typing import Optional

import more_itertools

from db.category_entity import Category
from services import video_service
from viewmodels.shared.viewmodelbase import ViewModelBase


class CategoryViewModel(ViewModelBase):
    def __init__(self, cat_name: str):
        super().__init__()

        self.cat_name = cat_name
        self.category: Optional[Category] = video_service.category_by_name(cat_name)
        self.rows = []
        self.videos = []
        if self.category:
            self.videos = video_service.videos_for_category(self.category.id)
            self.rows = [
                list(row)
                for row in more_itertools.chunked(self.videos, 3)
            ]
