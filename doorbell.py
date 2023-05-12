import sys
import time
import threading
import configparser
from os.path import exists

import RPi.GPIO as GPIO
import lock

import pjsua2 as pj
import endpoint
import settings
import account
import call

BUTTON = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
write=sys.stdout.write

configPath = sys.argv[1]
if(not exists(configPath)):
    print("Path to config is not set or is not valid path!")
    quit()



# Load config
userConfig = configparser.ConfigParser()
userConfig.read(configPath)

# Prepare lock class
lockInst = lock.Lock(userConfig['lock']['passcode'])

# Accounts
accList = []
ep = endpoint.Endpoint()
ep.libCreate()
# Default config
appConfig = settings.AppConfig()

# Threading
appConfig.epConfig.uaConfig.threadCnt = 0
appConfig.epConfig.uaConfig.mainThreadOnly = True

# Config

appConfig.epConfig.uaConfig.maxCalls = 1
appConfig.epConfig.medConfig.channelCount = 1  # Set the channel count to 1 (mono)
appConfig.epConfig.medConfig.clockRate = 8000
appConfig.epConfig.medConfig.sndClockRate = 8000  # Set the sample rate to 16000 Hz
appConfig.epConfig.medConfig.ptime = 140  # Set the ptime to 500 ms
ep.libInit(appConfig.epConfig)
ep.transportCreate(appConfig.udp.type, appConfig.udp.config)


#configure the library
config = pj.AccountConfig()
config.idUri = userConfig['pjsua2']['id']
config.regConfig.registrarUri = userConfig['pjsua2']['registrarUri']
#config.regConfig.contactParams = "sip:736370@sip.odorik.cz"




config.presConfig.publishEnabled = True

cred = pj.AuthCredInfo()
cred.realm = userConfig['pjsua2']['realm']
cred.scheme = userConfig['pjsua2']['scheme']
cred.username = userConfig['pjsua2']['username']
cred.data = userConfig['pjsua2']['password']

config.sipConfig.authCreds.append(cred)

if not endpoint.validateSipUri(config.idUri):
    print("ERROR IN ID URI")

if not endpoint.validateSipUri(config.regConfig.registrarUri):
    print("ERROR IN REGISTRAR URI")

if not endpoint.validateSipUri(config.regConfig.contactParams):
    print("ERROR IN CONTANT PARAMS")

account = account.Account()
account.create(config)

# Start library
ep.libStart()
ep.libHandleEvents(10)


# Initialize an ongoing_call variable before the loop
ongoing_call = None

while True:
    input = GPIO.input(BUTTON)
    if input == GPIO.HIGH:  # Button is pressed
        # Check if there's an ongoing call
        if ongoing_call is None or ongoing_call.isCallDisconnected():
            print("No call detected, creating a new one to " + userConfig['lock']['targetVoipUri'])
            call_param = pj.CallOpParam()
            call_param.opt.audioCount = 1
            call_param.opt.videoCount = 0

            ongoing_call = call.Call(account, userConfig['lock']['targetVoipUri'], lock=lockInst)
            ongoing_call.makeCall(userConfig['lock']['targetVoipUri'], call_param)
        else:
            print("There's an ongoing call, can't make a new one.")
        ep.libHandleEvents(10)
    ep.libHandleEvents(10)
    time.sleep(0.1)  # Add a short delay to avoid excessive CPU usage

