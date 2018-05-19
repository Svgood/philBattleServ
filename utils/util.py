import datetime

def bs(byteString):
    return byteString.decode("utf-8")

def sb(stringByte):
    return bytearray(stringByte, "utf-8")

def printLog(msg):
    log = "[{}]:{}".format(datetime.datetime.now().replace(microsecond=0), msg)
    print(log)
    with open("logs.txt", "a") as f:
        f.write(log + "\n")