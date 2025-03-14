from flask import Flask,jsonify,request
from flask_cors import CORS ,cross_origin

import BackEnd.Functions as Callmethod
import BackEnd.GlobalInfo.ResponseMessages as repuesta

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/mensaje', methods=['GET'])
@cross_origin(allow_headers=['content-type'])
def mensaje():
    try:
        variable={"mensaje":"hola jorais"}
        return jsonify(variable)
    except Exception as error:
        print(error)
        return jsonify(repuesta.err500)
    
@app.route('/getUsers', methods=['GET'])
@cross_origin(allow_headers=['content-type'])
def getUsers():
    try:
        objResult=Callmethod.fnGetUsers()
        return objResult
    except Exception as error:
        print("estoy en el route",error)
        return jsonify(repuesta.err500)

@app.route('/getUser/<id>', methods=['GET'])
@cross_origin(allow_headers=['content-type'])
def getUser(id):
    try:
        objResult=Callmethod.fnGetUser(id)
        return objResult
    except Exception as error:
        print("estoy en el route",error)
        return jsonify(repuesta.err500)
    

@app.route('/postUser', methods=['POST'])
@cross_origin(allow_headers=['content-type'])
def postUser():
    try:
        objResult=Callmethod.fnPostUser(request.json)
        return objResult
    except Exception as error:
        print("estoy en el route",error)
        return jsonify(repuesta.err500)
@app.route('/loginUser', methods=['POST'])
@cross_origin(allow_headers=['content-type'])
def login_user():
    if request.method != 'POST':
        return jsonify({"error": "Método no permitido"}), 405  # Esto evita que GET sea aceptado

    try:
        data = request.json
        response = Callmethod.fnLoginUser(data)
        return response
    except Exception as error:
        print("Error en el route '/loginUser':", error)
        return jsonify({"error": "Error interno"}), 500
    
@app.route('/updateLed/<led_id>', methods=['POST'])
@cross_origin(allow_headers=['content-type'])
def update_led(led_id):
    try:
        objResult = Callmethod.fnSetLedStateById(led_id)
        return objResult
    except Exception as error:
        print("Error en el route '/updateLed':", error)
        return jsonify(repuesta.err500) 
    
@app.route('/setLedTrue/<led_id>', methods=['POST'])
@cross_origin(allow_headers=['content-type'])
def set_led_true(led_id):
    try:
        objResult = Callmethod.fnSetLedStateTrueById(led_id)
        return objResult
    except Exception as error:
        print("Error en el route '/setLedTrue':", error)
        return jsonify(repuesta.err500)
@app.route('/setLedFalse/<led_id>', methods=['POST'])
@cross_origin(allow_headers=['content-type'])
def set_led_false(led_id):
    try:
        objResult = Callmethod.fnSetLedStateFalseById(led_id)
        return objResult
    except Exception as error:
        print("Error en el route '/setLedFalse':", error)
        return jsonify(repuesta.err500)
@app.route('/getLedState/<led_id>', methods=['GET'])
@cross_origin(allow_headers=['content-type'])
def get_led_state(led_id):
    try:
        objResult = Callmethod.fnGetLedStateById(led_id)
        return objResult
    except Exception as error:
        print("Error en el route '/getLedState':", error)
        return jsonify(repuesta.err500)
@app.route('/getAllLedsState', methods=['GET'])
@cross_origin(allow_headers=['content-type'])
def get_all_leds_state():
    try:
        objResult = Callmethod.fnGetAllLedsState()
        return objResult
    except Exception as error:
        print("Error en el route '/getAllLedsState':", error)
        return jsonify(repuesta.err500)


# fdsfsfsd
# app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)