from fastapi import FastAPI
from auth.routes import router as auth_router
from analysis.routes import router as analysis_router
from fastapi.middleware.cors import CORSMiddleware
# Initialize the FastAPI application with a title and description
app = FastAPI(
    title="AI Resume & Job Match Assistant",
    description="An API for analyzing resumes against job descriptions."
)

# --- 2. ADD THIS MIDDLEWARE CONFIGURATION ---
# Define the list of origins that are allowed to make requests
origins = [
    "http://localhost:5173",  # The default address for Vite React apps
    "http://localhost:3000",  # A common address for Create React App
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allow origins listed above
    allow_credentials=True,     # Allow cookies to be included in requests
    allow_methods=["*"],        # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

# Include the authentication router
# A prefix makes all routes in this router start with /auth (e.g., /auth/login)
app.include_router(auth_router, prefix="/auth")

# Include the analysis router
# This contains the core AI logic endpoints like /analysis/ and /analysis/history
app.include_router(analysis_router)

# A simple root endpoint to confirm the API is running
@app.get("/")
def root():
    """
    Root endpoint to verify API status.
    """
    return {"message": "Welcome to the AI Resume & Job Match Assistant API!"}