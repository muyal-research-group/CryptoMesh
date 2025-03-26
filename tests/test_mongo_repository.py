import pytest
from cryptomesh.repositories.mongo_repository import MongoRepository
from cryptomesh.db import connect_to_mongo

@pytest.mark.asyncio
async def test_insert_and_find_service():
    await connect_to_mongo()
    repo = MongoRepository("test_services")
    await repo.insert_one({"test": "value"})
    results = await repo.find_all()
    assert any(doc["test"] == "value" for doc in results)
