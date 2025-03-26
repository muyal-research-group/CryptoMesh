from cryptomesh.repositories.mongo_repository import MongoRepository
from cryptomesh.services.yaml_parser import load_yaml

class MongoService:
    def __init__(self):
        self.service_repo = MongoRepository("services")
        self.microservice_repo = MongoRepository("microservices")
        self.function_repo = MongoRepository("functions")

    async def store_yaml_in_mongo(self, yaml_path: str):
        """Lee el YAML y lo almacena en MongoDB"""
        policy = load_yaml(yaml_path)

        for service in policy.services.values():  
            service_data = service.model_dump()  
            await self.service_repo.insert_one(service_data)

            for microservice in service.microservices.values(): 
                microservice_data = microservice.model_dump()
                await self.microservice_repo.insert_one(microservice_data)

                for function in microservice.functions.values(): 
                    function_data = function.model_dump()
                    await self.function_repo.insert_one(function_data)

    async def get_services(self):
        return await self.service_repo.find_all()

    async def get_microservices(self):
        return await self.microservice_repo.find_all()

    async def get_functions(self):
        return await self.function_repo.find_all()

    async def create_indexes(self):
        await self.service_repo.create_indexes()
        await self.microservice_repo.create_indexes()
        await self.function_repo.create_indexes()