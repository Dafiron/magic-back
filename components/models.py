from pydantic import BaseModel
from fastapi import HTTPException, status
from db.client import db_client, get_sql_connection
from typing import Optional

# Modelo de ususario sin password
class User (BaseModel):
    id:str | None = None
    username:str
    email:str
    disable:bool = False

# Modelo de usuario con password
class Userdb(User):
    password:str

# Modelo de datos

class Dias(BaseModel):
    id_accion:Optional [int] = None
    ronda: int
    hora: float
    votos: int
    propios: int
    uni: str
    año: int
    dia: int



def search_user_db(user_dict:str):
    user = db_client.find_one({"email": user_dict["email"]})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no fue encontrado"
            )
    return User(**user)

# Verifica que el usuario no este ingresado
def verification_user(user_dict: dict):
    user = db_client.find_one({"email": user_dict["email"]})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
            )



#-------------------------------------------------------------#
def search_uni_año_sql(uni:str, año:int):
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query2 = "CALL p_search_id_uni_año (%s,%s);"
                # metodo para evitar inyecciones
                cursor.execute(query2,(uni,año))
                result = cursor.fetchone()
                print("search_uni_año_sql:",result)
                if result:
                    return result[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return result

#-------------------------------------------------------------------------------------#
def search_iduni_ronda_sql(id_uni:int,ronda:int, dia:int):
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = ("""SELECT uni,año,dia,ronda,hora,votos,propios,id_accion
                FROM acciones_numeros 
                INNER JOIN uni_año 
                ON acciones_numeros.id_uni_año = uni_año.id_uni_año
                WHERE uni_año.id_uni_año = %s
                AND acciones_numeros.ronda = %s
                AND acciones_numeros.dia = %s;""")
                # metodo para evitar inyecciones
                cursor.execute(query,(id_uni,ronda,dia))
                result = cursor.fetchall()
                print(f"resultado1 :{result}")
    except Exception as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
        )
    return result
#-----------------------------------------------------------------------------------#