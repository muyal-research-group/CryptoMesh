from fastapi import APIRouter, Depends, HTTPException, status
from cryptomesh.db import get_database
from cryptomesh.dtos.graphChoreography_dto import GraphSpecDTO
from cryptomesh.services.choreography_run_service import ChoreographyRunService
from cryptomesh.log.logger import get_logger


L = get_logger(__name__)
router = APIRouter()

def get_choreography_service(db=Depends(get_database)) -> ChoreographyRunService:
    return ChoreographyRunService(db)

@router.post(
    "/choreography/run",
    summary="Ejecuta una coreografía enriqueciendo el grafo con información de despliegue",
    status_code=status.HTTP_202_ACCEPTED,
)
async def run_choreography(
    graph: GraphSpecDTO, 
    service: ChoreographyRunService = Depends(get_choreography_service)
    # db=Depends(get_database)
):
    """Recibe el grafo lógico, lo enriquece con información de despliegue y lo envía a ShieldX."""

    L.info({"event": "CHOREOGRAPHY.RUN.START", "nodes": len(graph.vertices)})
    try:
        enriched_graph = await service.enrich_graph(graph)
        response = await service.send_to_shieldx(enriched_graph)
        print("RESPONSE SHIELDX:", response)
    except Exception as e:
        L.error({
            "event": "CHOREOGRAPHY.RUN.ERROR",
            "detail": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Error ejecutando coreografía: {str(e)}")

    return {
        "message": "Grafo enriquecido y enviado a ShieldX correctamente",
        "node_count": len(enriched_graph.vertices),
        "shieldx_response": getattr(response, "value", None)
    }

