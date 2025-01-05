import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *


@pytest.mark.asyncio
async def test_list_users(monkeypatch,test_users,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        response = await client.get("/users/?limit=10&offset=0",headers=get_Header_admin)
        print(f"error: {response.text}")
        assert response.status_code ==200
        print(response.json())

        #without query paramerters
        wo_response = await client.get("/users/",headers=get_Header_admin)
        assert wo_response.status_code ==200

        noauth_response = await client.get("/users/")
        assert noauth_response.status_code ==401

@pytest.mark.asyncio
async def test_details_users(monkeypatch,test_users,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        username=test_users[0].username

        response = await client.get(f"/users/{username}",headers=get_Header)
        assert response.status_code ==200

        response = await client.get("/users/hello")
        assert response.status_code ==404 or 500

@pytest.mark.asyncio
async def test_search_users(monkeypatch,test_users,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        username=test_users[0].username

        response = await client.get(f"/users/search/?query={username}",headers=get_Header)
        assert response.status_code ==200

        response = await client.get("/users/search/?query=mio",headers=get_Header)
        assert response.status_code ==200
             

@pytest.mark.asyncio
async def test_create_user(monkeypatch,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        valid_data={
            "username":"user2",
            "email":"me@me.com",
            "fullname":"user 1",
            "password":"1234",
            "profile_type":None,
            "profile_image":None
        }

        response = await client.post("/users/",json=valid_data,headers=get_Header_admin)
        assert response.status_code == 200

        invalid_response = await client.post("/users/",headers=get_Header_admin)
        assert invalid_response.status_code == 422

        auth_response = await client.post("/users/",json=valid_data)
        assert auth_response.status_code == 401


@pytest.mark.asyncio
async def test_update_user(test_users,monkeypatch,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        valid_data={
            "username":"user2",
            "email":"me@me.com",
            "fullname":"user 1",
            "password":"1234",
            "profile_type":None,
            "profile_image":None,
            "is_active":None,
            "is_verified":None
        }

        id=test_users[0].id

        response = await client.patch(f"/users/{id}",json=valid_data,headers=get_Header_admin)
        assert response.status_code == 200

        invalid_response = await client.post(f"/users/{id}",headers=get_Header_admin)
        assert invalid_response.status_code == 405

        auth_response = await client.post(f"/users/{id}",json=valid_data)
        assert auth_response.status_code == 405



@pytest.mark.asyncio 
async def test_delete_user(test_users,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id = test_users[0].id 
        response  = await client.delete(f"/users/{id}",headers=get_Header_admin)
        assert response.status_code == 204

        ivalid_response  = await client.delete(f"/users/1234",headers=get_Header_admin)
        assert ivalid_response.status_code == 422

        auth_response  = await client.delete(f"/users/{id}",)
        assert auth_response.status_code == 401
