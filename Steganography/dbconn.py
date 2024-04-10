import sys
sys.path.append('/Cryptosite')
from . import auth
import pyodbc


connection_string = ('Driver={ODBC Driver 18 for SQL Server};'
                    'Server=tcp:steganography.database.windows.net,1433;'
                    'Database=Steganography;Uid=admin123;Pwd=crypt@123;'
                    'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


# get user details when they login
def get_user(email, password):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # get salt value (if user exists)
    cursor.execute("SELECT salt FROM Users WHERE username = '" + email + "'")
    row = cursor.fetchone()
    if row:
        salt = row[0]
    else:
        return False 
       
    hashed_password, salt = auth.hash_password(password,salt)
    
    cursor.execute("SELECT name FROM Users WHERE username = '" + email + "' and password = '" + hashed_password + "'")
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return False    
  
# check if user exists  
def check_user(email):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Users WHERE username = '" + email + "'")
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return False
             

# save new user when they register
def save_user(name, email, password):
    hashed_password, salt = auth.hash_password(password)
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (name, username, password, salt) VALUES ('" + name + "','" + email + "','" + hashed_password + "','" + salt + "')")
    conn.commit()
    cursor.close()
    conn.close()
    return True 

 
    
    

    
    
    
                       
        

