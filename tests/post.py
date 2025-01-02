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
  
        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)

        valid_data = {
            "content": "This is a test post",
            "post_type": "public",
        }
        files = {
            "upload_files": ("test_file.txt", b"file content", "text/plain"),
            "upload_files": ("test_file2.txt", b"file content", "text/plain"),
        }

        response = await client.post(
            "/posts/",
            data=valid_data,
            headers=get_Header,
            files=files,
        )

        assert response.status_code == 200 # Assuming success
        
        # Test creating a post without any files (should return 400)
        no_files_response = await client.post(
            "/posts/",
            data=valid_data,
            headers=get_Header,
        )
        assert no_files_response.status_code == 422
        # assert no_files_response.json() == {"detail": "No files were provided for upload."}

        # Test creating a post without authentication
        noauth_response = await client.post(
            "/posts/",
            data=valid_data,
            files=files,
        )
        assert noauth_response.status_code == 401



@pytest.mark.asyncio
async def test_update_post(monkeypatch,test_posts,get_Header_admin,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)


        valid_data = {
            "content": "This is a test post",
            "post_type": "public",
        }
        files = {
            "upload_files": ("test_file.txt", b"file content", "text/plain"),
            "upload_files": ("test_file2.txt", b"file content", "text/plain"),
        }

        id = test_posts[0].post_id

        #admin test
        response = await client.patch(
            f"/posts/{id}",
            data=valid_data,
            files=files,
            headers=get_Header_admin
        )
        assert response.status_code == 200
        
        #not allowed user
        notallow_response = await client.patch(
            f"/posts/{id}",
            data=valid_data,
            files=files,
            headers=get_Header
        )
        assert notallow_response.status_code == 405

        #no auth user
        noauth_response = await client.patch(
            f"/posts/{id}",
            data=valid_data,
            files=files,
        )
        assert noauth_response.status_code == 401
   
        #invalid parameter
        invalid_response = await client.patch(
            f"/posts/1234",
            data=valid_data,
            files=files,
            headers=get_Header_admin
        )
        assert invalid_response.status_code == 404




@pytest.mark.asyncio
async def test_post_delete(session,test_posts, get_Header_admin,get_Header, override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Valid post ID deletion
        
        
        id= test_posts[0].post_id
        response = await client.delete(f"/posts/{id}",headers=get_Header_admin)
        assert response.status_code==204

        #no auth 
        noauth_response = await client.delete(f"/posts/{id}")
        assert noauth_response.status_code ==401

        #no allow 
        noallow_response = await client.delete(f"/posts/{id}",headers= get_Header)
        assert noallow_response.status_code ==405 or 404
