from pydantic import BaseModel,Field, ValidationInfo, field_validator
from typing import Any, Optional,Dict,List

class RuleTargetDTO(BaseModel):
    alias: str
    axo_bucket_id: str
    axo_endpoint_id: str

class RuleDTO(BaseModel):
    target: RuleTargetDTO

class ParamsDTO(BaseModel):
    init: Optional[Dict[str, str]] = None
    call: Optional[Dict[str, str]] = None

class NodeDTO(BaseModel):
    id: str
    type: str  
    name: Optional[str] = None
    rule: Optional[RuleDTO] = None
    params: Optional[ParamsDTO] = None
    sink_bucket_id: Optional[str] = None

    @field_validator("sink_bucket_id")
    def validate_sink_id(cls, v, info: ValidationInfo):
        """Evita que ActiveObjects incluyan sink_bucket_id por error."""
        node_type = info.data.get("type") if info.data else None
        if node_type == "ActiveObject" and v is not None:
            raise ValueError("sink_bucket_id solo es válido para nodos tipo 'Bucket'")
        return v

class EdgeDTO(BaseModel):
    from_: str = Field(..., alias="from")
    to: str

class GraphSpecDTO(BaseModel):
    vertices: List[NodeDTO]
    edges: List[EdgeDTO] = []




class DeploymentInfoDTO(BaseModel):
    host: str
    req_res_port: int
    pubsub_port: int

class EnrichedNodeDTO(NodeDTO):
    deployment_info: Optional[DeploymentInfoDTO] = None

class EnrichedGraphSpecDTO(BaseModel):
    vertices: List[EnrichedNodeDTO]
    edges: List = []