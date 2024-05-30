from pydantic import BaseModel

class ConfigModel(BaseModel):
    clanID: str
    days_threshold: int
    donation_threshold: int
    clanChestPoints_threshold: int