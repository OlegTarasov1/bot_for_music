from pydantic import BaseModel, ConfigDict


class SongMixin(BaseModel):
    id: int
    song_title: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )