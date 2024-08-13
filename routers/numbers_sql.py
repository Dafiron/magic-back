from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse, Response
from db.client import get_sql_connection
from components.models import Dias, search_uni_año_sql, search_iduni_ronda_sql
from db.Schemas.schemas import dias_a_dato_schema,float_to_str
from dotenv import load_dotenv
import os

router= APIRouter(
    prefix="/number",
    tags=["number"],
    responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}}
    )

load_dotenv()

DATABASE = os.getenv("db_sql_database")

# Los datos utiles estan en un sistema relacional "Mysql"  

# Get que pide todos los datos
@router.get("/all", status_code=status.HTTP_200_OK)
async def all():
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM numbers.acciones_numeros;"
                cursor.execute(query)
                result = cursor.fetchall()
                result_list= [row for row in result]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return result_list

# Get que pide de ingreso universidad y año

@router.get("/call_ua", status_code=status.HTTP_200_OK)
async def cal_ua(uni:str, año:int):
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = "CALL p_uni_año(%s,%s);"
                # metodo para evitar inyecciones  
                cursor.execute(query,(uni,año))
                result = cursor.fetchall()
                result_list= [row for row in result]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return result_list

# Get que pide de ingreso universidad, año y dia

@router.get("/call_uad", status_code=status.HTTP_200_OK)
async def call_uad(uni:str, año:int, dia:int):
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = "CALL p_uni_año_dia(%s, %s, %s);"
                # metodo para evitar inyecciones
                cursor.execute(query,(uni,año,dia))
                result = cursor.fetchall()
                result_list= [row for row in result]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return result_list


# Post para el ingreso de los datos a partir de un objeto de tipo Dias

@router.post("/on_numbers", status_code=status.HTTP_201_CREATED)
async def on_numbers(numero:Dias):
    result3 = None
    try:
        numero_dict = dias_a_dato_schema(numero)
        # Localiza el ID que corresponde a union del dia y el año 
        id_uni = search_uni_año_sql(numero_dict["uni"],numero_dict["año"])
        # Busca sobre la clave comformada por id_uni, la ronda y el dia
        result = search_iduni_ronda_sql(id_uni,numero_dict["ronda"],numero_dict["dia"])
        if not result:
            with get_sql_connection() as connection:
                with connection.cursor() as cursor:
                    query2 =(f"""
                            INSERT INTO {DATABASE}.acciones_numeros 
                            (ronda, hora, votos, propios, id_uni_año, dia)
                            VALUES (%s,%s,%s,%s,%s,%s);
                            """)
                    # metodo para evitar inyecciones
                    cursor.execute(
                        query2,(
                        numero_dict["ronda"],
                        float_to_str(numero_dict["hora"]),
                        numero_dict["votos"],
                        numero_dict["propios"],
                        id_uni,
                        numero_dict["dia"]
                        ))
                    connection.commit()
                    result3 = search_iduni_ronda_sql(id_uni,numero_dict["ronda"],numero_dict["dia"])
        else:
            result3 = result
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content= {"detail":"Ronda ingresada fue contabilizada"}
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    if result3 is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el resultado"
        )
    return  result3


# Actualizacion de datos

@router.put("/up_numbers", status_code=status.HTTP_200_OK)
async def up_numbers(numero:Dias):
    result3 = None
    try:
        # Ordena los datos
        numero_dict = dias_a_dato_schema(numero)
        # Localiza el ID que corresponde a union del dia y el año 
        id_uni = search_uni_año_sql(numero_dict["uni"],numero_dict["año"])
        # Busca sobre la clave comformada por id_uni, la ronda y el dia
        result = search_iduni_ronda_sql(id_uni,numero_dict["ronda"],numero_dict["dia"])
        if result:
            id_accion = result[0][-1]
            with get_sql_connection() as connection:
                with connection.cursor() as cursor:
                    query2 =(f"""
                            UPDATE {DATABASE}.acciones_numeros 
                            SET ronda = %s, hora = %s, votos = %s, propios = %s, id_uni_año = %s, dia = %s
                            WHERE id_accion = %s;
                            """)
                    # metodo para evitar inyecciones
                    cursor.execute(
                        query2,(
                        numero_dict["ronda"],
                        float_to_str(numero_dict["hora"]),
                        numero_dict["votos"],
                        numero_dict["propios"],
                        id_uni,
                        numero_dict["dia"],
                        id_accion
                        ))
                    connection.commit()
                    result3 = search_iduni_ronda_sql(id_uni,numero_dict["ronda"],numero_dict["dia"])
        else:
            result3 = None
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content= {"detail":"No se encontro el dato particular"}
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    if result3 is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el resultado"
        )
    return  result3

# Borrado a partir del dato entero

@router.delete("/del_numbers",status_code=status.HTTP_204_NO_CONTENT)
async def del_numbers(numero:Dias):
    try:
        # Ordena los datos
        numero_dict = dias_a_dato_schema(numero)
        # Localiza el ID que corresponde a union del dia y el año 
        id_uni = search_uni_año_sql(numero_dict["uni"],numero_dict["año"])
        # Busca sobre la clave comformada por id_uni, la ronda y el dia
        result = search_iduni_ronda_sql(id_uni,numero_dict["ronda"],numero_dict["dia"])
        if result:
            id_accion = result[0][-1]
            with get_sql_connection() as connection:
                with connection.cursor() as cursor:
                    query2 =(f"""
                        DELETE FROM {DATABASE}.acciones_numeros 
                        WHERE id_accion = %s;
                        """)
                    # metodo para evitar inyecciones
                    cursor.execute(query2,(id_accion,))
                    connection.commit()
                    print("Eliminacion realizada correctamente")
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={"detail": "Dato no encontrado en base de datos"}
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )

# Borrado a partir de los datos universidad, año, dia y ronda (estos datos jusntos no son repetibles)

@router.delete("/del_numbers_ronda",status_code=status.HTTP_204_NO_CONTENT)
async def del_numbers_ronda(uni:str, año:int,dia:int, ronda:int):
    try:
        # Localiza el ID que corresponde a union del dia y el año 
        id_uni = search_uni_año_sql(uni,año)
        # Busca sobre la clave comformada por id_uni, la ronda y el dia
        result = search_iduni_ronda_sql(id_uni,ronda,dia)
        if result:
            id_accion = result[0][-1]
            with get_sql_connection() as connection:
                with connection.cursor() as cursor:
                    query2 =(f"""
                        DELETE FROM {DATABASE}.acciones_numeros 
                        WHERE id_accion = %s;
                        """)
                    # metodo para evitar inyecciones
                    cursor.execute(query2,(id_accion,))
                    connection.commit()
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={"detail": "Dato no encontrado en base de datos"}
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
            )
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


