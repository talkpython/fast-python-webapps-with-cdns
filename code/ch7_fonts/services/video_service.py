from typing import Optional

from sqlalchemy import func
from sqlmodel import select

from db.category_entity import Category, VideosToCategories
from db.db_init import create_session
from db.video_entity import Video


def category_by_name(category: str) -> Optional[Category]:
    if not category or not category.strip():
        return None

    category = category.lower().strip()

    with create_session() as session:
        statement = select(Category).where(Category.id == category)
        category: Optional[Category] = session.exec(statement).one_or_none()

    return category


def all_videos(page: int = 1, page_size: Optional[int] = None) -> list[Video]:
    # noinspection PyUnresolvedReferences
    statement = select(Video).order_by(Video.views.desc())

    if page_size:
        start = page_size * (page - 1)
        statement = statement.offset(start).limit(page_size)

    with create_session() as session:
        videos: list[Video] = session.exec(statement).all()

    return videos


def all_categories() -> list[Category]:
    with create_session() as session:
        # noinspection PyUnresolvedReferences
        statement = select(Category).order_by(Category.title)
        categories: list[Category] = session.exec(statement).all()

    return categories


def video_by_id(video_id: str) -> Optional[Video]:
    if not video_id:
        return None

    # video_id = video_id.lower().strip()

    with create_session() as session:
        statement = select(Video).where(Video.id == video_id)
        video: Optional[Video] = session.exec(statement).one_or_none()

    return video


def search_videos(search_text: str) -> list[Video]:
    results: list[Video] = []

    if not search_text or not search_text.strip():
        return results

    search_text = search_text.lower().strip()

    for v in all_videos():
        text = f"{v.id} {v.title} {v.author}".lower()
        if search_text in text:
            results.append(v)

    return results


def add_video(cat_name: str, youtube_id: str, title: str, author: str, view_count: int):
    if video_by_id(youtube_id):
        return None

    cat = category_by_name(cat_name)
    if not cat:
        return None

    url = f'https://www.youtube.com/watch?v={youtube_id}'

    with create_session() as session:
        v = Video(id=youtube_id, title=title, url=url, author=author, views=view_count)
        video_to_category = VideosToCategories(video_id=v.id, category_id=cat.id)

        session.add(v)
        session.add(video_to_category)

        session.commit()

    return v


def video_count() -> int:
    with create_session() as session:
        count = session.exec(select([func.count(Video.id)])).one()

    # noinspection PyTypeChecker
    return count


def videos_for_category(category_id: str):
    with create_session() as session:
        videos_to_cat = select(VideosToCategories).where(VideosToCategories.category_id == category_id)
        video_ids: list[str] = [vtc.video_id for vtc in session.exec(videos_to_cat)]

        # noinspection PyUnresolvedReferences
        videos = session.query(Video) \
            .filter(Video.id.in_(video_ids)) \
            .order_by(Video.views.desc()) \
            .all()

    return videos
