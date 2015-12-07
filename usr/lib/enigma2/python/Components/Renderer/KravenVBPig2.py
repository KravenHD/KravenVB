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
from enigma import eVideoWidget,eTimer,getDesktop,eServiceCenter,iServiceInformation
from Screens.InfoBar import InfoBar
from Components.SystemInfo import SystemInfo
from Components.config import config
from enigma import eActionMap

fbtool_1=None
init_PiG_1=None
fb_size_history_1=[]

class KravenVBPig2(Renderer):
	def __init__(self):
		Renderer.__init__(self)
		global fbtool_1
		fbtool_1=KravenFBHelper()
		self.Position=self.Size=None
		self.decoder=0
		if SystemInfo.get("NumVideoDecoders",1)>1:
			self.decoder=1
		self.fb_w=getDesktop(0).size().width()
		self.fb_h=getDesktop(0).size().height()
		self.fb_size=None
		self._del_pip=False
		self._can_extended_PiG=False
		self.first_PiG=False
		self.is_channelselection=False

		#Added by tomele
		self.x2=97
		self.y2=369
		self.w2=400
		self.h2=220
		self.x2=format(int(float(self.x2)/self.fb_w*720.0),'x').zfill(8)
		self.y2=format(int(float(self.y2)/self.fb_h*576.0),'x').zfill(8)
		self.w2=format(int(float(self.w2)/self.fb_w*720.0),'x').zfill(8)
		self.h2=format(int(float(self.h2)/self.fb_h*576.0),'x').zfill(8)
		self.fb_size2=[self.w2,self.h2,self.x2,self.y2]
		self.prev_size2=None

	GUI_WIDGET=eVideoWidget

	def postWidgetCreate(self,instance):
		if config.usage.use_extended_pig.value and config.usage.use_pig.value and self.decoder==1:
			if InfoBar.instance:
				serviceHandler=eServiceCenter.getInstance()
				ref=InfoBar.instance.session.nav.getCurrentlyPlayingServiceReference()
				if ref:
					serviceinfo=serviceHandler.info(ref)
					if serviceinfo and not serviceinfo.getInfoObject(ref,iServiceInformation.sTransponderData):
						self.decoder=0
		else:
			self.decoder=0
		self.prev_fb_info=fbtool_1.getFBSize()
		if self.decoder>0:
			self.prev_fb_info_second_dec=fbtool_1.getFBSize(decoder=1)
		desk=getDesktop(0)
		instance.setDecoder(self.decoder)
		instance.setFBSize(desk.size())
		self.this_instance=instance

	def applySkin(self,desktop,parent):
		# do some voodoo for the lovely ChannelSelection ...
		if parent.__class__.__name__=="ChannelSelection":
			self.is_channelselection=True
			if not config.usage.use_extended_pig_channelselection.value:
				self.decoder=0
				self.this_instance.setDecoder(self.decoder)
		if self.skinAttributes is not None:
			attribs=[]
			for (attrib,value) in self.skinAttributes:
				if attrib=="OverScan":
					if value.lower()=="false" or value=="0":
						self.instance.setOverscan(False)
				else:
					attribs.append((attrib,value))
				if attrib=="position":
					x=value.split(',')[0]
					y=value.split(',')[1]
				elif attrib=="size":
					w=value.split(',')[0]
					h=value.split(',')[1]

			self.skinAttributes=attribs
			x=format(int(float(x)/self.fb_w*720.0),'x').zfill(8)
			y=format(int(float(y)/self.fb_h*576.0),'x').zfill(8)
			w=format(int(float(w)/self.fb_w*720.0),'x').zfill(8)
			h=format(int(float(h)/self.fb_h*576.0),'x').zfill(8)
			self.fb_size=[w,h,x,y]
		ret=Renderer.applySkin(self,desktop,parent)
		if ret:
			self.Position=self.instance.position() # fixme,scaling!
			self.Size=self.instance.size()
		return ret

	def onShow(self):
		fbtool_1.is_PiG=True
		if self.instance:
			if self.Size:
				self.instance.resize(self.Size)
			if self.Position:
				self.instance.move(self.Position)
			if self.decoder>0:
				fbtool_1.setFBSize(['000002d0','00000240','00000000','00000000'],decoder=0)
				if InfoBar.instance and not InfoBar.instance.session.pipshown:
					InfoBar.instance.showPiG()
					global init_PiG_1
					if not init_PiG_1 and not self.is_channelselection and InfoBar.instance.session.pipshown:
						self.first_PiG=True
						init_PiG_1=True
				cur_size=fbtool_1.getFBSize(decoder=1)
				if self.fb_size:
					global fb_size_history_1
					if fb_size_history_1 != self.fb_size:
						fb_size_history_1=self.fb_size
						fbtool_1.setFBSize(self.fb_size,self.decoder)
			elif InfoBar.instance and InfoBar.instance.session.pipshown and not InfoBar.instance.session.is_audiozap:
				fbtool_1.setFBSize(['000002d0','00000240','00000000','00000000'],decoder=0)
				if self.fb_size:
					fbtool_1.setFBSize(self.fb_size,decoder=1)

		#Added by tomele
		if self.decoder==0:
			self.prev_size2=fbtool_1.getFBSize(decoder=1)
			fbtool_1.setFBSize(self.fb_size2,decoder=1)
		else:
			self.prev_size2=fbtool_1.getFBSize(decoder=0)
			fbtool_1.setFBSize(self.fb_size2,decoder=0)

	def onHide(self):

		#Added by tomele
		if self.decoder==0:
			fbtool_1.setFBSize(['000002d0','00000240','00000000','00000000'],decoder=1,force=True)
		else:
			fbtool_1.setFBSize(['000002d0','00000240','00000000','00000000'],decoder=0,force=True)

		if self.instance:
			fbtool_1.is_PiG=False
			self.preWidgetRemove(self.instance)
			if InfoBar.instance and InfoBar.instance.session.pipshown and InfoBar.instance.session.is_splitscreen:
				self.prev_fb_info=InfoBar.instance.session.pip.prev_fb_info
				self.prev_fb_info_second_dec=InfoBar.instance.session.pip.prev_fb_info_second_dec
				fbtool_1.setFBSize(self.prev_fb_info_second_dec,decoder=1)
				fbtool_1.setFBSize_delayed(self.prev_fb_info,decoder=0,delay=200)
			elif InfoBar.instance and InfoBar.instance.session.pipshown and not InfoBar.instance.session.is_splitscreen and not InfoBar.instance.session.is_audiozap and not InfoBar.instance.session.is_pig:
				self.prev_fb_info=InfoBar.instance.session.pip.prev_fb_info
				fbtool_1.setFBSize_delayed(self.prev_fb_info,decoder=1,delay=200)

	#Added by tomele
	def changed(self,what):
		if InfoBar.instance:
			current=self.source.getCurrentService()
			if InfoBar.instance.session.pipshown:
				InfoBar.instance.session.pip.playService(current)
			else:
				InfoBar.instance.session.nav.playService(current)

	def destroy(self):
		if self.first_PiG and InfoBar.instance.session.pipshown:
			global init_PiG_1
			init_PiG_1=False
			if InfoBar.instance and InfoBar.instance.session.is_pig:
				InfoBar.instance.showPiP()
		self.__dict__.clear()

