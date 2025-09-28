# Messaging App API

A Django REST Framework messaging application with conversations and messages.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`

## API Endpoints

- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `POST /api/conversations/{id}/send_message/` - Send message to conversation
- `GET /api/messages/` - List user's messages

## Authentication

Use Django session authentication or basic authentication.