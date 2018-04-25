def bs(byteString):
    return byteString.decode("utf-8")

def sb(stringByte):
    return bytearray(stringByte, "utf-8")

def printLog(msg):
    print(msg)
    with open("logs.txt", "a") as f:
        f.write(msg + "\n")