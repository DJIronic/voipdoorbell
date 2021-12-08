import time

class Lock:
    def __init__(self, passphrase):
        self.passphrase = passphrase
        self.stack = []

    def unlock(self):
        print("==================== unlocked ====================")
        time.sleep(5)
        self.lock()

    def lock(self):
        print("==================== locked ====================")

    def addDigit(self, digit):
        self.stack.append(digit)

    def receiveOk(self):
        passcode = ""
        passcode = passcode.join(self.stack)
        print("Passcode is " + passcode)
        if(passcode == self.passphrase):
            self.unlock()
        else:
            print("Wrong passcode")

        self.stack = []

    def receiveReset(self):
        print("Resetting")
        self.stack = []

