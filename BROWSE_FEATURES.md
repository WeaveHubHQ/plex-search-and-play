# Plex Search and Play - Browse Features Guide

## 🎉 New Browsing Capabilities Added!

Your integration now includes **full library browsing** in addition to search! You no longer need PlexMeetsHomeAssistant.

## ✨ What's New

### Backend Services Added

1. **`plex_search_play.browse_library`** - Browse entire libraries with pagination
2. **`plex_search_play.get_on_deck`** - Continue watching / in-progress items
3. **`plex_search_play.get_recently_added`** - Recently added media
4. **`plex_search_play.get_by_genre`** - Filter by genre
5. **`plex_search_play.get_collections`** - Browse collections

### Features

✅ **Full Library Browsing** - Browse your entire Plex library
✅ **Pagination Support** - Load 50 items at a time, navigate pages
✅ **Continue Watching** - See in-progress media
✅ **Recently Added** - Browse new content
✅ **Genre Filtering** - Filter by Action, Comedy, etc.
✅ **Collections** - Browse your Plex collections
✅ **Sorting** - Sort by title, date added, year
✅ **Same Visual Interface** - Uses existing result sensors

---

## 🚀 Usage Examples

### 1. Browse Movies Library

```yaml
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  start: 0
  limit: 50
  sort: "titleSort"
```

### 2. Get Continue Watching

```yaml
service: plex_search_play.get_on_deck
data:
  limit: 20
```

### 3. Get Recently Added

```yaml
service: plex_search_play.get_recently_added
data:
  limit: 50
```

### 4. Browse By Genre

```yaml
service: plex_search_play.get_by_genre
data:
  library_name: "Movies"
  genre: "Action"
  limit: 50
```

### 5. Get Collections

```yaml
service: plex_search_play.get_collections
data:
  library_name: "Movies"
```

---

## 📱 Dashboard Integration

### Option 1: Quick Browse Buttons

```yaml
type: vertical-stack
cards:
  # Browse Buttons
  - type: horizontal-stack
    cards:
      - type: button
        name: Continue Watching
        icon: mdi:play-circle
        tap_action:
          action: call-service
          service: plex_search_play.get_on_deck
          service_data:
            limit: 20

      - type: button
        name: Recently Added
        icon: mdi:new-box
        tap_action:
          action: call-service
          service: plex_search_play.get_recently_added
          service_data:
            limit: 50

      - type: button
        name: Action Movies
        icon: mdi:movie-open
        tap_action:
          action: call-service
          service: plex_search_play.get_by_genre
          service_data:
            library_name: "Movies"
            genre: "Action"

  # Search Card (existing)
  - type: custom:plex-search-card
    # ... your existing config
```

### Option 2: Library Browser with Pagination

```yaml
type: entities
entities:
  # Library Selection
  - entity: input_select.plex_browse_library
    name: Select Library

  # Page Controls
  - type: custom:button-card
    name: "◀ Previous Page"
    tap_action:
      action: call-service
      service: plex_search_play.browse_library
      service_data:
        library_name: "{{ states('input_select.plex_browse_library') }}"
        start: "{{ [0, (states('input_number.plex_page') | int - 1) * 50] | max }}"
        limit: 50

  - entity: input_number.plex_page
    name: Page

  - type: custom:button-card
    name: "Next Page ▶"
    tap_action:
      action: call-service
      service: plex_search_play.browse_library
      service_data:
        library_name: "{{ states('input_select.plex_browse_library') }}"
        start: "{{ (states('input_number.plex_page') | int) * 50 }}"
        limit: 50
```

### Option 3: Genre Filter Dashboard

```yaml
type: vertical-stack
cards:
  # Genre Selector
  - type: entities
    entities:
      - entity: input_select.movie_genre

  # Genre Browse Button
  - type: button
    name: Browse Selected Genre
    icon: mdi:filter
    tap_action:
      action: call-service
      service: plex_search_play.get_by_genre
      service_data:
        library_name: "Movies"
        genre: "{{ states('input_select.movie_genre') }}"
        limit: 50

  # Results (uses same result sensors)
  - type: custom:plex-search-card
    # ... existing config
```

---

## 🎮 Automation Examples

### Auto-Show Continue Watching on TV Turn On

```yaml
automation:
  - alias: "Plex: Show Continue Watching on TV On"
    trigger:
      - platform: state
        entity_id: media_player.living_room
        to: "on"
    action:
      - service: plex_search_play.get_on_deck
        data:
          limit: 6
```

### Daily "New Content" Notification

