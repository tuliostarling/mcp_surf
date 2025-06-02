# MCP-Surf

This project is designed for educational purposes, demonstrating an Model Context Protocol (MCP) architecture using FastAPI with integrations to weather and surf condition APIs.

## Features

- Surf conditions from WeatherAPI
- Weather forecasts from WeatherAPI

## Requirements

- **Python**: 3.8+
- **Redis**: for session management (install and run a local redis server)

## Setup instructions

### 1. Install Python and Redis

- Make sure you have **Python 3.8+** installed.
- Install and run **Redis**:
  - On macOS: `brew install redis && brew services start redis`
  - On Ubuntu/Debian: `sudo apt install redis && sudo systemctl start redis`
  - On Windows: Install Redis using [Memurai](https://www.memurai.com/) or [Redis on Windows](https://github.com/microsoftarchive/redis).

### 2. Create and activate virtual environment (venv)

For macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add API keys to `.env`

```dotenv
WEATHERAPI_KEY=your_weatherapi_key
OPENAI_API_KEY=your_openai_api_key
```

### 5. Start the application

```bash
python -m __main__
```
