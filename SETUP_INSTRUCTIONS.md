# Plex Search and Play - Setup Instructions

This guide will walk you through the complete setup process for the Plex Search and Play integration in Home Assistant.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Finding Your Plex Token](#finding-your-plex-token)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Adding the Dashboard Card](#adding-the-dashboard-card)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- **Home Assistant**: Version 2024.1.0 or newer
- **Plex Media Server**: Running and accessible from your Home Assistant instance
- **HACS**: Installed (for easiest installation)
- **Media Players**: At least one media player entity configured in Home Assistant

### Verify Home Assistant Can Reach Plex

1. Open Terminal/SSH in Home Assistant
2. Run: `ping YOUR_PLEX_SERVER_IP`
3. If ping fails, check your network configuration

---

## Finding Your Plex Token

Your Plex authentication token is required for the integration to communicate with your Plex server. There are multiple methods to find it:

### Method 1: Via Plex Web App (Easiest)

1. Open Plex in your web browser: `https://app.plex.tv/`
2. Navigate to any item in your library
3. Click the **"..."** (three dots) menu
4. Select **"Get Info"**
5. Click on **"View XML"**
6. In the URL bar, look for `X-Plex-Token=XXXXX`
7. Copy the long alphanumeric string after `X-Plex-Token=`

**Example URL:**
```
https://app.plex.tv/web/index.html#!/server/.../details?key=/library/metadata/12345&X-Plex-Token=AbCdEfGhIjKlMnOpQrStUvWxYz
```
Your token would be: `AbCdEfGhIjKlMnOpQrStUvWxYz`

### Method 2: Via PlexAPI Settings

1. Open Plex Web App
2. Go to **Settings** → **Your Account**
3. At the bottom, you'll see your username
4. The token may be visible in browser developer tools:
   - Press `F12` to open developer tools
   - Go to **Console** tab
   - Type: `localStorage.getItem('myPlexAccessToken')`
   - Press Enter
   - Your token will be displayed

### Method 3: Via XML File (Desktop App)

1. Play any media in Plex Desktop App
2. Open Plex's settings folder:
   - **Windows**: `%LOCALAPPDATA%\Plex Media Server\`
   - **Mac**: `~/Library/Application Support/Plex Media Server/`
   - **Linux**: `$PLEX_HOME/Library/Application Support/Plex Media Server/`
3. Look for a file containing your token

### Method 4: Via curl Command

If you have command line access:

```bash
curl -u "your-username:your-password" 'https://plex.tv/users/sign_in.xml' -X POST
```

Your token will be in the response XML under `<authentication-token>`.

---

## Installation

### Option A: Install via HACS (Recommended)

1. **Open HACS**
   - Go to Home Assistant
   - Click **HACS** in the sidebar

2. **Add Custom Repository**
   - Click the **three dots** (⋮) in the top right
   - Select **"Custom repositories"**
   - Add URL: `https://github.com/yourusername/plex-search-and-play`
   - Category: **Integration**
   - Click **"Add"**

3. **Install the Integration**
   - Search for **"Plex Search and Play"**
   - Click on it
   - Click **"Download"**
   - Select the latest version
   - Click **"Download"**

4. **Restart Home Assistant**
   - Go to **Settings** → **System**
   - Click **"Restart"**
   - Wait for Home Assistant to come back online

### Option B: Manual Installation

1. **Download the Integration**
   - Download the latest release from GitHub
   - Or clone: `git clone https://github.com/yourusername/plex-search-and-play.git`

2. **Copy Files**
   ```bash
   # Copy integration
   cp -r custom_components/plex_search_play /config/custom_components/

   # Copy Lovelace card
   cp -r www/plex-search-card /config/www/
   ```

3. **Set Permissions**
   ```bash
   chmod -R 755 /config/custom_components/plex_search_play
   chmod -R 755 /config/www/plex-search-card
   ```

4. **Restart Home Assistant**

---

## Configuration

### Step 1: Add the Integration

1. **Navigate to Integrations**
   - Go to **Settings** → **Devices & Services**
   - Click **"+ Add Integration"** (bottom right)

2. **Search and Select**
   - Type **"Plex Search and Play"**
   - Click on it

3. **Enter Plex Server Details**

   **Plex Server URL:**
   - Format: `http://YOUR_IP:32400`
   - Examples:
     - Local: `http://192.168.1.100:32400`
     - Localhost: `http://localhost:32400`
     - Remote: `http://plex.example.com:32400`

   **Plex Authentication Token:**
   - Paste the token you found earlier
   - Should be a long alphanumeric string (20-30 characters)

4. **Click Submit**
   - The integration will test the connection
   - If successful, you'll move to the next step
   - If it fails, see [Troubleshooting](#troubleshooting)

### Step 2: Select Media Players

1. **Choose Media Players**
   - You'll see a list of all media players in your Home Assistant
   - Check the boxes for players you want to use with Plex
   - Common players:
     - `media_player.living_room`
     - `media_player.bedroom`
     - `media_player.office_sonos`
     - `media_player.lg_webos_tv_*`
     - `media_player.apple_tv_*`

2. **Select Plex Libraries** (Optional)
   - Choose which Plex libraries to search
   - Options might include:
     - Movies
     - TV Shows
     - Music
     - Home Videos
   - Leave empty to search all libraries

3. **Click Submit**
   - Configuration is complete!

### Step 3: Verify Entities Were Created

1. **Check Developer Tools**
   - Go to **Developer Tools** → **States**
   - Search for: `sensor.plex_search_and_play`

2. **You Should See:**
   - `sensor.plex_search_and_play_search_status`
   - `sensor.plex_search_and_play_result_1`
   - `sensor.plex_search_and_play_result_2`
   - `sensor.plex_search_and_play_result_3`
   - `sensor.plex_search_and_play_result_4`
   - `sensor.plex_search_and_play_result_5`
   - `sensor.plex_search_and_play_result_6`

---

## Adding the Dashboard Card

### Step 1: Add the Custom Card Resource

1. **Navigate to Resources**
   - Go to **Settings** → **Dashboards**
   - Click the **three dots** (⋮) in the top right
   - Select **"Resources"**

2. **Add JavaScript Module**
   - Click **"+ Add Resource"**
   - URL: `/local/plex-search-card/plex-search-card.js`
   - Resource type: **JavaScript Module**
   - Click **"Create"**

3. **Refresh Browser**
   - Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Step 2: Add the Card to Your Dashboard

1. **Edit Dashboard**
   - Go to your dashboard
   - Click **"Edit Dashboard"** (top right)

2. **Add Card**
   - Click **"+ Add Card"**
   - Search for **"Custom: Plex Search Card"**
   - Click on it

3. **Configure the Card**

   Switch to **YAML mode** and paste:

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
     - media_player.lg_webos_tv_oled65c4aua
     - media_player.living_room
     - media_player.family_room_sonos
     - media_player.playstation_5
     - media_player.lauren_s_lg_webos_2024_tv
     - media_player.bedroom
     - media_player.office_sonos
   title: Plex Search
   columns: 2
   show_thumbnails: true
   ```

4. **Customize (Optional)**
   - Change `title` to your preference
   - Adjust `columns` (1-4) based on screen size
   - Set `show_thumbnails: false` to hide images
   - Remove player_entities you don't need

5. **Save**
   - Click **"Save"**
   - Click **"Done"** to exit edit mode

---

## Testing

### Test 1: Basic Search

1. **Type a Search Query**
   - In the Plex Search card, type: "Inception"
   - Click **"Search"**

2. **Verify Results Appear**
   - You should see movie/show cards appear
   - Each card should have:
     - Thumbnail/poster image
     - Title and year
     - Media type badge
     - Rating
     - Synopsis
     - Play button

3. **Check Sensors**
   - Go to **Developer Tools** → **States**
   - Find `sensor.plex_search_and_play_search_status`
   - State should say: "Found X results"

### Test 2: Playback

1. **Select a Player**
   - In the dropdown, choose a media player

2. **Click Play on a Result**
   - Click the **"Play"** button on any result card

3. **Verify Playback Starts**
   - Media should start playing on the selected device
   - Check the media player entity in Home Assistant

### Test 3: Service Calls

1. **Open Developer Tools**
   - Go to **Developer Tools** → **Services**

2. **Test Search Service**
   - Service: `plex_search_play.search`
   - Data:
     ```yaml
     query: "Star Wars"
     limit: 6
     ```
   - Click **"Call Service"**
   - Check the card for results

3. **Test Play Service**
   - Service: `plex_search_play.play_media`
   - Data:
     ```yaml
     rating_key: "12345"  # Use a real rating_key from search results
     player_entity_id: media_player.living_room
     ```
   - Click **"Call Service"**

---

## Troubleshooting

### Issue: "Cannot Connect to Plex Server"

**Possible Causes:**
1. Incorrect Plex URL
2. Firewall blocking connection
3. Plex server is offline

**Solutions:**
1. Verify Plex URL format: `http://IP:32400` (not https for local)
2. Test connection from Home Assistant terminal:
   ```bash
   curl http://YOUR_PLEX_IP:32400/identity
   ```
3. Check Plex is running: open `http://YOUR_PLEX_IP:32400/web` in browser
4. Ensure port 32400 is open in firewall
5. Try using IP address instead of hostname

### Issue: "Invalid Authentication Token"

**Possible Causes:**
1. Incorrect token
2. Token expired
3. Copied token with extra spaces

**Solutions:**
1. Double-check token has no leading/trailing spaces
2. Get a fresh token using [Method 1](#method-1-via-plex-web-app-easiest)
3. Ensure you're logged into the correct Plex account
4. Try removing and re-adding the integration

### Issue: "Custom Card Not Appearing"

**Possible Causes:**
1. JavaScript file not loaded
2. Browser cache
3. File in wrong location

**Solutions:**
1. Verify file exists: `/config/www/plex-search-card/plex-search-card.js`
2. Check resource is added in Lovelace resources
3. Clear browser cache completely
4. Try incognito/private browsing mode
5. Check browser console for errors (F12 → Console tab)

### Issue: "No Search Results"

**Possible Causes:**
1. Library not selected in config
2. Media not in Plex library
3. Search query too specific

**Solutions:**
1. Reconfigure integration and select libraries (or leave empty)
2. Verify media exists in Plex web interface
3. Try broader search terms
4. Check Plex has scanned the library recently

### Issue: "Media Won't Play"

**Possible Causes:**
1. Player not compatible
2. Player offline
3. Media format not supported
4. Network issues

**Solutions:**
1. Test player with other media in Home Assistant
2. Verify player is online and reachable
3. Check player supports video playback
4. Try a different player
5. Check Home Assistant logs:
   ```yaml
   # configuration.yaml
   logger:
     logs:
       custom_components.plex_search_play: debug
   ```

### Issue: "Thumbnails Not Loading"

**Possible Causes:**
1. Network connectivity
2. Plex token issue
3. CORS policy

**Solutions:**
1. Check Plex server is reachable
2. Verify token is still valid
3. Test thumbnail URL directly in browser
4. Check browser console for CORS errors

### Getting Help

If you're still having issues:

1. **Enable Debug Logging**
   ```yaml
   # configuration.yaml
   logger:
     default: info
     logs:
       custom_components.plex_search_play: debug
   ```

2. **Check Logs**
   - Go to **Settings** → **System** → **Logs**
   - Look for errors related to `plex_search_play`

3. **Report Issue**
   - Go to: https://github.com/yourusername/plex-search-and-play/issues
   - Include:
     - Home Assistant version
     - Integration version
     - Relevant log entries
     - Steps to reproduce

---

## Advanced Configuration

### Changing Selected Players After Setup

1. Go to **Settings** → **Devices & Services**
2. Find **Plex Search and Play**
3. Click **"Configure"**
4. Update your selections
5. Click **"Submit"**

### Using in Automations

Example: Search on voice command
```yaml
automation:
  - alias: "Plex Voice Search"
    trigger:
      - platform: event
        event_type: alexa_actionable_notification
    action:
      - service: plex_search_play.search
        data:
          query: "{{ trigger.event.data.text }}"
          limit: 6
```

Example: Auto-play on schedule
```yaml
automation:
  - alias: "Friday Movie Night"
    trigger:
      - platform: time
        at: "20:00:00"
    condition:
      - condition: time
        weekday:
          - fri
    action:
      - service: plex_search_play.search
        data:
          query: "action movies"
          limit: 6
```

### Using Alternative Lovelace Cards

If you prefer YAML-based cards, you can use native Home Assistant cards:

```yaml
type: vertical-stack
cards:
  # Search input
  - type: entities
    entities:
      - entity: input_text.plex_search_query
        name: Search Query

  # Status
  - type: entity
    entity: sensor.plex_search_and_play_search_status

  # Results
  - type: grid
    columns: 2
    cards:
      - type: picture-entity
        entity: sensor.plex_search_and_play_result_1
        show_name: true
        show_state: true
        tap_action:
          action: call-service
          service: plex_search_play.play_media
          service_data:
            rating_key: "{{ state_attr('sensor.plex_search_and_play_result_1', 'rating_key') }}"
            player_entity_id: media_player.living_room
```

---

## Security Considerations

1. **Token Security**
   - Never share your Plex token publicly
   - Don't commit it to Git repositories
   - Use secrets if needed in automations

2. **Network Security**
   - Use HTTPS if accessing Plex remotely
   - Consider VPN for remote access
   - Keep Plex server updated

3. **Player Access**
   - Only add trusted media players
   - Be aware of who has access to your Home Assistant

---

## Next Steps

Now that you have Plex Search and Play set up:

1. **Customize the card** to match your dashboard theme
2. **Create automations** for voice control or scheduled playback
3. **Explore advanced features** in the README
4. **Share feedback** or contribute to the project

Enjoy your seamless Plex integration with Home Assistant! 🎬🍿
