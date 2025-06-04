# MCP-Surf

MCP-Surf is an educational project demonstrating a **Model Context Protocol (MCP)** architecture using **FastAPI**, **LangGraph**, and **tool calling**. It integrates with external APIs to provide **surf conditions** and **weather forecasts** for a given location and date.

## Features

- Query **surf data** (wave height, swell, tides, water temperature) using [WeatherAPI Marine API](https://www.weatherapi.com/docs/#marine-api).
- Query **weather forecasts** (temperature, rain, UV index, wind) using [WeatherAPI Forecast API](https://www.weatherapi.com/docs/#forecast-api).
- Integrated with **LangGraph** to simulate tool-based agent behavior.

## Requirements

- **Python** 3.8+
- [WeatherAPI key](https://www.weatherapi.com/)
- [OpenAI API key](https://platform.openai.com/)

> ✅ **Note**: Redis is no longer required — state is managed per session via `streamable_http`.

## Setup Instructions

### 1. Create and activate a virtual environment

**macOS/Linux**:

```bash
python -m venv venv
source venv/bin/activate
```

**Windows**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with the following:

```dotenv
WEATHERAPI_KEY=your_weatherapi_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the project

```bash
python -m __main__
```

You should see two services running:

- `http://localhost:8000` → Web API
- `http://localhost:9000` → MCP tool service

## Docker setup (alternative)

If you prefer using Docker:

### 1. Add your `.env` file

Same as above:

```dotenv
WEATHERAPI_KEY=your_weatherapi_key
OPENAI_API_KEY=your_openai_api_key
```

### 2. Build the docker image

```bash
docker build -t mcp-surf .
```

### 3. Run the container

```bash
docker run -it --rm -p 8000:8000 -p 9000:9000 --env-file .env mcp-surf
```

## Project structure

```text
mcp_surf/
├── config/               # App settings and environment loading
├── core/                 # Core models, logic, and shared utilities
├── services/
│   ├── web/              # Web-facing FastAPI service (message endpoint)
│   └── mcp/              # MCP agent tools and logic
├── __main__.py           # Entry point (launches both MCP and Web in parallel)
```

## Background

MCP-Surf simulates a **LangGraph tool agent** that dynamically selects tools to fulfill user requests based on natural language input. It highlights clean tool registration, session handling, and real-world API integrations in a structured FastAPI project.
