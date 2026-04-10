# SmartPass API Documentation

## Overview

The SmartPass API provides endpoints for user authentication, attendance tracking, and fraud detection analytics.

## Authentication

All API endpoints except `/auth/login` and `/auth/signup` require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Authentication

#### POST /auth/signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "student"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAi...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "student"
  }
}
```

#### POST /auth/login
Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:** Same as signup

### Attendance

#### POST /attendance/mark
Mark attendance with location data.

**Request Body:**
```json
{
  "latitude": 37.422,
  "longitude": -122.084
}
```

**Response:**
```json
{
  "id": 1,
  "timestamp": "2024-01-01T09:00:00Z",
  "latitude": 37.422,
  "longitude": -122.084,
  "fraud_score": 0.15,
  "is_flagged": false
}
```

#### GET /attendance/history
Get user's attendance history.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 50)
- `offset` (optional): Number of records to skip (default: 0)

**Response:**
```json
{
  "total": 25,
  "records": [
    {
      "id": 1,
      "timestamp": "2024-01-01T09:00:00Z",
      "latitude": 37.422,
      "longitude": -122.084,
      "fraud_score": 0.15,
      "is_flagged": false
    }
  ]
}
```

### Fraud Detection (Admin Only)

#### GET /fraud/analytics
Get fraud detection analytics and statistics.

**Response:**
```json
{
  "total_records": 1000,
  "flagged_records": 45,
  "fraud_percentage": 4.5,
  "recent_flagged": [
    {
      "id": 123,
      "user_id": 5,
      "timestamp": "2024-01-01T09:00:00Z",
      "fraud_score": 0.85,
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  ],
  "fraud_trends": {
    "daily": [2, 5, 3, 8, 1, 4, 6],
    "weekly": [15, 22, 18, 25]
  }
}
```

#### GET /fraud/reports
Get detailed fraud reports with filtering.

**Query Parameters:**
- `start_date` (optional): Start date (ISO format)
- `end_date` (optional): End date (ISO format)
- `min_score` (optional): Minimum fraud score (0-1)
- `user_id` (optional): Filter by user ID

**Response:**
```json
{
  "total": 45,
  "reports": [
    {
      "id": 123,
      "user_id": 5,
      "user_email": "student1@example.com",
      "timestamp": "2024-01-01T09:00:00Z",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "device_id": "device-123",
      "ip_address": "192.168.1.100",
      "fraud_score": 0.85,
      "risk_factors": [
        "Unusual location",
        "Unusual time",
        "New device"
      ]
    }
  ]
}
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Rate Limiting

API endpoints are rate limited to prevent abuse:
- Authentication endpoints: 10 requests per minute
- Attendance endpoints: 30 requests per hour per user
- Analytics endpoints: 100 requests per hour

## Data Models

### User
```json
{
  "id": "integer",
  "email": "string",
  "role": "student|admin",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Attendance
```json
{
  "id": "integer",
  "user_id": "integer",
  "timestamp": "datetime",
  "latitude": "float",
  "longitude": "float",
  "device_id": "string",
  "ip_address": "string",
  "fraud_score": "float",
  "is_flagged": "boolean"
}
```

### Fraud Analytics
```json
{
  "total_records": "integer",
  "flagged_records": "integer",
  "fraud_percentage": "float",
  "recent_flagged": "array",
  "fraud_trends": "object"
}
```