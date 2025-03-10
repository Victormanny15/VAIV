from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
import BackEnd.GlobalInfo.Keys as keys
import BackEnd.GlobalInfo.ResponseMessages as respuestas

if keys.dbconn==None:
    mongoConection =MongoClient(keys.strConnection)
    keys.dbconn=mongoConection[keys.strDBConnection]
    dbUsuarios = keys.dbconn['Usuarios']
    
def fnGetUsers():
    try:
        arrFinals =[]
        query=dbUsuarios.find()
        listUsuarios=list(query)
        if len(listUsuarios)!=0:
            for user in listUsuarios:
                objFormateado={
                    "id": str(user['_id']),
                    "nombre": user['Usuario'],
                    "pass":user['Contraseña'],
                }
                arrFinals.append(objFormateado)
        response=respuestas.succ200.copy()
        response['Respuesta']=arrFinals
        return jsonify(response)
    except Exception as e:
        print("Error en la funcion",e)
        return jsonify(respuestas.err500)

def fnGetUser(id):
    try:
        arrFinals =[]
        query=dbUsuarios.find({"_id":ObjectId(id)})
        listUsuarios=list(query)
        if len(listUsuarios)!=0:
            for user in listUsuarios:
                objFormateado={
                    "id": str(user['_id']),
                    "nombre": user['Usuario'],
                    "pass":user['Contraseña'],
                }
                arrFinals.append(objFormateado)
        response=respuestas.succ200.copy()
        response['Respuesta']=arrFinals
        return jsonify(response)
    except Exception as e:
        print("Error en la funcion",e)
        return jsonify(respuestas.err500)
    
def fnPostUser(data):
    try:
        query=dbUsuarios.insert_one({"Usuario":data.get('Usuario'),"Contraseña":data.get('Contraseña')})
        response=respuestas.succ200.copy()
        response['Respuesta']=True
        return jsonify(response)
    except Exception as e:
        print("Error en la funcion",e)
        return jsonify(respuestas.err500)
    
    

def fnLoginUser(data):
    try:
        usuario = data.get('Usuario')
        contraseña = data.get('Contraseña')

        # Buscar el usuario en la base de datos
        user = dbUsuarios.find_one({"Usuario": usuario})

        if user and user["Contraseña"] == contraseña:
            response = respuestas.succ200.copy()
            response["Respuesta"] = True
            response["Mensaje"] = "Inicio de sesión exitoso"
            response["Usuario"] = {
                "id": str(user["_id"]),
                "nombre": user["Usuario"]
            }
            return jsonify(response)

        return jsonify({"Respuesta": False, "Mensaje": "Usuario o contraseña incorrectos"})

    except Exception as e:
        print("Error en la función fnLoginUser", e)
        return jsonify(respuestas.err500)