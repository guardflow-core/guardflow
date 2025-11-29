# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Development Commands

### Backend (FastAPI) - Port 8002

```bash
# Navigate to backend directory
cd backend

# Install dependencies
python -m pip install -r requirements.txt

# Run development server
uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload

# Run with PowerShell virtual environment (Windows)
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8002 --reload
```

### Frontend (React) - Port 3000

```bash
# Navigate to frontend directory
cd guardflow-web

# Install dependencies
npm install

# Run development server
npm start
```

### Mobile (React Native)

```bash
# Navigate to mobile directory
cd mobile-app

# Install dependencies
npm install

# Run Android
npx react-native run-android

# Run iOS
npx react-native run-ios
```

### Database & Services (Docker)

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Testing

```bash
# Run all backend tests
cd backend
pytest

# Run specific test
pytest backend/tests/test_health.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run a single test function
pytest backend/tests/test_health.py::test_health_endpoint -v
```

### API Documentation

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

## High-Level Architecture

### System Overview

GuardFlow is a smart checkout system for retail that integrates:
1. **AI Scanner** - Product recognition using Google Vision API
2. **Payment Processing** - PIX instant payments via Mercado Pago
3. **ESG System** - Sustainability metrics and tokenization
4. **Government Monetization** - Tax credits and fiscal incentives

### Project Structure

```
GuardFlow/
├── backend/                 # FastAPI backend (Python 3.11)
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core business logic
│   │   ├── models/         # SQLAlchemy models
│   │   └── main.py         # FastAPI app entry point
│   └── tests/              # Backend tests
├── guardflow-web/          # React web dashboard
├── mobile-app/             # React Native mobile app
├── sdk/                    # JavaScript SDK
└── docker-compose.yml      # Local services setup
```

### Key Technologies

- **Backend**: FastAPI, SQLAlchemy, Pydantic, JWT authentication
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache**: Redis
- **Frontend**: React 18.2, Material-UI
- **Mobile**: React Native 0.72.6
- **AI/Vision**: Google Cloud Vision API
- **Payments**: Mercado Pago SDK

### Authentication Flow

1. Login via POST `/api/v1/auth/login` with email/password
2. Receive JWT access token
3. Include token in Authorization header: `Bearer YOUR_TOKEN`
4. Token-based authentication for all protected endpoints

### Development Workflow

1. **Initial Setup**:
   ```bash
   # Start backend
   cd backend && uvicorn app.main:app --port 8002 --reload
   
   # Login and get token
   # Use Swagger UI at http://localhost:8002/docs
   ```

2. **Populate Test Data**:
   ```bash
   # Via Swagger UI after authentication:
   POST /api/v1/scanner/populate-products
   POST /api/v1/stores/populate-stores
   ```

3. **Test Purchase Flow**:
   - GET `/api/v1/stores/` - List stores
   - GET `/api/v1/cart/?store_id={id}` - Get/create cart
   - GET `/api/v1/stores/{store_id}/products` - List products
   - POST `/api/v1/cart/add` - Add items
   - POST `/api/v1/payment/create-pix` - Create payment
   - GET `/api/v1/payment/status/{transaction_id}` - Check status

### Database Configuration

- **Development**: SQLite (`backend/guardflow_dev.db`)
- **Production**: PostgreSQL via Docker or cloud service
- **Migrations**: Alembic (run `alembic upgrade head`)

### API Versioning

All API endpoints are versioned under `/api/v1/`. Major endpoints include:

- `/api/v1/scanner/*` - Product scanning
- `/api/v1/cart/*` - Shopping cart management
- `/api/v1/payment/*` - Payment processing
- `/api/v1/stores/*` - Store management
- `/api/v1/esg/*` - ESG metrics and gamification
- `/api/v1/monetization/*` - Government monetization

### Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./guardflow_dev.db
SECRET_KEY=your-secret-key-here
GOOGLE_VISION_API_KEY=your-google-vision-key
MERCADO_PAGO_ACCESS_TOKEN=your-mp-token
```

### Error Handling

The API uses consistent error responses:
```json
{
  "success": false,
  "message": "Error description",
  "status_code": 400
}
```

### Performance Considerations

- Redis caching for session management
- Async SQLAlchemy queries for database operations
- Background tasks via Celery for heavy operations
- Rate limiting with SlowAPI

### Integration Points

GuardFlow integrates with:
- **ecosystem-gst**: Smart contracts for GST tokens
- **ecosystem-degov**: Rust backend for ESG token ecosystem
- **Google Vision API**: Product recognition
- **Mercado Pago**: Payment processing

## Development Tips

### Local Development with SQLite

When using SQLite for local development, UUID fields are stored as strings. The codebase handles this automatically, but be aware when debugging.

### Testing Authentication

1. Use the Swagger UI at http://localhost:8002/docs
2. Click "Authorize" button
3. Enter: `Bearer YOUR_ACCESS_TOKEN`
4. All authenticated endpoints will now work

### Port Configuration

Default ports:
- Backend API: 8002
- Frontend Web: 3000
- PostgreSQL: 5432
- Redis: 6379

### Quick Debugging

```bash
# Check if backend is running
curl http://localhost:8002/health

# Check available products
curl http://localhost:8002/api/v1/retail/products

# View SQLite database
sqlite3 backend/guardflow_dev.db ".tables"
```