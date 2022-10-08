export enum playSources {
  playlist,
  album,
  search,
  folder,
}

export enum NotifType {
  Success,
  Info,
  Error,
}

export enum FromOptions {
  playlist = "playlist",
  folder = "folder",
  album = "album",
  search = "search",
}

export enum ContextSrc {
  PHeader = "PHeader",
  Track = "Track",
  AHeader = "AHeader",
  FHeader = "FHeader",
}

export enum Routes {
  home = "Home",
  folder = "FolderView",
  playlists = "PlaylistList",
  playlist = "PlaylistView",
  albums = "AlbumsView",
  album = "AlbumView",
  artists = "ArtistsView",
  settings = "SettingsView",
  search = "SearchView",
  queue = "QueueView",
}

export const FuseTrackOptions = {
  keys: [
    { name: "title", weight: 1 },
    { name: "album", weight: 0.7 },
    { name: "artists", weight: 0.5 },
    { name: "albumartist", weight: 0.25 },
  ],
};

export enum contextChildrenShowMode {
  click = "click",
  hover = "hover",
}
