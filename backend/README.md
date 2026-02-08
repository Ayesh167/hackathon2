# Todo Web App Backend

This is the FastAPI backend for the Todo Web App with AI assistant capabilities.

## Features

- User authentication (registration/login)
- Task management (CRUD operations)
- AI-powered assistant for natural language task management
- Chat interface with conversation history
- JWT-based authentication
- SQLModel for database operations

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user details

### Tasks
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task

### Chat
- `POST /api/chat` - Send message to AI assistant
- `GET /api/conversations` - Get user's conversations
- `GET /api/conversations/{id}` - Get specific conversation

## Deployment

This backend is designed to be deployed on platforms that support Python/WSGI applications:

### Railway
1. Create a new app on [Railway](https://railway.app)
2. Connect to your GitHub repository
3. Add environment variables:
   - `DATABASE_URL`: Your database connection string
   - `SECRET_KEY`: Secret key for JWT tokens
   - `GEMINI_API_KEY`: Google Gemini API key

### Heroku
1. Create a new app on [Heroku](https://heroku.com)
2. Deploy using the Heroku CLI or GitHub integration
3. Configure environment variables in the Heroku dashboard

### Environment Variables Required
- `DATABASE_URL`: Database connection string (e.g., `sqlite:///./todo_app.db` or PostgreSQL URL)
- `SECRET_KEY`: Secret key for JWT token signing (generate a strong random key)
- `GEMINI_API_KEY`: Google Gemini API key for AI features
- `NEXT_PUBLIC_API_URL`: URL where the backend is hosted (for cross-origin requests)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create database tables
python create_tables.py

# Run the application
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLModel (with SQLAlchemy and SQLite/PostgreSQL)
- **Authentication**: JWT tokens with python-jose
- **Password hashing**: passlib with bcrypt
- **AI Integration**: Google Gemini API
- **Deployment**: Designed for containerized environments