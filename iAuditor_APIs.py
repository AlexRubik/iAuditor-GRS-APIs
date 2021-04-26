'''

https://developer.safetyculture.io/

Functions to use iAuditor APIs.

Contact: dewittat@g.cofc.edu
'''

import pyodbc
import pandas as pd
from pandasql import sqldf
import requests
import json






def getToken():
    global token

    url = "https://api.safetyculture.io/auth"
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    data = {"username":"iAuditor_EMAIL","password":"iAuditor_PASSWORD","grant_type":"password"}  # grant_type is the actual string "password"
    api_out = requests.post(url=url, data=data, headers=header)

    api_out = api_out.json()

    token = api_out['access_token']

    return token




'''
createResponseSet(name, responsesList)

name = a name of the set
responsesList = array of responses

responsesList should be a list of dictionaries in this format:

          {"label": “John Smith"}
          

https://developer.safetyculture.io/#create-a-global-response-set

POST https://api.safetyculture.io/response_sets

'''


def createResponseSet(name, responsesList, token):



    url = "https://api.safetyculture.io/response_sets"
    
    header = {'Content-Type':'application/json','Authorization': f'Bearer {token}'}
    
    data = {'name':f'{name}','responses':responsesList}
    
    api_out = requests.post(url=url, json=data,headers=header)
    json = api_out.json()
    print(json)
    print("status code = " + str(api_out.status_code))



'''
Update response set.

This replaces (overwrites) all current responses in the specified set with the responses
in the payload (json/data).

PUT https://api.safetyculture.io/response_sets/<responseset_id>
'''


def updateResponseSet(name, responsesList, responseset_id, token):
    
    url = f"https://api.safetyculture.io/response_sets/{responseset_id}"
    
    header = {'Content-Type':'application/json','Authorization': f'Bearer {token}'}
    
    data = {'name':f'{name}','responses':responsesList}
    
    api_out = requests.put(url=url, json=data,headers=header)
    json = api_out.json()
    print(json)
    print("status code = " + str(api_out.status_code))





'''
Here's an example of creating a new global response set from data pulled in from
a sql server.
'''

def main():

# responseset_id for Mobe3 Users = 'responseset_9cfdc2b6bbb645cbb4b5737801c84000'

# Connect to SQL server and query data for users' names and clockIds

    server = 'serverName' 
    database = 'databaseName' 
    username = 'username' 
    password = 'password' 
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()

    queryStr = "Select u.full_name,isnull([ext_employeeid],'NOID') as ClockID  from (SELECT distinct [userid]\n"\
               "FROM [mccall891].[export_tran]\n"\
               "where tran_date > getdate()-90) et\n"\
               "left join mccall891.export_user u on et.userid=u.userid\n"\
               "order by full_name"
               


    '''
    Query for reference:
    
    Select u.full_name,isnull([ext_employeeid],'NOID') as ClockID  from (SELECT distinct [userid]

    FROM [mccall891].[export_tran]
    where tran_date > getdate()-90) et
    left join mccall891.export_user u on et.userid=u.userid
    order by full_name

    '''
      
      
        
      
      

    sql_query = pd.read_sql_query(queryStr,conn)
    print(sql_query)
  

    responsesList = []
    for index, row in sql_query.iterrows():  # creates a list of dictionaries stored in responsesList
        
        current_name = row['full_name']
        current_clockid = row['ClockID']
        tempResponseDict = {"label": f"{current_name}","short_label":f"{current_clockid}"}  # this format can be found on the dev website in my header
        responsesList.append(tempResponseDict)

    print(responsesList)



    token = getToken()
    
    
    createResponseSet("Mobe3 Users", responsesList, token)





#main()
    



