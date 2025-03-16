# Email Marketing API

A FastAPI application for managing email marketing campaigns using SendGrid as the email delivery service.

## Features

- Create and manage subscriber lists
- Add subscribers to lists
- Create email campaigns with HTML templates
- Send campaigns to subscriber lists
- Background processing for email delivery

## Installation

### Prerequisites

- Python 3.10+
- UV Package Manager
- PostgreSQL or SQLite

### Setup

1. Clone the repository:

```bash
git clone https://github.com/PIxelshift-Intern/Awasthi/
cd EmailService
```

2. Set up a virtual environment and install dependencies using UV:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

3. Create a `.env` file in the root directory:

```
# App settings
DATABASE_URL=postgresql://user:password@localhost/email_marketing

# SendGrid
SENDGRID_API_KEY=your-sendgrid-api-key
SENDGRID_FROM_EMAIL=your-verified-email@example.com
```

## Usage

1. Start the application:

```bash
uvicorn app.main:app --port 8000
```

## API Endpoints

### Create a Subscriber List

```bash
curl -X POST "http://localhost:8000/api/v1/lists?list_name={Test%20List20%name}" -H "Content-Type: application/json"
```

### Add a Subscriber

```bash
curl -X POST "http://localhost:8000/api/v1/subscribers" -H "Content-Type: application/json" -d '{"email":"example@example.com","name":"Test User","list_id":1}'
```

### Create a Campaign

```bash
curl -X POST "http://localhost:8000/api/v1/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Happy Holi",
    "subject": "Wishing You a Happy Holi",
    "body": "<!DOCTYPE html>...", 
    "list_id": 1
  }'
```

> Note: The HTML email template content has been abbreviated in this example. Include your full HTML email template when creating a campaign.

### Send a Campaign

```bash
curl -X POST "http://localhost:8000/api/v1/campaigns/{campaign_id}/send" -H "Content-Type: application/json"
```

## Background Tasks

The application uses FastAPI's background tasks to handle email sending asynchronously. This ensures that API endpoints remain responsive even when sending emails to large lists of subscribers.

## PowerShell Example

For Windows users, here's how to create a campaign using PowerShell:

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/campaigns" `
    -Method POST `
    -Headers @{ "Content-Type" = "application/json" } `
    -Body @"
{
    "name": "Campaign Name",
    "subject": "Email Subject Line",
    "body": "HTML Email Body",
    "list_id": 1
}
"@ `
    | Select-Object -ExpandProperty Content
```
