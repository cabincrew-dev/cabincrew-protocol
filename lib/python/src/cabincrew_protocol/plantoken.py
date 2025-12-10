from typing import List, Optional
from pydantic import BaseModel, Field

class PlanArtifactHash(BaseModel):
    name: str
    hash: str
    size: Optional[float] = None

class PlanToken(BaseModel):
    """
    Cryptographic binding between a flight-plan and its subsequent take-off.
    Defined in schemas/draft/plan-token.schema.json
    """
    token: str = Field(..., description="Primary plan token identifier, e.g. SHA256 over all plan artifacts + context.")
    artifacts: List[PlanArtifactHash] = Field(..., description="Per-artifact hashes that contributed to this plan token.")
    engine_id: str = Field(..., description="Engine identity that produced this plan.")
    protocol_version: str = Field(..., description="Engine protocol version used when this plan was produced.")
    workspace_hash: str = Field(..., description="Hash of the workspace state when the plan was created.")
    created_at: str = Field(..., description="Timestamp when the plan was created (RFC3339).")
