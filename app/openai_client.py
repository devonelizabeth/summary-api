"""OpenAI GPT-4 client for summarization."""
import os
from openai import AsyncOpenAI

# Initialize the async client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = "Summarize this text in 3-5 concise bullet points that retain key information."

async def summarize_text(content: str) -> str:
    """Summarize the given content using OpenAI GPT-4.

    Args:
        content (str): The long-form text to summarize.
    Returns:
        str: The summary as bullet points.
    """
    if os.getenv("MOCK_OPENAI") == "true":
        return """• This is a mock summary
• Used for development only
• Saves API costs during testing"""
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using GPT-3.5 as it's available on free tier
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": content},
        ],
        max_tokens=400,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip() 