# Contributing to Plex Search and Play

Thank you for your interest in contributing to Plex Search and Play! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Submitting Changes](#submitting-changes)
6. [Coding Standards](#coding-standards)
7. [Testing](#testing)
8. [Documentation](#documentation)

## Code of Conduct

This project follows the Home Assistant community standards. Be respectful, inclusive, and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Home Assistant development environment
- Git
- Basic knowledge of Home Assistant integrations
- Familiarity with Plex API

### Finding Issues to Work On

1. Check the [Issues](https://github.com/InfoSecured/plex-search-and-play/issues) page
2. Look for issues tagged with `good first issue` for beginner-friendly tasks
3. Check `help wanted` for areas where contributions are especially needed
4. Feel free to propose new features via GitHub Discussions

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/plex-search-and-play.git
cd plex-search-and-play
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_dev.txt
```

### 3. Link to Home Assistant

```bash
# Create symbolic link to your Home Assistant config
ln -s $(pwd)/custom_components/plex_search_play \
      /path/to/homeassistant/custom_components/plex_search_play

# For www resources
ln -s $(pwd)/www/plex-search-card \
      /path/to/homeassistant/www/plex-search-card
```

### 4. Enable Debug Logging

Add to your Home Assistant `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.plex_search_play: debug
```

### 5. Restart Home Assistant

## Making Changes

### Branch Naming

Create a branch with a descriptive name:

```bash
git checkout -b feature/add-music-support
git checkout -b fix/thumbnail-loading
git checkout -b docs/improve-setup-guide
```

Branch prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

### Development Workflow

1. **Make your changes** in small, logical commits
2. **Test thoroughly** in your Home Assistant instance
3. **Update documentation** if needed
4. **Add tests** for new functionality
5. **Run linters** before committing

### Commit Messages

Follow conventional commit format:

```
type(scope): brief description

More detailed explanation if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(sensor): add support for music libraries

fix(api): handle connection timeout gracefully

docs(readme): add troubleshooting section for CORS issues
```

## Submitting Changes

### Before Submitting

1. **Test your changes**
   - Install in a test Home Assistant instance
   - Verify all existing functionality still works
   - Test edge cases and error conditions

2. **Run code quality checks**
   ```bash
   # Format code
   black custom_components/plex_search_play

   # Check for issues
   pylint custom_components/plex_search_play

   # Type checking
   mypy custom_components/plex_search_play
   ```

3. **Update documentation**
   - Update README.md if needed
   - Update SETUP_INSTRUCTIONS.md for setup changes
   - Add/update docstrings
   - Update examples if applicable

4. **Update CHANGELOG.md**
   ```markdown
   ## [Unreleased]
   ### Added
   - Music library support for search and playback

   ### Fixed
   - Thumbnail loading timeout issue
   ```

### Creating a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/add-music-support
   ```

2. **Open a Pull Request** on GitHub
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Reference related issues (Fixes #123)
   - Add screenshots for UI changes
   - Describe testing performed

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Tested in Home Assistant
   - [ ] All existing tests pass
   - [ ] Added new tests

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings
   ```

### After Submitting

- Respond to review feedback promptly
- Make requested changes in new commits
- Update the PR if requirements change
- Be patient and respectful with reviewers

## Coding Standards

### Python Code Style

Follow [PEP 8](https://pep8.org/) and Home Assistant's [style guide](https://developers.home-assistant.io/docs/development_guidelines).

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use type hints
- Write descriptive docstrings
- Use meaningful variable names

**Example:**
```python
async def async_search(
    self,
    query: str,
    library_sections: list[str] | None = None,
    limit: int = DEFAULT_SEARCH_LIMIT
) -> list[dict[str, Any]]:
    """Search Plex library for media.

    Args:
        query: Search query string
        library_sections: Optional list of library section names
        limit: Maximum number of results to return

    Returns:
        List of media items with metadata

    Raises:
        PlexSearchAPIError: If search fails
    """
    # Implementation
```

### JavaScript Code Style

For the Lovelace card:

- Use ES6+ features
- Use `const` and `let`, not `var`
- Use meaningful variable names
- Add JSDoc comments
- Follow existing code structure

**Example:**
```javascript
/**
 * Perform a Plex search
 * @param {string} query - Search query string
 * @returns {Promise<void>}
 */
async performSearch(query) {
  if (!query.trim()) {
    console.warn('Empty search query');
    return;
  }

  await this._hass.callService('plex_search_play', 'search', {
    query: query,
    limit: 6
  });
}
```

### File Structure

Maintain the existing structure:

```
custom_components/plex_search_play/
├── __init__.py          # Integration setup
├── config_flow.py       # Configuration UI
├── const.py             # Constants
├── manifest.json        # Metadata
├── plex_api.py         # API wrapper
├── sensor.py           # Sensors
├── services.yaml       # Service definitions
└── strings.json        # Translations

www/plex-search-card/
└── plex-search-card.js # Custom card
```

## Testing

### Manual Testing

1. **Install the integration**
   - Add integration via UI
   - Verify connection works
   - Test with invalid credentials

2. **Test search functionality**
   - Search for movies
   - Search for TV shows
   - Search with special characters
   - Search with no results

3. **Test playback**
   - Play on different media players
   - Test with offline players
   - Test with invalid media

4. **Test UI**
   - Custom card loads correctly
   - Results display properly
   - Thumbnails load
   - Responsive on mobile

### Automated Testing

(Future: Add pytest tests)

```python
# tests/test_plex_api.py
async def test_search_returns_results(hass, mock_plex_server):
    """Test that search returns expected results."""
    api = PlexSearchAPI("http://localhost:32400", "token")
    results = await api.async_search("Inception")

    assert len(results) > 0
    assert results[0]["title"] == "Inception"
```

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Use type hints
- Explain complex logic with comments
- Keep comments up to date

### User Documentation

- Update README.md for user-facing changes
- Update SETUP_INSTRUCTIONS.md for setup changes
- Add examples for new features
- Include screenshots for UI changes

### API Documentation

Document service calls and events:

```yaml
# services.yaml
search:
  name: Search Plex Library
  description: Search your Plex library for media
  fields:
    query:
      name: Query
      description: Search query string
      required: true
      example: "Inception"
```

## Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Home Assistant Community**: For Home Assistant specific questions
- **Plex Forums**: For Plex API questions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Plex Search and Play! Your efforts help make this integration better for everyone. 🎬
