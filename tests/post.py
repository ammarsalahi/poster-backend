import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.models import *
from .depends import *
from app.core.token import get_current_user


@pytest.mark.asyncio
async def test_list_posts(monkeypatch, test_posts, get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Use the headers returned by the get_Header fixture
        response = await client.get("/posts/?limit=10&offset=0", headers=get_Header)
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= len(test_posts)

        #without parameters 
        wo_response  = await client.get("/posts/",headers=get_Header)
        assert  wo_response.status_code == 200

        #no auth response
        noauth_response = await client.get("/posts/")
        assert noauth_response.status_code == 401



@pytest.mark.asyncio
async def test_detail_post_with_post_id(test_posts,get_Header,override_get_db):
    transport  = ASGITransport(app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        post_id= test_posts[0].post_id
        response = await client.get(f"/posts/{post_id}",headers=get_Header)
        assert response.status_code==200

        invalid_response = await client.get("/post/invalid-id",headers=get_Header)
        assert invalid_response.status_code==404


@pytest.mark.asyncio
async def test_detail_post_info(test_posts,get_Header_admin,override_get_db):
    transport  = ASGITransport(app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id= test_posts[0].id
        response = await client.get(f"/posts/info/{id}",headers=get_Header_admin)
        print(response.text)
        assert response.status_code==200

        invalid_response = await client.get("/post/info/invalid-id",headers=get_Header_admin)
        assert invalid_response.status_code==404


@pytest.mark.asyncio
async def test_create_post(get_Header, override_get_db, monkeypatch):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Use the headers returned by the get_Header fixture
        headers = get_Header

        # Mock the `save_media` function to simulate file uploads
        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.routers.posts.save_media", mock_save_media)

        # Test creating a post with valid data and files
        valid_data = {
            "content": "This is a test post",
            "post_type": "text",
        }
        files = {
            "upload_files": ("test_file.txt", b"file content", "text/plain"),
        }

        response = await client.post(
            "/posts/",
            data=valid_data,
            headers=headers,
            files=files,
        )
        assert response.status_code == 200  # Assuming success
        data = response.json()
        assert data["content"] == valid_data["content"]
        assert data["post_type"] == valid_data["post_type"]
        assert len(data["media_urls"]) == 1  # Check if one file was uploaded

        # Test creating a post without any files (should return 400)
        no_files_response = await client.post(
            "/posts/",
            data=valid_data,
            headers=headers,
        )
        assert no_files_response.status_code == 400
        assert no_files_response.json() == {"detail": "No files were provided for upload."}

        # Test creating a post without authentication
        noauth_response = await client.post(
            "/posts/",
            data=valid_data,
            files=files,
        )
        assert noauth_response.status_code == 401
        assert noauth_response.json() == {"detail": "Not authenticated"}

        # Test creating a post with insufficient permissions
        headers_non_admin = await get_Header_non_admin()  # Simulate another user
        insufficient_permission_response = await client.post(
            "/posts/",
            data=valid_data,
            headers=headers_non_admin,
            files=files,
        )
        assert insufficient_permission_response.status_code == 405
        assert insufficient_permission_response.json() == {"detail": "Method Not Allowed"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Use the headers returned by the get_Header fixture
        headers = get_Header

        # Test creating a valid post
        valid_post_data = {
            "content": "Test Content",
            "post_type": "text"
        }
        response = await client.post("/posts/", json=valid_post_data, headers=headers)
        assert response.status_code == 201  # Assuming the creation endpoint returns 201
        data = response.json()
        assert data["content"] == valid_post_data["content"]
        assert data["post_type"] == valid_post_data["post_type"]

        # Test creating a post without authentication
        noauth_response = await client.post("/posts/", json=valid_post_data)
        assert noauth_response.status_code == 401
        assert noauth_response.json() == {"detail": "Not authenticated"}

        # Test creating a post with invalid data
        invalid_post_data = {
            "content": "",  # Invalid because content is empty
            "post_type": "unsupported_type"  # Assuming this is not a valid type
        }
        invalid_response = await client.post("/posts/", json=invalid_post_data, headers=headers)
        assert invalid_response.status_code == 422  # Assuming validation catches this

@pytest.mark.asyncio
async def test_update_post(test_posts, get_Header, override_get_db, monkeypatch):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Use the headers returned by the get_Header fixture
        headers = get_Header

        # Get the ID of an existing post to update
        post_id = test_posts[0].id

        # Mock the `save_media` function to simulate media uploads
        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.routers.posts.save_media", mock_save_media)

        # Test updating a post with valid data
        update_data = {
            "content": "Updated Content",
            "post_type": "text",
            "views": 123,
            "visible": True,
        }
        files = {
            "upload_files": ("test_file.txt", b"file content", "text/plain")
        }

        response = await client.patch(
            f"/posts/{post_id}",
            data=update_data,
            headers=headers,
            files=files,
        )
        assert response.status_code == 200  # Assuming success
        data = response.json()
        assert data["content"] == update_data["content"]
        assert data["post_type"] == update_data["post_type"]
        assert data["views"] == update_data["views"]
        assert data["visible"] == update_data["visible"]

        # Test updating a post without authentication
        noauth_response = await client.patch(
            f"/posts/{post_id}",
            data=update_data,
            files=files,
        )
        assert noauth_response.status_code == 401
        assert noauth_response.json() == {"detail": "Not authenticated"}

        # Test updating a post with insufficient permissions
        headers_non_admin = await get_Header_non_admin()  # Simulate another user
        insufficient_permission_response = await client.patch(
            f"/posts/{post_id}",
            data=update_data,
            headers=headers_non_admin,
            files=files,
        )
        assert insufficient_permission_response.status_code == 405
        assert insufficient_permission_response.json() == {"detail": "Method Not Allowed"}

        # Test updating a non-existent post
        invalid_response = await client.patch(
            "/posts/invalid-id",
            data=update_data,
            headers=headers,
            files=files,
        )
        assert invalid_response.status_code == 404
        assert invalid_response.json() == {"detail": "Post not found"}


@pytest.mark.asyncio
async def test_post_delete(test_posts, get_Header_admin, override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Valid post ID deletion
        post_id = test_posts[0].id
        # response = await client.delete(f"/posts/{post_id}", headers=get_Header_admin)
        # print(f"Response for valid delete: {response.text}")
        # assert response.status_code == 204 

        # Deleting with an invalid post ID
        # invalid_response = await client.delete("/posts/invalid", headers=get_Header_admin)
        # print(f"Response for invalid delete: {invalid_response.text}")
        # assert invalid_response.status_code == 404
        # assert invalid_response.json() == {"detail": "Post not found"}

        # Deleting without authentication
        wo_response = await client.delete(f"/posts/{post_id}")
        print(f"Response for unauthenticated delete: {wo_response.text}")
        assert wo_response.status_code == 401
        assert wo_response.json() == {"detail": "Not authenticated"}
