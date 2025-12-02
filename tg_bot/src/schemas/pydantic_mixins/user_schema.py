from pydantic import BaseModel
from pydantic.types import AnyType

class UserMixin(BaseModel):

    id: int | None
    username: str | None
    first_name: str| None
    last_name: str | None
    chat_id: int | None
    is_admin: bool = False

    model_config = {
        "from_attributes": True
    }