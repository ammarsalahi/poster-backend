import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *


@pytest.mark.asyncio
async def test_list_settings(test_settings,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        response = await client.get("/settings/?limit=10&offset=0",headers=get_Header_admin)
        assert response.status_code ==200

        #whithout parameters
        wo_response = await client.get("/settings/",headers=get_Header_admin)
        assert wo_response.status_code ==200

        #without auth
        auth_response = await client.get("/settings/")
        assert auth_response.status_code ==401


@pytest.mark.asyncio
async def test_detail_settings(test_settings,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id=test_settings[0].id

        response = await client.get(f"/settings/{id}",headers=get_Header_admin)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/settings/mio",headers=get_Header_admin)
        assert invalid_response.status_code ==422

        auth_response = await client.get(f"/settings/{id}")
        assert auth_response.status_code ==401



# @pytest.mark.asyncio
# async def test_user_detail_settings(test_settings,get_Header_admin,override_get_db):
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport,base_url=BASE_URL) as client:


#         response = await client.get("/settings/detail",headers=get_Header_admin)
#         print(f"details: {response.text}")
#         assert response.status_code ==200

        #invalid
        # invalid_response = await client.get("/settings/detail",headers=get_Header_admin)
        # assert invalid_response.status_code ==422

        # auth_response = await client.get(f"/settings/detail")
        # assert auth_response.status_code ==401

@pytest.mark.asyncio 
async def test_create_settings(monkeypatch,test_users,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id = test_users[0].id 

        response = await client.post(
            "/settings/",
            json={"user_id":str(id)},
            headers = get_Header
        )        
        assert response.status_code ==200
        
        invalid_response = await client.post(
            "/settings/",
            headers = get_Header
        )        
        assert invalid_response.status_code ==422

        auth_response = await client.post(
            "/settings/",
            json={"user_id":str(id)},
        )        
        assert auth_response.status_code ==401



@pytest.mark.asyncio 
async def test_update_settings(monkeypatch,test_settings,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id = test_settings[0].id 
        response = await client.patch(
            f"/settings/{id}",
            json={
                "theme":"dark",
                "is_two_factor_auth":True,
            },
            headers = get_Header_admin
        )        
        assert response.status_code ==200   

@pytest.mark.asyncio
async def test_delete_settings(test_settings,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_settings[0].id 
        response =  await client.delete(f"/settings/{id}",headers=get_Header_admin)   
        assert response.status_code ==204         