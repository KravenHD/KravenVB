#
#  Channellist Preview Renderer
#
#  Modified by tomele for Kraven Skins
#
#  based on
#  P(icture)i(n)g(raphics) renderer
#  by VTi-Team
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan
#  Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source,
#  you are allowed to modify it (if you keep the license),
#  but it may not be commercially distributed other than
#  under the conditions noted above.
#

from Renderer import Renderer
from enigma import eVideoWidget, eSize, ePoint, getDesktop, eServiceCenter, eServiceReference, getDesktop, iServiceInformation
from Screens.InfoBar import InfoBar
from Tools.FBHelperTool import FBHelperTool
from Components.SystemInfo import SystemInfo
from Components.config import config

fbtool = FBHelperTool()
init_PiG = None
fb_size_history = []

class KravenVBPig3(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		self.Position = self.Size = None
		self.decoder = 0
		if SystemInfo.get("NumVideoDecoders", 1) > 1:
			self.decoder = 1
		self.fb_w = getDesktop(0).size().width()
		self.fb_h = getDesktop(0).size().height()
		self.fb_size = None
		self._del_pip = False
		self._can_extended_PiG = False
		self.first_PiG = False
		self.is_channelselection = False

	GUI_WIDGET = eVideoWidget

	def postWidgetCreate(self, instance):
		self.decoder = 0
		self.prev_fb_info = fbtool.getFBSize()
		if self.decoder > 0:
			self.prev_fb_info_second_dec = fbtool.getFBSize(decoder = 1)
		desk = getDesktop(0)
		instance.setDecoder(self.decoder)
		instance.setFBSize(desk.size())
		self.this_instance = instance

	def applySkin(self, desktop, parent):
		if self.skinAttributes is not None:
			attribs = []
			for (attrib, value) in self.skinAttributes:
				if attrib == "OverScan":
					if value.lower() == "false" or value == "0":
						self.instance.setOverscan(False)
				else:
					attribs.append((attrib, value))
				if attrib == "position":
					x = value.split(',')[0]
					y = value.split(',')[1]
				elif attrib == "size":
					w = value.split(',')[0]
					h = value.split(',')[1]
			self.skinAttributes = attribs
			x = format(int(float(x) / self.fb_w * 720.0), 'x').zfill(8)
			y = format(int(float(y) / self.fb_h * 576.0), 'x').zfill(8)
			w = format(int(float(w) / self.fb_w * 720.0), 'x').zfill(8)
			h = format(int(float(h) / self.fb_h * 576.0), 'x').zfill(8)
			self.fb_size = [w, h, x, y]
				
		ret = Renderer.applySkin(self, desktop, parent)
		if ret:
			self.Position = self.instance.position() # fixme, scaling!
			self.Size = self.instance.size()
		return ret

	def onShow(self):
		fbtool.is_PiG = True
		if self.instance:
			if self.Size:
				self.instance.resize(self.Size)
			if self.Position:
				self.instance.move(self.Position)
			if self.decoder > 0:
				fbtool.setFBSize(['000002d0', '00000240', '00000000', '00000000'], decoder = 0)
				if InfoBar.instance and not InfoBar.instance.session.pipshown:
					InfoBar.instance.showPiG()
					global init_PiG
					if not init_PiG and not self.is_channelselection and InfoBar.instance.session.pipshown:
						self.first_PiG = True
						init_PiG = True
				cur_size = fbtool.getFBSize(decoder = 1)
				if self.fb_size:
					global fb_size_history
					if fb_size_history != self.fb_size:
						fb_size_history = self.fb_size
						fbtool.setFBSize(self.fb_size, self.decoder)
			elif InfoBar.instance and InfoBar.instance.session.pipshown and not InfoBar.instance.session.is_audiozap:
				fbtool.setFBSize(['000002d0', '00000240', '00000000', '00000000'], decoder = 0)
				if self.fb_size:
					fbtool.setFBSize(self.fb_size, decoder = 1)

	def onHide(self):
		if self.instance:
			fbtool.is_PiG = False
			self.preWidgetRemove(self.instance)
			if InfoBar.instance and InfoBar.instance.session.pipshown and InfoBar.instance.session.is_splitscreen:
				self.prev_fb_info = InfoBar.instance.session.pip.prev_fb_info
				self.prev_fb_info_second_dec = InfoBar.instance.session.pip.prev_fb_info_second_dec
				fbtool.setFBSize(self.prev_fb_info_second_dec, decoder = 1)
				fbtool.setFBSize_delayed(self.prev_fb_info, decoder = 0, delay = 200)
			elif InfoBar.instance and InfoBar.instance.session.pipshown and not InfoBar.instance.session.is_splitscreen and not InfoBar.instance.session.is_audiozap and not InfoBar.instance.session.is_pig:
				self.prev_fb_info = InfoBar.instance.session.pip.prev_fb_info
				fbtool.setFBSize_delayed(self.prev_fb_info, decoder = 1, delay = 200)

	def destroy(self):
		if self.first_PiG and InfoBar.instance.session.pipshown:
			global init_PiG
			init_PiG = False
			if InfoBar.instance and InfoBar.instance.session.is_pig:
				InfoBar.instance.showPiP()
		self.__dict__.clear()