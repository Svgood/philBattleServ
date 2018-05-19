from configs import commands as c
from database import db


class PreGameHandler:

    def __init__(self, server):
        self.server = server

    def handle(self, command, user):
        cmd = command[0]

        if cmd == "register":
            if db.registerUser(command[1], command[2], command[3]):
                user.sendMsg(c.openLoginScreen())
                user.sendMsg(c.error("Регистрация успешна"))
            else:
                user.sendMsg(c.error("Пользователь уже зарегистрирован"))

        if cmd == "login":
            userInfo = db.getUser(command[1], command[2])
            if userInfo:

                user.authorised = True
                user.loadUser(userInfo)
                user.sendMsg(user.formPlayerInfo())
                user.sendMsg("log:1;")
            else:
                user.sendMsg("log:0;")
                user.sendMsg(c.error("Неверный логин или пароль"))

        if cmd == "gl":
            com = ""
            for l in self.server.lobbyManager.lobbies:
                if not l.gameStarted:
                    com += "lobbie:" + l.formLobbyInfo()
            com += "sl:;"
            user.sendMsg(com)

        if cmd == "cl":
            lobby = self.server.lobbyManager.createLobby(user)
            lobby.questionsType = int(command[1])
            com = "lobbie:" + lobby.formLobbyInfo()
            user.sendMsg(com)
            user.sendMsg(user.lobby.formPlayerInfo())
            user.sendMsg("jl:{}".format(lobby.lobbyId))

        if cmd == "jl":
            l = self.server.lobbyManager.findLobbyById(int(command[1]))
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