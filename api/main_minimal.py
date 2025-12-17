from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="TamilStream Test")

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
        "description": "Tamil Movies & Series",
        "resources": ["catalog", "stream", "meta"],
        "types": ["movie", "series"],
        "catalogs": [],
        "idPrefixes": ["tt"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def home():
    return JSONResponse(content={"message": "TamilStream Addon"})
