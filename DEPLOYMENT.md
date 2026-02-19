# Space-API Development & Deployment Guide

## Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Space-API
```

### 2. Create Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment File
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run Development Server
```bash
python run.py
```

Server will start at `http://localhost:8000`

## Testing

### Run Tests
```bash
# All tests
pytest

# With coverage report
pytest --cov=src --cov-report=html
```

### Code Quality Checks
```bash
# Format check
black --check src/ tests/

# Linting
pylint src/

# Auto-format
black src/ tests/
```

## Docker Deployment

### Build Image
```bash
docker build -t space-api:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e SPACE_API_PASSWORD=yourpassword \
  -v $(pwd)/api.json:/app/api.json \
  space-api:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

## API Endpoints

### SpaceAPI Standard
- `GET /api.json` - Complete SpaceAPI-compliant configuration

### Reading Values
- `GET /api/get/<path>` - Get value from api.json
  - Example: `/api/get/state/open`

### Changing Values (GET)
- `GET /api/change/<path>?value=<value>` - Change value via GET parameter
  - Example: `/api/change/state/open?value=true`

### Changing Values (POST/PUT)
- `POST /api/post/<path>` with JSON body `{"value": <value>}`
  - Example: `POST /api/post/state/open` with `{"value": true}`

### Manual Override Interface
- `GET /manual-override` - HTML interface for manual control (password protected)

## Configuration

### Environment Variables
Create `.env` file based on `.env.example`:

```bash
# Flask Settings
DEBUG=False
FLASK_HOST=localhost
FLASK_PORT=8000
FLASK_SECRET_KEY=your-secret-key

# Space API
KEEP_ALIVE_TIMEOUT=30
SPACE_API_PASSWORD=admin123
```

## Keep-Alive System

The Keep-Alive system automatically closes the space after 30 seconds without receiving an "open" signal.

To keep space open:
```bash
# Send keep-alive heartbeat every 25 seconds
while true; do
  curl -X POST http://localhost:8000/api/post/state/open -H "Content-Type: application/json" -d '{"value": true}'
  sleep 25
done
```

## Project Structure

```
Space-API/
├── src/
│   ├── __init__.py
│   ├── app.py           # Flask application
│   └── config.py        # Configuration management
├── tests/
│   ├── conftest.py      # Pytest fixtures
│   ├── test_unit.py     # Unit tests
│   └── test_integration.py  # Integration tests
├── .github/
│   └── workflows/
│       └── ci.yml       # CI/CD Pipeline
├── api.json             # Space configuration
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
└── README.md            # Project documentation
```

## CI/CD Pipeline

The project includes a GitHub Actions CI pipeline that:
1. Runs tests on Python 3.10 and 3.11
2. Checks code quality with pylint and black
3. Generates coverage reports
4. Builds Docker image

Pipeline triggers on:
- Push to main/develop branches
- Pull requests to main/develop

## Troubleshooting

### Port Already in Use
```bash
# Change port in .env
FLASK_PORT=8001
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

### Permission Denied on Docker
```bash
# Use sudo or add user to docker group
sudo docker-compose up
```

## Security Notes

⚠️ **Production Security**:
1. Change default password: `SPACE_API_PASSWORD`
2. Generate secure secret key: `FLASK_SECRET_KEY`
3. Set `DEBUG=False`
4. Use HTTPS in production
5. Add input validation for all endpoints

## Support & Contact

For issues or questions, check the main README.md or contact the project maintainers.
