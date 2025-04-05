from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TronAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)    
    id: int
    address: str = Field(..., description="TRON wallet address")
    bandwidth: int = Field(..., description="Bandwidth")
    energy: int = Field(..., description="Energy")
    balance: float = Field(..., description="Balance")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")
