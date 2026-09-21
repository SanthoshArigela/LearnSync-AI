from typing import Optional
from ..models.auth_models import LoginRequest, LoginResponse, UserModel

# Safe controlled demo credentials
DEMO_USERS = {
    "student@learnsync.ai": {
        "password": "student123",
        "role": "student",
        "user": UserModel(
            id="std_001",
            name="Santhosh",
            email="student@learnsync.ai",
            role="student"
        )
    },
    "faculty@learnsync.ai": {
        "password": "faculty123",
        "role": "faculty",
        "user": UserModel(
            id="fac_001",
            name="Prof. R. Sharma",
            email="faculty@learnsync.ai",
            role="faculty"
        )
    }
}

class AuthService:
    """
    Modular authentication service supporting demo credentials and extensible
    to real database/JWT authentication.
    """

    @staticmethod
    def authenticate(request: LoginRequest) -> LoginResponse:
        email = request.email.strip().lower()
        password = request.password.strip()
        role = request.role.strip().lower()

        if email not in DEMO_USERS:
            return LoginResponse(
                authenticated=False,
                message="Invalid email or password"
            )

        account = DEMO_USERS[email]

        if account["password"] != password:
            return LoginResponse(
                authenticated=False,
                message="Invalid email or password"
            )

        if account["role"] != role:
            return LoginResponse(
                authenticated=False,
                message=f"Account is registered as {account['role'].upper()}, not {role.upper()}"
            )

        return LoginResponse(
            authenticated=True,
            user=account["user"],
            message="Login successful"
        )
