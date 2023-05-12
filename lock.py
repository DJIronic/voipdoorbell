import time
import RPi.GPIO as GPIO

class Lock:
    def __init__(self, passphrase):
        self.passphrase = passphrase
        GPIO.setup(12, GPIO.OUT)
        self.stack = []


    def unlock(self):
        GPIO.output(12, GPIO.HIGH)
        print("==================== unlocked ====================")
        time.sleep(5)
        self.lock()

    def lock(self):
        GPIO.output(12, GPIO.LOW)
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

