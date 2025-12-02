from pydantic import BaseModel
from schemas.pydantic_mixins.song_mixin import SongMixin
from schemas.pydantic_mixins.playlists_schema import PlaylistMixin


class UsersPlaylistsSchema(
    PlaylistMixin,
    BaseModel
):
    songs: list[SongMixin] | None
    
    model_config = {
        "from_attributes": True
    }