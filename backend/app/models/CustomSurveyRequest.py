from pydantic import BaseModel, EmailStr
from typing import List, Dict, Union

class CustomSurveyRequest(BaseModel):
    questions: List[Dict]
    answers: Dict[str, Union[str, List[str]]]
    email: EmailStr

    model_config = {"use_enum_values": True}