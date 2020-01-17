from config.database import connect
from helper import utils
import json
from flask_jwt import current_identity
from config import constants

def addCredential(data):
        con = connect()
        hasAccess = checkProjectAccess(data['projectId'])
        if hasAccess:
                key = utils.generateAlphanumericKey()
                # To insert in credential table
                with con.cursor() as cursor:
                        sql = "INSERT INTO credential(id, name, projectId, createdBy, description) VALUES ('{}', '{}', {}, {}, '{}')".format(key, data['name'], data['projectId'], current_identity['userId'], data['description'] or "")
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()
                
                with con.cursor() as cursor:
                        sql = "INSERT INTO accessPermission(userId, canRead, canWrite, description, credentialId) VALUES ({}, 1, 1, '', '{}')".format(current_identity['userId'], key)  
                        cursor.execute(sql) 
                        con.commit()
                        cursor.close()

                # To insert in the event table
                with con.cursor() as cursor:
                        sql = "INSERT INTO cmsEvents(credentialId, projectId, userId, comments) VALUES ('{cred}', {project}, {user},concat((select full_name from employees where id={user}), '{operation}', '{credName}', '{where}', (select project_name from project where id={project})))".format(user = current_identity['userId'], cred = key, project = data['projectId'], credName = data['name'], operation = constants.addCredential, where = constants.inProject)
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()
                addCredentialFields(con, json.loads(data['fields']), key)
        con.close()
        return hasAccess

def updateCredential(data):
        con = connect()
        hasAccess = checkCredentialAccess(data['id'])
        if hasAccess:
                # To insert in the credential table
                with con.cursor() as cursor:
                        sql = "INSERT INTO credential(id, name, projectId, createdBy, version, description) VALUES ('{}', '{}', {}, {}, {}, '{}')".format(data['id'], data['name'], data['projectId'], current_identity['userId'], (int(data['version'])+1), data['description'] or "")
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()

                # To insert in the event table
                with con.cursor() as cursor:
                        sql = "INSERT INTO cmsEvents(credentialId, projectId, userId, comments) VALUES ('{cred}', {projectId}, {user}, concat((select full_name from employees where id={user}), '{operation}', '{credName}', '{where}', (select project_name from project where id={projectId})))".format(user = current_identity['userId'], cred = data['id'], projectId = data['projectId'], credName = data['name'], operation = constants.updateCredential, where = constants.inProject)
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()
        updateCredentialFields(con, json.loads(data['fields']))
        con.close()
        return hasAccess

def addCredentialFields(con, data, credentialId):
        with con.cursor() as cursor:
                values = ((utils.generateAlphanumericKey(), credentialId, *obj.values()) for obj in data)
                sql = "INSERT INTO field(id, credentialId, fieldType, label, value) VALUES (%s, %s, %s, %s, %s)"
                cursor.executemany(sql, values)
                con.commit()
                cursor.close()


def updateCredentialFields(con, data):
        with con.cursor() as cursor:
                values = []
                for obj in data:
                        if not obj['id']:
                                obj['id'] = utils.generateAlphanumericKey()
                        obj['version'] += 1
                        value = list(obj.values())
                        values.append(value)
                sql = "INSERT INTO field(id, credentialId, fieldType, label, value, version) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, values)
                con.commit()
                cursor.close()


