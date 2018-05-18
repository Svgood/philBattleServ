if __name__ == '__main__':
    print("PhilBattle Server console, help - for commands list")
    while True:
        s = input()
        if not handle(s):
            break
    print("Closed")
    input()

def handle(msg):
    if msg == "lobbies":
        print("Lobiesssss")