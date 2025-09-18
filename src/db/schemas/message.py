from pydantic import BaseModel, ConfigDict
from uuid import UUID

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class MessageSchema(MessageBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)