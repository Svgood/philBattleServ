def captureCell(playedId, x, y):
    return "c:{}:{}:{};".format(playedId, x, y)


def setPlayer(num):
    return "sp:{};".format(num)


def joinLobby(playerId, lobbyId):
    return "jl:{}:{};".format(playerId, lobbyId)


def setCurPlayer(playerId):
    return "scp:{};".format(playerId)


def commonQuestion():
    return "scq:;"


def contest(idDef, idAt):
    return "cq:{}:{}:;".format(idDef, idAt)


def contestWinner(playerId):
    return "cw:{};".format(playerId)


def contestNewQuestion():
    return "cnq:;"

def closeLobby():
    return "close:;"

def minusHealth(id):
    return "minusHealth:{}:;".format(id)

def openLoginScreen():
    return "logScreen:;"

def error(msg):
    return "error:{}:;".format(msg)