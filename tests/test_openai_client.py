import pytest
import os
from unittest.mock import patch, AsyncMock
from app.openai_client import summarize_text

@pytest.mark.asyncio
@patch.dict(os.environ, {"MOCK_OPENAI": "false"})  # Disable mock mode for this test
@patch('app.openai_client.client.chat.completions.create', new_callable=AsyncMock)
async def test_summarize_text(mock_create):
    # Create a mock response that matches the AsyncOpenAI response structure
    mock_response = AsyncMock()
    mock_response.choices = [
        type('Choice', (), {
            'message': type('Message', (), {
                'content': '• Bullet 1\n• Bullet 2'
            })
        })
    ]
    mock_create.return_value = mock_response
    
    result = await summarize_text("Long content here.")
    assert "Bullet 1" in result 