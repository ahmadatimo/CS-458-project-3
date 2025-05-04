from fastapi import APIRouter
from app.models.SurveyRequest import SurveyRequest
from app.managers.SurveyManager import SurveyManager

router = APIRouter()

@router.post("/survey")
async def submit_survey(survey_request: SurveyRequest):
    manager = SurveyManager(survey_request)
    return await manager.send_survey_email()