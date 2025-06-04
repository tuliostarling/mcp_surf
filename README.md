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
python __main__
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

## Request and response examples

### 1. Surf conditions

> ⚠️ **Note:** This project currently supports **Brazilian Portuguese** only. Prompts and tools are designed for it, and using other languages may lead to inaccurate results. To support another language, fork the project and update the prompts and tool definitions.

Request

```json
{
  "prompt": "As condições de surf em Maresias amanhã estão assim:\n\n- **Altura das ondas**: 1.0 m\n- **Direção do swell**: SSE\n- **Período do swell**: 16.2 s\n- **Temperatura da água**: 20.6 °C\n- **Vento**: 18.7 km/h, vindo do NE\n\nAs marés vão estar assim:\n- Baixa: 04:31 (0.52 m)\n- Alta: 10:48 (0.94 m)\n- Baixa: 17:03 (0.46 m)\n- Alta: 23:21 (0.99 m)\n\nParece que vai ter um mar tranquilo, mas com ondas razoáveis. Se você curte um surf mais leve, pode ser uma boa! Chega cedo pra evitar o crowd!"
}
```

Response

```json
{
  "response": "As condições de surf em Maresias amanhã indicam altura de onda de 1.3 metros, direção de swell vinda do sul e temperatura da água em torno de 25°C. Os ventos soprarão de leste com intensidade moderada. As marés variam ao longo do dia."
}
```

---

### 2. Weather forecast

Request

```json
{
  "prompt": "Vai chover em Florianópolis hoje?"
}
```

Response

```json
{
  "response": "Hoje em Florianópolis o tempo tá tranquilo, com sol e sem previsão de chuva. A temperatura tá em torno de 18,9°C e o vento tá leve, a 6,5 km/h. Então, pode surfar sossegado, sem preocupação com a chuva!"
}
```

---

### 3. Surf condition and Weather forecast

Request

```json
{
  "prompt": "Como estará o tempo e as ondas em Itacoatiara amanhã."
}
```

Response

```json
{
  "response": "As condições em Itacoatiara para amanhã, 5 de junho, estão assim:\n\n**Ondas:**\n- Altura das ondas: 0,7 m\n- Direção do swell: Leste\n- Período do swell: 0,1 s\n- Temperatura da água: 29,3 °C\n- Vento: 11,5 km/h, vindo do Leste\n\n**Maré:**\n- Baixa: 06:35 (0,84 m)\n- Alta: 12:03 (2,98 m)\n- Baixa: 19:11 (0,77 m)\n\n**Tempo:**\n- Previsão de chuvas leves nas proximidades\n- Temperatura: 26,1 °C\n- Umidade: 82%\n- Vento: 9,7 km/h\n- Índice UV: 2,2\n\nAs ondas estão pequenas, mas com um ventinho leve, pode ser uma boa para quem curte um surf mais tranquilo. Se você não se importa com a chuva, pode rolar um surf de boa!"
}
```
