import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.models import *
from .depends import session,test_messages,BASE_URL


# @pytest.mark.asyncio
# async def test_list_messages(test_notifications):
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url=BASE_URL) as client:
#         response = await client.get("/messages/?limit=10&offset=0")
#         assert response.status_code == 200
#         data = response.json()
#         assert len(data) <= len(test_messages)

#         wo_response = await client.get("/messages/")
#         assert wo_response.status_code ==200
#         data = wo_response.json()
#         assert len(data) <= len(test_messages)