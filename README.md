# summary-api

A full-stack FastAPI-based web service for summarizing long-form content (articles, PDFs, transcripts) using OpenAI GPT-4. Stores both the input and summary in a Postgres database.

## Features
- Summarizes long-form content into concise bullet points using GPT-4
- Stores original and summarized content with metadata
- REST API with OpenAPI docs
- Async SQLAlchemy + Postgres
- Dockerized for easy deployment
- GitHub Actions CI/CD for Google Cloud Run

## Summarization Prompt

"Summarize this text in 3-5 concise bullet points that retain key information."

## Quickstart (Docker)

1. Copy `.env.example` to `.env` and fill in values.
2. Run:

```sh
docker-compose up --build
```

App: http://localhost:8000
Docs: http://localhost:8000/docs

## API Contract

### POST /summarize
- **Request:**
  ```json
  { "content": "long text here", "source": "string describing source (e.g., URL, title, etc.)" }
  ```
- **Response:**
  ```json
  { "summary": "...", "id": "...", "created_at": "..." }
  ```

### GET /summaries/{id}
- **Response:**
  ```json
  { "id": "...", "content": "...", "summary": "...", "source": "...", "created_at": "..." }
  ```

## Environment Variables
See `.env.example` for required variables.

## License
MIT 