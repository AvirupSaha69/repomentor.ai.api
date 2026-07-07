# RepoMentor API

RepoMentor API is a Python-based REST API built with FastAPI that integrates MongoDB, GitHub API, and Gemini API to analyze repository structures, code quality, and provide developer assistant features.

## Tech Stack
- **Web Framework**: FastAPI (Asynchronous)
- **Database**: MongoDB (using Motor async driver)
- **APIs Integrated**:
  - GitHub REST API
  - Google Gemini API (via Google GenAI SDK)
- **Dependency Management**: pip
- **Testing**: pytest & pytest-asyncio

## Project Structure
```
repomentor-api/
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── requirements.txt          # Python packages
├── app/
│   ├── main.py               # API Entrypoint
│   ├── config.py             # Configuration & Settings
│   ├── api/                  # API Routers & Dependencies
│   │   ├── deps.py           # Dependency Injection
│   │   └── v1/               # Version 1 Router
│   ├── core/                 # DB connections, settings
│   ├── models/               # Pydantic Schemas / DB Models
│   └── services/             # Business Logic / API clients
└── tests/                    # Test Suite
```

## Setup & Installation

### Prerequisites
- Python 3.10+
- MongoDB instance (local or Atlas)
- GitHub Personal Access Token (PAT)
- Google Gemini API Key

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd repomentor.ai.api
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```

5. **Run the API Server**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The API documentation will be available at `http://localhost:8000/docs`.

## Running Tests
Run the test suite using `pytest`:
```bash
pytest
```
