# AI Analytics Dashboard

An AI-powered data analytics tool built with Python (FastAPI + Pandas) and Claude AI. Upload a CSV or Excel file and get automatic charts, statistics, and AI-powered insights in seconds.

## Features

- Upload CSV or Excel files
- Automatic chart generation (histogram, bar, pie, heatmap, line)
- AI-powered insights using Claude
- Natural language querying — ask questions about your data
- Column-level statistics
- Data preview table
- Sample data included

## Tech Stack

- **Backend:** Python, FastAPI, Pandas, Plotly, Anthropic Claude API
- **Frontend:** HTML, Tailwind CSS, Plotly.js

## Setup

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_key_here
```

Get your API key at: https://console.anthropic.com

### 3. Run the backend

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open the frontend

Open `frontend/index.html` in your browser.

Or serve it with Python:
```bash
cd frontend
python3 -m http.server 3000
```

Then visit http://localhost:3000

## Usage

1. Upload a CSV or Excel file (or click "Load sample data")
2. View automatic charts and statistics
3. Read AI-generated insights
4. Ask questions about your data in plain English

## API Endpoints

- `POST /api/upload` — Upload and analyse a file
- `POST /api/query` — Ask a question about the data
- `GET /api/health` — Health check
- `GET /docs` — Interactive API documentation
