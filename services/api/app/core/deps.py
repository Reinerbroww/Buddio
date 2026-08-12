from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import PyJWTError
from app.core.database import get_db
from app.core.config import settings
from app.core.security import ALGORITHM
from app.schemas.token import TokenPayload
from app.models.user import User
from app.services.user_service import UserService   

security_scheme = HTTPBearer()

def get_current_user(
    token_credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau kedaluwarsa.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token_credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_payload = TokenPayload(sub=user_id)
    except PyJWTError:
        raise credentials_exception
        
    user_service = UserService(db)
    user = user_service.get_user_by_id(int(token_payload.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )
    return user