def getProjectCredentials(keys):
        con = connect()
        # Credential data of a particular project
        with con.cursor() as cursor:
                limit = "LIMIT {}, {}".format((int(keys['page'])*int(keys['limit'])), int(keys['limit']))
                sql = '''SELECT if(JSON_CONTAINS_PATH(c.starredBy,'all',REPLACE(JSON_SEARCH(starredBy, 'one', {0}), '"', '')), 1, 0) AS star,
                 a.userId, a.canRead, a.canWrite, a.description  accessDesc, c.name AS credential,
                 c.id, c.version, c.description AS credDesc, f.id, f.label, f.value FROM accessPermission AS a 
                 LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) 
                 LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id 
                 LEFT JOIN field AS f ON f.credentialId = c.id 
                 WHERE c.version = latest AND a.canRead = 1 AND a.userId = {0} AND f.version = latest AND c.projectId = {1} {2}'''.format(current_identity['userId'], keys['pId'], limit)                
                cursor.execute(sql)
                projectData = cursor.fetchall()
                cursor.close()
        
        # Event data related to the project
        with con.cursor() as cursor:
                sql = "SELECT * FROM cmsEvents WHERE projectId = {}".format(keys['pId'])                
                cursor.execute(sql)
                eventData = cursor.fetchall()
                cursor.close()

        # Total number of records
        with con.cursor() as cursor:
                sql = "SELECT count(a.id) AS count FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id LEFT JOIN field AS f ON f.credentialId = c.id WHERE c.version = latest AND a.canRead = 1 AND a.userId = {} AND f.version = latest AND c.projectId = {}".format(current_identity['userId'], keys['pId'])                
                cursor.execute(sql)
                countData = cursor.fetchall()
                cursor.close()

        # Access permission data related to the project
        with con.cursor() as cursor:
                sql = "SELECT (SELECT id FROM accessPermission WHERE userId = e.id AND projectId = {0} GROUP BY e.id) as id ,ifnull(a.canRead, 0) as canRead, ifnull(a.canWrite, 0) as canWrite, a.description, ifnull(a.projectId, {0}) as projectId, e.full_name, e.id as userId FROM employees AS e LEFT JOIN accessPermission AS a ON a.userId = e.id WHERE projectId = {0} OR if(projectId != {0}, 0, 1) = 0 OR ifnull(projectId, 0) = 0 GROUP BY e.id".format(keys['pId'])                
                cursor.execute(sql)
                accessData = cursor.fetchall()
                cursor.close()

        con.close()
        if not len(countData):
                countData = [{'count' : 0}]
        
        return { 'projectData': projectData, 'eventData': eventData , 'count': countData[0]['count'], 'accessData': accessData}

def getProjects(keys):
        con = connect()
        isAGroupMember = checkGroupMember()
        if isAGroupMember:
                with con.cursor() as cursor:
                        limit = "LIMIT {}, {}".format((int(keys['page'])*int(keys['limit'])), int(keys['limit']))
                        sql = "SELECT p.id, project_name, if(ifnull(c.projectId, 0) = 0, 0, 1) as hasCredentials FROM project AS p LEFT JOIN credential AS c on c.projectId = p.id GROUP BY p.id {}".format(limit)                
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()

                # Total number of records
                with con.cursor() as cursor:
                        sql = "SELECT COUNT(id) AS count FROM project"            
                        cursor.execute(sql)
                        countData = cursor.fetchall()
                        cursor.close()
        else:        
                with con.cursor() as cursor:
                        limit = "LIMIT {}, {}".format((int(keys['page'])*int(keys['limit'])), int(keys['limit']))
                        sql = "SELECT p.id, p.project_name FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN project AS p ON p.id = c.projectId OR p.id = a.projectId  WHERE a.canRead = 1 AND a.userId = {} GROUP BY p.id {}".format(current_identity['userId'], limit)                
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()

                # Total number of records
                with con.cursor() as cursor:
                        sql = "SELECT COUNT(distinct(p.id)) AS count FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN project AS p ON p.id = c.projectId WHERE a.canRead = 1 AND a.userId = {} GROUP BY a.projectId".format(current_identity['userId'])                
                        cursor.execute(sql)
                        countData = cursor.fetchall()
                        cursor.close()  
        con.close()
        if not len(countData):
                countData = [{'count' : 0}]
        return {'projectData' : data, 'count': countData[0]['count']}

def checkCredentialAccess(credentialId):
        con = connect()
        with con.cursor() as cursor:
                sql = "SELECT c.id FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) WHERE a.userId = {} AND c.id = '{}' AND canWrite = 1".format(current_identity['userId'], credentialId)                                
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        con.close()
        return bool(len(data))

def checkProjectAccess(projectId):
        con = connect()
        with con.cursor() as cursor:
                sql = "SELECT a.id FROM accessPermission AS a WHERE a.userId = {} AND a.projectId = {} AND canWrite = 1".format(current_identity['userId'], projectId)                                
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        
        isAGroupMember = checkGroupMember()
        return bool(len(data) or isAGroupMember)


