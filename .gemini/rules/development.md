# Project Rules - RepoMentor API

## Formatting & Code Quality
- Enforce strict PEP 8 formatting rules.
- Use explicit type hinting for all function signatures and parameters (e.g. `def my_func(param: str) -> Optional[dict]:`).
- Always import `Optional`, `List`, `Dict`, `Any` from `typing`.
- Keep file paths relative to the root or resolve them relative to the current workspace root (`D:\repomentor.ai.api`).

## Services & Dependency Injection
- `app/services/github.py` -> Encapsulates all GitHub API interactions.
- `app/services/gemini.py` -> Encapsulates all Gemini AI interactions using `google-genai` SDK.
- `app/services/mongodb.py` -> Encapsulates all MongoDB CRUD operations using `motor`.
- Register new service dependencies inside `app/api/deps.py` to keep endpoint testing modular.

## Command & Environment Control
- Always verify all python code by running tests using `.venv\Scripts\python -m pytest` from the root directory.
- Append new packages to `requirements.txt` when installed.
