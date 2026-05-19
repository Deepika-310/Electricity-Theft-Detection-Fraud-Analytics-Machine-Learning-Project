from pydantic import BaseModel

class UsageInput(BaseModel):
    consumption: float
    voltage: float 