def checkGroupMember():
        con = connect()
        with con.cursor() as cursor:
                sql = "SELECT ge.id FROM groups_employees AS ge LEFT JOIN groups AS g ON g.id = ge.group_id WHERE g.id = 18 AND ge.employee_id = {}".format(current_identity['userId'])                                
                cursor.execute(sql)
                groupData = cursor.fetchall()
                cursor.close()        
        con.close()
        return bool(len(groupData))

def getCredentialDetails(credentialId):
        con = connect()
        # Credential Data
        with con.cursor() as cursor:
                sql = "SELECT * FROM credential AS c LEFT JOIN field AS f ON f.credentialId = c.id AND f.version = c.version WHERE c.id = '{}'".format(credentialId)                
                cursor.execute(sql)
                credentialData = cursor.fetchall()
                cursor.close()
        
        # Event data related to the credential
        with con.cursor() as cursor:
                sql = "SELECT * FROM cmsEvents WHERE credentialId = '{}'".format(credentialId)                
                cursor.execute(sql)
                eventData = cursor.fetchall()
                cursor.close()

        # Access permission data related to the credential
        with con.cursor() as cursor:
                sql = "SELECT (SELECT id FROM accessPermission WHERE userId = e.id AND credentialId = '{0}' GROUP BY e.id) AS id, ifnull(a.canRead, 0) as canRead, ifnull(a.canWrite, 0) as canWrite, ifnull(a.credentialId, '{0}') as credentialId ,e.id as userId, e.full_name, a.description FROM employees AS e LEFT JOIN accessPermission AS a ON a.userId = e.id WHERE credentialId = '{0}' OR projectId = (SELECT projectId FROM credential WHERE id = '{0}' GROUP BY projectId) OR ( ifnull(credentialId,0) = 0 AND (ifnull(projectId,0) = 0) ) GROUP BY e.id;".format(credentialId)                
                cursor.execute(sql)
                accessData = cursor.fetchall()
                cursor.close()
        con.close()
        hasWriteAccess = 0
        for data in accessData:
                if (data['canWrite'] and data['userId'] == current_identity['userId']):
                        hasWriteAccess = 1
        return { 'credentialData': credentialData, 'eventData': eventData, 'accessData': accessData, 'hasWriteAccess': hasWriteAccess, 'description': credentialData[0]['description'], 'name': credentialData[0]['name'] }

def getFavouriteCredentials():
        con = connect()
        with con.cursor() as cursor:
                sql = "SELECT c.id AS credential, c.name, c.version, c.description, f.id, f.label, f.value, p.project_name, c.createdAt FROM credential AS c LEFT JOIN field AS f ON f.credentialId = c.id AND f.version = c.version LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id LEFT JOIN project AS p ON c.projectId = p.id WHERE c.version = latest AND IF(JSON_CONTAINS_PATH(starredBy,'all',REPLACE(JSON_SEARCH(starredBy, 'one', {}), '\"', '')), 1, 0) = 1".format(current_identity['userId'])                
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        con.close()
        return data

def manageFavouriteCredential(params):
        con = connect()
        starred = bool(int(params['star']))
        with con.cursor() as cursor:
                if starred:
                        sql = "UPDATE credential SET starredBy = IF(IFNULL(starredBy, true) = true, '[\"{0}\"]', IF(JSON_CONTAINS_PATH(starredBy,'all',REPLACE(JSON_SEARCH(starredBy, 'one', {0}), '\"', '')), starredBy, JSON_ARRAY_INSERT(starredBy, '$[0]','{0}'))) WHERE id = '{1}'".format(current_identity['userId'], params['credentialId'])
                else:
                        sql = "UPDATE credential SET starredBy = JSON_REMOVE(starredBy, REPLACE(JSON_SEARCH(starredBy, 'one', {}), '\"', '')) WHERE id = '{}'".format(current_identity['userId'], params['credentialId'])
                cursor.execute(sql)
                con.commit()
                cursor.close()
        con.close()
        return starred