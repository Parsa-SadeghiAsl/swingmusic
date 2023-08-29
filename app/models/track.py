from dataclasses import dataclass

from app.settings import SessionVarKeys, get_flag
from app.utils.hashing import create_hash
from app.utils.parsers import (
    clean_title,
    get_base_title_and_versions,
    parse_feat_from_title,
    remove_prod,
    split_artists,
)

from .artist import ArtistMinimal


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    album: str
    albumartists: str | list[ArtistMinimal]
    albumhash: str
    artists: str | list[ArtistMinimal]
    bitrate: int
    copyright: str
    date: int
    disc: int
    duration: int
    filepath: str
    folder: str
    genre: str | list[str]
    title: str
    track: int
    trackhash: str
    last_mod: str | int

    filetype: str = ""
    image: str = ""
    artist_hashes: str = ""
    is_favorite: bool = False

    # temporary attributes
    _pos: int = 0  # for sorting tracks by disc and track number
    _ati: str = ""  # (album track identifier) for removing duplicates when merging album versions

    og_title: str = ""
    og_album: str = ""

    def __post_init__(self):
        self.og_title = self.title
        self.og_album = self.album
        self.last_mod = int(self.last_mod)

        if self.artists is not None:
            artists = split_artists(self.artists)
            new_title = self.title

            if get_flag(SessionVarKeys.EXTRACT_FEAT):
                featured, new_title = parse_feat_from_title(self.title)
                original_lower = "-".join([create_hash(a) for a in artists])
                artists.extend(
                    [a for a in featured if create_hash(a) not in original_lower]
                )

            if get_flag(SessionVarKeys.REMOVE_PROD):
                new_title = remove_prod(new_title)

            # if track is a single
            if self.og_title == self.album:
                self.rename_album(new_title)

            if get_flag(SessionVarKeys.REMOVE_REMASTER_FROM_TRACK):
                new_title = clean_title(new_title)

            self.title = new_title

            if get_flag(SessionVarKeys.CLEAN_ALBUM_TITLE):
                self.album, _ = get_base_title_and_versions(
                    self.album, get_versions=False
                )

            if get_flag(SessionVarKeys.MERGE_ALBUM_VERSIONS):
                self.recreate_albumhash()

            self.artist_hashes = "-".join(create_hash(a, decode=True) for a in artists)
            self.artists = [ArtistMinimal(a) for a in artists]

            albumartists = split_artists(self.albumartists)
            self.albumartists = [ArtistMinimal(a) for a in albumartists]

        self.image = self.albumhash + ".webp"

        if self.genre is not None and self.genre != "":
            self.genre = str(self.genre).replace("/", ",").replace(";", ",")
            self.genre = str(self.genre).lower().split(",")
            self.genre = [g.strip() for g in self.genre]

        self.recreate_hash()

    def recreate_hash(self):
        """
        Recreates a track hash if the track title was altered
        to prevent duplicate tracks having different hashes.
        """
        if self.og_title == self.title and self.og_album == self.album:
            return

        self.trackhash = create_hash(
            ", ".join([a.name for a in self.artists]), self.og_album, self.title
        )

    def recreate_artists_hash(self):
        """
        Recreates a track's artist hashes if the artist list was altered
        """
        self.artist_hashes = "-".join(a.artisthash for a in self.artists)

    def recreate_albumhash(self):
        """
        Recreates an albumhash of a track to merge all versions of an album.
        """
        self.albumhash = create_hash(self.album, self.albumartists)

    def rename_album(self, new_album: str):
        """
        Renames an album
        """
        self.album = new_album

    def add_artists(self, artists: list[str], new_album_title: str):
        for artist in artists:
            if create_hash(artist, decode=True) not in self.artist_hashes:
                self.artists.append(ArtistMinimal(artist))

        self.recreate_artists_hash()
        self.rename_album(new_album_title)
