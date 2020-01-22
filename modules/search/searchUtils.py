from config.database import connect
import json
from flask_jwt import current_identity
from modules.credential.credentialUtils import checkGroupMember

def getSearchedCredentials(params):
        con = connect()
        with con.cursor() as cursor:
                limit = "LIMIT {}, {}".format((int(params['page'])*int(params['limit'])), int(params['limit']))
                sql = '''SELECT c.id AS id, c.name, c.version, c.description, p.project_name, c.createdAt, c.projectId FROM accessPermission AS a 
                LEFT JOIN credential AS c ON (c.id = credentialId or c.projectId = a.projectId) 
                LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id 
                LEFT JOIN field AS f ON f.credentialId = c.id LEFT JOIN project AS p ON c.projectId = p.id 
                WHERE c.version = latest AND a.userId = {0} AND f.version = latest AND 
                (c.name like '%{1}%' OR f.fieldType like '%{1}%' OR p.project_name like '%{1}%') GROUP BY c.id {2}'''.format(current_identity['userId'], params['keyword'], limit)                
                cursor.execute(sql)
                data = cursor.fetchall()

        # Credential Fields' data
        for credential in data:
                with con.cursor() as cursor:
                        sql = "SELECT f.id, f.label, f.value, f.fieldType FROM credential AS c LEFT JOIN field AS f ON f.credentialId = c.id AND f.version = c.version LEFT JOIN (Select id, max(version) AS latest FROM credential group by id) AS mx ON mx.id = c.id WHERE c.version = latest AND c.id = '{0}' AND f.fieldType like '%{1}%'".format(credential['id'], params['keyword'])                
                        cursor.execute(sql)
                        fieldData = cursor.fetchall()
                        cursor.close()
                credential['fields'] = fieldData
        con.close()
        return data

def getSearchedUsers(params):
        con = connect()
        if 'projectId' in dict(params).keys():
                with con.cursor() as cursor:
                        sql = "SELECT (SELECT id FROM accessPermission WHERE userId = e.id AND projectId = {0} GROUP BY projectId) AS id, ifnull(a.canRead, 0) as canRead, ifnull(a.canWrite, 0) as canWrite, a.description, ifnull(a.projectId, {0}) as projectId, e.full_name, e.id as userId FROM employees AS e LEFT JOIN accessPermission AS a ON a.userId = e.id WHERE e.full_name LIKE '%{1}%' AND (projectId = {0} OR if(projectId != {0}, 0, 1) = 0 OR ifnull(projectId, 0) = 0) GROUP BY e.id".format(params['projectId'], params['keyword'])                
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()
        else:
                with con.cursor() as cursor:
                        sql = "SELECT (SELECT id FROM accessPermission WHERE userId = e.id AND credentialId = '{0}' GROUP BY credentialId) AS id, ifnull(a.canRead, 0) as canRead, ifnull(a.canWrite, 0) as canWrite, ifnull(a.credentialId, '{0}') as credentialId ,e.id as userId, e.full_name FROM employees AS e LEFT JOIN accessPermission AS a ON a.userId = e.id WHERE e.full_name LIKE '%{1}%' AND  (credentialId = '{0}' OR projectId = (SELECT projectId FROM credential WHERE id = '{0}' GROUP BY projectId) OR ( ifnull(credentialId,0) = 0 AND (ifnull(projectId,0) = 0) )) GROUP BY e.id;".format(params['credentialId'], params['keyword'])                
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()
        con.close()
        return data

def getSearchedProjects(params):
        con = connect()
        isAGroupMember = checkGroupMember()
        if isAGroupMember:
                with con.cursor() as cursor:
                        sql = "SELECT id, project_name, created_at FROM project"               
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()
        else:
                with con.cursor() as cursor:
                        sql = "SELECT p.id, project_name, p.created_at FROM accessPermission AS a LEFT JOIN project AS p ON (a.projectId = p.id OR (SELECT projectId FROM credential WHERE id = a.credentialId GROUP BY id) = p.id) WHERE a.userId = {} GROUP BY p.id".format(current_identity['userId'])               
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        cursor.close()
        con.close()
        return data