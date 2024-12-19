from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core import Base

liked_posts_table = Table(
    "liked_posts",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)
)

liked_stories_table = Table(
    "liked_stories",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("story_id", Integer, ForeignKey("stories.id"), primary_key=True)
)

liked_comments_table = Table(
    "liked_comments",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("comment_id", Integer, ForeignKey("comments.id"), primary_key=True)
)

saved_posts_table = Table(
    "saved_posts",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True)
)

saved_stories_table = Table(
    "saved_stories",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("story_id", Integer, ForeignKey("stories.id"), primary_key=True)
)
