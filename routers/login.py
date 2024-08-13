from fastapi import APIRouter, status, Depends, HTTPException
from components.models import User,Userdb, verification_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.client import db_client
from db.Schemas.schemas import user_schema
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

router= APIRouter(
    prefix="/login",
    tags=["login"],
    responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}}
    )

# Los datos de ususraio estan una una base de datos No relacional (Mongo db)

load_dotenv()

# Tipo de logaridmo
ALGORITHM = "HS256"

# Duracion del token en minutos
ACCESS_TOKEN_DURATION = 120

# Sistema de Autorización 
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Encriptacion
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Palabra secreta 
secret =os.getenv("SECRET")

# Cliente y localizacion los datos
data = db_client

# Funsion asyncrona que depende de la Autorizacion del oauth2 
# un token tiene todos los datos nesesarios para validad el cliente
# el token en este caso es de tipo Bearer
async def auth_user(token:str = Depends(oauth2)):
    # Exception ante la imposivilidad de valdidar 
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="No Autorizado",
        headers={"www-Authenticate":"Bearer"}
        )
    try:
        # Decodifica el token con el token, la palabra secreta y el tipo de logaritmo 
        user = jwt.decode(token, secret,algorithms=ALGORITHM)
        username = user.get("sub")
        if user is None:
            raise exception
        print(username)

    except JWTError:
        raise exception
    # Busca al ususario autenticado y lo debuelve de disct a una objeto tipo User
    user_db = data.find_one({"username": username})
    user_dict= user_schema(user_db)
    return User(**user_dict)

# Verifica si el usuario esta inactivo
async def current_user(user:User= Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo",
        )
    return user

# Post

@router.post("/on", response_model=User, status_code=status.HTTP_201_CREATED)
async def login_on(user:Userdb):

    user_dict= user.dict()
    # Encripta el password
    user_dict["password"] = crypt.hash(user_dict["password"])
    # Los mails simpre son en minuscula por combencion por eso pasa el ingreso de email a minuscula
    user_dict["email"] = str.lower(user_dict["email"])
    
    # Verifica mediente email su existencio o no
    verification_user(user_dict)
    
    # Elimina el id si lo tuviese por que mongodb genera uno automaticamnete
    if "id" in user_dict:
        del user_dict["id"]
    id= data.insert_one(user_dict).inserted_id

    # busca el nuevo ususario para devolverlo como respuesta
    new_user = user_schema(data.find_one({"_id":id}))
    return User(**new_user)

#post que busca el valida y genera el token con tiempo de validacion
@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Resive un Form y busca sobre el username
    user_db = data.find_one({"username":form.username})
    # Si no encontro exepccion 
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario no es correto"
            )
    # Se encontro pero al verificar el pasword no coincide, Exception 
    if not crypt.verify(form.password, user_db.get("password")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La contraseña no es correta"
            )
    # Genera token para un usuario con una expiracion programada 
    access_token = {
        "sub":user_db.get("username"),
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        }
    
    return {"access_token":jwt.encode(access_token,secret,algorithm=ALGORITHM ),"token_type":"bearer"}


# endpoint para verificar el token
@router.get("/verify-token")
async def verify_token(user: User = Depends(current_user)):
    return {"message": "Token is valid", "user": user.username}