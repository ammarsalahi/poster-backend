import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *


@pytest.mark.asyncio
async def test_list_stories(test_stories,get_Header,override_get_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        response = await client.get("/stories/?limit=10&offset=0",headers=get_Header)
        assert response.status_code ==200

        #without query paramerters
        wo_response = await client.get("/stories/",headers=get_Header)
        assert wo_response.status_code ==200

        #without auth 
        auth_response = await client.get("/stories/")
        assert auth_response.status_code ==401


@pytest.mark.asyncio
async def test_info_stories(test_stories,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id=test_stories[0].id
        response = await client.get(f"/stories/info/{id}",headers=get_Header_admin)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/stories/info/pppp",headers=get_Header_admin)
        assert invalid_response.status_code ==422

        #without auth 
        auth_response = await client.get(f"/stories/info/{id}")
        assert auth_response.status_code ==401


@pytest.mark.asyncio
async def test_detail_stories(test_stories,get_Header,override_get_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id=test_stories[0].story_id
        response = await client.get(f"/stories/{id}",headers=get_Header)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/stories/kkkk",headers=get_Header)
        assert invalid_response.status_code ==404

        #without auth 
        auth_response = await client.get(f"/stories/{id}")
        assert auth_response.status_code ==401



@pytest.mark.asyncio
async def test_create_story(get_Header, override_get_db, monkeypatch):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
  
        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)

        valid_data = {
            "story_type": "public",
        }
        files = {
            "media_file": ("test_file.txt", b"file content", "text/plain"),
        }

        response = await client.post(
            "/stories/",
            data=valid_data,
            headers=get_Header,
            files=files,
        )

        assert response.status_code == 200 # Assuming success
        
        # Test creating a post without any files (should return 400)
        no_files_response = await client.post(
            "/stories/",
            data=valid_data,
            headers=get_Header,
        )
        assert no_files_response.status_code == 422
        # assert no_files_response.json() == {"detail": "No files were provided for upload."}

        # Test creating a post without authentication
        noauth_response = await client.post(
            "/stories/",
            data=valid_data,
            files=files,
        )
        assert noauth_response.status_code == 401


@pytest.mark.asyncio
async def test_update_story(test_stories,get_Header_admin, override_get_db, monkeypatch):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
  
        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)

        valid_data = {
            "story_type": "public",
        }
        files = {
            "media_file": ("test_file.txt", b"file content", "text/plain"),
        }
        

        id=test_stories[0].story_id
        response = await client.patch(
            f"/stories/{id}",
            data=valid_data,
            headers=get_Header_admin,
            files=files,
        )

        assert response.status_code == 200 # Assuming success
        
        # Test creating a post without any files (should return 400)
        no_files_response = await client.patch(
            f"/stories/{id}",
            data=valid_data,
            headers=get_Header_admin,
        )
        assert no_files_response.status_code == 422
        # assert no_files_response.json() == {"detail": "No files were provided for upload."}

        # Test creating a post without authentication
        noauth_response = await client.post(
            f"/stories/{id}",
            data=valid_data,
            files=files,
        )
        assert noauth_response.status_code == 405






@pytest.mark.asyncio
async def test_post_delete(session,test_stories, get_Header_admin,get_Header, override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # Valid post ID deletion
        
        
        id= test_stories[0].story_id
        response = await client.delete(f"/stories/{id}",headers=get_Header_admin)
        assert response.status_code==204

        #no auth 
        noauth_response = await client.delete(f"/stories/{id}")
        assert noauth_response.status_code ==401

        #no allow 
        noallow_response = await client.delete(f"/stories/{id}",headers= get_Header)
        assert noallow_response.status_code ==405 or 404