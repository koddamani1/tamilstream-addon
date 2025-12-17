# TamilStream - Stremio Addon

## Overview

TamilStream is a Stremio addon focused on Tamil movies and series, with TorBox debrid service integration. It follows the MediaFusion-style architecture with FastAPI backend and a clean configuration UI.

## Project Structure

```
├── api/
│   ├── __init__.py          # Package init
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Settings and configuration
│   ├── models.py             # Pydantic data models
│   ├── stremio_routes.py     # Stremio addon protocol endpoints
│   ├── torbox_service.py     # TorBox API integration
│   ├── content_store.py      # JSON-based content storage
│   └── scraper.py            # Content scraper module
├── templates/
│   ├── configure.html        # Addon configuration page
│   └── install.html          # Installation instructions page
├── data/                     # Auto-generated content data
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel deployment configuration
└── README.md                # Project documentation
```

## Running the Application

```bash
uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload
```

## Key Features

1. **Stremio Addon Protocol** - Full implementation of manifest, catalog, meta, and stream endpoints
2. **TorBox Integration** - Debrid service for fast streaming
3. **Configuration UI** - User-friendly setup page
4. **Vercel Ready** - Optimized for serverless deployment

## Recent Changes

- Initial project setup with FastAPI
- Implemented Stremio addon protocol
- Added TorBox API integration
- Created configuration UI with Bootstrap 5
- Added Vercel deployment configuration

## User Preferences

- Tamil-focused content catalog
- TorBox as primary debrid service
- MediaFusion-inspired design
- GitHub + Vercel deployment target

## Development Notes

- Server runs on port 5000
- CORS enabled for all origins (Stremio requirement)
- Sample Tamil content included for testing
- JSON file storage for simplicity (can upgrade to MongoDB)
