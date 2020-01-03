from config.database import connection
from helper import utils
import json

def addCredential(data):
        cursor = connection.cursor()
        key = utils.generateAlphanumericKey()
        sql = "INSERT INTO credential(id, name, projectId, createdBy, description) VALUES ('{}', '{}', {}, {}, '{}')".format(key, data['name'], data['projectId'], data['createdBy'], data['description'])
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        addCredentialFields(json.loads(data['fields']), key)
        connection.close()

def updateCredential(data):
        cursor = connection.cursor()
        sql = "INSERT INTO credential(id, name, projectId, createdBy, version, description) VALUES ('{}', '{}', {}, {}, {}, '{}')".format(data['id'], data['name'], data['projectId'], data['createdBy'], (int(data['version'])+1), data['description'])
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        updateCredentialFields(json.loads(data['fields']))
        connection.close()

def addCredentialFields(data, credentialId):
        cursor = connection.cursor()
        key = utils.generateAlphanumericKey()
        values=[]
        for obj in data:
                value = list(obj.values())
                value.insert(0, key)
                value.insert(1, credentialId)
                values.append(value)
        sql = "INSERT INTO field(id, credentialId, fieldType, label, value) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(sql, values)
        connection.commit()
        cursor.close()

def updateCredentialFields(data):
        cursor = connection.cursor()
        values = []
        for obj in data:
                obj['version'] += 1
                value = list(obj.values())
                values.append(value)
        sql = "INSERT INTO field(id, credentialId, fieldType, label, value, version) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(sql, values)
        connection.commit()
        cursor.close()