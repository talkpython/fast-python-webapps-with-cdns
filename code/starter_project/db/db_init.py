from pathlib import Path

from sqlalchemy import func
from sqlmodel import create_engine, SQLModel, Session, select

# noinspection PyUnresolvedReferences
from db import video_entity, category_entity
from db.category_entity import Category, VideosToCategories
from db.video_entity import Video
from models.category_model import Category as JsonCategory
from services import json_video_service

has_initialized = False
engine = None


def init():
    global has_initialized, engine

    if has_initialized:
        return
    has_initialized = True

    here = Path(__file__).parent
    sqlite_file_name = here.parent / 'data_file' / "video_collector.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url, echo=False)
    SQLModel.metadata.create_all(engine)


def create_session() -> Session:
    if not engine:
        raise Exception("Must initialize DB first.")

    session = Session(engine)
    session.expire_on_commit = False

    return session


def ensure_data():
    json_video_service.load_data()
    categories: list[JsonCategory] = json_video_service.all_categories()

    with create_session() as session:
        count = session.exec(select([func.count(Category.id)])).one()
        # noinspection PyTypeChecker
        if count > 0:
            print("DB data already imported, skipping.")
            return

        print("Importing data to new SQLite DB...", flush=True)
        added_videos = set()
        for json_cat in categories:
            name = json_cat.category.strip()
            cat = Category(id=name.lower(), title=name, image=json_cat.image.replace(".jpg", ".webp"))
            session.add(cat)

            for json_vid in json_cat.videos:
                if json_vid.id not in added_videos:
                    added_videos.add(json_vid.id)
                    video = Video(id=json_vid.id,
                                  title=json_vid.title,
                                  url=json_vid.url,
                                  author=json_vid.author,
                                  views=json_vid.views,
                                  has_thumbnail=True)
                    session.add(video)

                video_to_category = VideosToCategories(video_id=json_vid.id, category_id=cat.id)
                session.add(video_to_category)

        print("Committing data to DB...", flush=True)
        session.commit()
