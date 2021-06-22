'''
Pulls the names of mobe3 users from sql server and updates the existing
Mobe3 Users global response set. (iAuditor)

Refer to iAuditor_APIs.py for comments on the functions used.

https://developer.safetyculture.io/

Contact: dewittat@g.cofc.edu
'''



import pyodbc
import pandas as pd
from pandasql import sqldf
import iAuditor_APIs



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
           

           
  
  
    
  
  

sql_query = pd.read_sql_query(queryStr,conn)
print(sql_query)


responsesList = []
for index, row in sql_query.iterrows():
    
    current_name = row['full_name']
    current_clockid = row['ClockID']
    tempResponseDict = {"label": f"{current_name}","short_label":f"{current_clockid}"}
    responsesList.append(tempResponseDict)

print(responsesList)





responseset_id = 'responseset_18a0db3e07f9466a970af5717f7a976a'
token = iAuditor_APIs.getToken()


iAuditor_APIs.updateResponseSet("Mobe3 Users", responsesList, responseset_id, token)
