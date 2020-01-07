from config.database import connect
from flask_jwt import current_identity
from config import constants

def addAccessPermission(data):
    con = connect()
    # For Credential based access
    if "credentialId" in dict(data).keys():
        with con.cursor() as cursor:
            sql = "INSERT INTO accessPermission (userId, canRead, canWrite, description, credentialId) VALUES ({}, {}, {}, '{}', '{}')".format(data['userId'], data['canRead'], data['canWrite'], data['description'], data['credentialId'])  
            cursor.execute(sql) 
            con.commit()
            cursor.close()
            
        # To insert in the event table
        with con.cursor() as cursor:
            sql = "INSERT INTO events(credentialId, projectId, userId, comments) (Select '{cred}', projectId, {assignee}, concat((select name from user where id={assignee}), '{operation}', (select name from user where id={user}), '{source}', (select name from credential where id='{cred}' group by id)) FROM credential WHERE id = '{cred}' GROUP BY projectId)".format(assignee = current_identity['userId'], cred = data['credentialId'], operation = constants.giveAccess, source = constants.forCredential, user = data['userId'])
            cursor.execute(sql)
            con.commit()
            cursor.close() 

    # For Project based access
    else:
        with con.cursor() as cursor:                
            sql = "INSERT INTO accessPermission (userId, canRead, canWrite, description, projectId) VALUES ({}, {}, {}, '{}', {})".format(data['userId'], data['canRead'], data['canWrite'], data['description'], data['projectId'])
            cursor.execute(sql)
            con.commit()
            cursor.close()

        # To remove all the individual credential's permission given to the user for that particular project
        with con.cursor() as cursor:
            sql = "DELETE FROM accessPermission WHERE credentialId IN (SELECT id FROM credential WHERE projectId = {}) AND userId = {}".format(data['projectId'], data['userId'])
            cursor.execute(sql)
            con.commit()
            cursor.close()

        # To insert in the event table
        with con.cursor() as cursor:
            sql = "INSERT INTO events(projectId, userId, comments) VALUES ({project}, {assignee}, concat((SELECT name FROM user WHERE id={assignee}), '{operation}', (SELECT name FROM user WHERE id={user}), '{source}', (SELECT name FROM project WHERE id={project})))".format(assignee = current_identity['userId'], project = data['projectId'], operation = constants.giveAccess , source = constants.forProject, user = data['userId'])
            cursor.execute(sql)
            con.commit()
            cursor.close() 
    con.close()

def updateAccessPermission(data):
    con = connect()
    # For Credential based access
    if "credentialId" in data.keys():
        with con.cursor() as cursor:
            sql = "UPDATE accessPermission SET userId = {}, canRead = {}, canWrite = {}, description = '{}', credentialId = '{}' WHERE id = {}".format(data['userId'], data['canRead'], data['canWrite'], data['description'], data['credentialId'], data['id'])  
            cursor.execute(sql) 
            con.commit()
            cursor.close()

        # To insert in the event table
        with con.cursor() as cursor:
            sql = "INSERT INTO events(credentialId, projectId, userId, comments) (Select '{cred}', projectId, {assignee}, concat((select name from user where id={assignee}), '{operation}', (select name from user where id={user}), '{source}', (select name from credential where id='{cred}' group by id)) FROM credential WHERE id = '{cred}' GROUP BY projectId)".format(assignee = current_identity['userId'], cred = data['credentialId'], operation = constants.updateAccess, source = constants.forCredential, user = data['userId'])
            cursor.execute(sql)
            con.commit()
            cursor.close() 


    # For Project based access
    else:
        with con.cursor() as cursor:                
            sql = "UPDATE accessPermission SET userId = {}, canRead = {}, canWrite = {}, description = '{}', projectId = {} WHERE id = {}".format(data['userId'], data['canRead'], data['canWrite'], data['description'], data['projectId'], data['id'])
            cursor.execute(sql)
            con.commit()
            cursor.close()
        
        # To insert in the event table
        with con.cursor() as cursor:
            sql = "INSERT INTO events(projectId, userId, comments) VALUES ({project}, {assignee}, concat((SELECT name FROM user WHERE id={assignee}), '{operation}', (SELECT name FROM user WHERE id={user}), '{source}', (SELECT name FROM project WHERE id={project})))".format(assignee = current_identity['userId'], project = data['projectId'], operation = constants.updateAccess , source = constants.forProject, user = data['userId'])
            cursor.execute(sql)
            con.commit()
            cursor.close() 
    con.close()