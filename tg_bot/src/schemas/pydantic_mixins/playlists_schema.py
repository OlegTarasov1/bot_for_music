from pydantic import BaseModel, ConfigDict


class PlaylistMixin(BaseModel):

    id: int
    title: str | None = None
    user_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )