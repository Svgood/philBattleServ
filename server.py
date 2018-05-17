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
from lobbyManager import LobbyManager


class Serv:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((config.host, config.port))
        self.lobbyManager = LobbyManager(self)

        self.conns = []
        self.users = []
        self.threads = []
        self.curThread = 0
        self.lobbiesId = 0
        self.usersId = 0

        print("started")

    def listen(self):

        #alive checker
        t = threading.Thread(target=self.aliveChecker)
        t.start()

        while True:
            print("listening")
            self.sock.listen(128)
            conn, addr = self.sock.accept()
            self.conns.append(conn)

            usr = User(self.curThread, "NoName{}".format(self.curThread), conn)
            self.users.append(usr)

            print("Got connection " + str(len(self.conns)))

            t = threading.Thread(target=self.listenConn, args=(usr, conn))
            self.threads.append(t)
            t.start()

            self.curThread += 1

    def listenConn(self, user, con):
        while True:
            try:
                data = con.recv(1024)
            except:
                self.closeConnection(user, 1)
                return
            if not data:
                self.closeConnection(user, 1)
                return
            else:
                print("Got message from conn id: " + str(user.id))
                print(util.bs(data))
                if not self.msgHandler(user, util.bs(data)):
                    self.closeConnection(user)
                    return

    def aliveChecker(self):
        while True:
            time.sleep(5)
            for user in self.users:
                #print("checking if alive")
                try:
                    user.sendMsg("?:;")
                except:
                    self.closeConnection(user, 1)

    def msgHandler(self, user, msg):
        if ";" in msg:
            msg = msg[:msg.find(";")]
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
            user.lobby.sendToPlayers(msg + ";")
            user.lobby.nextPlayer()
        if cmd == "nt":
            user.lobby.nextPlayer()

        if cmd == "quitLobby":
            user.lobby.kickPlayer(user.id)

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
            for l in self.lobbyManager.lobbies:
                if not l.gameStarted:
                    com += "lobbie:" + l.formLobbyInfo()
            com += "sl:;"
            user.sendMsg(com)

        if cmd == "cl":
            lobby = self.lobbyManager.createLobby(user)
            lobby.questionsType = int(command[1])
            com = "lobbie:" + lobby.formLobbyInfo()
            user.sendMsg(com)
            user.sendMsg(user.lobby.formPlayerInfo())
            user.sendMsg("jl:{}".format(lobby.lobbyId))

        if cmd == "jl":
            l = self.lobbyManager.findLobbyById(int(command[1]))
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

    def closeConnection(self, user, code=0):
        if code == 0:
            print("Closing connection - ok")
        else:
            print("Closing connection error")

        if user == None:
            return
        user.onCloseChecks()
        self.users.remove(user)
        try:
            user.conn.close()
        except:
            print("Closed already")


    def checkUser(self, login, password):
        return True
        if login == "admin" and password == "admin":
            return True

    def setRandomQuestion(self, type = 0):
        cmd = db.getQuestion(type)
        com = cmd[1]
        if ":" in cmd[1]:
            com = cmd[1][:cmd[1].find(":")]
        if ";" in cmd[1]:
            com = com.replace(";", ",")
        cmd = "sq:{}:{}:{}:{}:{};".format(com, cmd[2], cmd[3], cmd[4], cmd[5])
        return cmd





