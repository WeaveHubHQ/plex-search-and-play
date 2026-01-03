# Plex Search and Play for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/WeaveHubHQ/plex-search-and-play.svg)](https://github.com/WeaveHubHQ/plex-search-and-play/releases)
[![License](https://img.shields.io/github/license/WeaveHubHQ/plex-search-and-play.svg)](LICENSE)

A powerful Home Assistant integration that brings visual Plex media search and playback directly to your dashboard. Search your Plex library, browse results with thumbnails and metadata, and send content to any media player - all from a beautiful, glassmorphic interface.

![Plex Search and Play Demo](docs/images/demo.png)

## Features

✨ **Visual Search Interface**
- Search your entire Plex library from Home Assistant
- Display results with movie posters and thumbnails
- Rich metadata including title, year, rating, genres, cast, and synopsis

🎬 **Smart Media Playback**
- Send content to any selected media player
- Support for Movies, TV Shows, Episodes, and more
- Integrated with Home Assistant's native media player entities

🎨 **Beautiful UI**
- Custom Lovelace card with glassmorphic design
- Responsive layout that adapts to mobile and desktop
- Customizable themes and grid layouts

⚙️ **Easy Configuration**
- GUI-based setup through Home Assistant UI
- Select which media players to use with checkboxes
- Choose which Plex libraries to search
- No YAML editing required for basic setup

🔒 **Secure & Local**
- Uses official Plex API (plexapi)
- Direct connection to your local Plex server
- Authentication via Plex token

## Quick Start

### Prerequisites

- Home Assistant 2024.1.0 or newer
- A Plex Media Server (local or remote)
- Plex authentication token ([How to find it](#finding-your-plex-token))

### Installation via HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/WeaveHubHQ/plex-search-and-play`
6. Select "Integration" as the category
7. Click "Add"
8. Find "Plex Search and Play" in HACS and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/plex_search_play` folder to your Home Assistant's `custom_components` directory
2. Copy the `www/plex-search-card` folder to your Home Assistant's `www` directory
3. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Plex Search and Play"
4. Enter your Plex server URL (e.g., `http://192.168.1.100:32400`)
5. Enter your Plex authentication token
6. Click **Submit**
7. Select which media players you want to use
8. Select which Plex libraries to search (or leave empty for all)
9. Click **Submit**

### Finding Your Plex Token

See the [Setup Instructions](SETUP_INSTRUCTIONS.md#finding-your-plex-token) for detailed steps on how to find your Plex authentication token.

## Usage

### Using the Custom Card

1. Edit your dashboard
2. Click "Add Card"
3. Search for "Custom: Plex Search Card"
4. Add the following configuration:

```yaml
type: custom:plex-search-card
entity: sensor.plex_search_and_play_search_status
result_entities:
  - sensor.plex_search_and_play_result_1
  - sensor.plex_search_and_play_result_2
  - sensor.plex_search_and_play_result_3
  - sensor.plex_search_and_play_result_4
  - sensor.plex_search_and_play_result_5
  - sensor.plex_search_and_play_result_6
player_entities:
  - media_player.living_room
  - media_player.bedroom
  - media_player.office_sonos
title: Plex Search
columns: 2
show_thumbnails: true
```

### Using Services

The integration provides three services you can use in automations and scripts:

#### Search Service

```yaml
service: plex_search_play.search
data:
  query: "Inception"
  limit: 6
```

#### Play Media Service

```yaml
service: plex_search_play.play_media
data:
  rating_key: "12345"
  player_entity_id: media_player.living_room
```

#### Clear Results Service

```yaml
service: plex_search_play.clear_results
```

### Example Automation

Automatically search when you say "Plex search for [movie name]":

```yaml
automation:
  - alias: "Voice Search Plex"
    trigger:
      - platform: event
        event_type: voice_command
    condition:
      - condition: template
        value_template: "{{ 'plex search' in trigger.event.data.text.lower() }}"
    action:
      - service: plex_search_play.search
        data:
          query: "{{ trigger.event.data.text.lower().replace('plex search for', '').strip() }}"
          limit: 6
```

## Available Sensors

Once configured, the integration creates the following sensors:

### Search Status Sensor
`sensor.plex_search_and_play_search_status`
- State: Current search status
- Attributes:
  - `result_count`: Number of results found
  - `last_query`: Last search query

### Result Sensors
`sensor.plex_search_and_play_result_1` through `sensor.plex_search_and_play_result_6`
- State: Media title (or "Empty" if no result)
- Attributes:
  - `rating_key`: Plex rating key (used for playback)
  - `media_type`: Type of media (movie, show, episode, etc.)
  - `year`: Release year
  - `summary`: Plot synopsis
  - `thumb`: Thumbnail URL
  - `rating`: Content rating
  - `duration`: Runtime in milliseconds
  - `genres`: List of genres
  - `studio`: Production studio
  - `director`: Director(s)
  - `writers`: Writer(s)
  - `actors`: Cast members (top 5)
  - And more...

## Customization

### Custom Card Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | Required | Search status sensor entity |
| `result_entities` | list | Required | List of result sensor entities |
| `player_entities` | list | Required | List of media player entities |
| `title` | string | "Plex Search" | Card title |
| `columns` | number | 2 | Number of columns in results grid |
| `show_thumbnails` | boolean | true | Show media thumbnails |
| `theme` | string | "glassmorphic" | Visual theme |

### Theming

The custom card uses CSS variables that you can override with `card-mod`:

```yaml
type: custom:plex-search-card
card_mod:
  style: |
    :host {
      --card-background: rgba(0, 0, 0, 0.8);
      --accent-color: #ff6b6b;
      --text-primary: #ffffff;
    }
# ... rest of config
```

## Architecture

### Component Structure

```
custom_components/plex_search_play/
├── __init__.py          # Integration setup and services
├── config_flow.py       # GUI configuration flow
├── const.py             # Constants and configuration
├── manifest.json        # Integration metadata
├── plex_api.py         # Plex API wrapper
├── sensor.py           # Sensor platform
├── services.yaml       # Service definitions
└── strings.json        # UI translations

www/plex-search-card/
└── plex-search-card.js # Custom Lovelace card
```

### Data Flow

1. User enters search query in the custom card
2. Card calls `plex_search_play.search` service
3. Service queries Plex API via `plex_api.py`
4. Results are stored in integration data
5. Result sensors update automatically
6. Custom card displays updated results
7. User selects a result and player
8. Card calls `plex_search_play.play_media` service
9. Service gets media URL from Plex
10. Service calls `media_player.play_media` on selected device

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Plex server

**Solutions**:
- Verify Plex server URL is correct (include port, typically 32400)
- Ensure Home Assistant can reach your Plex server
- Check firewall settings
- Try using IP address instead of hostname

### Authentication Issues

**Problem**: Invalid authentication token

**Solutions**:
- Verify you're using the correct Plex token
- See [Finding Your Plex Token](#finding-your-plex-token)
- Regenerate token if necessary

### Playback Issues

**Problem**: Media won't play on selected device

**Solutions**:
- Ensure the media player is online and reachable
- Check that the player supports the media format
- Verify the player is in the selected players list
- Check Home Assistant logs for detailed error messages

### No Search Results

**Problem**: Search returns no results

**Solutions**:
- Verify library names in configuration
- Try searching with fewer/different keywords
- Check that libraries are accessible to the Plex token user
- Ensure media has been scanned into Plex

### Custom Card Not Appearing

**Problem**: Plex Search Card doesn't appear in card picker

**Solutions**:
- Clear browser cache
- Ensure `plex-search-card.js` is in `/config/www/plex-search-card/`
- Add resource manually in Lovelace resources:
  - URL: `/local/plex-search-card/plex-search-card.js`
  - Type: JavaScript Module
- Restart Home Assistant

## Development

### Testing Locally

1. Clone this repository
2. Create a symbolic link from your Home Assistant `custom_components` to this repo:
   ```bash
   ln -s /path/to/plex-search-and-play/custom_components/plex_search_play /path/to/homeassistant/custom_components/
   ```
3. Restart Home Assistant
4. Enable debug logging in `configuration.yaml`:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.plex_search_play: debug
   ```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Documentation**: [Setup Instructions](SETUP_INSTRUCTIONS.md)
- **Issues**: [GitHub Issues](https://github.com/WeaveHubHQ/plex-search-and-play/issues)
- **Discussions**: [GitHub Discussions](https://github.com/WeaveHubHQ/plex-search-and-play/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [plexapi](https://github.com/pkkid/python-plexapi)
- Inspired by the Home Assistant community
- Glassmorphic design inspired by modern UI trends

## Changelog

### v1.0.0 (2025-01-27)
- Initial release
- Visual search interface with custom Lovelace card
- GUI-based configuration
- Support for movies and TV shows
- Multi-player selection
- Library filtering
- Rich metadata display

---

Made with ❤️ for the Home Assistant community
