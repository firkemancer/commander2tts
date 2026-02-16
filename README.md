# COMMANDER2TTS - Import Moxfield MTG Commander decklists into Tabletop Simulator

Commander2TTS is a simple SPA to import Moxfield MTG Commander decklists, tweak alternate card artworks and export decks into Tabletop Simulator compatible .JSON format.  
You don't need to setup anything! Just visit [Commander2TTS](https://firkemancer.github.io/commander2tts)!  
If you want to host it locally, check the [Quick Start](https://github.com/firkemancer/commander2tts?tab=readme-ov-file#quick-start) guide

## Features

- Import decks from Moxfield
- Manually search and add/remove cards
- Choose alternate card art
- Use custom image URLs (both alternate card art and back card art)
- Multiple deck management
- Export to Tabletop Simulator's custom object JSON format
- Local storage (no account needed)

## Quick Start

Simply clone the repository and run one of the following:

```bash
# Windows: Double-click start_server.py
# Or from command line:
python start_server.py

# Linux/Mac:
python3 start_server.py

# Linux - Bash Script:
./start_server.sh
```

The browser will open automatically to `http://localhost:8000/index.html`

### Manual Python Command
```bash
cd /path/to/folder
python -m http.server 8000  # Windows
python3 -m http.server 8000  # Linux/Mac
# Then open browser to: http://localhost:8000/index.html
```

## Why Do I Need a Server?

The HTML file needs to run on a web server (not just opened directly) because:
- **CORS restrictions**: Browsers block API requests from `file://` URLs
- **Moxfield import**: The Moxfield API import requires proper HTTP origin headers
- **Better compatibility**: Many features work better when served over HTTP

---

**Note**: Your deck data is saved in your browser's localStorage. It persists between sessions but is tied to the `localhost:8000` origin. If you change ports, you'll need to re-import your decks.
