from utils import util
from utils.vec2 import Vec2
from database import db


class User:

    def __init__(self, id, name, conn):
        self.authorised = False
        self.id = id
        self.name = name
        self.conn = conn

        #lobby
        self.gameId = 0
        self.lobby = None
        self.contestAnswer = 0
        self.health = 1
        self.attackingCell = Vec2(-1, -1)

        #Stat
        self.avaId = 0
        self.color = "1:1:1"
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.questionsAnswered = 0
        self.questionsRight = 0

    def sendMsg(self, msg):
        self.conn.send(util.sb(msg))

    def load(self, data):
        self.name = data[1]
        self.avaId = data[5]
        self.gamesPlayed = data[3]
        self.gamesWon = data[4]
        self.color = data[6]
        self.questionsAnswered = data[7]
        self.questionsRight = data[8]
        self.authorised = True

    def onCloseChecks(self):
        if self.lobby is not None:
            if self == self.lobby.host:
                print("User was host, closing lobby")
                if not self.lobby.gameStarted:
                    self.lobby.closeLobby()
                else:
                    self.lobby.kickPlayer(self.id)
            else:
                tempLobby = self.lobby
                self.lobby.kickPlayer(self.id)

    def formPlayerInfo(self):
        return "playerInfo:{}:{}:{}:{}:{}:{};".format(self.name, self.avaId,
                                                     self.gamesPlayed, self.gamesWon,
                                                     self.questionsAnswered, self.questionsRight)

    def loadUser(self, info):
        print(info)
        self.name = info[1]
        self.gamesPlayed = info[3]
        self.gamesWon = info[4]
        self.avaId = info[5]
        self.questionsAnswered = info[7]
        self.questionsRight = info[8]
        pass


    def updatePlayer(self, gamesPlayed = 0, gamesWon = 0, questionsAnswered = 0, questionsRight = 0, avaId = -1):
        self.gamesPlayed += gamesPlayed
        self.gamesWon += gamesWon
        self.questionsAnswered += questionsAnswered
        self.questionsRight += questionsRight

        if (avaId != -1):
            self.avaId = avaId

        db.updateUser(self.name, self.avaId, self.gamesPlayed, self.gamesWon,
                      self.questionsAnswered, self.questionsRight)
