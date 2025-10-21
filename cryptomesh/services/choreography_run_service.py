from typing import List
from cryptomesh.dtos.graphChoreography_dto import GraphSpecDTO
from cryptomesh.dtos.graphChoreography_dto import EnrichedNodeDTO, EnrichedGraphSpecDTO, DeploymentInfoDTO
from cryptomesh.repositories.endpoints_repository import EndpointsRepository
from cryptomesh.services.endpoints_services import EndpointsService
from cryptomesh.repositories.security_policy_repository import SecurityPolicyRepository
from cryptomesh.services.security_policy_service import SecurityPolicyService
from shieldx_client import ShieldXClient
from cryptomesh.log.logger import get_logger
from cryptomesh import config
import json

SHIELDX_CLIENT_BASE_URL = config.SHIELDX_CLIENT_BASE_URL
L = get_logger(__name__)


class ChoreographyRunService:
    """Servicio encargado de enriquecer y enviar el grafo a ShieldX para su ejecución."""

    def __init__(self, db, base_url: str = SHIELDX_CLIENT_BASE_URL):
        endpoints_collection = db["endpoints"]
        endpoints_repo = EndpointsRepository(endpoints_collection)
        sp_collection = db["security_policies"]
        sp_repo = SecurityPolicyRepository(sp_collection)
        sp_service = SecurityPolicyService(sp_repo)

        self.db = db
        self.endpoints_repo = endpoints_repo
        self.endpoints_service = EndpointsService(endpoints_repo, sp_service)
        self.client = ShieldXClient(base_url=base_url)


    async def enrich_graph(self, graph: GraphSpecDTO) -> EnrichedGraphSpecDTO:
        """Consulta los endpoints y agrega información de despliegue al grafo."""
        enriched_nodes: List[EnrichedNodeDTO] = []

        for node in graph.vertices:
            deployment_info = None
            if node.rule and node.rule.target and node.rule.target.axo_endpoint_id:
                endpoint_id = node.rule.target.axo_endpoint_id
                try:
                    endpoint = await self.endpoints_service.get_endpoint(endpoint_id)
                    deployment_info = DeploymentInfoDTO(
                        host=endpoint.endpoint_id,
                        req_res_port=endpoint.req_res_port,
                        pubsub_port=endpoint.pubsub_port,
                    )
                    L.debug({
                        "event": "CHOREOGRAPHY.NODE.ENRICHED",
                        "endpoint_id": endpoint_id,
                        "req_res_port": deployment_info.req_res_port,
                        "pubsub_port": deployment_info.pubsub_port,
                    })
                except Exception as e:
                    L.warning({
                        "event": "CHOREOGRAPHY.NODE.SKIPPED",
                        "endpoint_id": endpoint_id,
                        "error": str(e)
                    })

            enriched_nodes.append(
                EnrichedNodeDTO(**node.model_dump(), deployment_info=deployment_info)
            )

        return EnrichedGraphSpecDTO(vertices=enriched_nodes, edges=graph.edges)

    async def send_to_shieldx(self, enriched_graph: EnrichedGraphSpecDTO):
        """Envía el grafo enriquecido a ShieldX usando el cliente asíncrono."""
        try:

            response = await self.client.run_choreography(enriched_graph)
            L.info({
                "event": "CHOREOGRAPHY.SENT_TO_SHIELDX",
                "nodes": len(enriched_graph.vertices),
                "status": "ok"
            })
            # print(json.dumps(enriched_graph.model_dump(by_alias=True, exclude_none=True), indent=2))

            return response
        except Exception as e:
            L.error({
                "event": "CHOREOGRAPHY.SHIELDX_ERROR",
                "detail": str(e)
            })
            raise e
