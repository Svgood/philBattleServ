from configs import netCodes
from database import db
from configs import commands as c

class GameHandler:

    def __init__(self, server):
        self.server = server

    def handle(self, command, user):
        cmd = command[0]

        #command for checking everybody game readiness.
        if cmd == "rdy":
            user.lobby.playerReady()

        #start contest
        if cmd == "sc":
            user.lobby.startContest(user.gameId, int(command[1]), int(command[2]), int(command[3]))

        #contest answer
        if cmd == "ca":
            if command[1] == "1":
                user.lobby.contestAnswer(user.gameId, True)
            else:
                user.lobby.contestAnswer(user.gameId, False)

        #capture cell
        if cmd == "c":
            user.updatePlayer(questionsRight=1)
            user.lobby.sendToPlayers(":".join(command) + ";")
            #user.lobby.nextTurn()

        #switch to next player
        if cmd == "nt":
            user.updatePlayer(questionsAnswered=1)
            user.lobby.nextTurn()

        if cmd == "quitLobby":
            user.lobby.kickPlayer(user.id)

        #Check net codes
        if cmd == str(netCodes.QuestionAnswered):
            user.lobby.questionAnswered()

        if cmd == str(netCodes.MarkCell):
            user.lobby.sendToPlayers(":".join(command) + ";")
            return
