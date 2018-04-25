from utils import util
from configs import commands as c
from utils.vec2 import Vec2

class Lobby:

    def __init__(self, lobbyId, host, serv):
        self.serv = serv
        self.lobbyId = lobbyId
        self.gameStarted = False
        self.name = "testLobby"
        self.maxPlayers = 2
        self.host = host
        self.host.lobby = self
        self.players = [self.host]

        self.state = 1
        self.currentPlayerTurn = 1

        self.contesters = []
        self.winContesters = []
        self.contestersAnswered = 0
        self.contestCell = Vec2(0, 0)
        self.contestType = 0

        self.playersReady = 0
        self.chat = ""

    def formLobbyInfo(self):
        return "{}:{}:{}:{};".format(self.name, len(self.players), self.maxPlayers, self.lobbyId)

    def formPlayerInfo(self):
        com = "cp:;"
        for p in self.players:
            com += "player:{};".format(p.name)
        return com

    def closeLobby(self):
        self.serv.lobbies.remove(self)
        self.sendToPlayers(c.closeLobby())
        del(self)


    def kickPlayer(self, id):
        p = self.findPlayerById(id)
        self.players.remove(p)

        if not self.gameStarted:
            self.sendToPlayers("cp:;" + self.formPlayerInfo())
            p.sendMsg(c.closeLobby())
        else:
            #Delete in game
            pass

        if len(self.players) == 0:
            self.closeLobby()


    def playerReady(self):
        self.playersReady += 1
        if (self.playersReady == len(self.players)):
            self.startGame()

    def startLobby(self):
        self.sendToPlayers("start:{}:;".format(len(self.players)))
        self.gameStarted = True

    def nextPlayer(self, bonus = 0):
        self.sendToPlayers(self.serv.setRandomQuestion())
        if bonus == 0:
            self.currentPlayerTurn += 1
            if self.currentPlayerTurn == len(self.players) + 1:
                self.startCommonQuestion()
                self.currentPlayerTurn = 0
            else:
                if self.currentPlayerTurn == 1:
                    self.sendToPlayers("nt:;")
                self.sendToPlayers("scp:{};".format(self.currentPlayerTurn))
        else:
            self.currentPlayerTurn = 0
            self.sendToPlayers("scp:{};".format(bonus))


    def sendToPlayers(self, msg):
        for p in self.players:
            p.conn.send(util.sb(msg))

    def startGame(self):
        num = 1
        cmd = ""
        for i in range(len(self.players)):
            self.players[i].gameId = num
            cmd += c.captureCell(num, 0 + num, 0 + num)
            num += 1

        num = 1
        for p in self.players:
            p.sendMsg(c.setPlayer(num) +
                           cmd +
                           c.setCurPlayer(1))
            num += 1
        self.sendToPlayers(self.serv.setRandomQuestion())

    def addUser(self, user):
        self.players.append(user)
        user.lobby = self

    def startCommonQuestion(self):
        self.contestType = 1
        self.winContesters = []
        self.contestersAnswered = 0
        self.contesters = self.players.copy()
        self.sendToPlayers(c.commonQuestion())

    def startContest(self, attackerId, defenderId, x, y):
        self.contestType = 0
        self.contestCell = Vec2(x, y)
        self.contestersAnswered = 0
        self.winContesters = []
        self.contesters = []
        for p in self.players:
            if p.gameId == attackerId or p.gameId == defenderId:
                p.contestAnswer = 0
                self.contesters.append(p)
                p.sendMsg(c.contest(defenderId, attackerId))

        for p in self.contesters:
            p.health = 2
            if p.gameId == defenderId: p.health += 1

    def contestAnswer(self, playerdId, yes : bool):
        if yes:
            for p in self.contesters:
                if p.gameId == playerdId:
                    p.contestAnswer = 1
                    self.winContesters.append(p)

        self.contestersAnswered += 1
        if self.contestersAnswered == len(self.contesters):
            if self.contestType == 0:
                if len(self.winContesters) == 1:
                    for p in self.contesters:
                        if p != self.winContesters[0]:
                            p.health -= 1
                            if p.health <= 0:
                                self.sendToContesters(c.minusHealth(p.gameId))
                                self.sendToPlayers(c.contestWinner(self.winContesters[0].gameId) +
                                                   c.captureCell(self.winContesters[0].gameId, self.contestCell.x, self.contestCell.y))
                                self.nextPlayer()
                                return
                            else:
                                self.sendToContesters(c.minusHealth(p.gameId))
                                self.resetContestVars()
                                return
                else:
                    self.resetContestVars()

            if self.contestType == 1:
                self.contesters = self.winContesters
                if len(self.winContesters) == 1:
                    self.nextPlayer(self.winContesters[0].gameId)
                elif len(self.winContesters) == 0:
                    self.nextPlayer()
                else:
                    self.resetContestVars()

    def sendToContesters(self, msg):
        for p in self.contesters:
            p.sendMsg(msg)

    def resetContestVars(self):
        self.winContesters = []
        self.contestersAnswered = 0
        question = self.serv.setRandomQuestion()
        for p in self.contesters:
            p.sendMsg(question)
            p.contestAnswer = 0
            p.sendMsg(c.contestNewQuestion())

    def findPlayerById(self, id):
        for i in range(len(self.players)):
            if self.players[i].id == id:
                return self.players[i]
        return None



