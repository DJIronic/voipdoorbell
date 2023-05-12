# $Id$
#
# pjsua Python GUI Demo
#
# Copyright (C)2013 Teluu Inc. (http://www.teluu.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
#
import sys

import random
import pjsua2 as pj
import endpoint as ep
import lock
import time


# Call class
class Call(pj.Call):
    """
    High level Python Call object, derived from pjsua2's Call object.
    """
    def __init__(self, acc, peer_uri='', chat=None, call_id = pj.PJSUA_INVALID_ID, lock=None):
        pj.Call.__init__(self, acc, call_id)
        self.acc = acc
        self.peerUri = peer_uri
        self.chat = chat
        self.connected = False
        self.onhold = False
        self.lockInst = lock

    def onCallState(self, prm):
        ci = self.getInfo()
        self.connected = ci.state == pj.PJSIP_INV_STATE_CONFIRMED



    def onCallMediaState(self, prm):
        ci = self.getInfo()
        print("Call state:", ci.state)

        for mi in ci.media:
            if mi.type == pj.PJMEDIA_TYPE_AUDIO and \
              (mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE or \
               mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD):
                m = self.getMedia(mi.index)
                am = pj.AudioMedia.typecastFromMedia(m)
                # connect ports
                ep.Endpoint.instance.audDevManager().getCaptureDevMedia().startTransmit(am)
                am.startTransmit(ep.Endpoint.instance.audDevManager().getPlaybackDevMedia())


                if mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD and not self.onhold:
                    self.chat.addMessage(None, "'%s' sets call onhold" % (self.peerUri))
                    self.onhold = True
                elif mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE and self.onhold:
                    self.chat.addMessage(None, "'%s' sets call active" % (self.peerUri))
                    self.onhold = False




        if self.chat:
            self.chat.updateCallMediaState(self, ci)

    def onDtmfDigit(self, prm):
        print("Received DTMF digit: " + prm.digit)

        if(prm.digit == "#"):
            print("Sending OK")
            self.lockInst.receiveOk()
            return

        if(prm.digit == "*"):
            print("Sending reset")
            self.lockInst.receiveReset()
            return

        self.lockInst.addDigit(prm.digit)

    def onCallMediaTransportState(self, prm):
        #msgbox.showinfo("pygui", "Media transport state")
        pass

    def setLock(self, lock):
        self.lockInst = lock

    # Check for call disconnection to prevent crashes when button is pressed repeatedly
    def isCallDisconnected(self):
        try:
         call_info = self.getInfo()
         return call_info.state in (pj.PJSIP_INV_STATE_DISCONNECTED, pj.PJSIP_INV_STATE_NULL)
        except pj.Error:
         return True