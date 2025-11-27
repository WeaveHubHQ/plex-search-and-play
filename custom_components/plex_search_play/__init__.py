"""The Plex Search and Play integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.media_player import (
    ATTR_MEDIA_CONTENT_ID,
    ATTR_MEDIA_CONTENT_TYPE,
    DOMAIN as MEDIA_PLAYER_DOMAIN,
    SERVICE_PLAY_MEDIA,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    ATTR_RATING_KEY,
    CONF_LIBRARIES,
    CONF_PLEX_TOKEN,
    CONF_PLEX_URL,
    CONF_SELECTED_PLAYERS,
    DOMAIN,
    EVENT_PLAYBACK_FAILED,
    EVENT_PLAYBACK_STARTED,
    EVENT_SEARCH_COMPLETED,
    EVENT_SEARCH_FAILED,
    EVENT_SEARCH_STARTED,
    SERVICE_CLEAR_RESULTS,
    SERVICE_PLAY_MEDIA as PLEX_SERVICE_PLAY_MEDIA,
    SERVICE_SEARCH,
)
from .plex_api import PlexSearchAPI, PlexSearchAPIError

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

# Service schemas
SERVICE_SEARCH_SCHEMA = vol.Schema(
    {
        vol.Required("query"): cv.string,
        vol.Optional("limit", default=6): cv.positive_int,
    }
)

SERVICE_PLAY_MEDIA_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_RATING_KEY): cv.string,
        vol.Required("player_entity_id"): cv.entity_id,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Plex Search and Play from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get configuration
    plex_url = entry.data[CONF_PLEX_URL]
    plex_token = entry.data[CONF_PLEX_TOKEN]
    selected_players = entry.data.get(CONF_SELECTED_PLAYERS, [])
    libraries = entry.data.get(CONF_LIBRARIES, [])

    # Create API instance
    api = PlexSearchAPI(plex_url, plex_token)

    try:
        await api.async_connect()
    except PlexSearchAPIError as err:
        _LOGGER.error("Failed to connect to Plex server: %s", err)
        return False

    # Store API instance and config
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "selected_players": selected_players,
        "libraries": libraries,
        "search_results": [],
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def handle_search(call: ServiceCall) -> None:
        """Handle the search service call."""
        query = call.data["query"]
        limit = call.data.get("limit", 6)

        _LOGGER.info("Searching Plex for: %s (limit: %d)", query, limit)

        # Fire search started event
        hass.bus.async_fire(
            EVENT_SEARCH_STARTED,
            {"query": query, "limit": limit}
        )

        try:
            # Perform search
            results = await api.async_search(
                query=query,
                library_sections=libraries if libraries else None,
                limit=limit
            )

            # Store results
            hass.data[DOMAIN][entry.entry_id]["search_results"] = results

            # Fire search completed event
            hass.bus.async_fire(
                EVENT_SEARCH_COMPLETED,
                {
                    "query": query,
                    "result_count": len(results),
                    "results": results
                }
            )

            _LOGGER.info("Search completed: %d results found", len(results))

        except PlexSearchAPIError as err:
            _LOGGER.error("Search failed: %s", err)
            hass.bus.async_fire(
                EVENT_SEARCH_FAILED,
                {"query": query, "error": str(err)}
            )
            raise HomeAssistantError(f"Search failed: {err}") from err

    async def handle_play_media(call: ServiceCall) -> None:
        """Handle the play_media service call."""
        rating_key = call.data[ATTR_RATING_KEY]
        player_entity_id = call.data["player_entity_id"]

        _LOGGER.info("Playing media (rating_key: %s) on %s", rating_key, player_entity_id)

        # Validate player is in selected list
        if selected_players and player_entity_id not in selected_players:
            error_msg = f"Player {player_entity_id} is not in the selected players list"
            _LOGGER.error(error_msg)
            hass.bus.async_fire(
                EVENT_PLAYBACK_FAILED,
                {
                    "rating_key": rating_key,
                    "player": player_entity_id,
                    "error": error_msg
                }
            )
            raise HomeAssistantError(error_msg)

        try:
            # Get media URL from Plex
            media_url = await api.async_get_media_url(rating_key)

            # Call media_player.play_media service
            await hass.services.async_call(
                MEDIA_PLAYER_DOMAIN,
                SERVICE_PLAY_MEDIA,
                {
                    "entity_id": player_entity_id,
                    ATTR_MEDIA_CONTENT_TYPE: MediaType.VIDEO,
                    ATTR_MEDIA_CONTENT_ID: media_url,
                },
                blocking=True,
            )

            # Fire playback started event
            hass.bus.async_fire(
                EVENT_PLAYBACK_STARTED,
                {
                    "rating_key": rating_key,
                    "player": player_entity_id,
                    "media_url": media_url
                }
            )

            _LOGGER.info("Playback started successfully")

        except PlexSearchAPIError as err:
            _LOGGER.error("Failed to get media URL: %s", err)
            hass.bus.async_fire(
                EVENT_PLAYBACK_FAILED,
                {
                    "rating_key": rating_key,
                    "player": player_entity_id,
                    "error": str(err)
                }
            )
            raise HomeAssistantError(f"Failed to play media: {err}") from err

    async def handle_clear_results(call: ServiceCall) -> None:
        """Handle the clear_results service call."""
        hass.data[DOMAIN][entry.entry_id]["search_results"] = []
        _LOGGER.info("Search results cleared")

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH,
        handle_search,
        schema=SERVICE_SEARCH_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        PLEX_SERVICE_PLAY_MEDIA,
        handle_play_media,
        schema=SERVICE_PLAY_MEDIA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CLEAR_RESULTS,
        handle_clear_results,
    )

    _LOGGER.info("Plex Search and Play integration setup complete")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Remove services (only if this is the last entry)
        entries = hass.config_entries.async_entries(DOMAIN)
        if len(entries) == 1:  # This is the last entry
            hass.services.async_remove(DOMAIN, SERVICE_SEARCH)
            hass.services.async_remove(DOMAIN, PLEX_SERVICE_PLAY_MEDIA)
            hass.services.async_remove(DOMAIN, SERVICE_CLEAR_RESULTS)

        # Remove data
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
