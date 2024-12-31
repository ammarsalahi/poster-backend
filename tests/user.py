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
async def test_details_users(monkeypatch,test_users,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        username=test_users[0].username

        response = await client.get(f"/users/{username}")
        assert response.status_code ==200

        response = await client.get("/users/hello")
        assert response.status_code ==404

@pytest.mark.asyncio
async def test_search_users(monkeypatch,test_users,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        username=test_users[0].username

        response = await client.get(f"/users/search/?query={username}",headers=get_Header)
        assert response.status_code ==200

        response = await client.get("/users/search/?query=mio",headers=get_Header)
        assert response.status_code ==404
             