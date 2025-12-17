from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import base64
import json

from api.config import settings
from api.stremio_routes import router as stremio_router
from api.content_store import initialize_sample_data

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

templates = Jinja2Templates(directory="templates")

app.include_router(stremio_router)


@app.on_event("startup")
async def startup_event():
    initialize_sample_data()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("configure.html", {
        "request": request,
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_description": settings.app_description
    })


@app.get("/configure", response_class=HTMLResponse)
async def configure(request: Request):
    return templates.TemplateResponse("configure.html", {
        "request": request,
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_description": settings.app_description
    })


@app.post("/configure")
async def save_configure(request: Request):
    form_data = await request.form()
    
    config = {
        "torbox_api_key": form_data.get("torbox_api_key", ""),
        "quality_filter": form_data.getlist("quality_filter") or ["1080p", "HD", "4K"],
        "show_cam_quality": form_data.get("show_cam_quality") == "on"
    }
    
    config_str = base64.urlsafe_b64encode(json.dumps(config).encode()).decode()
    
    host = request.headers.get("host", "localhost:5000")
    protocol = "https" if "https" in str(request.url) else "http"
    
    manifest_url = f"{protocol}://{host}/{config_str}/manifest.json"
    stremio_url = f"stremio://{host}/{config_str}/manifest.json"
    
    return templates.TemplateResponse("install.html", {
        "request": request,
        "app_name": settings.app_name,
        "manifest_url": manifest_url,
        "stremio_url": stremio_url,
        "config_str": config_str
    })


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}


@app.get("/{config}/configure", response_class=HTMLResponse)
async def configure_with_config(request: Request, config: str):
    try:
        decoded = base64.urlsafe_b64decode(config.encode()).decode()
        existing_config = json.loads(decoded)
    except:
        existing_config = {}
    
    return templates.TemplateResponse("configure.html", {
        "request": request,
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_description": settings.app_description,
        "existing_config": existing_config
    })