#Added by tomele
class KravenFBHelper:
	def __init__(self):
		self.fb_proc_path="/proc/stb/vmpeg"
		self.fb_info=["dst_width","dst_height","dst_left","dst_top"]
		self.new_fb_size_pos=None
		self.decoder=None
		self.delayTimer=None
		self.is_PiG=False

	def getFBSize(self,decoder=0):
		ret=[]
		for val in self.fb_info:
			try:
				f=open("%s/%d/%s" % (self.fb_proc_path,decoder,val),"r")
				fb_val=f.read().strip()
				ret.append(fb_val)
				f.close()
			except IOError:
				pass
		if len(ret)==4:
			return ret
		return None

	def setFBSize(self,fb_size_pos,decoder=0,force=False):
		if self.delayTimer:
			self.delayTimer.stop()
		if (InfoBar.instance and InfoBar.instance.session.pipshown) or force:
			if fb_size_pos and len(fb_size_pos)>=4:
				i=0
				for val in self.fb_info:
					try:
						f=open("%s/%d/%s" % (self.fb_proc_path,decoder,val),"w")
						fb_val=fb_size_pos[i]
						f.write(fb_val)
						f.close()
					except IOError:
						pass
					i+=1
				for val in ("00000001","00000000"):
					try:
						f=open("%s/%d/%s" % (self.fb_proc_path,decoder,"dst_apply"),"w")
						f.write(val)
						f.close()
					except IOError:
						pass

	def delayTimerFinished(self):
		fb_size_pos=self.new_fb_size_pos
		decoder=self.decoder
		self.new_fb_size_pos=None
		self.decoder=None
		if not self.is_PiG:
			self.setFBSize(fb_size_pos,decoder)

	def setFBSize_delayed(self,fb_size_pos,decoder=0,delay=1000):
		if fb_size_pos and len(fb_size_pos)>=4:
			self.new_fb_size_pos=fb_size_pos
			self.decoder=decoder
			self.delayTimer=eTimer()
			self.delayTimer.callback.append(self.delayTimerFinished)
			self.delayTimer.start(delay)

