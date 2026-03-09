from pydantic import BaseModel, ConfigDict


class UserMixin(BaseModel):

    id: int
    username: str | None = None
    first_name: str| None = None
    last_name: str | None = None
    chat_id: int
    is_admin: bool = False
    is_active: bool = True
    source: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )