import pytest
from unittest.mock import patch, AsyncMock
from app.openai_client import summarize_text

@pytest.mark.asyncio
@patch('app.openai_client.openai.chat.completions.create', new_callable=AsyncMock)
async def test_summarize_text(mock_create):
    mock_create.return_value.choices = [type('obj', (object,), {'message': type('msg', (object,), {'content': '• Bullet 1\n• Bullet 2'})})]
    result = await summarize_text("Long content here.")
    assert "Bullet 1" in result 