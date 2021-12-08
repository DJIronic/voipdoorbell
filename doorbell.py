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

BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON,GPIO.IN)

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

while(True):
    input = GPIO.input(BUTTON)
    if not input:
        call_param = pj.CallOpParam()
        call_param.opt.audioCount = 1
        call_param.opt.videoCount = 0

        newCall = call.Call(account, userConfig['lock']['targetVoipUri'], lock=lockInst)
        newCall.makeCall(userConfig['lock']['targetVoipUri'], call_param)
        ep.libHandleEvents(10)
    ep.libHandleEvents(10)
