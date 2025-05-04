from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.login import router as login_router
from app.routes.survey import router as survey_router

app = FastAPI()

# Allow CORS for your frontend origin
origins = [
    "http://localhost:3000",  # frontend URL
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"message": "YA halal Wallah"}

# Include login routes
app.include_router(login_router)
app.include_router(survey_router)