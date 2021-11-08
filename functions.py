import json, os
from re import T
import string
from datetime import datetime
from types import new_class

from flask.scaffold import F 

# Gestion de Usuarios
def addUser(user):
    response = [False,False,False]
    existUsr = existUser(user["username"])
    correctPassword = validatePassword(user["password"])
    data = readJSONUsers()
    response[1] = existUsr
    response[2] = not correctPassword
    script_dir = os.path.dirname(__file__)
    if not existUsr and correctPassword:
        data.append(user)
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir,'usuarios.json'),'w') as file:
            json.dump(data, file, indent=4)
            response[0] = True
    
    return response
def validateUser(user):
    existUser = False
    data = readJSONUsers()
    for userName in data:
        if user["username"] == userName["username"] and user["password"]==userName["password"]:
            existUser = True
            break
    return existUser
def getUser (username):
    data = readJSONUsers()
    userData = {}
    for user in data:
        if username == user["username"]:
            userData = user
            break
    return userData
def validatePassword(password):
    isCorrect = False
    hasNumber = False
    hasSimbol = False
    isSizeCorrect = False
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    if len(password) >=8:
        isSizeCorrect = True
    for letter in password:
        if letter.isdigit():
            hasNumber = True
        if letter in punc:
            hasSimbol = True
    if hasNumber and hasSimbol and isSizeCorrect:
        isCorrect = True
    return isCorrect
def editUser(oldUserName, newUser):
    isEdited = False
    isSameName = False
    data = readJSONUsers()
    if oldUserName == newUser["username"]:
        isSameName = True
    if isSameName or not existUser(newUser["username"]) and validatePassword(newUser["password"]):
        for user in  data:
            if user["username"] == oldUserName:
                user["name"]=newUser["name"]
                user["gender"]=newUser["gender"]
                user["username"]=newUser["username"]
                user["email"]=newUser["email"]
                user["password"]=newUser["password"]
                user["rol"]=newUser["rol"]
                break
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir,'usuarios.json'),'w') as file:
            json.dump(data, file, indent=4)
            isEdited = True
    return isEdited
def deleteUser(userName):
    isDeleted = False
    data = readJSONUsers()
    script_dir = os.path.dirname(__file__)
    for i in range(len(data)):
        if data[i]["username"]==userName:
            data.pop(i)
            isDeleted = True
            break
    with open(os.path.join(script_dir,'usuarios.json'),'w') as file:
        json.dump(data, file, indent=4)
    return isDeleted

def existUser(user):
    existUser = False
    data = readJSONUsers()
    if user == "":
        return True
    for userName in data:
        if user == userName["username"]:
            existUser = True
            break
    return existUser

def getAllUsers():
    data = readJSONUsers()
    return data
#--------------------------------------Gestion de Videos/Imagenes----------------------------------
def addPublication(type, publication):
    data = readJSONPubli()
    publication["id"] = len(data[type])
    publication["likes"] = 0
    publication["date"] = getTime()
    publication["users"] = []
    data[type].append(publication)
    return saveJSONPublication(data)

def addLike(id,username,type):
    publication = readJSONPubli()
    publication[type][id]["users"].append(username)
    publication[type][id]["likes"] = publication[type][id]["likes"]+1
    saveJSONPublication(publication)
    return True

def removeLike(id,username,type):
    publication = readJSONPubli()
    publication[type][id]["likes"] = publication[type][id]["likes"]-1
    for i in range(len(publication[type][id]["users"])):
        if username == publication[type][id]["users"][i]:
            publication[type][id]["users"].pop(i)
            saveJSONPublication(publication)
            break
    return True

def getMyPulications(username):
    data = readJSONPubli()
    structure = """{
        "images":[
        ],
        "videos":[
        ]
    }"""
    nd = dict(json.loads(structure))
    for publication in data['images']:
        if publication['user'] == username:
            nd['images'].append(publication)
            pass
    for publication in data['videos']:
        if publication['user'] == username:
            nd['videos'].append(publication)
    return nd

def loadData(typeOfValue, newData):
    if typeOfValue == "users":
        data = readJSONUsers()
        for user in newData:
            user['rol']='user'
            data.append(user)
        saveJSONUser(data)
    else:
        data = readJSONPubli()
        for image in newData['images']:
            image['user']='admin'
            addPublication('images',image) 
        for video in newData['videos']:
            video['user']='admin'
            addPublication('videos',video)   
    return True

#Lectura de Json
def readJSON():
    data = {}
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'data.json')) as file:
        data = json.load(file)
    for client in data['images']:
         print('First name:', client['url'])
    return data
def readJSONUsers():
    data = {}
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'usuarios.json')) as file:
        data = json.load(file)
    return data
def readJSONPubli():
    data = {}
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'publicaciones.json')) as file:
        data = json.load(file)
    return data
# Guardado de JSON
def saveJSONUser(data):
    isSaved = False
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir,'usuarios.json'),'w') as file:
        json.dump(data, file, indent=4)
        isSaved = True
    return isSaved

def saveJSONPublication(data):
    isSaved = False
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir,'publicaciones.json'),'w') as file:
        json.dump(data, file, indent=4)
        isSaved = True
    return isSaved

def getTime():
    return datetime.today().strftime('%d/%m/%Y')

#print(getTime())
#removeLike(0,"america","images")
#print(addPublication("images",{"id":-1,"new":"abc"}))
#print(validatePassword("admin#ipc3"))
#print(addUser({"name":"Auron Garica","gender":"M","username":"auronPlays23","email":"1","password":"password@1","rol":"user"}))
#print(editUser("auronPlays23",{"name":"userEdited","gender":"M","username":"auronPlays23","email":"1","password":"password@1","rol":"user"}))
#print(deleteUser("auronPlays23"))