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

## CI/CD and Linting Standards

7. **CI/CD Best Practices**:
   - **Action Pinning**: Pin all third-party GitHub Actions to a full-length commit SHA (40 characters) rather than version tags to guarantee build immutability.
   - **Continuous Delivery Trigger**: Make sure the CD deployment workflow is triggered only after the CI check suite has completed successfully using the `workflow_run` event.
   - **Gitleaks Organizational Check**: The official Gitleaks action requires a license key under GitHub organization accounts. For organization repos, download and run the Gitleaks CLI binary directly in a shell `run` command to bypass licensing checks.
   - **Linter Exclusions**: Always globally exclude `*.md`, `**/*.md`, and `requirements.txt` in `.codacy.yml` to prevent non-code files from causing AST parsing errors or blocking builds on documentation style checks.

8. **Python Code Quality & Formatting**:
   - **PEP 8 Spacing**: Strictly maintain exactly 2 blank lines before and after all class/method/router definitions in Python files.
   - **Docstring Standards**: Format multi-line docstring summaries to start directly on the first line (PEP 257 / D212 format). To resolve conflicts with D203 and D213, keep D203 and D213 ignored in the project's linter configuration files (`setup.cfg`, `.flake8`, `.pydocstyle`, `.prospector.yaml`).
   - **Unused Arguments**: Rename unused parameters to prefixed arguments (e.g. `_arg`) or use pylint ignore comments (e.g., `# pylint: disable=unused-argument` on lifespans) to ensure the pylint score remains a perfect 10.00/10.
   - **Local Host Bindings**: When writing configuration presets, default to binding the web servers to localhost (`127.0.0.1`) instead of all interfaces (`0.0.0.0`) to avoid security scanning warnings.
   - **Exception Reraising**: Use a plain `raise` instead of `raise e from e` when catching and re-throwing the same exception object to avoid redundant self-chaining.
