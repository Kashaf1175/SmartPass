# SmartPass - Smart Attendance Fraud Detection System

A comprehensive full-stack application for attendance tracking with machine learning-powered fraud detection.

## Features

- **User Authentication**: JWT-based authentication with role-based access (Admin/Student)
- **Real-time Attendance**: GPS location tracking and device fingerprinting
- **Fraud Detection**: ML-powered anomaly detection using Isolation Forest
- **Admin Dashboard**: Comprehensive analytics and fraud monitoring
- **Student Dashboard**: Simple attendance marking interface
- **RESTful API**: FastAPI backend with automatic documentation
- **Modern Frontend**: React.js with Tailwind CSS and responsive design

## Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database (SQLite for development)
- **Scikit-learn**: Machine learning for fraud detection
- **Pydantic**: Data validation and serialization

### Frontend
- **React.js**: Component-based UI framework
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server
- **Recharts**: Data visualization library
- **React Router**: Client-side routing

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Project Structure

```
SmartPass/
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── context/       # React context providers
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service functions
│   │   └── utils/         # Utility functions
│   └── package.json
├── server/                 # FastAPI backend
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Core functionality
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utility functions
│   ├── requirements.txt
│   └── alembic/           # Database migrations
├── ml/                     # Machine learning components
│   ├── models/            # Trained models
│   ├── preprocessing/     # Data preprocessing
│   ├── train.py           # Model training script
│   ├── predict.py         # Prediction functions
│   └── utils.py           # ML utilities
├── scripts/                # Utility scripts
│   ├── seed_data.py       # Database seeding
│   ├── run_migrations.py  # Database migrations
│   ├── train_model.py     # Model training
│   └── start_servers.py   # Development server starter
├── docker/                 # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── docs/                   # Documentation
    └── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartPass
   ```

2. **Setup Backend**
   ```bash
   cd server
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Frontend**
   ```bash
   cd ../client
   npm install
   ```

4. **Database Setup**
   ```bash
   cd ../scripts
   python run_migrations.py
   python seed_data.py
   ```

5. **Train ML Model**
   ```bash
   python train_model.py
   ```

6. **Start Development Servers**
   ```bash
   python start_servers.py
   ```

   Or start manually:
   ```bash
   # Terminal 1 - Backend
   cd server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd client
   npm run dev
   ```

7. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

### Key Endpoints

- `POST /auth/login` - User authentication
- `POST /auth/signup` - User registration
- `POST /attendance/mark` - Mark attendance
- `GET /attendance/history` - Get attendance history
- `GET /fraud/analytics` - Fraud detection analytics

## Configuration

### Environment Variables

Create a `.env` file in the server directory:

```env
DATABASE_URL=sqlite:///./smartpass.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database

The application supports both SQLite (development) and PostgreSQL (production).

## Testing

### Backend Tests
```bash
cd server
pytest
```

### Frontend Tests
```bash
cd client
npm test
```

## Deployment

### Production Docker Deployment

```bash
# Build production images
docker-compose -f docker-compose.yml up --build -d

# Scale services if needed
docker-compose up -d --scale backend=3
```

### Manual Deployment

1. Configure production database (PostgreSQL)
2. Set environment variables
3. Run database migrations
4. Train ML model on production data
5. Start servers with production settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the API documentation at `/docs`