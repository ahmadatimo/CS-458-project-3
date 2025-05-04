from app.managers.UserManager import UserManager
from app.managers.LoginManager import LoginManager
from app.managers.PasswordValidator import PasswordValidator
from app.managers.LockoutManager import LockoutManager
from app.database.users_db import users_db

class AuthManager:
    def __init__(self):
        self.user_manager = UserManager(users_db)
        self.password_validator = PasswordValidator()

    def process_login(self, email, password):
        """Process the login logic."""
        user = self.user_manager.validate_user_exists(email)
        self.user_manager.handle_lockout_expiry(user)

        lockout_manager = LockoutManager(user)
        lockout_manager.check_lockout()

        self.password_validator.validate(password)

        login_manager = LoginManager(user, password, lockout_manager)
        login_manager.validate_password_match()

        return login_manager.handle_successful_login()