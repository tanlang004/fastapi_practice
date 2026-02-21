# FastAPI Practice Project - AI Agent Instructions

## Project Overview
A minimal FastAPI practice project demonstrating basic HTTP API patterns. Single-file application served by Uvicorn.

**Tech Stack:** FastAPI 0.129.0, Pydantic 2.12.5, Uvicorn 0.41.0, Python 3.x

## Architecture & Structure

### Single-File Design
- **[main.py](../main.py)** - Complete application (one FastAPI instance with routes)
  - Pattern: Simple async route handlers using decorator syntax
  - No separate business logic layer; routes directly return responses

### Key Dependencies
- **FastAPI** - Web framework with automatic OpenAPI/Swagger docs
- **Pydantic** - Request/response validation via type hints
- **Uvicorn** - ASGI server runner with hot-reload support
- **python-dotenv** - Environment variable loading (setup available, not currently used)

## Development Workflows

### Starting the Server
```bash
# Development server with auto-reload
uvicorn main:app --reload

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- Automatically generated from route type hints

## Code Patterns & Conventions

### Route Definition
```python
@app.get('/path')
async def handler_name():
    return {"key": "value"}
```
- Use `async def` for all handlers (Pydantic v2 convention)
- Path operations return dicts; Pydantic automatically serializes to JSON
- Route names should reflect action (e.g., `root`, `get_users`)

### Response Format
- Currently returns plain dicts - upgrade to Pydantic models for validation
- Example upgrade path:
  ```python
  from pydantic import BaseModel
  
  class MessageResponse(BaseModel):
      message: str
  
  @app.get('/', response_model=MessageResponse)
  async def root() -> MessageResponse:
      return MessageResponse(message="hello world")
  ```

## Extension Points

### Adding Endpoints
1. Define Pydantic model for request body (if needed):
   ```python
   class Item(BaseModel):
       name: str
       price: float
   ```
2. Add route handler with appropriate HTTP verb
3. Test via Swagger UI at `/docs`

### Environment Configuration
- `python-dotenv` available in requirements; use `.env` file for secrets/config
- Pattern: `from dotenv import load_dotenv; load_dotenv()`

## Notes for Agents
- This is a learning project - prioritize clarity over premature scaling
- All functionality fits in main.py (no refactoring needed unless requirements grow significantly)
- Pydantic v2 syntax differs from v1 (BaseModel defaults changed) - ensure compatibility
- Hot-reload enabled during development catches most errors immediately
