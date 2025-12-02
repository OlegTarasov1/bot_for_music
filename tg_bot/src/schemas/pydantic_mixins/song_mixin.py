from pydantic import BaseModel


class SongMixin(BaseModel):
    id: int
    song_title: str

    model_config = {
        "from_attributes": True
    }