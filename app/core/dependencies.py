from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.database import get_db
from app.db.models import User

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no existe")

    return user
