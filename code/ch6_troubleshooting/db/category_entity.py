from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = 'categories'

    id: str = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    image: str


class VideosToCategories(SQLModel, table=True):
    __tablename__ = 'videos_categories'

    video_id: str = Field(nullable=False, primary_key=True)
    category_id: str = Field(nullable=False, primary_key=True)
