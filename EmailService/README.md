A FastAPI application for managing email marketing campaigns using SendGrid as the email delivery service.

## Features

- User authentication with JWT
- Subscriber management
- Subscriber list management
- Campaign creation and scheduling
- Email sending using SendGrid
- Background tasks for email sending
- Campaign statistics tracking

## Installation

### Prerequisites

- Python 3.10+
- UV Package Manager
- PostgreSQL or SQLite

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/email-marketing-api.git
cd email-marketing-api
```

2. Set up a virtual environment and install dependencies using UV:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
uv pip install -e .
```

3. Create a `.env` file in the root directory:

```
# App settings
DATABASE_URL=sqlite:///./email_marketing.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/email_marketing

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SendGrid
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=your-verified-email@example.com
```

## Usage

1. Start the application:

```bash
uvicorn app.main:app --reload
```

2. Open your browser and go to http://localhost:8000/docs to see the Swagger documentation.

## API Endpoints

### Authentication
- POST `/api/v1/auth/login` - Login with email and password
- POST `/api/v1/auth/register` - Register new user

### Users
- GET `/api/v1/users/me` - Get current user information

### Subscribers
- POST `/api/v1/subscribers` - Create a new subscriber
- GET `/api/v1/subscribers` - Get all subscribers
- GET `/api/v1/subscribers/{subscriber_id}` - Get a specific subscriber
- PUT `/api/v1/subscribers/{subscriber_id}` - Update a subscriber

### Subscriber Lists
- POST `/api/v1/lists` - Create a new subscriber list
- GET `/api/v1/lists` - Get all subscriber lists
- GET `/api/v1/lists/{list_id}` - Get a specific list with its subscribers
- POST `/api/v1/lists/{list_id}/subscribers/{subscriber_id}` - Add a subscriber to a list
- DELETE `/api/v1/lists/{list_id}/subscribers/{subscriber_id}` - Remove a subscriber from a list

### Campaigns
- POST `/api/v1/campaigns` - Create a new campaign
- GET `/api/v1/campaigns` - Get all campaigns
- GET `/api/v1/campaigns/{campaign_id}` - Get a specific campaign
- PUT `/api/v1/campaigns/{campaign_id}` - Update a campaign
- POST `/api/v1/campaigns/test` - Send a test email for a campaign
- POST `/api/v1/campaigns/send` - Send a campaign to all subscribers in a list
- GET `/api/v1/campaigns/{campaign_id}/stats` - Get campaign statistics

## Background Tasks

The application uses FastAPI's background tasks to handle email sending asynchronously. This ensures that API endpoints remain responsive even when sending emails to large lists of subscribers.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app tests
isort app tests
```

### Type Checking

```bash
mypy app
```

alembic init alembic
