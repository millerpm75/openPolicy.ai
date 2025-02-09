from fastapi import FastAPI
from api.routes.user_profiles import router as user_profiles_router

app = FastAPI()

# Include user profile routes
app.include_router(user_profiles_router)

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "API is running!"}
