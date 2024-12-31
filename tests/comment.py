import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import session,test_comments,BASE_URL


@pytest.mark.asyncio
async def test_list_comments(test_comments,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        response = await client.get("/comments/?limit=10&offset=0",headers=get_Header)
        assert response.status_code ==200
        
        #without query paramerters
        wo_response = await client.get("/comments/",headers=get_Header)
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
        assert invalid_response.status_code ==200

        auth_response = await client.get(f"/comments/{id}")
        assert auth_response.status_code ==401        