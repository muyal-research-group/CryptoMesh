from cryptomesh.db import get_collection

class MongoRepository:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name  # Se guarda el nombre de la colección
        self.collection = None  # Inicializamos la variable de la colección

    async def init_collection(self):
        """Inicializa la colección de forma asíncrona"""
        self.collection = await get_collection(self.collection_name)

    async def insert_one(self, data: dict):
        """Inserta un documento en la colección"""
        if self.collection is None:
            await self.init_collection()
        await self.collection.insert_one(data) 

    async def find_all(self):
        """Obtiene todos los documentos de la colección y convierte ObjectId a str"""
        if self.collection is None:
            await self.init_collection()
        results = await self.collection.find().to_list(length=100)
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])  # convierte ObjectId a string
        return results

    async def create_index(self, field: str):
        """Crea un índice en un campo específico"""
        if self.collection is None:
            await self.init_collection()
        await self.collection.create_index(field)


