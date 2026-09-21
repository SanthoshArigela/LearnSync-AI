from fastapi import APIRouter, HTTPException, status
from ..models.auth_models import LoginRequest, LoginResponse
from ..services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate a student or faculty user with controlled demo credentials.
    """
    response = AuthService.authenticate(request)
    if not response.authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.message or "Invalid credentials"
        )
    return response

@router.get("/me")
async def get_current_user():
    """
    Helper endpoint returning available demo roles.
    """
    return {
        "status": "online",
        "supported_roles": ["student", "faculty"],
        "demo_accounts": [
            {"role": "student", "email": "student@learnsync.ai"},
            {"role": "faculty", "email": "faculty@learnsync.ai"}
        ]
    }
