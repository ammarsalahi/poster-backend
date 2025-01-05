import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import *


@pytest.mark.asyncio 
async def test_list_validations(monkeypatch,get_Header_admin,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        response = await client.get("/validations/?limit=10&offset=0",headers=get_Header_admin)
        assert response.status_code == 200


        wo_response = await client.get("/validations/",headers=get_Header_admin)
        assert wo_response.status_code == 200


        user_response = await client.get("/validations/",headers=get_Header)
        assert user_response.status_code == 405


        auth_response = await client.get("/validations/?limit=10&offset=0")
        assert auth_response.status_code == 401

@pytest.mark.asyncio
async def test_detail_validation(test_validations,get_Header,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client: 

        id=test_validations[0].id 

        response = await client.get(f"/validations/info/{id}",headers=get_Header_admin)
        assert response.status_code ==200

        invalid_response = await client.get(f"/validations/info/123",headers=get_Header_admin)
        assert invalid_response.status_code ==422

        user_response = await client.get(f"/validations/info/{id}",headers=get_Header)
        assert user_response.status_code ==405

        auth_response = await client.get(f"/validations/info/{id}")
        assert auth_response.status_code ==401


@pytest.mark.asyncio
async def test_detail_email_validation(test_validations,get_Header,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client: 

        email=test_validations[0].email 

        response = await client.get(f"/validations/{email}",headers=get_Header)
        assert response.status_code ==200

        invalid_response = await client.get(f"/validations/info/me@mee.com",headers=get_Header)
        assert invalid_response.status_code ==422

        

        auth_response = await client.get(f"/validations/info/{email}")
        assert auth_response.status_code ==401       

@pytest.mark.asyncio
async def test_create_validation(override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client: 


        valid_data={
            "email":"me@me.com"
        }
        response = await client.post(f"/validations/",json=valid_data)
        print(f"details: {response.text}")
        assert response.status_code ==200

        invalid_response = await client.post(f"/validations/")
        assert invalid_response.status_code ==422


@pytest.mark.asyncio
async def test_update_validation(test_validations,get_Header_admin,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client: 


        valid_data={
            "email":"me@me.com",
            "is_verified":True
        }

        id=test_validations[0].id
        response = await client.patch(f"/validations/{id}",json=valid_data,headers=get_Header_admin)
        assert response.status_code ==200

        invalid_response = await client.patch(f"/validations/123",json=valid_data,headers=get_Header_admin)
        assert invalid_response.status_code ==422    

        json_response = await client.patch(f"/validations/{id}",headers=get_Header_admin)
        assert json_response.status_code ==422

        user_response = await client.patch(f"/validations/{id}",json=valid_data,headers=get_Header)
        assert user_response.status_code ==405 

        auth_response = await client.patch(f"/validations/{id}",json=valid_data)
        assert auth_response.status_code ==401       

@pytest.mark.asyncio
async def test_verify_validation(test_validations,session,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client: 


        valid = ValidationModel(
            email="me@me.com"
        )
        session.add(valid)
        await session.commit()

        valid_data={
            "email":"me@me.com",
            "code":str(valid.code)
        }

        not_valid_data={
            "email":"me@mee.com",
            "code":str(valid.code)
        }
        response = await client.post(f"/validations/verify",json=valid_data)
        assert response.status_code ==200

        invalid_response = await client.post("/validations/verify",json=not_valid_data)
        assert invalid_response.status_code ==500   

        json_response = await client.post("/validations/verify")
        assert json_response.status_code ==422


@pytest.mark.asyncio 
async def test_delete_balidation(test_validations,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id = test_validations[0].id 
        response  = await client.delete(f"/validations/{id}",headers=get_Header_admin)
        assert response.status_code == 204

        ivalid_response  = await client.delete(f"/validations/1234",headers=get_Header_admin)
        assert ivalid_response.status_code == 422

        auth_response  = await client.delete(f"/validations/{id}",)
        assert auth_response.status_code == 401
      
