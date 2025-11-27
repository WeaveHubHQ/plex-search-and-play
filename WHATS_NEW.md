# What's New in Plex Search and Play v2.0

## 🎉 Major Update: Full Library Browsing Added!

Your integration is now a **complete Plex browser** - no need for separate integrations!

---

## ✨ New Features

### 1. **Browse Entire Libraries**
Browse your complete Movies or TV Shows library with pagination support.

```yaml
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  start: 0
  limit: 50
  sort: "titleSort"
```

### 2. **Continue Watching (On Deck)**
Show in-progress media items.

```yaml
service: plex_search_play.get_on_deck
data:
  limit: 20
```

### 3. **Recently Added**
Display newly added content.

```yaml
service: plex_search_play.get_recently_added
data:
  limit: 50
```

### 4. **Browse by Genre**
Filter library by genre.

```yaml
service: plex_search_play.get_by_genre
data:
  library_name: "Movies"
  genre: "Action"
  limit: 50
```

### 5. **Collections Browser**
Browse your Plex collections.

```yaml
service: plex_search_play.get_collections
data:
  library_name: "Movies"
```

---

## 🚀 What This Means

### You Don't Need PlexMeetsHomeAssistant Anymore!

Your integration now provides:

| Feature | Plex Search and Play v2.0 | PlexMeetsHomeAssistant |
|---------|---------------------------|------------------------|
| **Search** | ✅ Built-in | ⚠️ Limited |
| **Browse Libraries** | ✅ With pagination | ✅ Yes |
| **Continue Watching** | ✅ Built-in | ✅ Yes |
| **Recently Added** | ✅ Built-in | ✅ Yes |
| **Genre Filtering** | ✅ Built-in | ✅ Yes |
| **Collections** | ✅ Built-in | ✅ Yes |
| **Automation Services** | ✅ Full integration | ❌ Card-only |
| **Voice Control** | ✅ Service-based | ❌ Limited |
| **Event System** | ✅ Full events | ❌ No |
| **GUI Config** | ✅ Full UI setup | ⚠️ Partial |

---

## 📊 Complete Feature Set

### Search Features (Original)
- ✅ Text search with query
- ✅ 6 visual result slots
- ✅ Rich metadata (thumbnails, cast, synopsis)
- ✅ Custom Lovelace card
- ✅ Automation services
- ✅ Event system

### Browse Features (NEW!)
- ✅ Full library browsing
- ✅ Pagination (50+ items per page)
- ✅ Continue watching
- ✅ Recently added
- ✅ Genre filtering
- ✅ Collections
- ✅ Flexible sorting
- ✅ Same visual interface

### Playback Features (Enhanced)
- ✅ Works with all services
- ✅ Multi-player support
- ✅ GUI player selection
- ✅ Automation-friendly

---

## 🎯 Quick Start

### 1. Browse Your Movies

```yaml
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  limit: 50
```

### 2. Add Continue Watching Button

```yaml
type: button
name: Continue Watching
icon: mdi:play-circle
tap_action:
  action: call-service
  service: plex_search_play.get_on_deck
  service_data:
    limit: 20
```

### 3. Auto-Show Recently Added

```yaml
automation:
  - alias: "Daily New Plex Content"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: plex_search_play.get_recently_added
        data:
          limit: 10
```

---

## 📱 Dashboard Ideas

### Quick Access Buttons

```yaml
type: horizontal-stack
cards:
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

  - type: button
    name: Action Movies
    icon: mdi:movie-open
    tap_action:
      action: call-service
      service: plex_search_play.get_by_genre
      service_data:
        library_name: "Movies"
        genre: "Action"
```

### Genre Browser

```yaml
type: entities
entities:
  - entity: input_select.movie_genre
    name: Select Genre

  - type: button
    name: Browse Genre
    tap_action:
      action: call-service
      service: plex_search_play.get_by_genre
      service_data:
        library_name: "Movies"
        genre: "{{ states('input_select.movie_genre') }}"
```

---

## 🔄 Pagination

Browse large libraries in chunks:

```yaml
# Page 1 (items 0-49)
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  start: 0
  limit: 50

# Page 2 (items 50-99)
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  start: 50
  limit: 50
```

---

## 🎨 Sort Options

```yaml
service: plex_search_play.browse_library
data:
  library_name: "Movies"
  sort: "year:desc"  # Options: titleSort, addedAt:desc, year:desc, rating:desc
```

---

## 📚 Documentation

- **[BROWSE_FEATURES.md](BROWSE_FEATURES.md)** - Complete browsing guide
- **[README.md](README.md)** - Full documentation
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Setup guide
- **[examples/](examples/)** - Dashboard and automation examples

---

## 🔧 Technical Details

### Files Modified
- ✅ `plex_api.py` - Added 5 new browse methods
- ✅ `const.py` - Added service constants
- ✅ `__init__.py` - Added 5 new services
- ✅ `services.yaml` - Documented new services

### Services Added
1. `browse_library`
2. `get_on_deck`
3. `get_recently_added`
4. `get_by_genre`
5. `get_collections`

### Backward Compatibility
✅ **100% backward compatible** - all existing functionality preserved

---

## 🚀 Migration from PlexMeetsHomeAssistant

If you were using PlexMeetsHomeAssistant, you can now:

1. **Keep using Plex Search and Play** for everything
2. **Remove PlexMeetsHomeAssistant** if desired (optional)
3. **Use service calls** instead of card-only browsing
4. **Enable automation** with browse features

### Recommended Setup

**Use This Integration For:**
- Searching
- Browsing
- Continue watching
- Recently added
- Automation
- Voice control
- Service-based workflows

---

## 🎉 Summary

Your integration now provides a **complete, unified Plex experience**:

✅ **Search** - Fast, query-based discovery
✅ **Browse** - Full library exploration
✅ **Continue** - Resume watching
✅ **Discover** - Recently added content
✅ **Filter** - Genre-based browsing
✅ **Collect** - Collection support
✅ **Automate** - Full service integration
✅ **Control** - Voice + automation ready

**One integration. Complete solution.** 🎬

---

## 💡 Next Steps

1. **Read** [BROWSE_FEATURES.md](BROWSE_FEATURES.md) for detailed examples
2. **Try** the browse services in Developer Tools
3. **Add** quick access buttons to your dashboard
4. **Create** automations for daily content updates
5. **Explore** genre filtering and collections

Enjoy your enhanced Plex integration! 🍿
