# Antigravity Agent Guidelines

This repository is optimized for autonomous development using **Google Antigravity (AGY)**. If you are an AI assistant (or a developer pairing with one), please adhere to the following rules and standards.

## Project Structure & Architecture

This is a FastAPI-based REST API. You must preserve its modular architecture:
- **Application Entrypoint**: [app/main.py](file:///D:/repomentor.ai.api/app/main.py)
- **Configuration & Env Settings**: [app/config.py](file:///D:/repomentor.ai.api/app/config.py)
- **Database Lifecycle**: [app/core/database.py](file:///D:/repomentor.ai.api/app/core/database.py)
- **Routing & Endpoints**: [app/api/v1/](file:///D:/repomentor.ai.api/app/api/v1/)
- **Data Models & Schemas**: [app/models/](file:///D:/repomentor.ai.api/app/models/)
- **Integrations & Business Logic**: [app/services/](file:///D:/repomentor.ai.api/app/services/)

## Agent Execution Rules

1. **Local Virtual Environment**:
   - Always run commands using the local virtual environment: `.venv\Scripts\python` or `.venv\Scripts\pip`.
   - Never install packages globally. If adding packages, make sure they are appended to [requirements.txt](file:///D:/repomentor.ai.api/requirements.txt).

2. **Automated Verification**:
   - Before completing any task or proposing any pull request, run pytest using the virtual environment to ensure the codebase remains healthy:
     ```powershell
     .venv\Scripts\python -m pytest
     ```

3. **Pydantic v2 Best Practices**:
   - Use Pydantic v2 schemas. Avoid deprecated configurations. Always use `ConfigDict` to set options (e.g. `model_config = ConfigDict(populate_by_name=True)`).

4. **Async-First Concurrency**:
   - This API is fully asynchronous. Always write async routes (`async def`) and leverage async functions in the `services/` layer.
   - Use `httpx.AsyncClient` for downstream API requests and `motor.motor_asyncio` for MongoDB database calls.

5. **Error Handling**:
   - Handle all connection timeouts and third-party API errors gracefully. Raise `HTTPException` with appropriate status codes in the routing layer.

6. **Documentation Integrity**:
   - Document any new environment variables in [.env.example](file:///D:/repomentor.ai.api/.env.example).
   - If adding endpoints, ensure they are registered under the `/api/v1` router so they auto-appear in FastAPI OpenAPI Swagger docs.
