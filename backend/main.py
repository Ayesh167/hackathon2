from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import tasks
from app.routers import auth
from app.routers import chat
from app.database import create_tables
import os

# Create FastAPI app
app = FastAPI(title="Todo Web App API", version="1.0.0")

# CORS middleware - properly configured for production
# IMPORTANT: Update this list with your actual frontend domains when deploying
allowed_origins = [
    "http://localhost:3000",  # Local frontend development
    "http://localhost:3001",  # Alternative local frontend port
    # PRODUCTION: Replace with your actual Vercel domain before deploying
    # Example: "https://your-todo-app.vercel.app"
    "https://*.vercel.app",  # Allow all Vercel deployments
    # Add your custom domain if you have one
    # "https://yourdomain.com",
]

# Add the frontend URL from environment variable if provided
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow JWT to be sent back to client
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

@app.on_event("startup")
def on_startup():
    """Create tables on startup"""
    create_tables()

@app.get("/")
def read_root():
    return {"message": "Todo Web App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}