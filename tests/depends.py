import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.main import app
from app.core.db import Base,get_db
from app.models import *
from app.schemas.response import UserOnlyResponse
import pytest_asyncio
from app.core.token import create_access_token,get_current_user
from datetime import timedelta
import pytest_asyncio


BASE_URL = "http://127.0.0.1:8000/api/v1"

    # Simulate creating a token with the user data
   

# Test Database URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"



# Create Async Engine and Session Maker
engine = create_async_engine(DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

# Fixture for database session
@pytest_asyncio.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def override_get_db(session):
    async def _get_db_override():
        yield session
    app.dependency_overrides[get_db] = _get_db_override


@pytest_asyncio.fixture
async def get_Header(session):
    user = UserModel(username="user123", email="me123@mail.com", password="1234")
    session.add(user)
    await session.commit()
    token_data = {"sub": user.username}  # sub is typically the username in your JWT payload
    token = create_access_token(data=token_data, expires_delta=timedelta(hours=1))
    HEADERS = {"Authorization": f"Bearer {token}"}
    return HEADERS

@pytest_asyncio.fixture
async def get_Header_admin(session):
    user = UserModel(fullname="admin",username="user1234", email="me1234@mail.com", password="1234",is_superuser=True)
    session.add(user)
    await session.commit()
    token_data = {"sub": user.username}  # sub is typically the username in your JWT payload
    token = create_access_token(data=token_data, expires_delta=timedelta(hours=1))
    HEADERS = {"Authorization": f"Bearer {token}"}
    return HEADERS   

# Fixture for creating test posts
@pytest_asyncio.fixture
async def test_posts(session):
    user=UserModel(username="user144",email="me124@mail.com",password="1234")
    session.add(user)
    await session.commit()
    posts = [
        PostModel(content="Post 1", post_type="text",user_id=user.id),
        PostModel(content="Post 2", post_type="image",user_id=user.id),
        PostModel(content="Post 3", post_type="video",user_id=user.id),
    ]
    session.add_all(posts)  # Use add_all for multiple objects
    await session.commit()
    return posts

@pytest_asyncio.fixture
async def test_stories(session):
    user=UserModel(username="user134",email="me124@mail.com",password="1234")
    session.add(user)
    await session.commit()
    stoires=[
        StoryModel(media_file="1.png",story_type="public",user_id=user.id),
        StoryModel(media_file="2.png",story_type="private",user_id=user.id),
        StoryModel(media_file="3.png",story_type="public",user_id=user.id),
    ]
    session.add_all(stoires)  # Use add_all for multiple objects
    await session.commit()
    return stoires


@pytest_asyncio.fixture
async def test_users(session):
    users=[
        UserModel(username="user1",email="me@mail.com",password="1234",fullname="user1"),
        UserModel(username="user2",email="me1@mail.com",password="1234",fullname="user2"),
        UserModel(username="user3",email="me2@mail.com",password="1234",fullname="user3"),

    ]
    session.add_all(users)  # Use add_all for multiple objects
    await session.commit()
    return users

@pytest_asyncio.fixture
async def test_comments(session):
    user=UserModel(username="user4",email="me44@mail.com",password="1234")
    post=PostModel(content="Post 1", post_type="text")
    session.add(user)
    session.add(post)
    await session.flush()
    comments=[
        CommentModel(content="hello",user_id=user.id,post_id=post.id),
        CommentModel(content="hello",user_id=user.id,post_id=post.id),
        CommentModel(content="hello",user_id=user.id,post_id=post.id),
    ]
    session.add_all(comments)  # Use add_all for multiple objects
    await session.commit()
    return comments


@pytest_asyncio.fixture
async def test_settings(session):
    user=UserModel(username="user4",email="me414@mail.com",password="1234")
    user2=UserModel(username="user5",email="me77@mail.com",password="1234")
    session.add_all(user,user2)
    await session.flush()
    setts=[
        SettingsModel(user_id=user.id),
        SettingsModel(user_id=user.id),
    ]
    session.add_all(setts)  # Use add_all for multiple objects
    await session.commit()
    return setts

@pytest_asyncio.fixture
async def test_medias(session):
    post=PostModel(content="Post new", post_type="text")
    session.add(post)
    await session.flush()
    medias=[
        MediaModel(media_file="22.png",post_id=post.id),
        MediaModel(media_file="23.png",post_id=post.id),
        MediaModel(media_file="24.png",post_id=post.id),
        MediaModel(media_file="25.png",post_id=post.id),
    ]
    session.add_all(medias)  # Use add_all for multiple objects
    await session.commit()
    return medias


@pytest_asyncio.fixture
async def test_validations(session):
    validations=[
        ValidationModel(email="me@me.com"),
        ValidationModel(email="me2@me.com"),
        ValidationModel(email="me3@me.com"),
        ValidationModel(email="me4@me.com")
    ]
    session.add_all(validations)  # Use add_all for multiple objects
    await session.commit()
    return validations


@pytest_asyncio.fixture
async def test_messages(session):
    user=UserModel(username="user4",email="me414@mail.com",password="1234")
    user2=UserModel(username="user5",email="me77@mail.com",password="1234")
    messages=[
        MessageModel(content="hello",send_user_id=user.id,recieve_user_id=user2.id),
        MessageModel(content="hi",send_user_id=user2.id,recieve_user_id=user.id),
    ]
    session.add_all(messages)  # Use add_all for multiple objects
    await session.commit()
    return messages


@pytest_asyncio.fixture
async def test_notifications(session):
    user=UserModel(username="user44",email="me88@mail.com",password="1234")
    user2=UserModel(username="user55",email="me99@mail.com",password="1234")

    notifications=[
        NotificationModel(
            action_type="like",
            content_type="post",
            user_id=user.id,
            action_user_id=user2.id
        ),
        NotificationModel(
            action_type="like",
            content_type="story",
            user_id=user.id,
            action_user_id=user2.id
        ),
        NotificationModel(
            action_type="like",
            content_type="comment",
            user_id=user2.id,
            action_user_id=user.id
        ),
    ]
    session.add_all(notifications)  # Use add_all for multiple objects
    await session.commit()
    return notifications