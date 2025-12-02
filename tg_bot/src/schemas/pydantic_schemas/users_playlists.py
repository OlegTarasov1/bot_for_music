from pydantic import BaseModel
from schemas.pydantic_mixins.user_schema import UserMixin
from schemas.pydantic_mixins.playlists_schema import PlaylistMixin


class UsersPlaylistsSchema(
    UserMixin,
    BaseModel
):
    playlists: list[PlaylistMixin] = []
    
    model_config = {
        "from_attributes": True
    }