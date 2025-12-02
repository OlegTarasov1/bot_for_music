from pydantic import BaseModel


class PlaylistMixin(BaseModel):

    id: int
    title: str
    user_id: int

    model_config = {
        "from_attributes": True
    }