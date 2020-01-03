from config.database import connection
from helper import utils
import json

def addCredential(data):
        con = connection
        with con.cursor() as cursor:
                key = utils.generateAlphanumericKey()
                sql = "INSERT INTO credential(id, name, projectId, createdBy, description) VALUES ('{}', '{}', {}, {}, '{}')".format(key, data['name'], data['projectId'], data['createdBy'], data['description'])
                cursor.execute(sql)
                con.commit()
        addCredentialFields(con, json.loads(data['fields']), key)
        con.close()

def updateCredential(data):
        con = connection
        with con.cursor() as cursor:
                sql = "INSERT INTO credential(id, name, projectId, createdBy, version, description) VALUES ('{}', '{}', {}, {}, {}, '{}')".format(data['id'], data['name'], data['projectId'], data['createdBy'], (int(data['version'])+1), data['description'])
                cursor.execute(sql)
                con.commit()
                cursor.close()
        updateCredentialFields(con, json.loads(data['fields']))
        con.close()

def addCredentialFields(con, data, credentialId):
        with con.cursor() as cursor:
                values = ((utils.generateAlphanumericKey(), credentialId, *obj.values()) for obj in data)
                sql = "INSERT INTO field(id, credentialId, fieldType, label, value) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql, values)
                con.commit()

def updateCredentialFields(con, data):
        with con.cursor() as cursor:
                values = []
                for obj in data:
                        obj['version'] += 1
                        value = list(obj.values())
                        values.append(value)
                sql = "INSERT INTO field(id, credentialId, fieldType, label, value, version) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, values)
                con.commit()

def getCredentials():
        con = connection
        with con.cursor() as cursor:
                sql = "SELECT * FROM credential AS c RIGHT JOIN field AS f ON f.credentialId = c.id groupBy()"
                cursor.execute(sql)
                data = cursor.fetchall()
        con.close()
        return data