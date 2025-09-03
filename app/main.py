from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
import aiohttp
import os

from app.config import settings
from app.log import logger as app_logger

app = FastAPI(title="GitHub Modules Proxy", version="1.0.0")

if not os.path.exists(settings.FRONTEND_DIST_DIR):
    app_logger.warning(f"Frontend directory not found: {settings.FRONTEND_DIST_DIR}")
    os.makedirs(settings.FRONTEND_DIST_DIR, exist_ok=True)


@app.middleware("http")
async def serve_github_py_txt(request: Request, call_next):
    path = request.url.path.lstrip("/")

    if path.endswith(".py") or path.endswith(".txt"):
        raw_url = f"{settings.GITHUB_RAW_BASE}/{quote(path)}"
        app_logger.info(f"Fetching from GitHub: {raw_url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(raw_url) as response:
                    if response.status == 200:
                        text = await response.text()
                        app_logger.info(f"Successfully fetched: {path}")
                        return PlainTextResponse(text, media_type="text/plain")

                    app_logger.warning(
                        f"File not found on GitHub: {path} (Status: {response.status})"
                    )
                    return JSONResponse(
                        content={"error": f"GitHub file not found: {response.status}"},
                        status_code=response.status,
                    )
        except aiohttp.ClientError as e:
            app_logger.error(f"Network error fetching {path}: {str(e)}")
            return JSONResponse(
                content={"error": f"Network error: {str(e)}"}, status_code=500
            )
        except Exception as e:
            app_logger.error(f"Unexpected error fetching {path}: {str(e)}")
            return JSONResponse(
                content={"error": f"Unexpected error: {str(e)}"}, status_code=500
            )

    return await call_next(request)


@app.get("/modules")
async def list_modules():
    app_logger.info("Fetching module list from GitHub API")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(settings.GITHUB_TREE_API) as response:
                if response.status != 200:
                    app_logger.error(f"GitHub API error: {response.status}")
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

        app_logger.info(f"Found {len(py_files)} Python modules")
        return {"modules": sorted(py_files)}

    except aiohttp.ClientError as e:
        app_logger.error(f"Network error fetching modules: {str(e)}")
        return JSONResponse({"error": f"Network error: {str(e)}"}, status_code=500)
    except Exception as e:
        app_logger.error(f"Unexpected error fetching modules: {str(e)}")
        return JSONResponse({"error": f"Unexpected error: {str(e)}"}, status_code=500)


@app.get("/config")
async def show_config():
    """Show current configuration (for debugging)"""
    return {
        "github_user": settings.GITHUB_USER,
        "github_repo": settings.GITHUB_REPO,
        "github_branch": settings.GITHUB_BRANCH,
        "port": settings.PORT,
    }


app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(settings.FRONTEND_DIST_DIR, "assets")),
    name="assets",
)
app.mount(
    "/", StaticFiles(directory=settings.FRONTEND_DIST_DIR, html=True), name="static"
)
