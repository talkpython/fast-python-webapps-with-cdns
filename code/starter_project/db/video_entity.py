from sqlmodel import Field, SQLModel


class Video(SQLModel, table=True):
    __tablename__ = 'videos'

    id: str = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    url: str = Field(nullable=False, index=True)
    author: str = Field(nullable=False)
    views: int = Field(default=0, index=True)
    has_thumbnail: bool = Field(default=False)
