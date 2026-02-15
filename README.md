# COMMANDER2TTS - Server Setup Guide

## Quick Start

### Windows & Linux - Python Script (Recommended)
```bash
# Windows: Double-click start_server.py
# Or from command line:
python start_server.py

# Linux/Mac:
python3 start_server.py
```

The browser will open automatically to `http://localhost:8000/commander2tts.html`

### Linux - Bash Script
```bash
./start_server.sh
```

### Manual Python Command
```bash
cd /path/to/folder
python -m http.server 8000  # Windows
python3 -m http.server 8000  # Linux/Mac
# Then open browser to: http://localhost:8000/commander2tts.html
```

## Why Do I Need a Server?

The HTML file needs to run on a web server (not just opened directly) because:
- **CORS restrictions**: Browsers block API requests from `file://` URLs
- **Moxfield import**: The Moxfield API import requires proper HTTP origin headers
- **Better compatibility**: Many features work better when served over HTTP

## Troubleshooting

### Windows: Python Not Found
Install Python from https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Restart your computer after installation

### Linux: Python Not Found
Install Python 3:
- **Ubuntu/Debian**: `sudo apt install python3`
- **Fedora**: `sudo dnf install python3`
- **Arch**: `sudo pacman -S python`

### Port Already in Use
If you see "Address already in use", either:
1. Close any other programs using port 8000
2. Edit the scripts and change `PORT=8000` to a different number (e.g., `8001`, `8080`)

### Permission Denied (Linux/Mac)
Make the scripts executable:
```bash
chmod +x start_server.py
chmod +x start_server.sh
```

## Features

✅ Search cards from Scryfall  
✅ Import decks from Moxfield  
✅ Choose alternate card art  
✅ Custom image URLs (Imgur, etc.)  
✅ Filter by card type  
✅ Multiple deck management  
✅ Export to Tabletop Simulator JSON  
✅ Light/Dark mode  
✅ Local storage (no account needed)

## File Structure

```
your-folder/
├── commander2tts.html     # Main application
├── start_server.py        # Python server launcher (Windows/Linux/Mac)
├── start_server.sh        # Bash server launcher (Linux/Mac)
└── README.md             # This file
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

**Note**: Your deck data is saved in your browser's localStorage. It persists between sessions but is tied to the `localhost:8000` origin. If you change ports, you'll need to re-import your decks.
