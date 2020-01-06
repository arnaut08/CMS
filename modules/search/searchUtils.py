from config.database import connect
import json
from flask_jwt import current_identity


def getSearchedCredentials(params):
        con = connect()
        with con.cursor() as cursor:
                limit = "LIMIT {}, {}".format((int(params['page'])*int(params['limit'])), int(params['limit']))
                sql = "SELECT a.userId, a.canRead, a.canWrite, a.description AS accessDesc, c.name AS credential, c.id AS credentialId, c.version, c.description AS credDesc, f.id AS fieldId, f.fieldType, f.label, f.value FROM accessPermission AS a LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id LEFT JOIN field AS f ON f.credentialId = c.id WHERE c.version = latest AND a.userId = {0} AND f.version = latest AND (c.name like '%{1}%' OR f.fieldType like '%{1}%') {2}".format(current_identity['userId'], params['keyword'], limit)                
                cursor.execute(sql)
                data = cursor.fetchall()
        con.close()
        return data
