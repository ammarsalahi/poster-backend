import pytest 
from httpx import ASGITransport,AsyncClient
from app.main import app
from app.models import *
from .depends import session,test_settings,BASE_URL


@pytest.mark.asyncio
async def test_list_settings(test_settings,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        response = await client.get("/settings/?limit=10&offset=0",headers=get_Header)
        assert response.status_code ==200

        #whithout parameters
        wo_response = await client.get("/settings/",headers=get_Header)
        assert wo_response.status_code ==200

        auth_response = await client.get("/settings/")
        assert auth_response.status_code ==401


@pytest.mark.asyncio
async def test_detail_settings(test_settings,get_Header,override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=BASE_URL) as client:
        id=test_settings[0].id
        response = await client.get(f"/settings/{id}",headers=get_Header)
        assert response.status_code ==200

        #invalid
        invalid_response = await client.get("/settings/mio",headers=get_Header)
        assert invalid_response.status_code ==200

        auth_response = await client.get(f"/settings/{id}")
        assert auth_response.status_code ==401