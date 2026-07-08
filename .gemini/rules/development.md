# Project Rules - RepoMentor API

## Formatting & Code Quality
- Enforce strict PEP 8 formatting rules.
- Maintain exactly 2 blank lines before/after classes, function definitions, and routes.
- Use explicit type hinting for all function signatures and parameters (e.g. `def my_func(param: str) -> Optional[dict]:`).
- Always import `Optional`, `List`, `Dict`, `Any` from `typing`.
- Keep file paths relative to the root or resolve them relative to the current workspace root (`D:\repomentor.ai.api`).
- Keep code quality rate at 10.00/10 with pylint. Format multi-line docstring summaries to start directly on the first line. Ignore D203 and D213 rules in linter profiles.

## Services & Dependency Injection
- `app/services/github.py` -> Encapsulates all GitHub API interactions.
- `app/services/gemini.py` -> Encapsulates all Gemini AI interactions using `google-genai` SDK. Keep model configuration externalized to the `Settings` class (`settings.GEMINI_MODEL_NAME`).
- `app/services/mongodb.py` -> Encapsulates all MongoDB CRUD operations using `motor`.
- Register new service dependencies inside `app/api/deps.py` to keep endpoint testing modular.

## Command & Environment Control
- Always verify all python code by running tests using `.venv\Scripts\python -m pytest` from the root directory.
- Append new packages to `requirements.txt` when installed, and upgrade packages to their secure releases to prevent vulnerability scans from failing.
- Bound servers to `127.0.0.1` by default rather than `0.0.0.0` in settings configurations.
