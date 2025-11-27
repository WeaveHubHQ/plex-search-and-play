"""Constants for the Plex Search and Play integration."""

from typing import Final

# Integration domain
DOMAIN: Final = "plex_search_play"

# Configuration keys
CONF_PLEX_URL: Final = "plex_url"
CONF_PLEX_TOKEN: Final = "plex_token"
CONF_SELECTED_PLAYERS: Final = "selected_players"
CONF_LIBRARIES: Final = "libraries"

# Default values
DEFAULT_PORT: Final = 32400
DEFAULT_SEARCH_LIMIT: Final = 6
DEFAULT_TIMEOUT: Final = 10

# Service names
SERVICE_SEARCH: Final = "search"
SERVICE_PLAY_MEDIA: Final = "play_media"
SERVICE_CLEAR_RESULTS: Final = "clear_results"

# Sensor attributes
ATTR_RATING_KEY: Final = "rating_key"
ATTR_MEDIA_TYPE: Final = "media_type"
ATTR_YEAR: Final = "year"
ATTR_THUMB: Final = "thumb"
ATTR_SUMMARY: Final = "summary"
ATTR_DURATION: Final = "duration"
ATTR_RATING: Final = "rating"
ATTR_GENRES: Final = "genres"
ATTR_STUDIO: Final = "studio"
ATTR_DIRECTOR: Final = "director"
ATTR_WRITERS: Final = "writers"
ATTR_ACTORS: Final = "actors"
ATTR_LIBRARY_SECTION_ID: Final = "library_section_id"
ATTR_LIBRARY_SECTION_TITLE: Final = "library_section_title"
ATTR_PARENT_TITLE: Final = "parent_title"  # For TV show episodes
ATTR_GRANDPARENT_TITLE: Final = "grandparent_title"  # For TV show series
ATTR_INDEX: Final = "index"  # Episode or season number
ATTR_PARENT_INDEX: Final = "parent_index"  # Season number for episodes

# Media types
MEDIA_TYPE_MOVIE: Final = "movie"
MEDIA_TYPE_SHOW: Final = "show"
MEDIA_TYPE_SEASON: Final = "season"
MEDIA_TYPE_EPISODE: Final = "episode"
MEDIA_TYPE_ARTIST: Final = "artist"
MEDIA_TYPE_ALBUM: Final = "album"
MEDIA_TYPE_TRACK: Final = "track"

# Event types
EVENT_SEARCH_STARTED: Final = f"{DOMAIN}_search_started"
EVENT_SEARCH_COMPLETED: Final = f"{DOMAIN}_search_completed"
EVENT_SEARCH_FAILED: Final = f"{DOMAIN}_search_failed"
EVENT_PLAYBACK_STARTED: Final = f"{DOMAIN}_playback_started"
EVENT_PLAYBACK_FAILED: Final = f"{DOMAIN}_playback_failed"

# Storage keys
STORAGE_VERSION: Final = 1
STORAGE_KEY: Final = f"{DOMAIN}_storage"

# Update intervals
SCAN_INTERVAL_SECONDS: Final = 300  # 5 minutes for library updates

# Error messages
ERROR_CANNOT_CONNECT: Final = "cannot_connect"
ERROR_INVALID_AUTH: Final = "invalid_auth"
ERROR_UNKNOWN: Final = "unknown"
ERROR_NO_RESULTS: Final = "no_results"
ERROR_INVALID_PLAYER: Final = "invalid_player"
ERROR_PLAYBACK_FAILED: Final = "playback_failed"

# Icons
ICON_SEARCH: Final = "mdi:magnify"
ICON_MOVIE: Final = "mdi:movie"
ICON_TV: Final = "mdi:television"
ICON_MUSIC: Final = "mdi:music"
ICON_PLAY: Final = "mdi:play"
ICON_PLEX: Final = "mdi:plex"
