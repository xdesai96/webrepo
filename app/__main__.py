import uvicorn
from app.config import settings
from app.log import logger as app_logger


def main():
    """Main entry point for the application"""
    if not settings.validate():
        app_logger.error("Invalid configuration. Please check your .env file")
        return

    app_logger.info(f"Starting GitHub Modules Proxy server")
    app_logger.info(f"GitHub User: {settings.GITHUB_USER}")
    app_logger.info(f"GitHub Repo: {settings.GITHUB_REPO}")
    app_logger.info(f"GitHub Branch: {settings.GITHUB_BRANCH}")
    app_logger.info(f"Server will run on port: {settings.PORT}")

    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=settings.PORT,
            log_level=settings.LOG_LEVEL.lower(),
            reload=True,
        )
    except Exception as e:
        app_logger.error(f"Failed to start server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
