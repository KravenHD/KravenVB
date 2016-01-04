#
#  Menu Icon Path Converter
#
#  Coded by tomele for Kraven Skins
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#

from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll

class KravenVBMenuIconPath(Poll,Converter,object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.poll_interval = 1000
		self.poll_enabled = True
		self.logo = "/usr/share/enigma2/KravenVB/logo.png"
		self.path = "/usr/share/enigma2/KravenVB-menu-icons/"
		self.type = str(type)
		
		self.names=[
		("about_screen","info.png"),
		("auto_scan","tuner.png"),
		("autores_setup","service_info.png"),
		("autoshutdown_setup","shutdowntimer.png"),
		("av_setup","movie_list.png"),
		("ci_assign","setup.png"),
		("ci_setup","setup.png"),
		("deep_standby","shutdown.png"),
		("default_lists","paket.png"),
		("default_wizard","timezone.png"),
		("device_manager","hdd.png"),
		("device_setup","setup.png"),
		("dns_setup","net.png"),
		("dvdplayer","dvd.png"),
		("ecm_info","webb.png"),
		("factory_reset","reset.png"),
		("filecommand","filecom.png"),
		("googlemaps","google.png"),
		("harddisk_check","hdd.png"),
		("harddisk_init","hdd.png"),
		("harddisk_setup","hdd.png"),
		("hardisk_selection","hdd.png"),
		("info_screen","info.png"),
		("input_device_setup","keyb.png"),
		("keyboard_setup","keyb.png"),
		("language_setup","tuner.png"),
		("lcd_setup","setup.png"),
		("lcd4linux","plugin.png"),
		("manual_scan","tuner.png"),
		("mediaplayer","media.png"),
		("mediaportal","plugin.png"),
		("movie_list","movie_list.png"),
		("moviebrowser","plugin.png"),
		("multi_quick","mqb.png"),
		("network_setup","net.png"),
		("parental_setup","look.png"),
		("picturecenterfs","plugin.png"),
		("plugin_select","plugin.png"),
		("plugin_selection","plugin.png"),
		("pvmc_mainmenu","plugin.png"),
		("RecordPaths","hdd.png"),
		("restart","restart.png"),
		("restart_enigma","restart_enigma.png"),
		("rfmod_setup","setup.png"),
		("sat_ip_client","net.png"),
		("service_info_screen","service_info.png"),
		("service_searching_selection","tuner.png"),
		("setup_selection","setup.png"),
		("sibsetup","plugin.png"),
		("sleep","shutdowntimer.png"),
		("software_manager","setup.png"),
		("sportspub_plugin","plugin.png"),
		("standby","power.png"),
		("standby_restart_list","shutdown.png"),
		("startwizzard","paket.png"),
		("subtitle_selection","sub.png"),
		("streamconvert","webb.png"),
		("system_selection","setup.png"),
		("timer_edit","timer.png"),
		("timezone_setup","tuner.png"),
		("tuner_setup","setup.png"),
		("usage_setup","setup.png"),
		("video_setup","setup.png"),
		("video_finetune","service_info.png"),
		("videoenhancement_setup","service_info.png"),
		("vti_epg_panel","paket.png"),
		("vti_menu","vtimenu.png"),
		("vti_movies","movie_list.png"),
		("vti_panel","vtimenu.png"),
		("vti_panel_news","webb.png"),
		("vti_servicelist","service_info.png"),
		("vti_subtitles","sub.png"),
		("vti_system_setup","setup.png"),
		("vti_timer","timer.png"),
		("vti_tv_radio","movie_list.png"),
		("vti_user_interface","camd.png"),
		("webradiofs","plugin.png"),
		("xbmc_starten","plugin.png"),
		("yamp","plugin.png"),
		("yamp_music_player","plugin.png"),
		("youtube_tv","plugin.png")
		]
	
	@cached
	def getText(self):
		cur = self.source.current
		if cur and len(cur) > 2:
			selection = cur[2]
			if selection in ("skin_selector","atilehd_setup"):
				return self.logo
			name = self.path+selection.lower()+".png"
			if fileExists(name):
				return name
			name=""
			for pair in self.names:
				if pair[0] == selection:
					name=self.path+pair[1]
					break
			if name != "" and fileExists(name):
				return name
			if fileExists(self.path+"plugin.png"):
				return self.path+"plugin.png" 
		return self.logo
	
	text = property(getText)
