import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.GITHUB_USER: str = os.getenv("GITHUB_USERNAME", "xdesai96")
        self.GITHUB_REPO: str = os.getenv("GITHUB_REPO", "modules")
        self.GITHUB_BRANCH: str = os.getenv("GITHUB_BRANCH", "main")
        self.PORT: int = int(os.getenv("PORT", 8080))
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

        self.GITHUB_RAW_BASE: str = (
            f"https://raw.githubusercontent.com/"
            f"{self.GITHUB_USER}/{self.GITHUB_REPO}/{self.GITHUB_BRANCH}"
        )
        self.GITHUB_TREE_API: str = (
            f"https://api.github.com/repos/"
            f"{self.GITHUB_USER}/{self.GITHUB_REPO}/git/trees/{self.GITHUB_BRANCH}?recursive=1"
        )

        self.FRONTEND_DIST_DIR: str = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "frontend", "dist"
        )

    def validate(self) -> bool:
        """Validate required settings"""
        required_vars = [self.GITHUB_USER, self.GITHUB_REPO, self.GITHUB_BRANCH]
        return all(required_vars)


settings = Settings()
