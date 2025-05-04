from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict
from datetime import date
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class SurveyRequest(BaseModel):
    name_surname: str
    birth_date: date
    education_level: str
    city: str
    gender: GenderEnum
    ai_models: List[str]
    defects: Dict[str, str] = Field(default_factory=dict)
    beneficial_use: str
    email: EmailStr

    model_config = {"use_enum_values": True}  # Updated for Pydantic 2.x