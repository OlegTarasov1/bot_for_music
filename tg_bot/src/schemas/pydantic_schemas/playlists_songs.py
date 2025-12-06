from pydantic import BaseModel, ConfigDict
from schemas.pydantic_mixins.song_mixin import SongMixin
from schemas.pydantic_mixins.playlists_schema import PlaylistMixin


class PlaylistsSongsSchema(
    PlaylistMixin,
    BaseModel
):
    songs: list[SongMixin | None] | None = None
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )