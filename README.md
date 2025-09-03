# GitHub Modules Proxy

A FastAPI-based web application that serves Python modules from a GitHub repository with a clean web interface.

## Features

- 📁 Serves `.py` and `.txt` files directly from GitHub
- 🌐 Web interface for browsing available modules
- 🔍 Real-time GitHub API integration for module listing
- 📊 Detailed logging with file and line information
- ⚙️ Configurable via environment variables
- 🐳 Modular and scalable architecture

## Project Structure

```
webrepo/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── log.py            # Logging configuration
│   ├── main.py           # FastAPI application
│   └── __main__.py       # Application entry point
├── frontend/
│   └── dist/             # Frontend static files
│       └── assets/
├── .env                  # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd webrepo
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with the following variables:

```env
GITHUB_USERNAME=your_github_username
GITHUB_REPO=your_repository_name
GITHUB_BRANCH=main
PORT=8080
LOG_LEVEL=INFO
```

## Usage

### Development mode
```bash
python -m app
```

### Production mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Using directly with uvicorn
```bash
uvicorn app.main:app --reload --port 8080
```

## API Endpoints

- `GET /` - Web interface
- `GET /modules` - List all available Python modules
- `GET /config` - Show current configuration
- `GET /{module}.py` - Serve individual Python files

### Logging levels
- `DEBUG` - Detailed debug information
- `INFO` - General operational information
- `WARNING` - Warning messages
- `ERROR` - Error messages
