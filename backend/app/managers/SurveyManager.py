from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.models.SurveyRequest import SurveyRequest
from app.database.surveys_db import surveys_db

class SurveyManager:
    def __init__(self, survey: SurveyRequest):
        self.survey = survey

    def validate_survey(self):
        if not self.survey.name_surname.strip():
            raise HTTPException(status_code=400, detail="Name-surname is required.")
        if not self.survey.beneficial_use.strip():
            raise HTTPException(status_code=400, detail="Beneficial use description is required.")

    def store_survey(self):
        surveys_db.append(self.survey.dict())

    async def send_survey_email(self):
        self.validate_survey()
        self.store_survey()

        print(f"Using email: {self.survey.email}, username: cs458tests@gmail.com, password: [hidden]")
        
        subject = "New AI Survey Submission"
        body = (
            f"Survey Submission Details:\n\n"
            f"Name-Surname: {self.survey.name_surname}\n"
            f"Birth Date: {self.survey.birth_date}\n"
            f"Education Level: {self.survey.education_level}\n"
            f"City: {self.survey.city}\n"
            f"Gender: {self.survey.gender}\n"
            f"AI Models: {', '.join(self.survey.ai_models)}\n"
            f"Defects: {self.survey.defects}\n"
            f"Beneficial Use: {self.survey.beneficial_use}\n"
        )

        conf = ConnectionConfig(
            MAIL_USERNAME="cs458tests",
            MAIL_PASSWORD="eowkuagnnvtgzwdj",  # Replace with App Password if using Gmail
            MAIL_FROM="cs458tests@gmail.com",
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True
        )

        message = MessageSchema(
            subject=subject,
            recipients=[self.survey.email],
            body=body,
            subtype="plain"
        )

        try:
            fm = FastMail(conf)
            await fm.send_message(message)
            return {"message": "Survey submitted, stored and email sent successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")