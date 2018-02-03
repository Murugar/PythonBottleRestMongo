from bottle import get,run,post,request,delete
from pymongo import MongoClient

def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

db = get_db('examples')
projection = {'_id': 0, 'name': 1,'surname':1,'age':1}

def findMongo(db,query=None):
    # For local use
    results = db.bottleExample.find(query,projection)
    dict = []
    for record in results:
        dict.append(record)
    return (dict)

@get('/people/all')
def getAll():
    return {'people' : findMongo(db)}

@get('/people/<name>')
def getOne(name):
    the_name = findMongo(db,{'name': name })
    return {'person' : the_name}

@post('/people/create')
def addOne():
    new_person = {'name' : request.json.get('name'),
                  'surname' : request.json.get('surname'),
                  'age' : request.json.get('age')}
    if insertMongo(db,new_person) :
        return {'people' : findMongo(db)}
    else:
        return {'ERROR!':'There is already same record!'}
def insertMongo(db,data):

    if findMongo(db,{'name': data['name']}) != []:
        print('There is already same record.')
        return False
    else:
        db.bottleExample.insert(data)
        print(data)
        return True

@delete('/people/remove/<name>')
def deleteOne(name):
    deleted_person = findMongo(db,{'name':name}) #Searching for name.
    db.bottleExample.remove({'name':name})
    return {'people' : findMongo(db,None)}

run(reloader=True, debug= True)

