import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *


@pytest.mark.asyncio
async def test_list_comments(test_comments,get_Header,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        response = await client.get("/comments/?limit=10&offset=0",headers=get_Header_admin)
        assert response.status_code ==200
        
        #without query paramerters
        wo_response = await client.get("/comments/",headers=get_Header_admin)
        assert wo_response.status_code ==200

        #without auth 
        auth_response = await client.get("/comments/")
        assert auth_response.status_code==401


        


@pytest.mark.asyncio
async def test_detail_comments(test_comments,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_comments[0].id
        
        response = await client.get(f"/comments/{id}",headers=get_Header)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/comments/mio",headers=get_Header)
        print(invalid_response.text)
        assert invalid_response.status_code ==422


        auth_response = await client.get(f"/comments/{id}")
        assert auth_response.status_code ==401        



@pytest.mark.asyncio
async def test_create_comment(monkeypatch,test_posts,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id = test_posts[0].id
        valid_data={
            "content":"comment content",
            "post_id":id
        }

        response = await client.post("/comments/",data=valid_data,headers=get_Header)
        assert response.status_code == 200

        noauth_response = await client.post("/comments/",data=valid_data)
        assert noauth_response.status_code ==401


@pytest.mark.asyncio
async def test_update_comment(monkeypatch,test_comments,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_comments[0].id
        valid_data={
            "content":"hello",
        }
        response = await client.patch(f"/comments/{id}",data=valid_data,headers=get_Header_admin)
        print(f"details: {response.text}")
        assert response.status_code == 200



@pytest.mark.asyncio
async def test_delete_comment(monkeypatch,test_comments,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_comments[0].id 
        response = await client.delete(f"/comments/{id}",headers=get_Header_admin)
        print(f"detailss: {response.text}")
        assert response.status_code == 204