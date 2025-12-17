from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
import os
import base64
import json

try:
    from fastapi.templating import Jinja2Templates
except ImportError:
    Jinja2Templates = None

from api.config import settings

try:
    from api.stremio_routes import router as stremio_router
    _stremio_routes_available = True
except Exception as e:
    stremio_router = None
    _stremio_routes_available = False
    import logging
    logging.error(f"Failed to import stremio_routes: {e}")

try:
    from api.tamildhool_scraper import (
        scrape_latest_episodes, scrape_show_list, scrape_all_shows,
        convert_to_stremio_format, CHANNELS
    )
    from api.content_store import add_content
    _scraper_available = True
except Exception:
    _scraper_available = False
    CHANNELS = {}
    scrape_latest_episodes = lambda x: []
    scrape_show_list = lambda x, y: []
    scrape_all_shows = lambda: []
    convert_to_stremio_format = lambda x: []
    add_content = lambda x: False

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
template_paths = [
    os.path.join(parent_dir, "templates"),
    os.path.join(current_dir, "..", "templates"),
    "templates",
    "/var/task/templates"
]

template_dir = None
for path in template_paths:
    if os.path.exists(path):
        template_dir = path
        break

if template_dir and Jinja2Templates:
    templates = Jinja2Templates(directory=template_dir)
else:
    templates = None

if stremio_router:
    app.include_router(stremio_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if templates:
        return templates.TemplateResponse("configure.html", {
            "request": request,
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "app_description": settings.app_description
        })
    return HTMLResponse(content=get_fallback_html(request), status_code=200)


@app.get("/configure", response_class=HTMLResponse)
async def configure(request: Request):
    if templates:
        return templates.TemplateResponse("configure.html", {
            "request": request,
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "app_description": settings.app_description
        })
    return HTMLResponse(content=get_fallback_html(request), status_code=200)


@app.post("/configure")
async def save_configure(request: Request):
    form_data = await request.form()
    
    config = {
        "torbox_api_key": form_data.get("torbox_api_key", ""),
        "quality_filter": form_data.getlist("quality_filter") or ["1080p", "HD", "4K"],
        "show_cam_quality": form_data.get("show_cam_quality") == "on"
    }
    
    config_str = base64.urlsafe_b64encode(json.dumps(config).encode()).decode().rstrip('=')
    
    host = request.headers.get("host", "localhost:5000")
    protocol = "https" if "vercel" in host or "https" in str(request.url) else "http"
    
    manifest_url = f"{protocol}://{host}/{config_str}/manifest.json"
    stremio_url = f"stremio://{host}/{config_str}/manifest.json"
    
    if templates:
        return templates.TemplateResponse("install.html", {
            "request": request,
            "app_name": settings.app_name,
            "manifest_url": manifest_url,
            "stremio_url": stremio_url,
            "config_str": config_str
        })
    return HTMLResponse(content=get_install_html(manifest_url, stremio_url), status_code=200)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}


@app.get("/api/scrape/latest")
async def scrape_latest():
    """Scrape latest episodes from TamilDhool"""
    episodes = scrape_latest_episodes(20)
    return {"count": len(episodes), "episodes": episodes}


@app.get("/api/scrape/channel/{channel}")
async def scrape_channel(channel: str):
    """Scrape shows from a specific channel"""
    if channel not in CHANNELS:
        return {"error": f"Unknown channel. Available: {list(CHANNELS.keys())}"}
    
    serials = scrape_show_list(channel, "serials")
    shows = scrape_show_list(channel, "shows")
    
    return {
        "channel": CHANNELS[channel]["name"],
        "serials_count": len(serials),
        "shows_count": len(shows),
        "serials": serials,
        "shows": shows
    }


@app.post("/api/scrape/update")
async def scrape_and_update():
    """Scrape all shows and update the content catalog"""
    all_shows = scrape_all_shows()
    stremio_content = convert_to_stremio_format(all_shows)
    
    added_count = 0
    for content in stremio_content:
        if add_content(content):
            added_count += 1
    
    return {
        "scraped": len(all_shows),
        "added": added_count,
        "message": "Content catalog updated with TamilDhool shows"
    }


@app.get("/api/channels")
async def list_channels():
    """List available channels"""
    return {"channels": CHANNELS}


@app.get("/{config}/configure", response_class=HTMLResponse)
async def configure_with_config(request: Request, config: str):
    try:
        padding = 4 - len(config) % 4
        if padding != 4:
            config += '=' * padding
        decoded = base64.urlsafe_b64decode(config.encode()).decode()
        existing_config = json.loads(decoded)
    except:
        existing_config = {}
    
    if templates:
        return templates.TemplateResponse("configure.html", {
            "request": request,
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "app_description": settings.app_description,
            "existing_config": existing_config
        })
    return HTMLResponse(content=get_fallback_html(request), status_code=200)


def get_fallback_html(request: Request):
    host = request.headers.get("host", "localhost:5000")
    protocol = "https" if "vercel" in host else "http"
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{settings.app_name} - Configure</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }}
        .card {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); }}
        .card, .form-control, .form-check-label, h1, p, label {{ color: #fff; }}
        .btn-primary {{ background: #e50914; border-color: #e50914; }}
        .btn-primary:hover {{ background: #b20710; }}
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="text-center mb-4">
                    <h1>{settings.app_name}</h1>
                    <p>{settings.app_description}</p>
                </div>
                <div class="card p-4">
                    <form method="POST" action="/configure">
                        <div class="mb-3">
                            <label class="form-label">TorBox API Key (Optional)</label>
                            <input type="password" class="form-control bg-dark text-white" name="torbox_api_key" placeholder="Your TorBox API key">
                            <small class="text-muted">Get your API key from <a href="https://torbox.app" target="_blank">torbox.app</a></small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Quality Preferences</label>
                            <div class="form-check"><input class="form-check-input" type="checkbox" name="quality_filter" value="4K" checked><label class="form-check-label">4K</label></div>
                            <div class="form-check"><input class="form-check-input" type="checkbox" name="quality_filter" value="1080p" checked><label class="form-check-label">1080p</label></div>
                            <div class="form-check"><input class="form-check-input" type="checkbox" name="quality_filter" value="HD" checked><label class="form-check-label">720p/HD</label></div>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Generate Install Link</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""


def get_install_html(manifest_url, stremio_url):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{settings.app_name} - Install</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }}
        .card {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); }}
        .card, h1, p, label, .form-control {{ color: #fff; }}
        .btn-primary {{ background: #e50914; border-color: #e50914; }}
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="text-center mb-4">
                    <h1>Install {settings.app_name}</h1>
                    <p>Your addon is ready to install!</p>
                </div>
                <div class="card p-4">
                    <div class="mb-4">
                        <a href="{stremio_url}" class="btn btn-primary btn-lg w-100">Install in Stremio</a>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Or copy this manifest URL:</label>
                        <input type="text" class="form-control bg-dark" value="{manifest_url}" readonly onclick="this.select()">
                    </div>
                    <p class="text-muted small">Open Stremio, go to Addons, click the puzzle icon, and paste the manifest URL.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
