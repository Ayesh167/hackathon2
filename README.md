# Todo Fullstack Application

This is a full-stack todo application with AI assistant capabilities built using:
- Frontend: Next.js/React
- Backend: FastAPI
- Database: SQLite (with option for PostgreSQL)
- AI Integration: Google Gemini API

## Project Structure

```
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── vercel.json       # Vercel configuration for frontend deployment
└── README.md
```

## Deployment Instructions

### Frontend Deployment (Vercel)

1. Deploy the frontend to Vercel:
   - Go to [Vercel](https://vercel.com)
   - Connect to your GitHub repository
   - Select the `frontend` directory as the root
   - Add the following environment variables:
     - `NEXT_PUBLIC_API_URL`: URL of your deployed backend (e.g., `https://your-backend-app.herokuapp.com`)

### Backend Deployment Options

Deploy the backend to a platform that supports Python/FastAPI:

#### Option 1: Railway
1. Create a new app on [Railway](https://railway.app)
2. Connect to your GitHub repository
3. Select the `backend` directory
4. Add environment variables:
   - `DATABASE_URL`: Your database connection string
   - `SECRET_KEY`: Secret key for JWT tokens
   - `GEMINI_API_KEY`: Google Gemini API key

#### Option 2: Heroku
1. Create a new app on [Heroku](https://heroku.com)
2. Deploy using the Heroku CLI or GitHub integration
3. Configure environment variables in the Heroku dashboard

## Environment Variables

### Frontend (Vercel)
- `NEXT_PUBLIC_API_URL`: URL of the deployed backend API

### Backend
- `DATABASE_URL`: Database connection string (e.g., `sqlite:///./todo_app.db` or PostgreSQL URL)
- `SECRET_KEY`: Secret key for JWT token signing
- `GEMINI_API_KEY`: Google Gemini API key for AI features

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python create_tables.py
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Features

- User authentication (registration/login)
- Task management (CRUD operations)
- AI-powered assistant for natural language task management
- Chat interface for interacting with the AI assistant
- Responsive design for all device sizes

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

## Technologies Used

- **Frontend**: Next.js, React, Tailwind CSS
- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **Database**: SQLite (local), PostgreSQL (production-ready)
- **AI**: Google Gemini API
- **Authentication**: JWT tokens
- **Deployment**: Vercel (frontend), Railway/Heroku (backend)