from fastapi import HTTPException

class PasswordValidator:
    @staticmethod
    def validate(password):
        """Validate the password against specific rules."""
        if len(password) <= 5:
            raise HTTPException(status_code=403, detail="Password must be at least 5 characters")
        if len(password) >= 15:
            raise HTTPException(status_code=403, detail="Password must be at most 15 characters")
        if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            raise HTTPException(status_code=403, detail="Password must contain numbers and letters")