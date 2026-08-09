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

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload and analyse a file |
| `POST` | `/api/query` | Ask a question about the data |
| `GET`  | `/api/health` | Health check |
| `GET`  | `/docs` | Interactive API documentation |

## Architecture

The backend exposes a REST API built with FastAPI. Uploaded files are parsed with Pandas, statistics and charts are generated server-side with Plotly, and Claude generates natural-language insights from the processed data. The frontend is a lightweight HTML/Tailwind interface that renders the charts and handles the query flow.

## Author

Built by **Enoch Sagini** — Full-Stack & AI Engineer.
Portfolio: [sagini.me](https://sagini.me) · GitHub: [@IamSagini](https://github.com/IamSagini)
