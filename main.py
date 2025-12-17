from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="TamilStream")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/manifest.json")
async def manifest():
    return {
        "id": "com.tamilstream.addon",
        "version": "1.0.0",
        "name": "TamilStream",
        "description": "Tamil Movies & Series Stremio Addon",
        "resources": ["catalog", "stream", "meta"],
        "types": ["movie", "series"],
        "catalogs": [
            {"id": "tamilstream_movies", "type": "movie", "name": "Tamil Movies"},
            {"id": "tamilstream_series", "type": "series", "name": "Tamil Series"}
        ],
        "idPrefixes": ["tt"],
        "behaviorHints": {"configurable": True, "configurationRequired": False}
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def home():
    return JSONResponse(content={"message": "TamilStream Addon - Install in Stremio"})

@app.get("/catalog/{type}/{id}.json")
async def catalog(type: str, id: str):
    return {"metas": []}

@app.get("/meta/{type}/{id}.json")
async def meta(type: str, id: str):
    return {"meta": None}

@app.get("/stream/{type}/{id}.json")
async def stream(type: str, id: str):
    return {"streams": []}
