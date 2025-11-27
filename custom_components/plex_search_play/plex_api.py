"""Plex API wrapper for search and playback functionality."""

from __future__ import annotations

import logging
from typing import Any

from plexapi.exceptions import BadRequest, NotFound, Unauthorized
from plexapi.server import PlexServer
from plexapi.video import Episode, Movie, Show

from homeassistant.exceptions import HomeAssistantError

from .const import (
    ATTR_ACTORS,
    ATTR_DIRECTOR,
    ATTR_DURATION,
    ATTR_GENRES,
    ATTR_GRANDPARENT_TITLE,
    ATTR_INDEX,
    ATTR_LIBRARY_SECTION_ID,
    ATTR_LIBRARY_SECTION_TITLE,
    ATTR_MEDIA_TYPE,
    ATTR_PARENT_INDEX,
    ATTR_PARENT_TITLE,
    ATTR_RATING,
    ATTR_RATING_KEY,
    ATTR_STUDIO,
    ATTR_SUMMARY,
    ATTR_THUMB,
    ATTR_WRITERS,
    ATTR_YEAR,
    DEFAULT_SEARCH_LIMIT,
    DEFAULT_TIMEOUT,
    ERROR_CANNOT_CONNECT,
    ERROR_INVALID_AUTH,
    ERROR_NO_RESULTS,
    MEDIA_TYPE_EPISODE,
    MEDIA_TYPE_MOVIE,
    MEDIA_TYPE_SEASON,
    MEDIA_TYPE_SHOW,
)

_LOGGER = logging.getLogger(__name__)


class PlexSearchAPIError(HomeAssistantError):
    """Exception raised for Plex API errors."""


