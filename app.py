from flask import Flask, jsonify, request
from flask_cors import CORS
import flask
import functions, json
app = Flask(__name__)
CORS(app)


# ---------------------------------- Usuarios ----------------------------------
@app.route('/validateUser')
def validateUsers():
    userData = {}
    user = request.args.get('user')
    password = request.args.get('pass')
    result = functions.validateUser({"username":user,"password":password})
    if result:
        userData = functions.getUser(user)
    response =  flask.jsonify({'result': result,'userData':userData})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/registerUser',  methods = ['POST'])
def createUser():
    if request.method == 'POST':
        print("fue Post")
    newUser = request.get_json()
    result = functions.addUser(newUser)
    return {'register': result[0], "password": result[2], "user": result[1]}

@app.route('/updatUser', methods=['POST'])
def updateUser():
    newUser = request.get_json()
    oldUser = request.args.get('oldUser')
    return {'result':functions.editUser(oldUser,newUser)}

@app.route('/removeUser')
def removeUser():
    user = request.args.get('user')
    return {'result':functions.deleteUser(user)}
@app.route("/getUser")
def getUser():
    user = request.args.get('user')
    return{'result': functions.getUser(user)}
    
@app.route("/getAllUsers")
def getAllUsers():
    return {'result':functions.getAllUsers()}

# --------------------   Publicaciones ---------------------------------
@app.route('/addPublication', methods=['POST'])
def addPublication():
    newP = request.get_json()
    typeOfP = request.args.get('typeOfP')
    return {'result': functions.addPublication(typeOfP, newP)}

@app.route('/getPublications')
def getPublication():
    return functions.readJSONPubli()

@app.route("/addLike")
def addLike():
    status = False
    id = request.args.get('id')
    user = request.args.get('user')
    type = request.args.get('type')
    status = functions.addLike(int(id),user,type)
    return {'status': status}

@app.route("/removeLike")
def removeLike():
    status = False
    id = request.args.get('id')
    user = request.args.get('user')
    type = request.args.get('type')
    status = functions.removeLike(int(id),user,type)
    return {'status': status}

@app.route("/getMyPublications")
def getMy():
    user = request.args.get('username')
    return functions.getMyPulications(user)

@app.route("/loadData", methods=['POST'])
def loadData():
    typeOfValue = request.args.get('type')
    data = request.get_json()
    nd =json.loads(data['data'])
    newD = json.loads(nd)
    for n in newD:
        print(n)

    status = functions.loadData(typeOfValue, newD)
    return {'status': True}

# ----------------------- Otros -----------------------------
@app.route("/")
def hello():
    return "Server is On"

if __name__ == "__main__":
    app.run()

