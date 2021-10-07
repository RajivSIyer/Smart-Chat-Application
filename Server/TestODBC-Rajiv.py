import pyodbc
import sqlite3

for driver in pyodbc.drivers():
    print(driver)
    
db_conn_str = "DRIVER={ODBC Driver 17 for SQL Server};\
    SERVER=BALROG;\
    DATABASE=SmartChat;\
    UID=sa;\
    PWD=Technobase2021;\
    Trusted_Connection=no;"
    
try:
    connection = sqlite3.connect(db_conn_str)

except Exception as e:
    print("mama mia\n")
    print(str(e))
    
cursor = connection.cursor()
cursor.execute('''SELECT * FROM dbo.Users''')
for row in cursor:
    print(row)


    
    