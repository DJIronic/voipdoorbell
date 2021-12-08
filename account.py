import random

import pjsua2 as pj
import call

class Account(pj.Account):
    def __init__(self):
        pj.Account.__init__(self)
        self.randId = random.randint(1, 9999)
        self.cfg = pj.AccountConfig()
        self.cfgChanged = False
        self.buddyList = []
        self.chatList = []
        self.deleting = False

    def onIncomingCall(self, prm):
        c = call.Call(self, call_id=prm.callId)
        call_prm = pj.CallOpParam()
        call_prm.statusCode = 180
        c.hangup(call_prm)
