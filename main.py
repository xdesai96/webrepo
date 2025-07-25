from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
import aiohttp
import os

app = FastAPI()

GITHUB_USER = "xdesai96"
GITHUB_REPO = "modules"
GITHUB_BRANCH = "main"
GITHUB_RAW_BASE = (
    f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"
)
GITHUB_TREE_API = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/git/trees/{GITHUB_BRANCH}?recursive=1"

FRONTEND_DIST_DIR = os.path.join(os.path.dirname(__file__), "frontend", "master")


@app.middleware("http")
async def serve_github_py_txt(request: Request, call_next):
    path = request.url.path.lstrip("/")

    if path.endswith(".py") or path.endswith(".txt"):
        raw_url = f"{GITHUB_RAW_BASE}/{quote(path)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(raw_url) as response:
                if response.status == 200:
                    text = await response.text()
                    return PlainTextResponse(text, media_type="text/plain")
                return JSONResponse(
                    content={"error": f"GitHub file not found: {response.status}"},
                    status_code=response.status,
                )

    return await call_next(request)


@app.get("/modules")
async def list_modules():
    async with aiohttp.ClientSession() as session:
        async with session.get(GITHUB_TREE_API) as response:
            if response.status != 200:
                return JSONResponse(
                    {"error": f"GitHub API error: {response.status}"},
                    status_code=response.status,
                )
            data = await response.json()

    py_files = [
        item["path"]
        for item in data.get("tree", [])
        if item["path"].endswith(".py") and item["path"] != "full.txt"
    ]
    return {"modules": sorted(py_files)}


app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(FRONTEND_DIST_DIR, "assets")),
    name="assets",
)
app.mount("/", StaticFiles(directory=FRONTEND_DIST_DIR, html=True), name="static")
