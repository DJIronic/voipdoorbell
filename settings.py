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

import pjsua2 as pj
#import application

# Transport setting
class SipTransportConfig:
	def __init__(self, type, enabled):
		#pj.PersistentObject.__init__(self)
		self.type = type
		self.enabled = enabled
		self.config = pj.TransportConfig()
	def readObject(self, node):
		child_node = node.readContainer("SipTransport")
		self.type = child_node.readInt("type")
		self.enabled = child_node.readBool("enabled")
		self.config.readObject(child_node)
	def writeObject(self, node):
		child_node = node.writeNewContainer("SipTransport")
		child_node.writeInt("type", self.type)
		child_node.writeBool("enabled", self.enabled)
		self.config.writeObject(child_node)

# Account setting with buddy list
class AccConfig:
	def __init__(self):
		self.enabled = True
		self.config = pj.AccountConfig()
		self.buddyConfigs = []
	
# Master settings
class AppConfig:
	def __init__(self):
		self.epConfig = pj.EpConfig()	# pj.EpConfig()
		self.udp = SipTransportConfig(pj.PJSIP_TRANSPORT_UDP, True)
		self.tcp = SipTransportConfig(pj.PJSIP_TRANSPORT_TCP, True)
		self.tls = SipTransportConfig(pj.PJSIP_TRANSPORT_TLS, False)
		self.accounts = []		# Array of AccConfig

