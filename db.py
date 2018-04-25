from configs import config
import mysql.connector

def connect():
    db = mysql.connector.connect(user=config.dbusername, password=config.dbpassword,
                                 host="127.0.0.1", database=config.dbname)
    return db

def getQuestion():
    return exec("SELECT * FROM questions WHERE category = 1 ORDER BY RAND() LIMIT 1;")

def getUser(login):
    return exec("SELECT * FROM users WHERE login = '{}';".format(login))

def registerUser(login, pas, email):
    exec("INSERT INTO users (l")
    return True

def exec(command):
    db = connect()
    cursor = db.cursor()
    cursor.execute(command)
    try:
        cmd = cursor.fetchall()[0]
    except:
        print("No data to fetch")
        cmd = None
    cursor.close()
    db.close()
    return cmd