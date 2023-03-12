from typing import List

import more_itertools

from db.category_entity import Category
from services import video_service
from viewmodels.shared.viewmodelbase import ViewModelBase


class CategoryViewModel:
    def __init__(self, category: Category):
        super().__init__()

        self.id = category.id
        self.category = category
        self.title = category.title
        self.image = category.image
        self.videos = video_service.videos_for_category(category.id)


class IndexViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()

        self.categories: List[Category] = video_service.all_categories()
        self.rows = [
            [CategoryViewModel(c) for c in row]
            for row in more_itertools.chunked(self.categories, 3)
        ]
