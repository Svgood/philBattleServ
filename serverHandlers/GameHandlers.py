from database import db
from configs import commands as c

class GameHandler:

    def __init__(self, server):
        self.server = server

    def handle(self, command, user):
        cmd = command[0]

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
            user.updatePlayer(questionsRight=1)
            user.lobby.sendToPlayers(":".join(command) + ";")
            user.lobby.nextPlayer()
        if cmd == "nt":
            user.updatePlayer(questionsAnswered=1)
            user.lobby.nextPlayer()

        if cmd == "quitLobby":
            user.lobby.kickPlayer(user.id)