from config.database import connect
from helper import utils
import json
from flask_jwt import current_identity

def addCredential(data):
        con = connect()
        with con.cursor() as cursor:
                key = utils.generateAlphanumericKey()
                sql = "INSERT INTO credential(id, name, projectId, createdBy, description) VALUES ('{}', '{}', {}, {}, '{}')".format(key, data['name'], data['projectId'], data['createdBy'], data['description'])
                cursor.execute(sql)
                con.commit()
        addCredentialFields(con, json.loads(data['fields']), key)
        con.close()

def updateCredential(data):
        con = connect()
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

def getProjectCredentials(keys):
        con = connect()
        with con.cursor() as cursor:
                limit = "LIMIT {}, {}".format((int(keys['page'])*int(keys['limit'])), int(keys['limit']))
                sql = "SELECT a.userId, a.canRead, a.canWrite, a.description  accessDesc, c.name AS credential, c.id, c.version, c.description AS credDesc, f.id, f.label, f.value FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id LEFT JOIN field AS f ON f.credentialId = c.id WHERE c.version = latest AND a.userId = {} AND f.version = latest AND c.projectId = {} {}".format(current_identity['userId'], keys['pId'], limit)                
                cursor.execute(sql)
                data = cursor.fetchall()
        con.close()
        return data

def getProjects(keys):
        con = connect()
        with con.cursor() as cursor:
                limit = "LIMIT {}, {}".format((int(keys['page'])*int(keys['limit'])), int(keys['limit']))
                sql = "SELECT p.id, p.name FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id LEFT JOIN project AS p ON p.id = c.projectId WHERE c.version = latest AND a.userId = {} {}".format(current_identity['userId'], limit)                
                cursor.execute(sql)
                data = cursor.fetchall()
        con.close()
        return data