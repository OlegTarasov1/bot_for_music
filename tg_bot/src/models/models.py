from models.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger, String
from datetime import datetime


class UsersBase(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key = True)
    username: Mapped[str | None] = mapped_column(String(255), nullable = True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable = True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable = True)
    chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable = True)
    is_admin: Mapped[bool] = mapped_column(default = False)

    playlists: Mapped[list["PlaylistsBase"]] = relationship(back_populates = "user")
    favorite_tracks: Mapped[list["SongsBase"]] = relationship(
        back_populates = "users",
        secondary = "favorite_tracks",
        order_by = "desc(FavoritTracksAssociation.time_added)"
    )


class PlaylistsBase(Base):

    __tablename__ = "playlists"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"))

    user: Mapped["UsersBase"] = relationship(back_populates = "playlists")
    songs: Mapped[list["SongsBase"]] = relationship(
        back_populates = "playlists",
        secondary = "songs_playlists_association",
        order_by = "desc(SongsPlaylistsAssociation.time_added)"
    )


class SongsBase(Base):

    __tablename__ = "songs"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key = True)
    song_title: Mapped[str] = mapped_column(String(255))

    playlists: Mapped[list["PlaylistsBase"]] = relationship(back_populates = "songs", secondary = "songs_playlists_association")
    users: Mapped[list["UsersBase"]] = relationship(back_populates = "favorite_tracks", secondary = "favorite_tracks")

    users_with_favorits: Mapped[list["FavoritTracksAssociation"]] = relationship(back_populates = 'songs')
    playlists_tracks: Mapped[list["SongsPlaylistsAssociation"]] = relationship(back_populates = "song")


# Association tables

class SongsPlaylistsAssociation(Base):

    __tablename__ = "songs_playlists_association"

    id: Mapped[int] = mapped_column(primary_key = True)

    song_id: Mapped[int] = mapped_column(ForeignKey("songs.id", ondelete = "CASCADE"))
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlists.id", ondelete = "CASCADE"))
    time_added: Mapped[datetime] = mapped_column(server_default = func.now(), nullable = False)

    song: Mapped["SongsBase"] = relationship(back_populates = "playlists_tracks")

    __table_args__ = (
        UniqueConstraint("song_id", "playlist_id", name = "song_playlist_connection"),
    )


class FavoritTracksAssociation(Base):
    __tablename__ = "favorite_tracks"

    id: Mapped[int] = mapped_column(primary_key = True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete = "CASCADE"))
    song_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("songs.id", onupdate = "CASCADE"))
    time_added: Mapped[datetime] = mapped_column(server_default = func.now(), nullable = False)

    songs: Mapped["SongsBase"] = relationship(back_populates = "users_with_favorits")

    __table_args__ = (
        UniqueConstraint("song_id", "user_id", name = "song_user_connection"),
    )
