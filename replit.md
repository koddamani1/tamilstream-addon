# TamilStream - Stremio Addon

## Overview

TamilStream is a Stremio addon focused on Tamil movies and series, with TorBox debrid service integration. It follows the MediaFusion-style architecture with FastAPI backend and a clean configuration UI.

## Project Structure

```
├── api/
│   ├── __init__.py           # Package init
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Settings and configuration
│   ├── models.py             # Pydantic data models
│   ├── stremio_routes.py     # Stremio addon protocol endpoints
│   ├── torbox_service.py     # TorBox API integration
│   ├── content_store.py      # PostgreSQL-based content storage
│   ├── db.py                 # SQLAlchemy database models
│   ├── metadata_service.py   # OMDb API for auto poster fetching
│   └── tamildhool_scraper.py # TamilDhool.tech content scraper
├── templates/
│   ├── configure.html        # Addon configuration page
│   └── install.html          # Installation instructions page
├── requirements.txt          # Python dependencies
└── vercel.json               # Vercel deployment configuration
```

## Running the Application

```bash
uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

### Stremio Protocol
- `GET /manifest.json` - Addon manifest
- `GET /catalog/{type}/{id}.json` - Content catalog
- `GET /meta/{type}/{id}.json` - Content metadata
- `GET /stream/{type}/{id}.json` - Stream sources

### Scraper API
- `GET /api/channels` - List available Tamil TV channels
- `GET /api/scrape/latest` - Get latest episodes from TamilDhool
- `GET /api/scrape/channel/{channel}` - Get shows from specific channel
- `POST /api/scrape/update` - Scrape all shows and update catalog

## Key Features

1. **Stremio Addon Protocol** - Full implementation with all endpoints
2. **TorBox Integration** - Debrid service for torrent-based content
3. **PostgreSQL Database** - Persistent storage for scraped content
4. **TamilDhool Scraper** - Automatic content discovery from tamildhool.tech
5. **Auto Poster Fetching** - OMDb API integration for movie posters
6. **Configuration UI** - User-friendly setup page

## Recent Changes (December 2024)

- Added PostgreSQL database for persistent storage
- Built TamilDhool scraper for Tamil TV series content
- Added OMDb API integration for automatic poster fetching
- Created scraper API endpoints
- Fixed episode streaming with proper ID parsing

## User Preferences

- Tamil-focused content catalog
- TorBox as primary debrid service for torrent content
- TamilDhool as source for Tamil TV series
- MediaFusion-inspired design
- GitHub + Vercel deployment target

## Development Notes

- Server runs on port 5000
- CORS enabled for all origins (Stremio requirement)
- PostgreSQL for persistent content storage
- OMDb API (free) for poster/metadata fetching
- TamilDhool scraper for TV series discovery
