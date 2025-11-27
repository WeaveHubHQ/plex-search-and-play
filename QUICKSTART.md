# Quick Start Guide - Plex Search and Play

Get up and running with development in 5 minutes!

## Prerequisites

- Home Assistant running (version 2024.1.0+)
- Plex Media Server accessible
- Python 3.11+
- Git

## Installation for Development

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/plex-search-and-play.git
cd plex-search-and-play
```

### 2. Link to Home Assistant

#### Option A: Symbolic Links (Recommended)

```bash
# Link integration
ln -s $(pwd)/custom_components/plex_search_play \
      ~/.homeassistant/custom_components/plex_search_play

# Link Lovelace card
ln -s $(pwd)/www/plex-search-card \
      ~/.homeassistant/www/plex-search-card
```

#### Option B: Copy Files

```bash
# Copy integration
cp -r custom_components/plex_search_play \
      ~/.homeassistant/custom_components/

# Copy Lovelace card
cp -r www/plex-search-card \
      ~/.homeassistant/www/
```

### 3. Enable Debug Logging

Edit `~/.homeassistant/configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.plex_search_play: debug
```

### 4. Restart Home Assistant

```bash
# Using Home Assistant CLI
ha core restart

# Or restart via UI: Settings → System → Restart
```

## Initial Configuration

### 1. Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Plex Search and Play"
4. Enter Plex server URL: `http://YOUR_IP:32400`
5. Enter Plex token (see below)
6. Select media players
7. Select libraries (or leave empty)
8. Click Submit

### 2. Get Your Plex Token

**Quick Method:**
1. Go to https://app.plex.tv/
2. Open any media item
3. Click "..." → "Get Info" → "View XML"
4. Copy token from URL: `X-Plex-Token=YOUR_TOKEN_HERE`

### 3. Add the Dashboard Card

1. Edit any dashboard
2. Add Card → Custom: Plex Search Card
3. Use this minimal config:

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
  - media_player.YOUR_PLAYER
title: Plex Search
```

## First Test

### Test Search

1. Type "Inception" in the search box
2. Click Search
3. Results should appear in ~1-2 seconds

### Test Playback

1. Select a media player from dropdown
2. Click Play on any result
3. Media should start playing

### Check Logs

```bash
tail -f ~/.homeassistant/home-assistant.log | grep plex_search
```

## Development Workflow

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/my-feature

# Make your changes
vim custom_components/plex_search_play/sensor.py

# Restart Home Assistant to test
ha core restart

# Check logs for errors
tail -f ~/.homeassistant/home-assistant.log
```

### Testing Services

Use Developer Tools → Services:

**Test Search:**
```yaml
service: plex_search_play.search
data:
  query: "Star Wars"
  limit: 6
```

**Test Play:**
```yaml
service: plex_search_play.play_media
data:
  rating_key: "12345"
  player_entity_id: media_player.living_room
```

### Debugging

**Check Integration Loaded:**
```bash
ha core info | grep plex_search_play
```

**Check Entities:**
1. Developer Tools → States
2. Filter: `plex_search`
3. Should see 7 entities (1 status + 6 results)

**Check Events:**
1. Developer Tools → Events
2. Listen to: `plex_search_play_search_completed`
3. Perform a search
4. Event should fire with results

## Common Issues

### Issue: Integration not appearing

**Fix:**
```bash
# Verify files are in place
ls ~/.homeassistant/custom_components/plex_search_play/

# Should see: __init__.py, manifest.json, etc.

# Restart Home Assistant
ha core restart
```

### Issue: Custom card not loading

**Fix:**
```bash
# Verify card exists
ls ~/.homeassistant/www/plex-search-card/

# Clear browser cache: Ctrl+Shift+R

# Add resource manually:
# Settings → Dashboards → Resources
# URL: /local/plex-search-card/plex-search-card.js
# Type: JavaScript Module
```

### Issue: Connection to Plex fails

**Fix:**
```bash
# Test Plex is reachable
curl http://YOUR_PLEX_IP:32400/identity

# Should return XML with server info

# Check token is valid
curl -H "X-Plex-Token: YOUR_TOKEN" \
     http://YOUR_PLEX_IP:32400/library/sections
```

## Quick Reference

### File Locations

| Component | Path |
|-----------|------|
| Integration | `~/.homeassistant/custom_components/plex_search_play/` |
| Lovelace Card | `~/.homeassistant/www/plex-search-card/` |
| Config | `~/.homeassistant/.storage/core.config_entries` |
| Logs | `~/.homeassistant/home-assistant.log` |

### Key Files

| File | Purpose |
|------|---------|
| `__init__.py` | Services & setup |
| `config_flow.py` | GUI configuration |
| `plex_api.py` | Plex communication |
| `sensor.py` | Result sensors |
| `plex-search-card.js` | Frontend UI |

### Useful Commands

```bash
# Restart Home Assistant
ha core restart

# Check Home Assistant version
ha core info

# View real-time logs
ha core logs -f

# Validate configuration
ha core check

# List integrations
ha core info | grep custom_components
```

### Service Data Templates

**Search with variable:**
```yaml
service: plex_search_play.search
data:
  query: "{{ states('input_text.search_query') }}"
```

**Play with sensor attribute:**
```yaml
service: plex_search_play.play_media
data:
  rating_key: "{{ state_attr('sensor.plex_search_and_play_result_1', 'rating_key') }}"
  player_entity_id: "{{ states('input_select.active_player') }}"
```

## Next Steps

1. **Read** [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture details
2. **Review** [CONTRIBUTING.md](CONTRIBUTING.md) before making changes
3. **Check** [examples/](examples/) for automation ideas
4. **Follow** [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for end-user docs

## Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and help
- **Home Assistant Community**: General HA questions
- **Logs**: Always check logs first!

## Pro Tips

1. **Use symbolic links** for development (changes reflect immediately)
2. **Enable debug logging** to see what's happening
3. **Test with multiple libraries** (Movies, TV Shows, Music)
4. **Test edge cases** (no results, offline server, invalid token)
5. **Clear browser cache** when testing frontend changes
6. **Use Developer Tools** extensively for testing

---

**Happy coding! 🎬**

Need help? Open an issue or discussion on GitHub!
