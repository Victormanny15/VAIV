from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
import BackEnd.GlobalInfo.Keys as keys
import BackEnd.GlobalInfo.ResponseMessages as respuestas

if keys.dbconn==None:
    mongoConection =MongoClient(keys.strConnection)
    keys.dbconn=mongoConection[keys.strDBConnection]
    dbUsuarios = keys.dbconn['Usuarios']
    dbLeds = keys.dbconn['Leds']
    
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
    
def fnSetLedStateById(led_id):
    try:
        data = request.get_json()  # Obtener datos JSON de la solicitud

        new_status = data.get("status")  # Nuevo estado (True/False)

        if new_status is None:
            return jsonify({"Respuesta": False, "Mensaje": "El campo 'status' es obligatorio"}), 400

        # Convertir el ID a ObjectId y actualizar el estado en la base de datos
        result = dbLeds.update_one(
            {"_id": ObjectId(led_id)},
            {"$set": {"status": new_status}}
        )

        if result.matched_count == 0:
            return jsonify({"Respuesta": False, "Mensaje": "LED no encontrado"}), 404

        response = respuestas.succ200.copy()
        response["Mensaje"] = f"Estado del LED {led_id} actualizado a {new_status}"
        return jsonify(response)

    except Exception as e:
        print("Error en la función fnSetLedStateById", e)
        return jsonify(respuestas.err500)
    
def fnSetLedStateTrueById(led_id):
    try:
        # Actualizar el estado del LED a True
        result = dbLeds.update_one(
            {"_id": ObjectId(led_id)},
            {"$set": {"status": True}}
        )

        if result.matched_count == 0:
            return jsonify({"Respuesta": False, "Mensaje": "LED no encontrado"}), 404

        response = respuestas.succ200.copy()
        response["Mensaje"] = f"Estado del LED {led_id} actualizado a True"
        return jsonify(response)

    except Exception as e:
        print("Error en la función fnSetLedStateTrueById", e)
        return jsonify(respuestas.err500)
def fnSetLedStateFalseById(led_id):
    try:
        # Actualizar el estado del LED a False
        result = dbLeds.update_one(
            {"_id": ObjectId(led_id)},
            {"$set": {"status": False}}
        )

        if result.matched_count == 0:
            return jsonify({"Respuesta": False, "Mensaje": "LED no encontrado"}), 404

        response = respuestas.succ200.copy()
        response["Mensaje"] = f"Estado del LED {led_id} actualizado a False"
        return jsonify(response)

    except Exception as e:
        print("Error en la función fnSetLedStateFalseById", e)
        return jsonify(respuestas.err500)
def fnGetLedStateById(led_id):
    try:
        # Buscar el estado del LED por ID
        led = dbLeds.find_one({"_id": ObjectId(led_id)})

        if led is None:
            return jsonify({"Respuesta": False, "Mensaje": "LED no encontrado"}), 404

        response = respuestas.succ200.copy()
        response["Mensaje"] = f"Estado del LED {led_id}"
        response["Estado"] = led.get("status")
        return jsonify(response)

    except Exception as e:
        print("Error en la función fnGetLedStateById", e)
        return jsonify(respuestas.err500)
