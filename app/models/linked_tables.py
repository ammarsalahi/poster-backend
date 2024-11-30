# from sqlalchemy import Table,Column,ForeignKey,UUID
# from db import Base


# #user relation tables

# user_posts=Table(
#     'user_posts',Base.metadata,
#     Column('users_id',UUID,ForeignKey('users.id')),
# 	Column('posts_id',UUID,ForeignKey('posts.id'))
# )
# user_stories=Table(
#     'user_stories',Base.metadata,
#     Column('users_id',UUID,ForeignKey('users.id')),
# 	Column('stories_id',UUID,ForeignKey('stories.id'))
# )

# user_comments=Table(
#     'user_comments',Base.metadata,
#     Column('users_id',UUID,ForeignKey('users.id')),
# 	Column('comments_id',UUID,ForeignKey('comments.id'))
# )



# #post ...

# post_comments=Table(
#     'post_comments',Base.metadata,
#     Column('posts_id',UUID,ForeignKey('posts.id')),
# 	Column('comments_id',UUID,ForeignKey('comments.id'))
# )

# post_medias=Table(
#     'post_medias',Base.metadata,
#     Column('posts_id',UUID,ForeignKey('posts.id')),
# 	Column('medias_id',UUID,ForeignKey('media.id'))
# )

# post_liked_user=Table(
#     'post_liked_user',Base.metadata,
#     Column('posts_id',UUID,ForeignKey('posts.id')),
# 	Column('users_id',UUID,ForeignKey('users.id'))    
# )

# #Comment
# comment_liked_user=Table(
#     'comment_liked_user',Base.metadata,
#     Column('comments_id',UUID,ForeignKey('comments.id')),
# 	Column('users_id',UUID,ForeignKey('users.id'))    
# )


# #Story
# story_liked_user=Table(
#     'story_liked_user',Base.metadata,
#     Column('stories_id',UUID,ForeignKey('stories.id')),
# 	Column('users_id',UUID,ForeignKey('users.id'))    
# )
from sqlmodel import SQLModel,Field
from uuid import UUID


class UserPostLink(SQLModel,table=True):
    post_id:UUID | None = Field(default=None,foreign_key='post.id',primary_key=True)
    user_id:UUID | None = Field(default=None,foreign_key='user.id',primary_key=True)


class UserCommentLink(SQLModel,table=True):
    comment_id:UUID | None = Field(default=None,foreign_key='comment.id',primary_key=True)
    user_id:UUID | None = Field(default=None,foreign_key='user.id',primary_key=True)

class UserStoryLink(SQLModel,table=True):
    story_id:UUID | None = Field(default=None,foreign_key='story.id',primary_key=True)
    user_id:UUID | None = Field(default=None,foreign_key='user.id',primary_key=True)