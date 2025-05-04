from fastapi import HTTPException

class LoginManager:
    def __init__(self, user, password, lockout_manager):
        self.user = user
        self.password = password
        self.lockout_manager = lockout_manager

    def handle_failed_login(self):
        """Handle a failed login attempt."""
        self.user["failed_attempts"] += 1
        if self.user["failed_attempts"] >= self.lockout_manager.MAX_ATTEMPTS:
            self.lockout_manager.lockout_mechanism()
        raise HTTPException(status_code=401, detail="Invalid password. Try again.")

    def handle_successful_login(self):
        """Handle a successful login."""
        return {"message": "✅ Login successful!"}

    def validate_password_match(self):
        """Check if the provided password matches the user's password."""
        if self.password != self.user["password"]:
            self.handle_failed_login()