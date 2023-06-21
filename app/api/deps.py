import time
from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import auth_jwt, config
from app.core.session import async_session
from app.models import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[auth_jwt.JWT_ALGORITHM]
        )
    except jwt.DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        ) from e
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = auth_jwt.JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    if user := result.scalars().first():
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found.")
