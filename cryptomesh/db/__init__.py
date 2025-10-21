import os
from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorCollection
from typing import Optional
import cryptomesh.config as config


client = None

# Get the MongoDB client and database instance
def get_database(db_name:Optional[str] = None):
    _db_name = db_name if db_name else config.CRYPTOMESH_MONGO_DATABASE_NAME 
    global client
    return  client[_db_name] if client else None 

def get_client():
    global client
    return client

def get_collection(name:str)->AsyncIOMotorCollection:
    db =  get_database()
    return db[name] if not db is None else None 
# Startup event to initialize the MongoClient when the application starts
async def connect_to_mongo(uri:Optional[str]= None):
    _uri = uri if uri else config.CRYPTOMESH_MONGODB_URI
    global client
    client = AsyncIOMotorClient(_uri)

# Shutdown event to close the MongoClient when the application shuts down
async def close_mongo_connection():
    global client
    client.close()