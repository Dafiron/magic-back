
#---------------------------------------------------#
def user_schema(user) -> dict:
    return  {
        "id":str(user["_id"]),
        "username":user["username"],
        "email":user["email"],
        "disable":user["disable"]
        }

#-------------------------------------------------#
def dias_a_dato_schema(dato)->dict:
    return{
        "id_accion":dato.id_accion,
        "ronda":int(dato.ronda),
        "hora":float(dato.hora),
        "votos":int(dato.votos),
        "propios":int(dato.propios),
        "uni":str(dato.uni),
        "año":int(dato.año),
        "dia":int(dato.dia),
    }

#---------------------------------------------------#

def float_to_str(hora: float) -> str:
    horas = int(hora)
    minutos = int((hora - horas)*100)
    return (f"{horas}:{minutos}:00")

#-------------------------------------------------#