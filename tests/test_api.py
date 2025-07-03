import pytest
from httpx import AsyncClient
from app.main import app
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
@patch('app.openai_client.summarize_text', new_callable=AsyncMock)
async def test_post_summarize(mock_summarize):
    mock_summarize.return_value = "• Bullet 1\n• Bullet 2"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/summarize", json={"content": "Long text", "source": "test-source"})
        assert resp.status_code == 200
        data = resp.json()
        assert "summary" in data
        assert data["summary"].startswith("•")
        assert "id" in data
        assert "created_at" in data

@pytest.mark.asyncio
@patch('app.db.get_summary_by_id', new_callable=AsyncMock)
async def test_get_summary(mock_get):
    mock_get.return_value = type('obj', (object,), {
        'id': 1,
        'content': 'Long text',
        'summary': '• Bullet 1',
        'source': 'test-source',
        'created_at': '2024-01-01T00:00:00Z',
    })
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/summaries/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == 1
        assert data["summary"].startswith("•") 