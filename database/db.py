from configs import config
import mysql.connector

def connect():
    db = mysql.connector.connect(user=config.dbusername, password=config.dbpassword,
                                 host="127.0.0.1", database=config.dbname)
    return db

def getQuestion(type = 0):
    return exec("SELECT * FROM questions WHERE category = {} ORDER BY RAND() LIMIT 1;".format(type))

def getUser(login, pas):
    return exec("SELECT * FROM users WHERE username = '{}' and password = '{}' ;".format(login, pas))

def registerUser(login, pas, email):
    if (exec("SELECT * FROM users WHERE username = '{}'".format(login)) != None):
        return False
    exec("INSERT INTO users (username, password, gamesPlayed, gamesWon, avaId, color, questionsAnswered, questionsCorrect, email) "
         "VALUES ('{}', '{}', 0, 0, 0, '1:1:1', 0, 0, '{}');".format(login, pas, email))

    return True

def updateUser(name ,avaId, gamesPlayed, gamesWon, questions, questionsAnswered):
    exec("UPDATE users SET gamesPlayed = {}, gamesWon = {}, avaId = {}, "
         "questionsAnswered = {}, questionsCorrect = {} WHERE username = '{}';".format(gamesPlayed,
                                                                                     gamesWon, avaId,
                                                                                     questions, questionsAnswered,
                                                                                     name))

def exec(command):
    db = connect()
    cursor = db.cursor()
    cursor.execute(command)
    try:
        cmd = cursor.fetchall()[0]
    except:
        print("No data to fetch")
        cmd = None
    db.commit()
    cursor.close()
    db.close()
    return cmd