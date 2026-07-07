import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_database
from bson import ObjectId

class MockCollection:
    def __init__(self):
        self.documents = []

    async def find_one(self, query):
        email = query.get("email")
        if email:
            for doc in self.documents:
                if doc.get("email") == email.lower():
                    return dict(doc)
        return None

    async def insert_one(self, document):
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = ObjectId()
        self.documents.append(doc)
        
        class InsertOneResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertOneResult(doc["_id"])

class MockDatabase:
    def __init__(self):
        self.collections = {}

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection()
        return self.collections[name]

@pytest.fixture(scope="module", autouse=True)
def mock_db() -> Generator[MockDatabase, None, None]:
    db = MockDatabase()
    app.dependency_overrides[get_database] = lambda: db
    yield db
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """Test client fixture for checking endpoints without starting the ASGI server."""
    with TestClient(app) as c:
        yield c