class PlexSearchAPI:
    """Interface to communicate with Plex server for search and playback."""

    def __init__(self, plex_url: str, plex_token: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Initialize the Plex API wrapper.

        Args:
            plex_url: The base URL of the Plex server (e.g., http://192.168.1.100:32400)
            plex_token: The authentication token for the Plex server
            timeout: Request timeout in seconds
        """
        self._plex_url = plex_url
        self._plex_token = plex_token
        self._timeout = timeout
        self._server: PlexServer | None = None

    async def async_connect(self) -> bool:
        """Test connection to Plex server.

        Returns:
            True if connection successful

        Raises:
            PlexSearchAPIError: If connection fails
        """
        try:
            self._server = PlexServer(
                self._plex_url,
                self._plex_token,
                timeout=self._timeout
            )
            # Test the connection
            _ = self._server.friendlyName
            _LOGGER.info("Successfully connected to Plex server: %s", self._server.friendlyName)
            return True
        except Unauthorized as err:
            _LOGGER.error("Invalid Plex token")
            raise PlexSearchAPIError(ERROR_INVALID_AUTH) from err
        except (BadRequest, ConnectionError) as err:
            _LOGGER.error("Cannot connect to Plex server at %s", self._plex_url)
            raise PlexSearchAPIError(ERROR_CANNOT_CONNECT) from err
        except Exception as err:
            _LOGGER.exception("Unexpected error connecting to Plex: %s", err)
            raise PlexSearchAPIError(ERROR_CANNOT_CONNECT) from err

    def get_server_name(self) -> str:
        """Get the friendly name of the Plex server."""
        if self._server:
            return self._server.friendlyName
        return "Unknown"

    async def async_search(
        self,
        query: str,
        library_sections: list[str] | None = None,
        limit: int = DEFAULT_SEARCH_LIMIT
    ) -> list[dict[str, Any]]:
        """Search Plex library for media.

        Args:
            query: Search query string
            library_sections: Optional list of library section names to search
            limit: Maximum number of results to return

        Returns:
            List of media items with metadata

        Raises:
            PlexSearchAPIError: If search fails
        """
        if not self._server:
            await self.async_connect()

        try:
            results = []

            if library_sections:
                # Search specific library sections
                for section_name in library_sections:
                    try:
                        section = self._server.library.section(section_name)
                        section_results = section.search(query, limit=limit)
                        results.extend(section_results)
                    except NotFound:
                        _LOGGER.warning("Library section '%s' not found", section_name)
                        continue
            else:
                # Search all libraries
                results = self._server.library.search(query, limit=limit)

            if not results:
                _LOGGER.info("No results found for query: %s", query)
                return []

            # Parse and format results
            formatted_results = []
            for idx, item in enumerate(results[:limit]):
                try:
                    formatted_item = self._format_media_item(item, idx)
                    formatted_results.append(formatted_item)
                except Exception as err:
                    _LOGGER.warning("Error formatting media item: %s", err)
                    continue

            _LOGGER.info("Found %d results for query: %s", len(formatted_results), query)
            return formatted_results

        except Exception as err:
            _LOGGER.exception("Error searching Plex: %s", err)
            raise PlexSearchAPIError(ERROR_NO_RESULTS) from err

    def _format_media_item(self, item: Any, index: int) -> dict[str, Any]:
        """Format a Plex media item into a standardized dictionary.

        Args:
            item: Plex media item
            index: Index in the results list

        Returns:
            Formatted media item dictionary
        """
        # Common attributes
        formatted = {
            "index": index,
            ATTR_RATING_KEY: str(item.ratingKey),
            "title": item.title,
            ATTR_SUMMARY: getattr(item, "summary", ""),
            ATTR_THUMB: self._get_thumb_url(item),
            ATTR_YEAR: getattr(item, "year", None),
            ATTR_RATING: getattr(item, "rating", None),
            ATTR_DURATION: getattr(item, "duration", 0),
            ATTR_LIBRARY_SECTION_ID: item.librarySectionID,
            ATTR_LIBRARY_SECTION_TITLE: item.librarySectionTitle,
        }

        # Media type specific attributes
        if isinstance(item, Movie):
            formatted[ATTR_MEDIA_TYPE] = MEDIA_TYPE_MOVIE
            formatted[ATTR_STUDIO] = getattr(item, "studio", None)
            formatted[ATTR_DIRECTOR] = self._get_directors(item)
            formatted[ATTR_WRITERS] = self._get_writers(item)
            formatted[ATTR_ACTORS] = self._get_actors(item)
            formatted[ATTR_GENRES] = self._get_genres(item)

        elif isinstance(item, Show):
            formatted[ATTR_MEDIA_TYPE] = MEDIA_TYPE_SHOW
            formatted[ATTR_STUDIO] = getattr(item, "studio", None)
            formatted[ATTR_GENRES] = self._get_genres(item)

        elif isinstance(item, Episode):
            formatted[ATTR_MEDIA_TYPE] = MEDIA_TYPE_EPISODE
            formatted[ATTR_PARENT_TITLE] = getattr(item, "seasonEpisode", "")  # e.g., "S01E05"
            formatted[ATTR_GRANDPARENT_TITLE] = getattr(item, "grandparentTitle", "")  # Show name
            formatted[ATTR_INDEX] = getattr(item, "index", None)  # Episode number
            formatted[ATTR_PARENT_INDEX] = getattr(item, "parentIndex", None)  # Season number
            formatted[ATTR_DIRECTOR] = self._get_directors(item)
            formatted[ATTR_WRITERS] = self._get_writers(item)

        else:
            # Generic handling for other types
            formatted[ATTR_MEDIA_TYPE] = item.type

        return formatted

    def _get_thumb_url(self, item: Any) -> str:
        """Get the full URL for the item's thumbnail.

        Args:
            item: Plex media item

        Returns:
            Full thumbnail URL
        """
        if not hasattr(item, "thumb") or not item.thumb:
            return ""

        # Return full URL including the server base URL
        return f"{self._plex_url}{item.thumb}?X-Plex-Token={self._plex_token}"

    def _get_genres(self, item: Any) -> list[str]:
        """Extract genre names from a media item."""
        try:
            return [genre.tag for genre in item.genres] if hasattr(item, "genres") else []
        except Exception:
            return []

    def _get_directors(self, item: Any) -> list[str]:
        """Extract director names from a media item."""
        try:
            return [director.tag for director in item.directors] if hasattr(item, "directors") else []
        except Exception:
            return []

    def _get_writers(self, item: Any) -> list[str]:
        """Extract writer names from a media item."""
        try:
            return [writer.tag for writer in item.writers] if hasattr(item, "writers") else []
        except Exception:
            return []

    def _get_actors(self, item: Any) -> list[str]:
        """Extract actor names from a media item (limited to first 5)."""
        try:
            if hasattr(item, "roles"):
                return [actor.tag for actor in item.roles[:5]]
            return []
        except Exception:
            return []

    async def async_get_media_url(self, rating_key: str) -> str:
        """Get the playback URL for a media item.

        Args:
            rating_key: The Plex rating key for the media item

        Returns:
            Playback URL

        Raises:
            PlexSearchAPIError: If media item not found
        """
        if not self._server:
            await self.async_connect()

        try:
            item = self._server.fetchItem(int(rating_key))
            # Get the first media part URL
            if hasattr(item, "media") and item.media:
                media = item.media[0]
                if hasattr(media, "parts") and media.parts:
                    part = media.parts[0]
                    key = part.key
                    return f"{self._plex_url}{key}?X-Plex-Token={self._plex_token}"

            raise PlexSearchAPIError("No playable media found")

        except NotFound as err:
            _LOGGER.error("Media item with rating key %s not found", rating_key)
            raise PlexSearchAPIError(ERROR_NO_RESULTS) from err
        except Exception as err:
            _LOGGER.exception("Error getting media URL: %s", err)
            raise PlexSearchAPIError(ERROR_NO_RESULTS) from err

    def get_libraries(self) -> list[str]:
        """Get list of available library section names.

        Returns:
            List of library section names
        """
        if not self._server:
            return []

        try:
            return [section.title for section in self._server.library.sections()]
        except Exception as err:
            _LOGGER.exception("Error getting libraries: %s", err)
            return []
