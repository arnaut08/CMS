from config.database import connect
import json
from flask_jwt import current_identity
from modules.credential.credentialUtils import checkGroupMember

def getSearchedCredentials(params):
        con = connect()
        
        # To get each word in a list 
        keywords = params['keyword'].split(' ')

        # Variable Declaration
        selectMatchCount = ''
        selectStrength = ''
        joinTerm = ''
        conditionTerm = ''
        wordCount = 0
        
        # To form subqueries and other required statements, in order to be inserted in the sql query
        for keyword in keywords:
                credentialTable = 'c' + str(wordCount)
                projectTable = 'p' + str(wordCount)
                # Match count is the number of searched words that matches the respective credential
                selectMatchCount += ' IFNULL({}.cnt,0) +'.format(credentialTable)
                # Strength is the order of matched words considering the match count
                selectStrength += ' IFNULL({}.cnt,0)*{} +'.format(credentialTable,pow(10,len(keywords) - wordCount))
                joinTerm += " LEFT JOIN (SELECT {1}.id,1 AS cnt FROM credential AS {1} LEFT JOIN project AS {2} ON {2}.id = {1}.projectId  WHERE ({1}.name LIKE '%{0}%') OR ({2}.project_name LIKE '%{0}%')) AS {1} ON {1}.id = c.id".format(keyword, credentialTable, projectTable)
                conditionTerm += " {}.cnt != 0 OR".format(credentialTable)
                wordCount += 1

        # To remove the trailing '+'
        selectMatchCount = selectMatchCount[:-1]
        selectStrength = selectStrength[:-1]
        # To remove the trailing 'OR'
        conditionTerm = conditionTerm[:-2]

        with con.cursor() as cursor:
                sql = '''SELECT c.id, c.name, c.createdAt, c.starredBy, c.description, c.version, p.project_name, 
                p.id, ({}) AS matchCount, ({}) AS strength FROM credential AS c LEFT JOIN (Select id, max(version) AS latest 
                FROM credential group by id) AS mx ON mx.id = c.id {} LEFT JOIN project AS p on p.id = c.projectId WHERE c.version = latest 
                AND ({}) GROUP BY c.id, c.name, c.createdAt, c.starredBy, c.description, c.version, p.project_name, p.id 
                ORDER BY matchCount DESC, strength DESC'''.format(selectMatchCount, selectStrength, joinTerm, conditionTerm)
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        con.close()
        return data

def getSearchedUsers(params):
        con = connect()
        with con.cursor() as cursor:
                sql = '''SELECT id as userId, full_name FROM employees WHERE full_name LIKE '%{}%' AND id != {} '''.format(params['keyword'], current_identity['userId'])                
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        con.close()
        return data

def getSearchedProjects(params):
        con = connect()
        with con.cursor() as cursor:
                sql = "SELECT id, project_name, created_at FROM project WHERE project_name LIKE '%{}%' AND id NOT IN (SELECT distinct(projectId) FROM credential)".format(params['keyword'])               
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.close()
        con.close()
        return data