```yaml
automation:
  - alias: "Plex: Daily New Content Check"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: plex_search_play.get_recently_added
        data:
          limit: 10
      - delay:
          seconds: 2
      - condition: template
        value_template: "{{ states('sensor.plex_search_and_play_search_status') != 'Found 0 results' }}"
      - service: notify.mobile_app
        data:
          title: "New on Plex!"
          message: "{{ states('sensor.plex_search_and_play_search_status') }}"
```

### Genre-Based Movie Night

```yaml
automation:
  - alias: "Plex: Friday Night Action Movies"
    trigger:
      - platform: time
        at: "19:00:00"
    condition:
      - condition: time
        weekday: [fri]
    action:
      - service: plex_search_play.get_by_genre
        data:
          library_name: "Movies"
          genre: "Action"
          limit: 6
```

---

## 🔄 Pagination Example

To implement pagination for browsing large libraries:

### Required Input Helpers

```yaml
input_number:
  plex_current_page:
    name: Plex Current Page
    min: 0
    max: 1000
    step: 1
    mode: box

input_select:
  plex_browse_library:
    name: Plex Library
    options:
      - Movies
      - TV Shows
    icon: mdi:filmstrip
```

### Scripts

```yaml
script:
  plex_browse_next_page:
    sequence:
      - service: input_number.increment
        target:
          entity_id: input_number.plex_current_page
      - service: plex_search_play.browse_library
        data:
          library_name: "{{ states('input_select.plex_browse_library') }}"
          start: "{{ states('input_number.plex_current_page') | int * 50 }}"
          limit: 50

  plex_browse_previous_page:
    sequence:
      - service: input_number.decrement
        target:
          entity_id: input_number.plex_current_page
      - service: plex_search_play.browse_library
        data:
          library_name: "{{ states('input_select.plex_browse_library') }}"
          start: "{{ states('input_number.plex_current_page') | int * 50 }}"
          limit: 50
```

---

## 📊 Available Sort Orders

Use the `sort` parameter in `browse_library`:

- `"titleSort"` - Alphabetical by title
- `"addedAt:desc"` - Recently added first
- `"year:desc"` - Newest first
- `"rating:desc"` - Highest rated first
- `"duration:desc"` - Longest first

### Example:

```yaml
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  start: 0
  limit: 50
  sort: "year:desc"  # Newest movies first
```

---

## 🎯 Combined Browse + Search Dashboard

Complete dashboard combining search and browse:

```yaml
type: vertical-stack
cards:
  # Header
  - type: markdown
    content: |
      # 🎬 Plex Media Center
      Search or browse your entire library

  # Mode Selection
  - type: horizontal-stack
    cards:
      - type: button
        name: Search Mode
        icon: mdi:magnify
        tap_action:
          action: navigate
          navigation_path: /lovelace/plex-search

      - type: button
        name: Browse Mode
        icon: mdi:view-grid
        tap_action:
          action: navigate
          navigation_path: /lovelace/plex-browse

      - type: button
        name: Continue Watching
        icon: mdi:play-circle
        tap_action:
          action: call-service
          service: plex_search_play.get_on_deck

      - type: button
        name: Recently Added
        icon: mdi:new-box
        tap_action:
          action: call-service
          service: plex_search_play.get_recently_added

  # Existing Search Card
  - type: custom:plex-search-card
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
    title: Results
    columns: 3
```

---

## 🔍 Key Differences from Search

| Feature | Search | Browse |
|---------|--------|--------|
| **Query Required** | Yes | No |
| **Result Limit** | 6 (default) | 50+ (paginated) |
| **Use Case** | Find specific content | Explore library |
| **Speed** | Fast | May take longer for large libraries |
| **Filters** | Query-based | Genre, sort, library |

---

## 💡 Pro Tips

1. **Use Continue Watching** for the best user experience - shows what users care about most
2. **Recently Added** is perfect for automation notifications
3. **Browse by Genre** works great with button cards for quick access
4. **Pagination** is automatic - results use the same 6 sensor slots, just call the service again with different `start` value
5. **Combine with Search** - Use browse buttons alongside search for maximum flexibility

---

## 🎨 Visual Browse Interface (Coming Soon)

The custom Lovelace card will be enhanced with:
- **Tabs** for Search vs Browse modes
- **Library selector** dropdown
- **Genre filter** chips
- **Pagination** controls (Previous/Next)
- **Sort** dropdown
- **Collection** browser

For now, use the service calls directly with button cards!

---

## 📝 Summary

You now have:

✅ **5 new services** for browsing
✅ **Full library access** with pagination
✅ **Continue watching** integration
✅ **Recently added** tracking
✅ **Genre filtering** capabilities
✅ **Collection** browsing
✅ **Flexible sorting** options

**Your integration is now a complete Plex browser!** 🎉

No need for PlexMeetsHomeAssistant - you have everything in one integration.
