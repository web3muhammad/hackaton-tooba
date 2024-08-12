from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    phone: str
    full_name: str
    thread: int

class CampaignSchema(BaseModel):
    id: int
    goal: int
    collected: int
    title: str
    description: str
    link: str

class Item(BaseModel):
    user_id: int
    campaign_id: int
