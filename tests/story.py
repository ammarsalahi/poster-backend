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
        data = wo_response.json()

        #without auth 
        auth_response = await client.get("/stories/")
        assert wo_response.status_code ==401
        data = wo_response.json()


@pytest.mark.asyncio
async def test_info_stories(test_stories,get_Header_admin,override_get_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:

        id=test_stories[0].id
        response = await client.get("/stories/info/{id}",headers=get_Header_admin)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/stories/info/pppp",headers=get_Header_admin)
        assert invalid_response.status_code ==404

        #without auth 
        auth_response = await client.get("/stories/info/{id}")
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
