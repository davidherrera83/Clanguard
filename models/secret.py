from pydantic import BaseModel

class SecretModel(BaseModel):
    discord_token: str
    channel_id: int
    clash_royale_api_base: str
    clash_royale_token: str