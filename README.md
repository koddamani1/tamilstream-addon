# TamilStream - Stremio Addon

A Stremio addon for Tamil movies and series with TorBox debrid integration.

## Features

- Tamil Movies & Series catalog
- TorBox debrid service integration
- Multiple quality options (4K, 1080p, 720p)
- Automatic content updates
- Fast cached streams
- Clean configuration UI

## Installation

### Prerequisites

- Python 3.11+
- TorBox account with API key

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tamilstream.git
cd tamilstream
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 5000 --reload
```

4. Open http://localhost:5000 in your browser

### Deploy to Vercel

1. Fork this repository to your GitHub account

2. Go to [Vercel](https://vercel.com) and sign in with GitHub

3. Click "Add New Project" and select your forked repository

4. Vercel will auto-detect the configuration - click "Deploy"

5. Your addon will be available at `https://your-project.vercel.app`

## Configuration

1. Visit your deployed addon URL (or localhost:5000 for local)
2. Enter your TorBox API key (get it from https://torbox.app/settings)
3. Select quality preferences
4. Click "Generate Addon Link"
5. Click "Open in Stremio App" or copy the manifest URL

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Configuration page |
| `GET /manifest.json` | Stremio manifest |
| `GET /catalog/{type}/{id}.json` | Content catalog |
| `GET /meta/{type}/{id}.json` | Content metadata |
| `GET /stream/{type}/{id}.json` | Available streams |
| `GET /health` | Health check |

## Project Structure

```
tamilstream/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── stremio_routes.py    # Stremio addon endpoints
│   ├── torbox_service.py    # TorBox API integration
│   ├── content_store.py     # Content storage
│   └── scraper.py           # Content scraper
├── templates/
│   ├── configure.html       # Configuration page
│   └── install.html         # Installation page
├── data/                    # Content data (auto-generated)
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel deployment config
└── README.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_SECRET` | Session encryption key | Auto-generated |
| `MONGODB_URI` | MongoDB connection string (optional) | None |

## Tech Stack

- **Backend**: FastAPI (Python)
- **Templates**: Jinja2
- **Styling**: Bootstrap 5
- **Debrid**: TorBox API
- **Deployment**: Vercel Serverless

## License

MIT License

## Disclaimer

This addon is for educational purposes only. Users are responsible for ensuring they have the right to access any content. The developers do not host or distribute any copyrighted content.
