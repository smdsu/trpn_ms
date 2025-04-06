from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class STronAddress(BaseModel):
    model_config = ConfigDict(from_attributes=True)    
    id: int | None = Field(None, description="ID")
    address: str | None = Field(None, description="TRON wallet address")
    bandwidth: int = Field(..., description="Bandwidth")
    energy: int = Field(..., description="Energy")
    balance: float = Field(..., description="Balance")
    created_at: datetime | None = Field(None, description="Created at")
    updated_at: datetime | None = Field(None, description="Updated at")
