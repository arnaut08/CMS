from config.database import connection

def addCredential(data):
        cursor = connection.cursor()
        sql = "INSERT INTO credential(id, name, projectId, createdBy, description) (Select max(id)+1, '{}', {}, {}, '{}' from credential)".format(data['name'], data['projectId'], data['createdBy'], data['description'])
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

def updateCredential(data):
        cursor = connection.cursor()
        sql = "INSERT INTO credential(id, name, projectId, createdBy, version, description) VALUES ({}, '{}', {}, {}, {}, '{}')".format(data['id'], data['name'], data['projectId'], data['createdBy'], (int(data['version'])+1), data['description'])
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()