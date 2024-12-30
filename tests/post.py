import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_list_post():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/api/v1/posts"
    ) as ac:
        response = await ac.get("/")
    print(response.text)
    assert response.status_code == 200
    # assert response.json() == {"message": "Tomato"}
