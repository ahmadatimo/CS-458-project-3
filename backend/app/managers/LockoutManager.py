from datetime import datetime, timedelta
from fastapi import HTTPException

class LockoutManager:
    def __init__(self, user, max_attempts=5, lockout_duration=timedelta(minutes=1)):
        self.user = user
        self.MAX_ATTEMPTS = max_attempts
        self.LOCKOUT_DURATION = lockout_duration

    def reset_lockout(self):
        """Reset the lockout mechanism for a user."""
        self.user["failed_attempts"] = 0
        self.user["lockout_time"] = None

    def check_lockout(self):
        """Check if the user is locked out and raise an exception if they are."""
        if self.user["lockout_time"] and datetime.now() < self.user["lockout_time"]:
            remaining_time = (self.user["lockout_time"] - datetime.now()).seconds
            raise HTTPException(status_code=403, detail=f"Too many failed attempts. Try again in {remaining_time} seconds.")

    def lockout_mechanism(self):
        """Lock out the user if they exceed the maximum failed attempts."""
        self.user["lockout_time"] = datetime.now() + self.LOCKOUT_DURATION
        self.check_lockout()