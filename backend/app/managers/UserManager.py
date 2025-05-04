from datetime import datetime
from fastapi import HTTPException
from app.managers.LockoutManager import LockoutManager

class UserManager:
    def __init__(self, users_db):
        self.users_db = users_db  # Store the users_db for use in methods

    def validate_user_exists(self, email):
        """Check if the user exists in the database."""
        user = self.users_db.get(email)  # Use self.users_db
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email")
        return user

    def handle_lockout_expiry(self, user):
        """Reset the lockout if the lockout time has expired."""
        if user["lockout_time"] and datetime.now() > user["lockout_time"]:
            LockoutManager(user).reset_lockout()