import socket
import threading
import mysql.connector
import db
import time

from utils import util
from configs import config
from configs import commands as c

from objects.users import User
from objects.lobby import Lobby


class Serv:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config.host, config.port))
        self.conns = []
        self.users = []
        self.lobbies = []
        self.threads = []
        self.curThread = 0
        self.lobbiesId = 0
        self.usersId = 0

        print("started")

    def listen(self):

        t = threading.Thread(target=self.aliveChecker)
        t.start()

        while True:
            print("listening")
            self.sock.listen(10)
            conn, addr = self.sock.accept()
            self.conns.append(conn)

            usr = User(self.curThread, "testUser{}".format(self.curThread), conn)
            self.users.append(usr)

            print("Got connection " + str(len(self.conns)))

            t = threading.Thread(target=self.listenConn, args=(usr, conn))
            self.threads.append(t)
            self.threads[len(self.threads) - 1].start()

            self.curThread += 1

    def listenConn(self, user, con):
        while True:
            data = con.recv(1024)
            if not data:
                print("Closing connection error")
                if user == None:
                    return
                user.onCloseChecks()
                self.users.remove(user)
                return
            else:
                print("Got message from conn id: " + str(user.id))
                print(util.bs(data))
                if not self.msgHandler(user, util.bs(data)):
                    print("Closing connection standart")
                    user.onCloseChecks()
                    self.users.remove(user)
                    user.conn.close()
                    return

    def aliveChecker(self):
        while True:
            time.sleep(5)
            for user in self.users:
                #print("checking if alive")
                try:
                    user.sendMsg("?:;")
                except:
                    print("error")
                    self.users.remove(user)

    def msgHandler(self, user, msg):
        command = msg.split(":")
        cmd = command[0]

        if cmd == "closeConnection":
            return False

        #Game commands
        if cmd == "rdy":
            user.lobby.playerReady()

        if cmd == "sc":
            user.lobby.startContest(user.gameId, int(command[1]), int(command[2]), int(command[3]))
        if cmd == "ca":
            if command[1] == "1":
                user.lobby.contestAnswer(user.gameId, True)
            else:
                user.lobby.contestAnswer(user.gameId, False)

        if cmd == "c":
            user.lobby.sendToPlayers(msg)
            user.lobby.nextPlayer()
        if cmd == "nt":
            user.lobby.nextPlayer()

        #Pregame handle
        #
        #
        #
        #
        if cmd == "register":
            if len(db.getUser(command[1])) == 0:
                db.registerUser(command[1], command[2], command[3])
                user.sendMsg(c.error("Регистрация успешна"))
            else:
                user.sendMsg(c.error("Пользователь уже зарегестрирован"))

        if cmd == "login":
            if self.checkUser(command[1], command[2]):
                user.authorised = True
                user.name = command[1]
                user.sendMsg("log:1")
            else:
                user.sendMsg("log:0")

        if cmd == "gl":
            com = ""
            for l in self.lobbies:
                if not l.gameStarted:
                    com += "lobbie:" + l.formLobbyInfo()
            com += "sl:;"
            user.sendMsg(com)

        if cmd == "cl":
            lobby = self.createLobby(user)
            com = "lobbie:" + lobby.formLobbyInfo()
            user.sendMsg(com)
            user.sendMsg(user.lobby.formPlayerInfo())
            user.sendMsg("jl:{}".format(lobby.lobbyId))

        if cmd == "jl":
            l = self.findLobbyById(int(command[1]))
            if l.maxPlayers != len(l.players):
                l.sendToPlayers("player:{};ul:;".format(user.name))
                l.addUser(user)
                user.sendMsg(user.lobby.formPlayerInfo())
                user.sendMsg("jl:" + command[1])
            else:
                user.sendMsg(c.error("Лобби заполнено"))

        if cmd == "closel":
            if user.lobby.host == user:
                user.lobby.closeLobby()
            else:
                user.lobby.kickPlayer(user.id)

        if cmd == "sl":
            if user.lobby.host == user:
                if len(user.lobby.players) > 1:
                    user.lobby.startLobby()
                else:
                    user.sendMsg(c.error("Слишком мало игроков в лобби"))

        return True




    def checkUser(self, login, password):
        return True
        if login == "admin" and password == "admin":
            return True

    def createLobby(self, hostUser):
        lobby = Lobby(self.lobbiesId, hostUser, self)
        self.lobbies.append(lobby)
        self.lobbiesId += 1
        return lobby

    def send(self, conn, message):
        conn.send(util.sb(message))

    def findLobbyById(self, id):
        for i in range(len(self.lobbies)):
            if self.lobbies[i].lobbyId == id:
                return self.lobbies[i]
        return None

    def setRandomQuestion(self):
        cmd = db.getQuestion()
        com = cmd[1]
        if ":" in cmd[1]:
            com = cmd[1][:cmd[1].find(":")]
        if ";" in cmd[1]:
            com = com.replace(";", ",")
        cmd = "sq:{}:{}:{}:{}:{};".format(com, cmd[2], cmd[3], cmd[4], cmd[5])
        return cmd





