import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *



@pytest.mark.asyncio
async def test_list_medias(test_medias,get_Header,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        response = await client.get("/medias/?limit=10&offset=0",headers=get_Header_admin)
        assert response.status_code ==200
        
        #without query paramerters
        wo_response = await client.get("/medias/",headers=get_Header_admin)
        assert wo_response.status_code ==200

        #without auth 
        auth_response = await client.get("/medias/")
        assert auth_response.status_code==401


        


@pytest.mark.asyncio
async def test_detail_medias(test_medias,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id=test_medias[0].id
        
        response = await client.get(f"/medias/{id}",headers=get_Header)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/medias/mio",headers=get_Header)
        assert invalid_response.status_code ==422


        auth_response = await client.get(f"/medias/{id}")
        assert auth_response.status_code ==401        



@pytest.mark.asyncio
async def test_create_media(monkeypatch,test_posts,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)
        id = test_posts[0].id

        valid_data={
            "post_id":str(id)
        }
        files={
            "media_file": ("test_file2.txt", b"file content", "text/plain"),
        }

        response = await client.post("/medias/",data=valid_data,files=files,headers=get_Header)
        print(f"details :  {response.text}")
        assert response.status_code == 200

        noauth_response = await client.post("/medias/",data=valid_data,files=files)
        assert noauth_response.status_code ==401
        
        invalid_response = await client.post("/medias/",data=valid_data,headers=get_Header)
        assert invalid_response.status_code ==422


@pytest.mark.asyncio
async def test_update_media(monkeypatch,test_medias,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        async def mock_save_media(upload_file):
            return f"/mock/path/{upload_file.filename}"

        monkeypatch.setattr("app.utils.media.save_media", mock_save_media)

        files={
            "media_file": ("test_file2.txt", b"file content", "text/plain"),
        }

        id=test_medias[0].id
        response = await client.patch(f"/medias/{id}",files=files,headers=get_Header)
        print(f"details :  {response.text}")
        assert response.status_code == 200

        noauth_response = await client.patch(f"/medias/{id}",files=files)
        assert noauth_response.status_code ==401
        
        invalid_response = await client.patch("/medias/123",headers=get_Header)
        assert invalid_response.status_code ==422





@pytest.mark.asyncio
async def test_delete_media(monkeypatch,test_medias,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_medias[0].id 
        response = await client.delete(f"/medias/{id}",headers=get_Header)
        print(f"detailss: {response.text}")
        assert response.status_code == 204