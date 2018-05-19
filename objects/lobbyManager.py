import threading
import time

from objects.lobby import Lobby

class LobbyManager:

    def __init__(self, server):
        self.lobbies = []
        self.lobbiesId = 1
        self.server = server
        t = threading.Thread(target=self.lobbyChecker)
        t.start()

    def createLobby(self, hostUser):
        lobby = Lobby(self.lobbiesId, hostUser, self.server)
        self.lobbies.append(lobby)
        self.lobbiesId += 1
        return lobby

    def findLobbyById(self, id):
        for i in range(len(self.lobbies)):
            if self.lobbies[i].lobbyId == id:
                return self.lobbies[i]
        return None

    def lobbyChecker(self):
        while True:
            time.sleep(10)
            for l in self.lobbies:
                if len(l.players) == 0:
                    l.closeLobby()