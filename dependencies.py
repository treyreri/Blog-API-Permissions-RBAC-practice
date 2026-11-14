from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User
from security import ALGORITHM, SECRET_KEY

DB = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    db: DB,
    token: Annotated[str, Depends(oauth2_scheme)], ) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials",
        headers={"WWW-Authenticate": "Bearer"}, )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_error

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_error

    return user





CurrentUser = Annotated[User, Depends(get_current_user)]
#авторизация : роли и права

USER_PERMISSIONS = {
    "posts:read",
    "posts:create",
    "posts:update",
    "posts:delete", }

MODERATOR_PERMISSIONS = USER_PERMISSIONS | {
    "posts:moderate", }

ADMIN_PERMISSIONS = MODERATOR_PERMISSIONS | {
    "posts:manage_any",
    "users:manage", }

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "user": USER_PERMISSIONS,
    "moderator": MODERATOR_PERMISSIONS,
    "admin": ADMIN_PERMISSIONS, }


def has_permission(user: User, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(user.role, set())


def require_permissions(*permissions: str):
    #требуется чтобы у пользователя были все указанные права

    def checker(current_user: CurrentUser) -> User:
        for permission in permissions:
            if not has_permission(current_user, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing permission: {permission}",
                )
        return current_user
    return checker


def require_roles(*roles: str):
    #Любую из указанных ролей

    def checker(current_user: CurrentUser) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="role is not allowed", )
        return current_user
    return checker