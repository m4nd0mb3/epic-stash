# authorization.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token")

# Função para verificar e decodificar um token JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return username

# Função de autorização para verificar se o usuário possui permissões necessárias
async def check_authorization(username: str = Depends(get_current_user)):
    # Lógica de autorização aqui (por exemplo, verificar o usuário no banco de dados e suas permissões)
    authorized = True  # Substitua isso pela lógica real de autorização

    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return True
