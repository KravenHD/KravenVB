# -*- coding: utf-8 -*-

#######################################################################
#
# KravenVB by Team-Kraven
#
# Thankfully inspired by:
# MyMetrix
# Coded by iMaxxx (c) 2013
#
# This plugin is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock, ConfigSlider
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system, popen
from shutil import move, rmtree
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from Components.SystemInfo import SystemInfo
from PIL import Image, ImageFilter
import gettext, time, subprocess, re, requests
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from copy import deepcopy

try:
	from boxbranding import getImageDistro
	if getImageDistro() == "openatv":
		from lxml import etree
		from xml.etree.cElementTree import fromstring
except ImportError:
	brand = False
	from xml import etree
	from xml.etree.cElementTree import fromstring

#############################################################

DESKTOP_WIDTH = getDesktop(0).size().width()

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("KravenVB", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/KravenVB/locale/"))

def _(txt):
	t = gettext.dgettext("KravenVB", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

#############################################################

ColorList = [
	("00F0A30A", _("amber")),
	("00B27708", _("amber dark")),
	("001B1775", _("blue")),
	("000E0C3F", _("blue dark")),
	("007D5929", _("brown")),
	("003F2D15", _("brown dark")),
	("000050EF", _("cobalt")),
	("00001F59", _("cobalt dark")),
	("001BA1E2", _("cyan")),
	("000F5B7F", _("cyan dark")),
	("00FFEA04", _("yellow")),
	("00999999", _("grey")),
	("003F3F3F", _("grey dark")),
	("0070AD11", _("green")),
	("00213305", _("green dark")),
	("00A19181", _("Kraven")),
	("0028150B", _("Kraven dark")),
	("006D8764", _("olive")),
	("00313D2D", _("olive dark")),
	("00C3461B", _("orange")),
	("00892E13", _("orange dark")),
	("00F472D0", _("pink")),
	("00723562", _("pink dark")),
	("00E51400", _("red")),
	("00330400", _("red dark")),
	("00000000", _("black")),
	("00647687", _("steel")),
	("00262C33", _("steel dark")),
	("006C0AAB", _("violet")),
	("001F0333", _("violet dark")),
	("00ffffff", _("white"))
	]

BackgroundList = [
	("F0A30A", _("amber")),
	("B27708", _("amber dark")),
	("665700", _("amber very dark")),
	("1B1775", _("blue")),
	("0E0C3F", _("blue dark")),
	("03001E", _("blue very dark")),
	("7D5929", _("brown")),
	("3F2D15", _("brown dark")),
	("180B00", _("brown very dark")),
	("0050EF", _("cobalt")),
	("001F59", _("cobalt dark")),
	("000E2B", _("cobalt very dark")),
	("1BA1E2", _("cyan")),
	("0F5B7F", _("cyan dark")),
	("01263D", _("cyan very dark")),
	("FFEA04", _("yellow")),
	("999999", _("grey")),
	("3F3F3F", _("grey dark")),
	("1C1C1C", _("grey very dark")),
	("70AD11", _("green")),
	("213305", _("green dark")),
	("001203", _("green very dark")),
	("A19181", _("Kraven")),
	("28150B", _("Kraven dark")),
	("1D130B", _("Kraven very dark")),
	("6D8764", _("olive")),
	("313D2D", _("olive dark")),
	("161C12", _("olive very dark")),
	("C3461B", _("orange")),
	("892E13", _("orange dark")),
	("521D00", _("orange very dark")),
	("F472D0", _("pink")),
	("723562", _("pink dark")),
	("2F0029", _("pink very dark")),
	("E51400", _("red")),
	("330400", _("red dark")),
	("240004", _("red very dark")),
	("000000", _("black")),
	("647687", _("steel")),
	("262C33", _("steel dark")),
	("131619", _("steel very dark")),
	("6C0AAB", _("violet")),
	("1F0333", _("violet dark")),
	("11001E", _("violet very dark")),
	("ffffff", _("white"))
	]
	
TextureList = []

for i in range(1,50):
	n=str(i)
	if fileExists("/usr/share/enigma2/Kraven-user-icons/usertexture"+n+".png") or fileExists("/usr/share/enigma2/Kraven-user-icons/usertexture"+n+".jpg"):
		TextureList.append(("usertexture"+n,_("user texture")+" "+n))
for i in range(1,50):
	n=str(i)
	if fileExists("/usr/share/enigma2/KravenVB/textures/texture"+n+".png") or fileExists("/usr/share/enigma2/KravenVB/textures/texture"+n+".jpg"):
		TextureList.append(("texture"+n,_("texture")+" "+n))

BackgroundSelfList = deepcopy(BackgroundList)
BackgroundSelfList.append(("self", _("self")))

BackgroundSelfGradientList = deepcopy(BackgroundSelfList)
BackgroundSelfGradientList.append(("gradient", _("gradient")))

BackgroundSelfTextureList = deepcopy(BackgroundSelfList)
BackgroundSelfTextureList.append(("texture", _("texture")))

BackgroundSelfGradientTextureList = deepcopy(BackgroundSelfGradientList)
BackgroundSelfGradientTextureList.append(("texture", _("texture")))

LanguageList = [
	("de", _("Deutsch")),
	("en", _("English")),
	("ru", _("Russian")),
	("it", _("Italian")),
	("es", _("Spanish (es)")),
	("sp", _("Spanish (sp)")),
	("uk", _("Ukrainian (uk)")),
	("ua", _("Ukrainian (ua)")),
	("pt", _("Portuguese")),
	("ro", _("Romanian")),
	("pl", _("Polish")),
	("fi", _("Finnish")),
	("nl", _("Dutch")),
	("fr", _("French")),
	("bg", _("Bulgarian")),
	("sv", _("Swedish (sv)")),
	("se", _("Swedish (se)")),
	("zh_tw", _("Chinese Traditional")),
	("zh", _("Chinese Simplified (zh)")),
	("zh_cn", _("Chinese Simplified (zh_cn)")),
	("tr", _("Turkish")),
	("hr", _("Croatian")),
	("ca", _("Catalan"))
	]

TransList = [
	("00", "0%"),
	("0C", "5%"),
	("18", "10%"),
	("32", "20%"),
	("58", "35%"),
	("7E", "50%")
	]

config.plugins.KravenVB = ConfigSubsection()
config.plugins.KravenVB.Primetime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))
config.plugins.KravenVB.InfobarSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorB = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorB = ConfigSlider(default=75, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenVB.ECMLineAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenVB.ScreensAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))

config.plugins.KravenVB.customProfile = ConfigSelection(default="1", choices = [
				("1", _("1")),
				("2", _("2")),
				("3", _("3")),
				("4", _("4")),
				("5", _("5"))
				])

profList = [("default", _("0 (hardcoded)"))]
for i in range(1,21):
	n=name=str(i)
	if fileExists("/etc/enigma2/kraven_default_"+n):
		if i==1:
			name="1 (@tomele)"
		elif i==2:
			name="2 (@örlgrey)"
		elif i==3:
			name="3 (@stony272)"
		elif i==4:
			name="4 (@Linkstar)"
		elif i==5:
			name="5 (@Rene67)"
		elif i==6:
			name="6 (@Mister-T)"
		profList.append((n,_(name)))
config.plugins.KravenVB.defaultProfile = ConfigSelection(default="default", choices = profList)
				
config.plugins.KravenVB.refreshInterval = ConfigSelection(default="15", choices = [
				("0", _("0")),
				("15", _("15")),
				("30", _("30")),
				("60", _("60")),
				("120", _("120")),
				("240", _("240")),
				("480", _("480"))
				])

config.plugins.KravenVB.Volume = ConfigSelection(default="volume-border", choices = [
				("volume-original", _("original")),
				("volume-border", _("with Border")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-center", _("center"))
				])

config.plugins.KravenVB.MenuColorTrans = ConfigSelection(default="32", choices = TransList)

config.plugins.KravenVB.BackgroundColorTrans = ConfigSelection(default="32", choices = TransList)

config.plugins.KravenVB.InfobarColorTrans = ConfigSelection(default="00", choices = TransList)

config.plugins.KravenVB.BackgroundColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)

config.plugins.KravenVB.BackgroundAlternateColor = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.InfobarGradientColor = ConfigSelection(default="self", choices = BackgroundSelfTextureList)

config.plugins.KravenVB.InfobarBoxColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)

config.plugins.KravenVB.InfobarAlternateColor = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.BackgroundGradientColorPrimary = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.BackgroundGradientColorSecondary = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.InfobarGradientColorPrimary = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.InfobarGradientColorSecondary = ConfigSelection(default="000000", choices = BackgroundList)

config.plugins.KravenVB.SelectionBackground = ConfigSelection(default="000050EF", choices = ColorList)

config.plugins.KravenVB.Font1 = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.Font2 = ConfigSelection(default="00F0A30A", choices = ColorList)

config.plugins.KravenVB.IBFont1 = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.IBFont2 = ConfigSelection(default="00F0A30A", choices = ColorList)

config.plugins.KravenVB.PermanentClockFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.SelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.MarkedFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.ECMFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.ChannelnameFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.PrimetimeFont = ConfigSelection(default="0070AD11", choices = ColorList)

config.plugins.KravenVB.ButtonText = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.Android = ConfigSelection(default="00000000", choices = ColorList)

config.plugins.KravenVB.Border = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.Progress = ConfigSelection(default="progress", choices = [
				("00F0A30A", _("amber")),
				("00B27708", _("amber dark")),
				("001B1775", _("blue")),
				("000E0C3F", _("blue dark")),
				("007D5929", _("brown")),
				("003F2D15", _("brown dark")),
				("progress", _("colorfull")),
				("progress2", _("colorfull2")),
				("000050EF", _("cobalt")),
				("00001F59", _("cobalt dark")),
				("001BA1E2", _("cyan")),
				("000F5B7F", _("cyan dark")),
				("00FFEA04", _("yellow")),
				("00999999", _("grey")),
				("003F3F3F", _("grey dark")),
				("0070AD11", _("green")),
				("00213305", _("green dark")),
				("00A19181", _("Kraven")),
				("0028150B", _("Kraven dark")),
				("006D8764", _("olive")),
				("00313D2D", _("olive dark")),
				("00C3461B", _("orange")),
				("00892E13", _("orange dark")),
				("00F472D0", _("pink")),
				("00723562", _("pink dark")),
				("00E51400", _("red")),
				("00330400", _("red dark")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])

config.plugins.KravenVB.Line = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.IBLine = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.IBStyle = ConfigSelection(default="grad", choices = [
				("grad", _("gradient")),
				("box", _("box"))
				])

config.plugins.KravenVB.InfoStyle = ConfigSelection(default="gradient", choices = [
				("gradient", _("gradient")),
				("primary", _("          Primary Color")),
				("secondary", _("          Secondary Color"))
				])

config.plugins.KravenVB.InfobarTexture = ConfigSelection(default="texture1", choices = TextureList)
				
config.plugins.KravenVB.BackgroundTexture = ConfigSelection(default="texture1", choices = TextureList)
				
BorderList = [("none", _("off"))]
BorderList = BorderList + ColorList
config.plugins.KravenVB.SelectionBorder = ConfigSelection(default="none", choices = BorderList)

config.plugins.KravenVB.MiniTVBorder = ConfigSelection(default="003F3F3F", choices = ColorList)

config.plugins.KravenVB.AnalogStyle = ConfigSelection(default="00999999", choices = [
				("00F0A30A", _("amber")),
				("001B1775", _("blue")),
				("007D5929", _("brown")),
				("000050EF", _("cobalt")),
				("001BA1E2", _("cyan")),
				("00999999", _("grey")),
				("0070AD11", _("green")),
				("00C3461B", _("orange")),
				("00F472D0", _("pink")),
				("00E51400", _("red")),
				("00000000", _("black")),
				("00647687", _("steel")),
				("006C0AAB", _("violet")),
				("00ffffff", _("white"))
				])

config.plugins.KravenVB.InfobarStyle = ConfigSelection(default="infobar-style-x3", choices = [
				("infobar-style-nopicon", _("no Picon")),
				("infobar-style-x1", _("X1")),
				("infobar-style-x2", _("X2")),
				("infobar-style-x3", _("X3")),
				("infobar-style-z1", _("Z1")),
				("infobar-style-z2", _("Z2")),
				("infobar-style-zz1", _("ZZ1")),
				("infobar-style-zz2", _("ZZ2")),
				("infobar-style-zz3", _("ZZ3")),
				("infobar-style-zz4", _("ZZ4")),
				("infobar-style-zzz1", _("ZZZ1"))
				])

config.plugins.KravenVB.InfobarChannelName = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small", _("Name small")),
				("infobar-channelname-number-small", _("Name & Number small")),
				("infobar-channelname", _("Name big")),
				("infobar-channelname-number", _("Name & Number big"))
				])

config.plugins.KravenVB.InfobarChannelName2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small", _("Name")),
				("infobar-channelname-number-small", _("Name & Number"))
				])

config.plugins.KravenVB.IBFontSize = ConfigSelection(default="size-30", choices = [
				("size-22", _("small")),
				("size-26", _("middle")),
				("size-30", _("big"))
				])

config.plugins.KravenVB.TypeWriter = ConfigSelection(default="runningtext", choices = [
				("typewriter", _("typewriter")),
				("runningtext", _("runningtext")),
				("none", _("off"))
				])

config.plugins.KravenVB.alternativeChannellist = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenVB.ChannelSelectionHorStyle = ConfigSelection(default="cshor-minitv", choices = [
				("cshor-transparent", _("transparent")),
				("cshor-minitv", _("MiniTV"))
				])

config.plugins.KravenVB.ChannellistPicon = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenVB.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-minitv3", _("Preview")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-nobile-minitv3", _("Nobile Preview"))
				])

config.plugins.KravenVB.ChannelSelectionStyle2 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-minitv3", _("Preview")),
				("channelselection-style-minitv33", _("Extended Preview")),
				("channelselection-style-minitv2", _("Dual TV")),
				("channelselection-style-minitv22", _("Dual TV 2")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-nobile-minitv3", _("Nobile Preview")),
				("channelselection-style-nobile-minitv33", _("Nobile Extended Preview"))
				])

config.plugins.KravenVB.ChannelSelectionMode = ConfigSelection(default="zap", choices = [
				("zap", _("Zap (1xOK)")),
				("preview", _("Preview (2xOK)"))
				])

config.plugins.KravenVB.ChannelSelectionTrans = ConfigSelection(default="32", choices = TransList)

config.plugins.KravenVB.ChannelSelectionServiceSize = ConfigSelection(default="size-24", choices = [
				("size-16", _("16")),
				("size-18", _("18")),
				("size-20", _("20")),
				("size-22", _("22")),
				("size-24", _("24")),
				("size-26", _("26")),
				("size-28", _("28")),
				("size-30", _("30"))
				])

config.plugins.KravenVB.ChannelSelectionInfoSize = ConfigSelection(default="size-24", choices = [
				("size-16", _("16")),
				("size-18", _("18")),
				("size-20", _("20")),
				("size-22", _("22")),
				("size-24", _("24")),
				("size-26", _("26")),
				("size-28", _("28")),
				("size-30", _("30"))
				])

config.plugins.KravenVB.ChannelSelectionServiceSize1 = ConfigSelection(default="size-20", choices = [
				("size-16", _("16")),
				("size-18", _("18")),
				("size-20", _("20")),
				("size-22", _("22")),
				("size-24", _("24")),
				("size-26", _("26"))
				])

config.plugins.KravenVB.ChannelSelectionInfoSize1 = ConfigSelection(default="size-20", choices = [
				("size-16", _("16")),
				("size-18", _("18")),
				("size-20", _("20")),
				("size-22", _("22")),
				("size-24", _("24")),
				("size-26", _("26"))
				])

config.plugins.KravenVB.ChannelSelectionEPGSize1 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.ChannelSelectionEPGSize2 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.ChannelSelectionEPGSize3 = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.ChannelSelectionServiceNA = ConfigSelection(default="00FFEA04", choices = ColorList)

config.plugins.KravenVB.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-xpicon", _("X-Picons")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-zzpicon", _("ZZ-Picons")),
				("numberzapext-zzzpicon", _("ZZZ-Picons"))
				])

config.plugins.KravenVB.NZBorder = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])

config.plugins.KravenVB.GraphMultiEPG = ConfigSelection(default="graphmultiepg-minitv", choices = [
				("graphmultiepg-minitv", _("MiniTV right")),
				("graphmultiepg-minitv2", _("MiniTV left")),
				("graphmultiepg", _("no MiniTV"))
				])

config.plugins.KravenVB.GraphicalEPG = ConfigSelection(default="text-minitv", choices = [
				("text", _("Text")),
				("text-minitv", _("Text with MiniTV")),
				("graphical", _("graphical")),
				("graphical-minitv", _("graphical with MiniTV"))
				])

config.plugins.KravenVB.GMEDescriptionSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.GMErunningbg = ConfigSelection(default="00389416", choices = [
				("global", _("global selection background")),
				("00389416", _("green")),
				("000064c7", _("blue"))
				])

config.plugins.KravenVB.GMEBorder = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.VerticalEPG = ConfigSelection(default="verticalepg-minitv", choices = [
				("verticalepg-minitv", _("MiniTV right")),
				("verticalepg-minitv2", _("MiniTV left")),
				("verticalepg-description", _("description")),
				("verticalepg-full", _("full"))
				])

config.plugins.KravenVB.VEPGBorder = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.MovieSelection = ConfigSelection(default="movieselection-no-cover", choices = [
				("movieselection-no-cover", _("no Cover")),
				("movieselection-small-cover", _("small Cover")),
				("movieselection-big-cover", _("big Cover")),
				("movieselection-minitv", _("MiniTV")),
				("movieselection-minitv-cover", _("MiniTV + Cover"))
				])

config.plugins.KravenVB.MovieSelectionEPGSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.EPGSelection = ConfigSelection(default="epgselection-standard", choices = [
				("epgselection-standard", _("standard")),
				("epgselection-minitv", _("MiniTV"))
				])

config.plugins.KravenVB.EPGSelectionEPGSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.EPGListSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.EMCStyle = ConfigSelection(default="emc-minitv", choices = [
				("emc-nocover", _("no Cover")),
				("emc-nocover2", _("no Cover2")),
				("emc-smallcover", _("small Cover")),
				("emc-smallcover2", _("small Cover2")),
				("emc-bigcover", _("big Cover")),
				("emc-bigcover2", _("big Cover2")),
				("emc-verybigcover", _("very big Cover")),
				("emc-verybigcover2", _("very big Cover2")),
				("emc-minitv", _("MiniTV")),
				("emc-minitv2", _("MiniTV2"))
				])

config.plugins.KravenVB.EMCEPGSize = ConfigSelection(default="small", choices = [
				("small", _("small")),
				("big", _("big"))
				])

config.plugins.KravenVB.RunningText = ConfigSelection(default="startdelay=4000", choices = [
				("none", _("off")),
				("startdelay=2000", _("2 sec")),
				("startdelay=4000", _("4 sec")),
				("startdelay=6000", _("6 sec")),
				("startdelay=8000", _("8 sec")),
				("startdelay=10000", _("10 sec")),
				("startdelay=15000", _("15 sec")),
				("startdelay=20000", _("20 sec"))
				])

config.plugins.KravenVB.RunningTextSpeed = ConfigSelection(default="steptime=100", choices = [
				("steptime=200", _("5 px/sec")),
				("steptime=100", _("10 px/sec")),
				("steptime=66", _("15 px/sec")),
				("steptime=50", _("20 px/sec"))
				])

config.plugins.KravenVB.ScrollBar = ConfigSelection(default="scrollbarWidth=0", choices = [
				("scrollbarWidth=0", _("off")),
				("scrollbarWidth=5", _("thin")),
				("scrollbarWidth=10", _("middle")),
				("scrollbarWidth=15", _("wide"))
				])
				
config.plugins.KravenVB.ScrollBar2 = ConfigSelection(default="showOnDemand", choices = [
				("showOnDemand", _("on")),
				("showNever", _("off"))
				])

config.plugins.KravenVB.IconStyle = ConfigSelection(default="icons-light", choices = [
				("icons-light", _("light")),
				("icons-dark", _("dark"))
				])

config.plugins.KravenVB.IconStyle2 = ConfigSelection(default="icons-light2", choices = [
				("icons-light2", _("light")),
				("icons-dark2", _("dark"))
				])

config.plugins.KravenVB.ClockStyle = ConfigSelection(default="clock-classic", choices = [
				("clock-classic", _("standard")),
				("clock-classic-big", _("standard big")),
				("clock-analog", _("analog")),
				("clock-android", _("android")),
				("clock-color", _("colored")),
				("clock-flip", _("flip")),
				("clock-weather", _("weather icon"))
				])

config.plugins.KravenVB.ClockIconSize = ConfigSelection(default="size-96", choices = [
				("size-96", _("96")),
				("size-128", _("128"))
				])

config.plugins.KravenVB.WeatherStyle = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-big", _("big")),
				("weather-small", _("small"))
				])

config.plugins.KravenVB.WeatherStyle2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-left", _("on"))
				])

config.plugins.KravenVB.WeatherStyle3 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("weather-left", _("on")),
				("netatmobar", _("NetatmoBar"))
				])

config.plugins.KravenVB.ECMVisible = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ib", _("Infobar")),
				("sib", _("SecondInfobar")),
				("ib+sib", _("Infobar & SecondInfobar"))
				])

config.plugins.KravenVB.ECMLine1 = ConfigSelection(default="ShortReader", choices = [
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact"))
				])

config.plugins.KravenVB.ECMLine2 = ConfigSelection(default="ShortReader", choices = [
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				("VeryLong", _("complete"))
				])

config.plugins.KravenVB.ECMLine3 = ConfigSelection(default="ShortReader", choices = [
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				])

config.plugins.KravenVB.FTA = ConfigSelection(default="FTAVisible", choices = [
				("FTAVisible", _("on")),
				("none", _("off"))
				])

config.plugins.KravenVB.SystemInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("systeminfo-small", _("small")),
				("systeminfo-big", _("big")),
				("systeminfo-bigsat", _("big + Sat"))
				])

config.plugins.KravenVB.SIB = ConfigSelection(default="sib4", choices = [
				("sib1", _("top/bottom")),
				("sib2", _("left/right")),
				("sib3", _("single")),
				("sib4", _("MiniTV")),
				("sib5", _("MiniTV2")),
				("sib6", _("Weather")),
				("sib7", _("Weather2"))
				])

config.plugins.KravenVB.SIBFont = ConfigSelection(default="sibfont-big", choices = [
				("sibfont-big", _("big")),
				("sibfont-small", _("small"))
				])

config.plugins.KravenVB.IBtop = ConfigSelection(default="infobar-x2-z1_top2", choices = [
				("infobar-x2-z1_top2", _("2 Tuner")),
				("infobar-x2-z1_top", _("4 Tuner")),
				("infobar-x2-z1_top3", _("8 Tuner"))
				])

config.plugins.KravenVB.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenVB.Infobox2 = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("db", _("Tuner/Satellite + dB")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])

config.plugins.KravenVB.tuner = ConfigSelection(default="4-tuner", choices = [
				("2-tuner", _("2 Tuner")),
				("4-tuner", _("4 Tuner")),
				("8-tuner", _("8 Tuner"))
				])

config.plugins.KravenVB.tuner2 = ConfigSelection(default="4-tuner", choices = [
				("2-tuner", _("2 Tuner")),
				("4-tuner", _("4 Tuner")),
				("8-tuner", _("8 Tuner")),
				("10-tuner", _("10 Tuner"))
				])

config.plugins.KravenVB.record = ConfigSelection(default="record-shine", choices = [
				("record-blink", _("record blink")),
				("record-shine", _("record shine"))
				])

config.plugins.KravenVB.record2 = ConfigSelection(default="record-shine+no-record-tuner", choices = [
				("record-blink+tuner-shine", _("record blink, tuner shine")),
				("record-shine+tuner-blink", _("record shine, tuner blink")),
				("record+tuner-blink", _("record & tuner blink")),
				("record+tuner-shine", _("record & tuner shine")),
				("record-blink+no-record-tuner", _("record blink, no record tuner")),
				("record-shine+no-record-tuner", _("record shine, no record tuner"))
				])

config.plugins.KravenVB.record3 = ConfigSelection(default="no-record-tuner", choices = [
				("tuner-blink", _("tuner blink")),
				("tuner-shine", _("tuner shine")),
				("no-record-tuner", _("no record tuner"))
				])

config.plugins.KravenVB.record4 = ConfigSelection(default="record-shine", choices = [
				("record-blink", _("record blink")),
				("record-shine", _("record shine"))
				])

config.plugins.KravenVB.IBColor = ConfigSelection(default="all-screens", choices = [
				("all-screens", _("in all Screens")),
				("only-infobar", _("only Infobar, SecondInfobar & Players"))
				])

config.plugins.KravenVB.About = ConfigSelection(default="about", choices = [
				("about", _("KravenVB"))
				])

config.plugins.KravenVB.Logo = ConfigSelection(default="minitv", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV")),
				("metrix-icons", _("Icons")),
				("minitv-metrix-icons", _("MiniTV + Icons"))
				])

config.plugins.KravenVB.MenuIcons = ConfigSelection(default="stony272", choices = [
				("stony272", _("stony272")),
				("stony272-metal", _("stony272-metal")),
				("stony272-gold-round", _("stony272-gold-round")),
				("stony272-gold-square", _("stony272-gold-square")),
				("rennmaus-kleinerteufel", _("rennmaus-kleiner.teufel"))
				])

config.plugins.KravenVB.DebugNames = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("screennames-on", _("on"))
				])

config.plugins.KravenVB.WeatherView = ConfigSelection(default="meteo", choices = [
				("icon", _("Icon")),
				("meteo", _("Meteo"))
				])

config.plugins.KravenVB.MeteoColor = ConfigSelection(default="meteo-light", choices = [
				("meteo-light", _("light")),
				("meteo-dark", _("dark"))
				])

config.plugins.KravenVB.Primetimeavailable = ConfigSelection(default="primetime-on", choices = [
				("none", _("off")),
				("primetime-on", _("on"))
				])

config.plugins.KravenVB.EMCSelectionColors = ConfigSelection(default="emc-colors-on", choices = [
				("none", _("off")),
				("emc-colors-on", _("on"))
				])

config.plugins.KravenVB.EMCSelectionBackground = ConfigSelection(default="00213305", choices = ColorList)

config.plugins.KravenVB.EMCSelectionFont = ConfigSelection(default="00ffffff", choices = ColorList)

config.plugins.KravenVB.SerienRecorder = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("serienrecorder", _("on"))
				])

config.plugins.KravenVB.MediaPortal = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("mediaportal", _("on"))
				])

config.plugins.KravenVB.PVRState = ConfigSelection(default="pvrstate-center-big", choices = [
				("pvrstate-center-big", _("center big")),
				("pvrstate-center-small", _("center small")),
				("pvrstate-left-small", _("left small")),
				("pvrstate-off", _("off"))
				])

config.plugins.KravenVB.PigStyle = ConfigText(default="")
config.plugins.KravenVB.PigMenuActive = ConfigYesNo(default=False)

config.plugins.KravenVB.SplitScreen = ConfigSelection(default="splitscreen1", choices = [
				("splitscreen1", _("without description")),
				("splitscreen2", _("with description"))
				])

config.plugins.KravenVB.TimerEditScreen = ConfigSelection(default="timer-standard", choices = [
				("timer-standard", _("standard layout")),
				("timer-medium", _("medium font with EPG Info")),
				("timer-big", _("big font with EPG Info"))
				])

config.plugins.KravenVB.TimerListStyle = ConfigSelection(default="timerlist-standard", choices = [
				("timerlist-standard", _("standard")),
				("timerlist-1", _("Style 1")),
				("timerlist-2", _("Style 2")),
				("timerlist-3", _("Style 3")),
				("timerlist-4", _("Style 4")),
				("timerlist-5", _("Style 5"))
				])

config.plugins.KravenVB.weather_gmcode = ConfigText(default="GM")
config.plugins.KravenVB.weather_cityname = ConfigText(default = "")
config.plugins.KravenVB.weather_language = ConfigSelection(default="de", choices = LanguageList)
config.plugins.KravenVB.weather_server = ConfigSelection(default="_owm", choices = [
				("_owm", _("OpenWeatherMap")),
				("_accu", _("Accuweather")),
				("_realtek", _("RealTek"))
				])

config.plugins.KravenVB.weather_search_over = ConfigSelection(default="ip", choices = [
				("ip", _("Auto (IP)")),
				("name", _("Search String")),
				("gmcode", _("GM Code"))
				])

config.plugins.KravenVB.weather_owm_latlon = ConfigText(default = "")
config.plugins.KravenVB.weather_accu_latlon = ConfigText(default = "")
config.plugins.KravenVB.weather_realtek_latlon = ConfigText(default = "")
config.plugins.KravenVB.weather_accu_id = ConfigText(default = "")
config.plugins.KravenVB.weather_foundcity = ConfigText(default = "")

config.plugins.KravenVB.PlayerClock = ConfigSelection(default="player-classic", choices = [
				("player-classic", _("standard")),
				("player-android", _("android")),
				("player-flip", _("flip")),
				("player-weather", _("weather icon"))
				])

config.plugins.KravenVB.Android2 = ConfigSelection(default="00000000", choices = ColorList)

config.plugins.KravenVB.CategoryProfiles = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategorySystem = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryGlobalColors = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryInfobarLook = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryInfobarContents = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategorySIB = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryWeather = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryClock = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryECMInfos = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryViews = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryPermanentClock = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryChannellist = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryNumberZap = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryEPGSelection = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryGraphMultiEPG = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryGraphicalEPG = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryVerticalEPG = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryTimerEdit = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryEMC = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryMovieSelection = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryPlayers = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryAntialiasing = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.CategoryDebug = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.Unskinned = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("unskinned-colors-on", _("on"))
				])

config.plugins.KravenVB.UnwatchedColor = ConfigSelection(default="00F0A30A", choices = ColorList)

config.plugins.KravenVB.WatchingColor = ConfigSelection(default="000050EF", choices = ColorList)

config.plugins.KravenVB.FinishedColor = ConfigSelection(default="0070AD11", choices = ColorList)

config.plugins.KravenVB.PermanentClock = ConfigSelection(default="permanentclock-infobar-big", choices = [
				("permanentclock-infobar-big", _("infobar colors big")),
				("permanentclock-infobar-small", _("infobar colors small")),
				("permanentclock-global-big", _("global colors big")),
				("permanentclock-global-small", _("global colors small")),
				("permanentclock-transparent-big", _("transparent big")),
				("permanentclock-transparent-small", _("transparent small"))
				])

config.plugins.KravenVB.ATVna = ConfigSelection(default="na", choices = [
				("na", _("not available for openATV"))
				])

#######################################################################

class KravenVB(ConfigListScreen, Screen):

	if DESKTOP_WIDTH <= 1280:
	  skin = """
<screen name="KravenVB-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <widget font="Regular; 20" halign="left" valign="center" source="key_red" position="70,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_green" position="320,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_yellow" position="570,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_blue" position="820,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget name="config" position="70,85" size="708,540" itemHeight="30" font="Regular;24" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,12" size="708,46" text="KravenVB - Konfigurationstool" font="Regular; 35" valign="center" halign="left" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" />
  <eLabel position="847,208" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="847,417" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="845,208" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel position="1215,208" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap pixmap="KravenVB/buttons/key_red1.png" position="65,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_green1.png" position="315,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_yellow1.png" position="565,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_blue1.png" position="815,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1138,22" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="830,80" size="402,46" text="KravenVB" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" />
  <eLabel position="845,139" size="372,40" text="Version: 6.2.32" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
  <widget name="helperimage" position="847,210" size="368,207" zPosition="1" backgroundColor="#00000000" />
  <widget source="Canvas" render="Canvas" position="847,210" size="368,207" zPosition="-1" backgroundColor="#00000000" />
  <widget source="help" render="Label" position="847,440" size="368,196" font="Regular;20" backgroundColor="#00000000" foregroundColor="#00f0a30a" halign="center" valign="top" transparent="1" />
</screen>
"""
	else:
	  skin = """
<screen name="KravenVB-Setup" position="0,0" size="1920,1080" flags="wfNoBorder" backgroundColor="#00000000">
  <widget font="Regular;30" halign="left" valign="center" source="key_red" position="105,997" size="330,39" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular;30" halign="left" valign="center" source="key_green" position="480,997" size="330,39" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular;30" halign="left" valign="center" source="key_yellow" position="855,997" size="330,39" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular;30" halign="left" valign="center" source="key_blue" position="1230,997" size="330,39" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget name="config" position="105,127" size="1062,810" itemHeight="45" font="Regular;32" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="105,18" size="1500,69" text="KravenVB - Konfigurationstool" backgroundColor="#00000000" font="Regular;51" foregroundColor="#00f0a30a" valign="center" halign="left" transparent="1" />
  <eLabel position="1313,337" size="466,3" backgroundColor="#00f0a30a" />
  <eLabel position="1313,599" size="466,3" backgroundColor="#00f0a30a" />
  <eLabel position="1313,340" size="3,259" backgroundColor="#00f0a30a" />
  <eLabel position="1776,340" size="3,259" backgroundColor="#00f0a30a" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1920,1080" transparent="0" zPosition="-9" />
  <ePixmap pixmap="KravenVB/buttons/key_red1.png" position="97,1038" size="200,5" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_green1.png" position="472,1038" size="200,5" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_yellow1.png" position="847,1038" size="200,5" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_blue1.png" position="1222,1038" size="200,5" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1707,33" size="150,42" font="Regular;39" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="1245,120" size="603,69" text="KravenVB" font="Regular;54" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" />
  <eLabel position="1267,208" size="558,60" text="Version: 6.2.32" font="Regular; 45" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" />
  <widget name="helperimage" position="1316,340" size="460,259" zPosition="1" backgroundColor="#00000000" />
  <widget source="Canvas" render="Canvas" position="1316,340" size="460,259" zPosition="-1" backgroundColor="#00000000" />
  <widget source="help" render="Label" position="1270,660" size="552,294" font="Regular;30" backgroundColor="#00000000" foregroundColor="#00f0a30a" halign="center" valign="top" transparent="1" />
</screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/KravenVB/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/comp/"
		self.picPath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/"
		self.profiles = "/etc/enigma2/"
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		self["Canvas"] = CanvasSource()
		self["help"] = StaticText()

		list = []
		ConfigListScreen.__init__(self, list)

		self["actions"] = ActionMap(["KravenVBConfigActions", "OkCancelActions", "DirectionActions", "ColorActions", "InputActions"],
		{
			"upUp": self.keyUpLong,
			"downUp": self.keyDownLong,
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"red": self.faq,
			"green": self.save,
			"yellow": self.categoryDown,
			"blue": self.categoryUp,
			"cancel": self.exit,
			"pageup": self.pageUp,
			"papedown": self.pageDown,
			"ok": self.OK
		}, -1)

		self["key_red"] = StaticText(_("FAQs"))
		self["key_green"] = StaticText(_("Save skin"))
		self["key_yellow"] = StaticText()
		self["key_blue"] = StaticText()

		self.UpdatePicture()

		self.timer = eTimer()
		self.timer.callback.append(self.updateMylist)
		self.onLayoutFinish.append(self.updateMylist)

		self.lastProfile="0"

		self.actClockstyle=""
		self.actWeatherstyle=""
		self.actChannelselectionstyle=""
		self.actCity=""
		
		self.skincolorinfobarcolor=""
		self.skincolorbackgroundcolor=""

	def mylist(self):
		self.timer.start(100, True)

	def updateMylist(self):
		
		if config.plugins.KravenVB.customProfile.value!=self.lastProfile:
			self.loadProfile()
			self.lastProfile=config.plugins.KravenVB.customProfile.value
			
		# page 1
		emptyLines=0
		list = []
		list.append(getConfigListEntry(_("About"), config.plugins.KravenVB.About, _("The KravenVB skin will be generated by this plugin according to your preferences. Make your settings and watch the changes in the preview window above. When finished, save your skin by pressing the green button and restart the GUI.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("PROFILES __________________________________________________________________"), config.plugins.KravenVB.CategoryProfiles, _("This sections offers all profile settings. Different settings can be saved, modified, shared and cloned. Read the FAQs.")))
		list.append(getConfigListEntry(_("Active Profile / Save"), config.plugins.KravenVB.customProfile, _("Select the profile you want to work with. Profiles are saved automatically on switching them or by pressing the OK button. New profiles will be generated based on the actual one. Profiles are interchangeable between boxes.")))
		list.append(getConfigListEntry(_("Default Profile / Reset"), config.plugins.KravenVB.defaultProfile, _("Select the default profile you want to use when resetting the active profile (OK button). You can add your own default profiles under /etc/enigma2/kraven_default_n (n<=20).")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("SYSTEM ____________________________________________________________________"), config.plugins.KravenVB.CategorySystem, _("This sections offers all basic settings.")))
		list.append(getConfigListEntry(_("Icons (except Infobar)"), config.plugins.KravenVB.IconStyle2, _("Choose between light and dark icons in system screens. The icons in the infobars are not affected.")))
		list.append(getConfigListEntry(_("Running Text (Delay)"), config.plugins.KravenVB.RunningText, _("Choose the start delay for running text.")))
		if not config.plugins.KravenVB.RunningText.value == "none":
			list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenVB.RunningTextSpeed, _("Choose the speed for running text.")))
		else:
			emptyLines+=1
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenVB.ScrollBar, _("Choose the width of scrollbars in lists or deactivate scrollbars completely.")))
		elif self.gete2distroversion() == "openatv":
			list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenVB.ScrollBar2, _("Choose whether scrollbars should be shown.")))
		list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenVB.IBColor, _("Choose whether you want to see the infobar background in all screens (bicolored background).")))
		list.append(getConfigListEntry(_("Menus"), config.plugins.KravenVB.Logo, _("Choose from different options to display the system menus. Press red button for the FAQs with details on installing menu icons.")))
		if config.plugins.KravenVB.Logo.value in ("metrix-icons","minitv-metrix-icons"):
			list.append(getConfigListEntry(_("Menu-Icons"), config.plugins.KravenVB.MenuIcons, _("Choose from different icon sets for the menu screens. Many thanks to rennmaus and kleiner.teufel for their icon set.")))
		else:
			emptyLines+=1
		if config.plugins.KravenVB.Logo.value in ("logo","metrix-icons"):
			list.append(getConfigListEntry(_("Menu-Transparency"), config.plugins.KravenVB.MenuColorTrans, _("Choose the degree of background transparency for system menu screens.")))
		else:
			emptyLines+=1
		for i in range(emptyLines+3):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 2
		emptyLines=0
		list.append(getConfigListEntry(_("GLOBAL COLORS _____________________________________________________________"), config.plugins.KravenVB.CategoryGlobalColors, _("This sections offers offers all basic color settings.")))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenVB.BackgroundColor, _("Choose the background for all screens. You can choose from a list of predefined colors or textures, create your own color using RGB sliders or define a color gradient.")))
		if config.plugins.KravenVB.BackgroundColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.BackgroundSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.BackgroundSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.BackgroundSelfColorB, _("Set the intensity of this basic color with the slider.")))
		elif config.plugins.KravenVB.BackgroundColor.value == "gradient":
			list.append(getConfigListEntry(_("          Primary Color"), config.plugins.KravenVB.BackgroundGradientColorPrimary, _("Choose the primary color for the background gradient.")))
			list.append(getConfigListEntry(_("          Secondary Color"), config.plugins.KravenVB.BackgroundGradientColorSecondary, _("Choose the secondary color for the background gradient.")))
			emptyLines+=1
		elif config.plugins.KravenVB.BackgroundColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenVB.BackgroundTexture, _("Choose the texture for the background.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenVB.BackgroundAlternateColor, _("Choose the alternate color for the background. It should match the texture at the best.")))
			emptyLines+=1
		else:
			emptyLines+=3
		list.append(getConfigListEntry(_("Background-Transparency"), config.plugins.KravenVB.BackgroundColorTrans, _("Choose the degree of background transparency for all screens except system menus and channellists.")))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenVB.SelectionBackground, _("Choose the background color of selection bars.")))
		list.append(getConfigListEntry(_("Listselection-Border"), config.plugins.KravenVB.SelectionBorder, _("Choose the border color of selection bars or deactivate borders completely.")))
		list.append(getConfigListEntry(_("Listselection-Font"), config.plugins.KravenVB.SelectionFont, _("Choose the color of the font in selection bars.")))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenVB.Progress, _("Choose the color of progress bars.")))
		list.append(getConfigListEntry(_("Progress-Border"), config.plugins.KravenVB.Border, _("Choose the border color of progress bars.")))
		list.append(getConfigListEntry(_("MiniTV-Border"), config.plugins.KravenVB.MiniTVBorder, _("Choose the border color of MiniTV's.")))
		list.append(getConfigListEntry(_("Lines"), config.plugins.KravenVB.Line, _("Choose the color of all lines. This affects dividers as well as the line in the center of some progress bars.")))
		list.append(getConfigListEntry(_("Primary-Font"), config.plugins.KravenVB.Font1, _("Choose the color of the primary font. The primary font is used for list items, textboxes and other important information.")))
		list.append(getConfigListEntry(_("Secondary-Font"), config.plugins.KravenVB.Font2, _("Choose the color of the secondary font. The secondary font is used for headers, labels and other additional information.")))
		list.append(getConfigListEntry(_("Marking-Font"), config.plugins.KravenVB.MarkedFont, _("Choose the font color of marked list items.")))
		list.append(getConfigListEntry(_("Colorbutton-Font"), config.plugins.KravenVB.ButtonText, _("Choose the font color of the color button labels.")))
		list.append(getConfigListEntry(_("Unskinned Colors"), config.plugins.KravenVB.Unskinned, _("Choose whether some foreground and background colors of unskinned screens are changed or not.")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 3
		emptyLines=0
		list.append(getConfigListEntry(_("INFOBAR-LOOK _________________________________________________________________"), config.plugins.KravenVB.CategoryInfobarLook, _("This sections offers all settings for the infobar-look.")))
		list.append(getConfigListEntry(_("Infobar-Style"), config.plugins.KravenVB.InfobarStyle, _("Choose from different infobar styles. Please note that not every style provides every feature. Therefore some features might be unavailable for the chosen style.")))
		list.append(getConfigListEntry(_("Infobar-Background-Style"), config.plugins.KravenVB.IBStyle, _("Choose from different infobar background styles.")))
		if config.plugins.KravenVB.IBStyle.value == "box":
			list.append(getConfigListEntry(_("Infobar-Box-Line"), config.plugins.KravenVB.IBLine, _("Choose the color of the infobar box lines.")))
		else:
			emptyLines+=1
		if config.plugins.KravenVB.IBStyle.value == "grad":
			list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenVB.InfobarGradientColor, _("Choose the background for the infobars. You can choose from a list of predefined colors or textures or create your own color using RGB sliders.")))
		else:
			list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenVB.InfobarBoxColor, _("Choose the background for the infobars. You can choose from a list of predefined colors or textures, create your own color using RGB sliders or define a color gradient.")))
		if config.plugins.KravenVB.IBStyle.value == "box" and config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
			list.append(getConfigListEntry(_("          Primary Color"), config.plugins.KravenVB.InfobarGradientColorPrimary, _("Choose the primary color for the infobar gradient.")))
			list.append(getConfigListEntry(_("          Secondary Color"), config.plugins.KravenVB.InfobarGradientColorSecondary, _("Choose the secondary color for the infobar gradient.")))
			list.append(getConfigListEntry(_("          Info Panels"), config.plugins.KravenVB.InfoStyle, _("Choose gradient or color for the info panels (Sysinfos, Timeshiftbar etc.).")))
		elif config.plugins.KravenVB.IBStyle.value == "box" and config.plugins.KravenVB.InfobarBoxColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.InfobarSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.InfobarSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.InfobarSelfColorB, _("Set the intensity of this basic color with the slider.")))
		elif config.plugins.KravenVB.IBStyle.value == "box" and config.plugins.KravenVB.InfobarBoxColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenVB.InfobarTexture, _("Choose the texture for the infobars.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenVB.InfobarAlternateColor, _("Choose the alternate color for the infobars. It should match the texture at the best.")))
			emptyLines+=1
		elif config.plugins.KravenVB.IBStyle.value == "grad" and config.plugins.KravenVB.InfobarGradientColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.InfobarSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.InfobarSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.InfobarSelfColorB, _("Set the intensity of this basic color with the slider.")))
		elif config.plugins.KravenVB.IBStyle.value == "grad" and config.plugins.KravenVB.InfobarGradientColor.value == "texture":
			list.append(getConfigListEntry(_("          Texture"), config.plugins.KravenVB.InfobarTexture, _("Choose the texture for the infobars.")))
			list.append(getConfigListEntry(_("          Alternate Color"), config.plugins.KravenVB.InfobarAlternateColor, _("Choose the alternate color for the infobars. It should match the texture at the best.")))
			emptyLines+=1
		else:
			emptyLines+=3
		list.append(getConfigListEntry(_("Infobar-Transparency"), config.plugins.KravenVB.InfobarColorTrans, _("Choose the degree of background transparency for the infobars.")))
		list.append(getConfigListEntry(_("Primary-Infobar-Font"), config.plugins.KravenVB.IBFont1, _("Choose the color of the primary infobar font.")))
		list.append(getConfigListEntry(_("Secondary-Infobar-Font"), config.plugins.KravenVB.IBFont2, _("Choose the color of the secondary infobar font.")))
		list.append(getConfigListEntry(_("Infobar-Icons"), config.plugins.KravenVB.IconStyle, _("Choose between light and dark infobar icons.")))
		list.append(getConfigListEntry(_("Eventname Fontsize"), config.plugins.KravenVB.IBFontSize, _("Choose the font size of eventname.")))
		list.append(getConfigListEntry(_("Eventname effect"), config.plugins.KravenVB.TypeWriter, _("Choose from different effects to display eventname.")))
		for i in range(emptyLines+4):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 4
		emptyLines=0
		list.append(getConfigListEntry(_("INFOBAR-CONTENTS _____________________________________________________________"), config.plugins.KravenVB.CategoryInfobarContents, _("This sections offers all settings for infobar-contents.")))
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			list.append(getConfigListEntry(_("Tuner number"), config.plugins.KravenVB.IBtop, _("Choose from different options to display tuner.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
			list.append(getConfigListEntry(_("Tuner number"), config.plugins.KravenVB.tuner2, _("Choose from different options to display tuner.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Tuner number"), config.plugins.KravenVB.tuner, _("Choose from different options to display tuner.")))
		else:
			emptyLines+=1
		try:
			f=open("/proc/stb/info/vumodel","r")
			vumodel=f.read().strip()
			f.close()
		except IOError:
			pass
		if vumodel.lower() == "ultimo":
			if not config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2","infobar-style-zz3"):
				list.append(getConfigListEntry(_("Record-State"), config.plugins.KravenVB.record4, _("Choose from different options to display recording state.")))
			else:
				emptyLines+=1
		else:
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				list.append(getConfigListEntry(_("Record-State"), config.plugins.KravenVB.record2, _("Choose from different options to display recording state.")))
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				list.append(getConfigListEntry(_("Record-State"), config.plugins.KravenVB.record, _("Choose from different options to display recording state.")))
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
					list.append(getConfigListEntry(_("Record-State"), config.plugins.KravenVB.record2, _("Choose from different options to display recording state.")))
				else:
					list.append(getConfigListEntry(_("Record-State"), config.plugins.KravenVB.record3, _("Choose from different options to display recording state.")))
			else:
				emptyLines+=1
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			if not config.plugins.KravenVB.tuner2.value == "10-tuner":
				if self.gete2distroversion() == "VTi":
					list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox, _("Choose which informations will be shown in the info box.")))
				elif self.gete2distroversion() == "openatv":
					list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox2, _("Choose which informations will be shown in the info box.")))
			else:
				emptyLines+=1
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			if self.gete2distroversion() == "VTi":
				list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox, _("Choose which informations will be shown in the info box.")))
			elif self.gete2distroversion() == "openatv":
				list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox2, _("Choose which informations will be shown in the info box.")))
		else:
			emptyLines+=1
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz1","infobar-style-zz4"):
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName, _("Choose from different options to show the channel name and number in the infobar.")))
			if not config.plugins.KravenVB.InfobarChannelName.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
			else:
				emptyLines+=1
		else:
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName2, _("Choose from different options to show the channel name and number in the infobar.")))
			if not config.plugins.KravenVB.InfobarChannelName2.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
			else:
				emptyLines+=1
		list.append(getConfigListEntry(_("System-Infos"), config.plugins.KravenVB.SystemInfo, _("Choose from different additional windows with system informations or deactivate them completely.")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 4 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("SECONDINFOBAR _____________________________________________________________"), config.plugins.KravenVB.CategorySIB, _("This sections offers all settings for SecondInfobar.")))
		list.append(getConfigListEntry(_("SecondInfobar-Style"), config.plugins.KravenVB.SIB, _("Choose from different styles for SecondInfobar.")))
		list.append(getConfigListEntry(_("SecondInfobar Fontsize"), config.plugins.KravenVB.SIBFont, _("Choose the font size of SecondInfobar.")))
		for i in range(emptyLines+7):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 5
		emptyLines=0
		list.append(getConfigListEntry(_("WEATHER ___________________________________________________________________"), config.plugins.KravenVB.CategoryWeather, _("This sections offers all weather settings.")))
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle, _("Choose from different options to show the weather in the infobar.")))
			self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle3, _("Activate or deactivate displaying the weather in the infobar.")))
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle3.value
			else:
				list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle2, _("Activate or deactivate displaying the weather in the infobar.")))
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle2.value
		list.append(getConfigListEntry(_("Search by"), config.plugins.KravenVB.weather_search_over, _("Choose from different options to specify your location.")))
		if config.plugins.KravenVB.weather_search_over.value == 'name':
			list.append(getConfigListEntry(_("Search String"), config.plugins.KravenVB.weather_cityname, _("Specify any search string for your location (zip/city/district/state single or combined). Press OK to use the virtual keyboard. Step up or down in the menu to start the search.")))
		elif config.plugins.KravenVB.weather_search_over.value == 'gmcode':
			list.append(getConfigListEntry(_("GM Code"), config.plugins.KravenVB.weather_gmcode, _("Specify the GM code for your location. You can find it at https://weather.codes. Press OK to use the virtual keyboard. Step up or down in the menu to start the search.")))
		else:
			emptyLines+=1
		list.append(getConfigListEntry(_("Server"), config.plugins.KravenVB.weather_server, _("Choose from different servers for the weather data.")))
		list.append(getConfigListEntry(_("Language"), config.plugins.KravenVB.weather_language, _("Specify the language for the weather output.")))
		list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.KravenVB.refreshInterval, _("Choose the frequency of loading weather data from the internet.")))
		list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenVB.WeatherView, _("Choose between graphical weather symbols and Meteo symbols.")))
		if config.plugins.KravenVB.WeatherView.value == "meteo":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenVB.MeteoColor, _("Choose between light and dark Meteo symbols.")))
		else:
			emptyLines+=1
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 5 (category 2)
		emptyLines=0
		if not config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("CLOCK _____________________________________________________________________"), config.plugins.KravenVB.CategoryClock, _("This sections offers all settings for the different clocks.")))
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenVB.ClockStyle.value
			if self.actClockstyle == "clock-analog":
				list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenVB.AnalogStyle, _("Choose from different colors for the analog type clock in the infobar.")))
			elif self.actClockstyle == "clock-android":
				list.append(getConfigListEntry(_("Android-Temp-Color"), config.plugins.KravenVB.Android, _("Choose the font color of android-clock temperature.")))
			elif self.actClockstyle == "clock-weather":
				list.append(getConfigListEntry(_("Weather-Icon-Size"), config.plugins.KravenVB.ClockIconSize, _("Choose the size of the icon for 'weather icon' clock.")))
			else:
				emptyLines+=1
		else:
			emptyLines+=3
			self.actClockstyle="none"
		for i in range(emptyLines+5):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 6
		emptyLines=0
		list.append(getConfigListEntry(_("ECM INFOS _________________________________________________________________"), config.plugins.KravenVB.CategoryECMInfos, _("This sections offers all settings for showing the decryption infos.")))
		list.append(getConfigListEntry(_("Show ECM Infos"), config.plugins.KravenVB.ECMVisible, _("Choose from different options where to display the ECM informations.")))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" and not config.plugins.KravenVB.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenVB.ECMLine1, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenVB.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFont, _("Choose the font color of the ECM information.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2") and not config.plugins.KravenVB.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenVB.ECMLine2, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenVB.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFont, _("Choose the font color of the ECM information.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1") and not config.plugins.KravenVB.ECMVisible.value == "none":
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenVB.ECMLine3, _("Choose from different options to display the ECM informations.")))
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenVB.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFont, _("Choose the font color of the ECM information.")))
		else:
			emptyLines+=3
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 6 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("VIEWS _____________________________________________________________________"), config.plugins.KravenVB.CategoryViews, _("This sections offers all settings for skinned plugins.")))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenVB.Volume, _("Choose from different styles for the volume display.")))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenVB.CoolTVGuide, _("Choose from different styles for CoolTVGuide.")))
		list.append(getConfigListEntry(_("SerienRecorder"), config.plugins.KravenVB.SerienRecorder, _("Choose whether you want the Kraven skin to be applied to 'Serienrecorder' or not. Activation of this option prohibits the skin selection in the SR-plugin.")))
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			list.append(getConfigListEntry(_("MediaPortal"), config.plugins.KravenVB.MediaPortal, _("Choose whether you want the Kraven skin to be applied to 'MediaPortal' or not. To remove it again, you must deactivate it here and activate another skin in 'MediaPortal'.")))
		else:
			emptyLines+=1
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("SplitScreen"), config.plugins.KravenVB.SplitScreen, _("Choose from different styles to display SplitScreen.")))
		elif self.gete2distroversion() == "openatv":
			list.append(getConfigListEntry(_("SplitScreen"), config.plugins.KravenVB.ATVna, _("")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 6 (category 3)
		emptyLines=0
		list.append(getConfigListEntry(_("PERMANENTCLOCK __________________________________________________________"), config.plugins.KravenVB.CategoryPermanentClock, _("This sections offers all settings for PermanentClock.")))
		list.append(getConfigListEntry(_("PermanentClock-Color"), config.plugins.KravenVB.PermanentClock, _("Choose the colors of PermanentClock.")))
		if config.plugins.KravenVB.PermanentClock.value in ("permanentclock-transparent-big","permanentclock-transparent-small"):
			list.append(getConfigListEntry(_("PermanentClock-Font"), config.plugins.KravenVB.PermanentClockFont, _("Choose the fontcolor of PermanentClock.")))
		else:
			emptyLines+=1
		for i in range(emptyLines+2):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 7
		emptyLines=0
		list.append(getConfigListEntry(_("CHANNELLIST _______________________________________________________________"), config.plugins.KravenVB.CategoryChannellist, _("This sections offers all channellist settings.")))
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("use alternative (horizontal) channellist"), config.plugins.KravenVB.alternativeChannellist, _("Choose whether use alternative horizontal channellist or not.")))
			if config.plugins.KravenVB.alternativeChannellist.value == "none":
				if SystemInfo.get("NumVideoDecoders",1) > 1:
					list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle2, _("Choose from different styles for the channel selection screen.")))
					self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle2.value
				else:
					list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle, _("Choose from different styles for the channel selection screen.")))
					self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle.value
				if self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-minitv4","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv33"):
					list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenVB.ChannelSelectionMode, _("Choose between direct zapping (1xOK) and zapping after preview (2xOK).")))
				else:
					emptyLines+=1
				if not self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv3","channelselection-style-minitv4","channelselection-style-minitv22","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
					list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenVB.ChannelSelectionTrans, _("Choose the degree of background transparency for the channellists.")))
				else:
					emptyLines+=1
				if self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
					list.append(getConfigListEntry(_("Servicenumber/-name Fontsize"), config.plugins.KravenVB.ChannelSelectionServiceSize1, _("Choose the font size of channelnumber and channelname.")))
					list.append(getConfigListEntry(_("Serviceinfo Fontsize"), config.plugins.KravenVB.ChannelSelectionInfoSize1, _("Choose the font size of serviceinformation.")))
				else:
					list.append(getConfigListEntry(_("Servicenumber/-name Fontsize"), config.plugins.KravenVB.ChannelSelectionServiceSize, _("Choose the font size of channelnumber and channelname.")))
					list.append(getConfigListEntry(_("Serviceinfo Fontsize"), config.plugins.KravenVB.ChannelSelectionInfoSize, _("Choose the font size of serviceinformation.")))
				if self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
					list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize1, _("Choose the font size of event description, EPG list and primetime.")))
				elif self.actChannelselectionstyle == "channelselection-style-minitv22":
					list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize2, _("Choose the font size of EPG list and primetime.")))
				else:
					list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize3, _("Choose the font size of event description, EPG list and primetime.")))
				list.append(getConfigListEntry(_("show Picons in channellist"), config.plugins.KravenVB.ChannellistPicon, _("Choose whether picons are shown in channellist or not.")))
				list.append(getConfigListEntry(_("'Not available'-Font"), config.plugins.KravenVB.ChannelSelectionServiceNA, _("Choose the font color of channels that are unavailable at the moment.")))
				list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenVB.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
				if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
					list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.Primetime, _("Specify the time for your primetime.")))
					list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFont, _("Choose the font color of the primetime information.")))
				else:
					emptyLines+=2
				for i in range(emptyLines+1):
					list.append(getConfigListEntry(_(" "), ))
			else:
				list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionHorStyle, _("Choose from different styles for the channel selection screen.")))
				list.append(getConfigListEntry(_("show Picons in channellist"), config.plugins.KravenVB.ChannellistPicon, _("Choose whether picons are shown in channellist or not.")))
				list.append(getConfigListEntry(_("'Not available'-Font"), config.plugins.KravenVB.ChannelSelectionServiceNA, _("Choose the font color of channels that are unavailable at the moment.")))
				if config.plugins.KravenVB.ChannelSelectionHorStyle.value == "cshor-minitv":
					list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenVB.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
					if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
						list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.Primetime, _("Specify the time for your primetime.")))
						list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFont, _("Choose the font color of the primetime information.")))
					else:
						emptyLines+=2
				else:
					emptyLines+=3
				for i in range(emptyLines+6):
					list.append(getConfigListEntry(_(" "), ))
		elif self.gete2distroversion() == "openatv":
			if SystemInfo.get("NumVideoDecoders",1) > 1:
				list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle2, _("Choose from different styles for the channel selection screen.")))
				self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle2.value
			else:
				list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle, _("Choose from different styles for the channel selection screen.")))
				self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle.value
			if self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-minitv4","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv33"):
				list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenVB.ChannelSelectionMode, _("Choose between direct zapping (1xOK) and zapping after preview (2xOK).")))
			else:
				emptyLines+=1
			if not self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv3","channelselection-style-minitv4","channelselection-style-minitv22","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
				list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenVB.ChannelSelectionTrans, _("Choose the degree of background transparency for the channellists.")))
			else:
				emptyLines+=1
			if self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
				list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize1, _("Choose the font size of event description, EPG list and primetime.")))
			elif self.actChannelselectionstyle == "channelselection-style-minitv22":
				list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize2, _("Choose the font size of EPG list and primetime.")))
			else:
				list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.ChannelSelectionEPGSize3, _("Choose the font size of event description, EPG list and primetime.")))
			list.append(getConfigListEntry(_("'Not available'-Font"), config.plugins.KravenVB.ChannelSelectionServiceNA, _("Choose the font color of channels that are unavailable at the moment.")))
			list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenVB.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
				list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.Primetime, _("Specify the time for your primetime.")))
				list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFont, _("Choose the font color of the primetime information.")))
			else:
				emptyLines+=2
			for i in range(emptyLines+5):
				list.append(getConfigListEntry(_(" "), ))
		
		# page 7 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("NUMBERZAP ________________________________________________________________"), config.plugins.KravenVB.CategoryNumberZap, _("This sections offers all settings for NumberZap.")))
		list.append(getConfigListEntry(_("NumberZap-Style"), config.plugins.KravenVB.NumberZapExt, _("Choose from different styles for NumberZap.")))
		if not config.plugins.KravenVB.NumberZapExt.value == "none":
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenVB.NZBorder, _("Choose the border color for NumberZap.")))
		else:
			emptyLines+=1
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 8
		emptyLines=0
		list.append(getConfigListEntry(_("EPGSELECTION ____________________________________________________________"), config.plugins.KravenVB.CategoryEPGSelection, _("This sections offers all settings for EPGSelection.")))
		list.append(getConfigListEntry(_("EPGSelection-Style"), config.plugins.KravenVB.EPGSelection, _("Choose from different styles to display EPGSelection.")))
		list.append(getConfigListEntry(_("EPG-List Fontsize"), config.plugins.KravenVB.EPGListSize, _("Choose the font size of EPG-List.")))
		list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.EPGSelectionEPGSize, _("Choose the font size of event description.")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 8 (category 2)
		emptyLines=0
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("GRAPHMULTIEPG ___________________________________________________________"), config.plugins.KravenVB.CategoryGraphMultiEPG, _("This sections offers all settings for GraphMultiEPG.")))
			list.append(getConfigListEntry(_("GraphMultiEPG-Style"), config.plugins.KravenVB.GraphMultiEPG, _("Choose from different styles for GraphMultiEPG.")))
			list.append(getConfigListEntry(_("Event Description Fontsize"), config.plugins.KravenVB.GMEDescriptionSize, _("Choose the font size of event description.")))
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenVB.GMEBorder, _("Choose the border color for GraphMultiEPG.")))
			list.append(getConfigListEntry(_("Selected Event Background"), config.plugins.KravenVB.GMErunningbg, _("Choose the background color of selected events for GraphMultiEPG.")))
		elif self.gete2distroversion() == "openatv":
			list.append(getConfigListEntry(_("GRAPHICALEPG _____________________________________________________________"), config.plugins.KravenVB.CategoryGraphicalEPG, _("This sections offers all settings for GraphicalEPG.")))
			list.append(getConfigListEntry(_("GraphicalEPG-Style"), config.plugins.KravenVB.GraphicalEPG, _("Choose from different styles for GraphicalEPG.")))
			list.append(getConfigListEntry(_("Event Description Fontsize"), config.plugins.KravenVB.GMEDescriptionSize, _("Choose the font size of event description.")))
			if config.plugins.KravenVB.GraphicalEPG.value in ("text","text-minitv"):
				list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenVB.GMEBorder, _("Choose the border color for GraphicalEPG.")))
				list.append(getConfigListEntry(_("Selected Event Background"), config.plugins.KravenVB.GMErunningbg, _("Choose the background color of selected events for GraphicalEPG.")))
			else:
				emptyLines+=2
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 8 (category 3)
		emptyLines=0
		list.append(getConfigListEntry(_("VERTICALEPG ______________________________________________________________"), config.plugins.KravenVB.CategoryVerticalEPG, _("This sections offers all settings for VerticalEPG.")))
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("VerticalEPG-Style"), config.plugins.KravenVB.VerticalEPG, _("Choose from different styles for VerticalEPG.")))
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenVB.VEPGBorder, _("Choose the border color for VerticalEPG.")))
		elif self.gete2distroversion() == "openatv":
			list.append(getConfigListEntry(_("VerticalEPG-Style"), config.plugins.KravenVB.ATVna, _("")))
			list.append(getConfigListEntry(_("Border Color"), config.plugins.KravenVB.ATVna, _("")))
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 8 (category 4)
		emptyLines=0
		list.append(getConfigListEntry(_("TIMEREDITSCREEN ___________________________________________________________"), config.plugins.KravenVB.CategoryTimerEdit, _("This sections offers all settings for TimerEditScreen.")))
		list.append(getConfigListEntry(_("TimerEdit-Style"), config.plugins.KravenVB.TimerEditScreen, _("Choose from different styles to display TimerEditScreen.")))
		if self.gete2distroversion() == "VTi":
			list.append(getConfigListEntry(_("TimerList-Style"), config.plugins.KravenVB.TimerListStyle, _("Choose from different styles to display TimerList.")))
		elif self.gete2distroversion() == "openatv":
			list.append(getConfigListEntry(_("TimerList-Style"), config.plugins.KravenVB.ATVna, _("")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 9
		emptyLines=0
		list.append(getConfigListEntry(_("ENHANCED MOVIE CENTER _____________________________________________________"), config.plugins.KravenVB.CategoryEMC, _("This sections offers all settings for EMC ('EnhancedMovieCenter').")))
		list.append(getConfigListEntry(_("EMC-Style"), config.plugins.KravenVB.EMCStyle, _("Choose from different styles for EnhancedMovieCenter.")))
		list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.EMCEPGSize, _("Choose the font size of event description.")))
		list.append(getConfigListEntry(_("Custom EMC-Selection-Colors"), config.plugins.KravenVB.EMCSelectionColors, _("Choose whether you want to customize the selection-colors for EnhancedMovieCenter.")))
		if config.plugins.KravenVB.EMCSelectionColors.value == "emc-colors-on":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenVB.EMCSelectionBackground, _("Choose the background color of selection bars for EnhancedMovieCenter.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenVB.EMCSelectionFont, _("Choose the color of the font in selection bars for EnhancedMovieCenter.")))
		else:
			emptyLines+=2
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 9 (category 2)
		emptyLines=0
		list.append(getConfigListEntry(_("MOVIESELECTION ____________________________________________________________"), config.plugins.KravenVB.CategoryMovieSelection, _("This sections offers all settings for MovieSelection.")))
		list.append(getConfigListEntry(_("MovieSelection-Style"), config.plugins.KravenVB.MovieSelection, _("Choose from different styles for MovieSelection.")))
		list.append(getConfigListEntry(_("EPG Fontsize"), config.plugins.KravenVB.MovieSelectionEPGSize, _("Choose the font size of event description.")))
		if not fileExists("/usr/lib/enigma2/python/Plugins/Extensions/SerienFilm/plugin.py"):
			list.append(getConfigListEntry(_("Unwatched Color"), config.plugins.KravenVB.UnwatchedColor, _("Choose the font color of unwatched movies.")))
			list.append(getConfigListEntry(_("Watching Color"), config.plugins.KravenVB.WatchingColor, _("Choose the font color of watching movies.")))
			list.append(getConfigListEntry(_("Finished Color"), config.plugins.KravenVB.FinishedColor, _("Choose the font color of watched movies.")))
		else:
			emptyLines+=3
		for i in range(emptyLines+1):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 9 (category 3)
		emptyLines=0
		list.append(getConfigListEntry(_("PLAYER ____________________________________________________________________"), config.plugins.KravenVB.CategoryPlayers, _("This sections offers all settings for the movie players.")))
		list.append(getConfigListEntry(_("Clock"), config.plugins.KravenVB.PlayerClock, _("Choose from different options to show the clock in the players.")))
		if config.plugins.KravenVB.PlayerClock.value == "player-android":
			list.append(getConfigListEntry(_("Android-Temp-Color"), config.plugins.KravenVB.Android2, _("Choose the font color of android-clock temperature.")))
		else:
			emptyLines+=1
		list.append(getConfigListEntry(_("PVRState"), config.plugins.KravenVB.PVRState, _("Choose from different options to display the PVR state.")))
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))
		
		# page 10
		emptyLines=0
		if config.plugins.KravenVB.IBStyle.value == "grad":
			list.append(getConfigListEntry(_("ANTIALIASING BRIGHTNESS ________________________________________________________________"), config.plugins.KravenVB.CategoryAntialiasing, _("This sections offers all antialiasing settings. Distortions or color frames around fonts can be reduced by this settings.")))
			list.append(getConfigListEntry(_("Infobar"), config.plugins.KravenVB.InfobarAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts in the infobar and widgets by adjusting the antialiasing brightness.")))
			list.append(getConfigListEntry(_("ECM Infos"), config.plugins.KravenVB.ECMLineAntialias, _("Reduce distortions (faint/blurry) or color frames around the ECM information in the infobar by adjusting the antialiasing brightness.")))
			list.append(getConfigListEntry(_("Screens"), config.plugins.KravenVB.ScreensAntialias, _("Reduce distortions (faint/blurry) or color frames around fonts at top and bottom of screens by adjusting the antialiasing brightness.")))
			emptyLines=1
		else:
			emptyLines+=0
		for i in range(emptyLines):
			list.append(getConfigListEntry(_(" "), ))

		# page 10 (category 2)
		list.append(getConfigListEntry(_("DEBUG _____________________________________________________________________"), config.plugins.KravenVB.CategoryDebug, _("This sections offers all debug settings.")))
		list.append(getConfigListEntry(_("Screennames"), config.plugins.KravenVB.DebugNames, _("Activate or deactivate small screen names for debugging purposes.")))

		### Calculate Backgrounds
		if config.plugins.KravenVB.BackgroundColor.value == "self":
			self.skincolorbackgroundcolor = str(hex(config.plugins.KravenVB.BackgroundSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.BackgroundSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.BackgroundSelfColorB.value)[2:4]).zfill(2)
		elif config.plugins.KravenVB.BackgroundColor.value == "gradient":
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundGradientColorPrimary.value
		elif config.plugins.KravenVB.BackgroundColor.value == "texture":
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundAlternateColor.value
		else:
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundColor.value

		if config.plugins.KravenVB.IBStyle.value == "grad":
			if config.plugins.KravenVB.InfobarGradientColor.value == "self":
				self.skincolorinfobarcolor = str(hex(config.plugins.KravenVB.InfobarSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorB.value)[2:4]).zfill(2)
			elif config.plugins.KravenVB.InfobarGradientColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarGradientColor.value
		else:
			if config.plugins.KravenVB.InfobarBoxColor.value == "self":
				self.skincolorinfobarcolor = str(hex(config.plugins.KravenVB.InfobarSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorB.value)[2:4]).zfill(2)
			elif config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarGradientColorPrimary.value
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarBoxColor.value

		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self["helperimage"].hide()
		self.ShowPicture()

		position = self["config"].instance.getCurrentIndex()
		if position == 0: # about
			self["key_yellow"].setText("<< " + _("debug"))
			self["key_blue"].setText(_("profiles") + " >>")
		if (2 <= position <= 4): # profiles
			self["key_yellow"].setText("<< " + _("about"))
			self["key_blue"].setText(_("system") + " >>")
		if (6 <= position <= 17): # system
			self["key_yellow"].setText("<< " + _("profiles"))
			self["key_blue"].setText(_("global colors") + " >>")
		if (18 <= position <= 35): # global colors
			self["key_yellow"].setText("<< " + _("system"))
			self["key_blue"].setText(_("infobar-look") + " >>")
		if (36 <= position <= 53): # infobar-look
			self["key_yellow"].setText("<< " + _("global colors"))
			self["key_blue"].setText(_("infobar-contents") + " >>")
		if (54 <= position <= 60): # infobar-contents
			self["key_yellow"].setText("<< " + _("infobar-look"))
			self["key_blue"].setText(_("SecondInfobar") + " >>")
		if (62 <= position <= 71): # secondinfobar
			self["key_yellow"].setText("<< " + _("infobar-contents"))
			self["key_blue"].setText(_("weather") + " >>")
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			if (72 <= position <= 80): # weather
				self["key_yellow"].setText("<< " + _("SecondInfobar"))
				self["key_blue"].setText(_("ECM infos") + " >>")
		else:
			if (72 <= position <= 80): # weather
				self["key_yellow"].setText("<< " + _("SecondInfobar"))
				self["key_blue"].setText(_("clock") + " >>")
		if (82 <= position <= 84): # clock
			self["key_yellow"].setText("<< " + _("weather"))
			self["key_blue"].setText(_("ECM infos") + " >>")
		if (90 <= position <= 94): # ecm infos
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				self["key_yellow"].setText("<< " + _("weather"))
			else:
				self["key_yellow"].setText("<< " + _("clock"))
			self["key_blue"].setText(_("views") + " >>")
		if (96 <= position <= 101): # views
			self["key_yellow"].setText("<< " + _("ECM infos"))
			self["key_blue"].setText(_("PermanentClock") + " >>")
		if (103 <= position <= 105): # permanentclock
			self["key_yellow"].setText("<< " + _("views"))
			self["key_blue"].setText(_("channellist") + " >>")
		if (108 <= position <= 119): # channellist
			self["key_yellow"].setText("<< " + _("PermanentClock"))
			self["key_blue"].setText(_("NumberZap") + " >>")
		if (121 <= position <= 123): # numberzap
			self["key_yellow"].setText("<< " + _("channellist"))
			self["key_blue"].setText(_("EPGSelection") + " >>")
		if (126 <= position <= 129): # epgselection
			self["key_yellow"].setText("<< " + _("NumberZap"))
			self["key_blue"].setText(_("GraphEPG") + " >>")
		if (131 <= position <= 135): # graphepg
			self["key_yellow"].setText("<< " + _("EPGSelection"))
			self["key_blue"].setText(_("VerticalEPG") + " >>")
		if (137 <= position <= 139): # verticalepg
			self["key_yellow"].setText("<< " + _("GraphEPG"))
			self["key_blue"].setText(_("TimerEditScreen") + " >>")
		if (141 <= position <= 143): # timereditscreen
			self["key_yellow"].setText("<< " + _("VerticalEPG"))
			self["key_blue"].setText(_("EMC") + " >>")
		if (144 <= position <= 149): # emc
			self["key_yellow"].setText("<< " + _("TimerEditScreen"))
			self["key_blue"].setText(_("MovieSelection") + " >>")
		if (151 <= position <= 156): # movieselection
			self["key_yellow"].setText("<< " + _("EMC"))
			self["key_blue"].setText(_("player") + " >>")
		if config.plugins.KravenVB.IBStyle.value == "box":
			if (158 <= position <= 161): # player
				self["key_yellow"].setText("<< " + _("MovieSelection"))
				self["key_blue"].setText(_("debug") + " >>")
		else:
			if (158 <= position <= 161): # player
				self["key_yellow"].setText("<< " + _("MovieSelection"))
				self["key_blue"].setText(_("antialiasing") + " >>")
		if config.plugins.KravenVB.IBStyle.value == "box":
			if (162 <= position <= 163): # debug
				self["key_yellow"].setText("<< " + _("player"))
				self["key_blue"].setText(_("about") + " >>")
		else:
			if (162 <= position <= 165): # antialiasing
				self["key_yellow"].setText("<< " + _("player"))
				self["key_blue"].setText(_("debug") + " >>")
			if (167 <= position <= 168): # debug
				self["key_yellow"].setText("<< " + _("antialiasing"))
				self["key_blue"].setText(_("about") + " >>")

		option = self["config"].getCurrent()[1]
		
		if option == config.plugins.KravenVB.customProfile:
			if config.plugins.KravenVB.customProfile.value==self.lastProfile:
				self.saveProfile(msg=False)
				
		if option.value == "none":
			self.showText(50,_("Off"))
		elif option.value == "on":
			self.showText(50,_("On"))
		elif option == config.plugins.KravenVB.customProfile:
			self.showText(25,"/etc/enigma2/kraven_profile_"+str(config.plugins.KravenVB.customProfile.value))
		elif option == config.plugins.KravenVB.defaultProfile:
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/"+str(config.plugins.KravenVB.defaultProfile.value)+".jpg"):
				self["helperimage"].show()
			else:
				self.showText(25,"/etc/enigma2/kraven_default_"+str(config.plugins.KravenVB.defaultProfile.value))
		elif option == config.plugins.KravenVB.TimerListStyle:
			if option.value == "timerlist-standard":
				self.showText(50,_("standard"))
			elif option.value == "timerlist-1":
				self.showText(50,_("Style 1"))
			elif option.value == "timerlist-2":
				self.showText(50,_("Style 2"))
			elif option.value == "timerlist-3":
				self.showText(50,_("Style 3"))
			elif option.value == "timerlist-4":
				self.showText(50,_("Style 4"))
			elif option.value == "timerlist-5":
				self.showText(50,_("Style 5"))
		elif option == config.plugins.KravenVB.TypeWriter:
			if option.value == "runningtext":
				self.showText(48,_("runningtext"))
			elif option.value == "typewriter":
				self.showText(48,_("typewriter"))
		elif option == config.plugins.KravenVB.IBtop:
			if option.value == "infobar-x2-z1_top":
				self.showText(50,_("4 Tuner"))
			elif option.value == "infobar-x2-z1_top2":
				self.showText(50,_("2 Tuner"))
			elif option.value == "infobar-x2-z1_top3":
				self.showText(50,_("8 Tuner"))
		elif option == config.plugins.KravenVB.tuner:
			if option.value == "2-tuner":
				self.showText(50,_("2 Tuner"))
			elif option.value == "4-tuner":
				self.showText(50,_("4 Tuner"))
			elif option.value == "8-tuner":
				self.showText(50,_("8 Tuner"))
		elif option == config.plugins.KravenVB.tuner2:
			if option.value == "2-tuner":
				self.showText(50,_("2 Tuner"))
			elif option.value == "4-tuner":
				self.showText(50,_("4 Tuner"))
			elif option.value == "8-tuner":
				self.showText(50,_("8 Tuner"))
			elif option.value == "10-tuner":
				self.showText(50,_("10 Tuner"))
		elif option in (config.plugins.KravenVB.InfobarChannelName,config.plugins.KravenVB.InfobarChannelName2):
			if option.value == "infobar-channelname-small":
				self.showText(40,_("RTL"))
			elif option.value == "infobar-channelname-number-small":
				self.showText(40,_("5 - RTL"))
			elif option.value == "infobar-channelname":
				self.showText(76,_("RTL"))
			elif option.value == "infobar-channelname-number":
				self.showText(76,_("5 - RTL"))
		elif option in (config.plugins.KravenVB.ECMLine1,config.plugins.KravenVB.ECMLine2,config.plugins.KravenVB.ECMLine3):
			if option.value == "VeryShortCaid":
				self.showText(17,"CAID - Time")
			elif option.value == "VeryShortReader":
				self.showText(17,"Reader - Time")
			elif option.value == "ShortReader":
				self.showText(17,"CAID - Reader - Time")
			elif option.value == "Normal":
				self.showText(17,"CAID - Reader - Hops - Time")
			elif option.value == "Long":
				self.showText(17,"CAID - System - Reader - Hops - Time")
			elif option.value == "VeryLong":
				self.showText(17,"CAM - CAID - System - Reader - Hops - Time")
		elif option == config.plugins.KravenVB.FTA and option.value == "FTAVisible":
			self.showText(17,_("free to air"))
		elif option in (config.plugins.KravenVB.weather_gmcode,config.plugins.KravenVB.weather_cityname,config.plugins.KravenVB.weather_server,config.plugins.KravenVB.weather_search_over):
			self.get_weather_data()
			self.showText(20,self.actCity)
		elif option == config.plugins.KravenVB.weather_language:
			self.showText(60,option.value)
		elif option == config.plugins.KravenVB.refreshInterval:
			if option.value == "0":
				self.showText(50,_("Off"))
			elif option.value == "15":
				self.showText(50,"00:15")
			elif option.value == "30":
				self.showText(50,"00:30")
			elif option.value == "60":
				self.showText(50,"01:00")
			elif option.value == "120":
				self.showText(50,"02:00")
			elif option.value == "240":
				self.showText(50,"04:00")
			elif option.value == "480":
				self.showText(50,"08:00")
		elif option == config.plugins.KravenVB.ChannelSelectionMode:
			if option.value == "zap":
				self.showText(50,"1 x OK")
			elif option.value == "preview":
				self.showText(50,"2 x OK")
		elif option == config.plugins.KravenVB.PVRState:
			if option.value == "pvrstate-center-big":
				self.showText(44,">> 8x")
			elif option.value == "pvrstate-center-small":
				self.showText(22,">> 8x")
			else:
				self["helperimage"].show()
		elif option == config.plugins.KravenVB.record3:
			if option.value == "no-record-tuner":
				self.showText(50,_("Off"))
			else:
				self["helperimage"].show()
		elif option == config.plugins.KravenVB.ChannelSelectionServiceSize:
			size=config.plugins.KravenVB.ChannelSelectionServiceSize.value
			self.showText(int(size[-2:]),size[-2:]+" Pixel")
		elif option == config.plugins.KravenVB.ChannelSelectionInfoSize:
			size=config.plugins.KravenVB.ChannelSelectionInfoSize.value
			self.showText(int(size[-2:]),size[-2:]+" Pixel")
		elif option == config.plugins.KravenVB.ChannelSelectionServiceSize1:
			size=config.plugins.KravenVB.ChannelSelectionServiceSize1.value
			self.showText(int(size[-2:]),size[-2:]+" Pixel")
		elif option == config.plugins.KravenVB.ChannelSelectionInfoSize1:
			size=config.plugins.KravenVB.ChannelSelectionInfoSize1.value
			self.showText(int(size[-2:]),size[-2:]+" Pixel")
		elif option == config.plugins.KravenVB.ChannelSelectionEPGSize1:
			if config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.showText(24,_("description - 19 Pixel \nEPG list - 18 Pixel \nprimetime - 18 Pixel"))
			elif config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.showText(24,_("description - 22 Pixel \nEPG list - 20 Pixel \nprimetime - 20 Pixel"))
		elif option == config.plugins.KravenVB.ChannelSelectionEPGSize2:
			if config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "small":
				self.showText(24,_("EPG list - 22 Pixel \nprimetime - 22 Pixel"))
			elif config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "big":
				self.showText(24,_("EPG list - 24 Pixel \nprimetime - 24 Pixel"))
		elif option == config.plugins.KravenVB.ChannelSelectionEPGSize3:
			if config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.showText(24,_("description - 22 Pixel \nEPG list - 22 Pixel \nprimetime - 22 Pixel"))
			elif config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.showText(24,_("description - 24 Pixel \nEPG list - 24 Pixel \nprimetime - 24 Pixel"))
		elif option == config.plugins.KravenVB.MovieSelectionEPGSize:
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "small":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.showText(24,_("24 Pixel"))
		elif option == config.plugins.KravenVB.EPGSelectionEPGSize:
			if config.plugins.KravenVB.EPGSelectionEPGSize.value == "small":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.EPGSelectionEPGSize.value == "big":
				self.showText(24,_("24 Pixel"))
		elif option == config.plugins.KravenVB.EPGListSize:
			if config.plugins.KravenVB.EPGListSize.value == "small":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.EPGListSize.value == "big":
				self.showText(26,_("26 Pixel"))
		elif option == config.plugins.KravenVB.GMEDescriptionSize:
			if config.plugins.KravenVB.GMEDescriptionSize.value == "small":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.GMEDescriptionSize.value == "big":
				self.showText(24,_("24 Pixel"))
		elif option == config.plugins.KravenVB.EMCEPGSize:
			if config.plugins.KravenVB.EMCEPGSize.value == "small":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.showText(24,_("24 Pixel"))
		elif option == config.plugins.KravenVB.IBFontSize:
			if config.plugins.KravenVB.IBFontSize.value == "size-22":
				self.showText(22,_("22 Pixel"))
			elif config.plugins.KravenVB.IBFontSize.value == "size-26":
				self.showText(26,_("26 Pixel"))
			elif config.plugins.KravenVB.IBFontSize.value == "size-30":
				self.showText(30,_("30 Pixel"))
		elif option == config.plugins.KravenVB.SIBFont:
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.showText(22,_("small"))
			else:
				self.showText(26,_("big"))
		elif option == config.plugins.KravenVB.ClockIconSize:
			if config.plugins.KravenVB.ClockIconSize.value == "size-96":
				self.showText(48,_("96 Pixel"))
			elif config.plugins.KravenVB.ClockIconSize.value == "size-128":
				self.showText(64,_("128 Pixel"))
		elif option in (config.plugins.KravenVB.InfobarAntialias,config.plugins.KravenVB.ECMLineAntialias,config.plugins.KravenVB.ScreensAntialias):
			if option.value == 10:
				self.showText(50,"+/- 0%")
			elif option.value in range(0,10):
				self.showText(50,"- "+str(100-option.value*10)+"%")
			elif option.value in range(11,21):
				self.showText(50,"+ "+str(option.value*10-100)+"%")
		elif option == config.plugins.KravenVB.DebugNames and option.value == "screennames-on":
			self.showText(50,"Debug")
		elif option in (config.plugins.KravenVB.MenuColorTrans,config.plugins.KravenVB.BackgroundColorTrans,config.plugins.KravenVB.InfobarColorTrans,config.plugins.KravenVB.ChannelSelectionTrans) and option.value == "00":
			self.showText(50,_("Off"))
		elif option == config.plugins.KravenVB.BackgroundColor:
			if config.plugins.KravenVB.BackgroundColor.value == "self":
				self.showColor(self.RGB(int(config.plugins.KravenVB.BackgroundSelfColorR.value), int(config.plugins.KravenVB.BackgroundSelfColorG.value), int(config.plugins.KravenVB.BackgroundSelfColorB.value)))
			elif config.plugins.KravenVB.BackgroundColor.value == "gradient":
				self.showGradient(config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value)
			elif config.plugins.KravenVB.BackgroundColor.value == "texture":
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.BackgroundColor.value))
		elif option == config.plugins.KravenVB.BackgroundGradientColorPrimary:
			self.showGradient(config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value)
		elif option == config.plugins.KravenVB.BackgroundGradientColorSecondary:
			self.showGradient(config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value)
		elif option in (config.plugins.KravenVB.BackgroundSelfColorR,config.plugins.KravenVB.BackgroundSelfColorG,config.plugins.KravenVB.BackgroundSelfColorB):
			self.showColor(self.RGB(int(config.plugins.KravenVB.BackgroundSelfColorR.value), int(config.plugins.KravenVB.BackgroundSelfColorG.value), int(config.plugins.KravenVB.BackgroundSelfColorB.value)))
		elif option == config.plugins.KravenVB.BackgroundAlternateColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.SelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionBackground.value))
		elif option == config.plugins.KravenVB.SelectionBorder:
			self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionBorder.value))
		elif option == config.plugins.KravenVB.EMCSelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenVB.EMCSelectionBackground.value))
		elif option == config.plugins.KravenVB.Progress:
			if config.plugins.KravenVB.Progress.value in ("progress", "progress2"):
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.Progress.value))
		elif option == config.plugins.KravenVB.Border:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Border.value))
		elif option == config.plugins.KravenVB.MiniTVBorder:
			self.showColor(self.hexRGB(config.plugins.KravenVB.MiniTVBorder.value))
		elif option == config.plugins.KravenVB.NZBorder:
			self.showColor(self.hexRGB(config.plugins.KravenVB.NZBorder.value))
		elif option == config.plugins.KravenVB.GMEBorder:
			self.showColor(self.hexRGB(config.plugins.KravenVB.GMEBorder.value))
		elif option == config.plugins.KravenVB.GMErunningbg:
			if config.plugins.KravenVB.GMErunningbg.value == "global":
				self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionBackground.value))
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.GMErunningbg.value))
		elif option == config.plugins.KravenVB.VEPGBorder:
			self.showColor(self.hexRGB(config.plugins.KravenVB.VEPGBorder.value))
		elif option == config.plugins.KravenVB.Line:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Line.value))
		elif option == config.plugins.KravenVB.Font1:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Font1.value))
		elif option == config.plugins.KravenVB.Font2:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Font2.value))
		elif option == config.plugins.KravenVB.IBFont1:
			self.showColor(self.hexRGB(config.plugins.KravenVB.IBFont1.value))
		elif option == config.plugins.KravenVB.IBFont2:
			self.showColor(self.hexRGB(config.plugins.KravenVB.IBFont2.value))
		elif option == config.plugins.KravenVB.PermanentClockFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.PermanentClockFont.value))
		elif option == config.plugins.KravenVB.SelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionFont.value))
		elif option == config.plugins.KravenVB.EMCSelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.EMCSelectionFont.value))
		elif option == config.plugins.KravenVB.UnwatchedColor:
			self.showColor(self.hexRGB(config.plugins.KravenVB.UnwatchedColor.value))
		elif option == config.plugins.KravenVB.WatchingColor:
			self.showColor(self.hexRGB(config.plugins.KravenVB.WatchingColor.value))
		elif option == config.plugins.KravenVB.FinishedColor:
			self.showColor(self.hexRGB(config.plugins.KravenVB.FinishedColor.value))
		elif option == config.plugins.KravenVB.MarkedFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.MarkedFont.value))
		elif option == config.plugins.KravenVB.ButtonText:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ButtonText.value))
		elif option == config.plugins.KravenVB.Android:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Android.value))
		elif option == config.plugins.KravenVB.Android2:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Android2.value))
		elif option == config.plugins.KravenVB.ChannelSelectionServiceNA:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ChannelSelectionServiceNA.value))
		elif option == config.plugins.KravenVB.IBLine:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfobarGradientColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfobarBoxColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfobarGradientColorPrimary:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfobarGradientColorSecondary:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfoStyle:
			if config.plugins.KravenVB.InfoStyle.value == "primary":
				self.showColor(self.hexRGB(config.plugins.KravenVB.InfobarGradientColorPrimary.value))
			elif config.plugins.KravenVB.InfoStyle.value == "secondary":
				self.showColor(self.hexRGB(config.plugins.KravenVB.InfobarGradientColorSecondary.value))
			else:
				self.showGradient(config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value)
		elif option in (config.plugins.KravenVB.InfobarSelfColorR,config.plugins.KravenVB.InfobarSelfColorG,config.plugins.KravenVB.InfobarSelfColorB):
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.InfobarAlternateColor:
			self["helperimage"].show()
		elif option == config.plugins.KravenVB.ChannelnameFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ChannelnameFont.value))
		elif option == config.plugins.KravenVB.ECMFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ECMFont.value))
		elif option == config.plugins.KravenVB.PrimetimeFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.PrimetimeFont.value))
		elif option == config.plugins.KravenVB.ECMVisible:
			if option.value == "0":
				self.showText(36,_("Off"))
			elif option.value == "ib":
				self.showText(36,_("Infobar"))
			elif option.value == "sib":
				self.showText(36,"SecondInfobar")
			elif option.value == "ib+sib":
				self.showText(36,_("Infobar & \nSecondInfobar"))
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def GetPicturePath(self):
		try:
			optionValue = self["config"].getCurrent()[1]
			returnValue = self["config"].getCurrent()[1].value
			if optionValue == config.plugins.KravenVB.BackgroundColor and config.plugins.KravenVB.BackgroundColor.value == "texture":
					self.makeTexturePreview(config.plugins.KravenVB.BackgroundTexture.value)
					path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			if optionValue == config.plugins.KravenVB.BackgroundTexture:
				self.makeTexturePreview(returnValue)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.InfobarTexture:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.BackgroundAlternateColor:
				self.makeAlternatePreview(config.plugins.KravenVB.BackgroundTexture.value,returnValue)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.InfobarAlternateColor:
				self.makeAlternatePreview(config.plugins.KravenVB.InfobarTexture.value,returnValue)
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			if optionValue == config.plugins.KravenVB.IBStyle:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.IBLine:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.InfobarGradientColor:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue == config.plugins.KravenVB.InfobarBoxColor:
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue in (config.plugins.KravenVB.InfobarGradientColorPrimary,config.plugins.KravenVB.InfobarGradientColorSecondary):
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif optionValue in (config.plugins.KravenVB.InfobarSelfColorR,config.plugins.KravenVB.InfobarSelfColorG,config.plugins.KravenVB.InfobarSelfColorB):
				self.makePreview()
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg"
			elif returnValue in ("startdelay=2000","startdelay=4000","startdelay=6000","startdelay=8000","startdelay=10000","startdelay=15000","startdelay=20000"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/running-delay.jpg"
			elif returnValue in ("steptime=200","steptime=100","steptime=66","steptime=50"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/running-speed.jpg"
			elif returnValue in ("about","about2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/about.png"
			elif returnValue == ("meteo-light"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/meteo.jpg"
			elif returnValue == "progress":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull.jpg"
			elif returnValue == "progress2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull2.jpg"
			elif returnValue in ("self","emc-colors-on","unskinned-colors-on",config.plugins.KravenVB.PermanentClock.value):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colors.jpg"
			elif returnValue == ("channelselection-style-minitv3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/channelselection-style-minitv.jpg"
			elif returnValue == "channelselection-style-nobile-minitv3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/channelselection-style-nobile-minitv.jpg"
			elif returnValue == "all-screens":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/emc-smallcover.jpg"
			elif returnValue == "player-classic":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-classic.jpg"
			elif returnValue == "player-android":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-android.jpg"
			elif returnValue == "player-flip":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-flip.jpg"
			elif returnValue == "player-weather":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-weather.jpg"
			elif returnValue in ("zap","preview"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/modus.jpg"
			elif returnValue == "box":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/2.jpg"
			elif returnValue == "grad":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/infobar-style-x2.jpg"
			elif returnValue in ("record-blink","record-blink+no-record-tuner","record-shine+no-record-tuner"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/record-shine.jpg"
			elif returnValue == "tuner-blink":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/tuner-shine.jpg"
			elif returnValue in ("record-blink+tuner-shine","record-shine+tuner-blink","record+tuner-blink"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/record+tuner-shine.jpg"
			elif returnValue == "only-infobar":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/infobar-style-x3.jpg"
			elif returnValue in ("0C","18","32","58","7E"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/transparent.jpg"
			elif fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/" + returnValue + ".jpg"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/" + returnValue + ".jpg"
			if fileExists(path):
				return path
			else:
				return "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/black.jpg"
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/fb.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#00000000"])
		if self.picPath is not None:
			if self.gete2distroversion() == "VTi":
				self.PicLoad.startDecode(self.picPath)
				self.picPath = None
			elif self.gete2distroversion() == "openatv":
				self.picPath = None
				self.PicLoad.startDecode(self.picPath)
		else:
			self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.mylist()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.mylist()

	def keyDown(self):
		if self.gete2distroversion() == "openatv":
			self["config"].instance.moveSelection(self["config"].instance.moveDown)
			self.mylist()
		elif self.gete2distroversion() == "VTi":
			pass

	def keyUp(self):
		if self.gete2distroversion() == "openatv":
			self["config"].instance.moveSelection(self["config"].instance.moveUp)
			self.mylist()
		elif self.gete2distroversion() == "VTi":
			pass

	def keyUpLong(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def keyDownLong(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)
		self.mylist()

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)
		self.mylist()

	def categoryDown(self):
		position = self["config"].instance.getCurrentIndex()
		if config.plugins.KravenVB.IBStyle.value == "box":
			if position == 0: # about
				self["config"].instance.moveSelectionTo(162)
		else:
			if position == 0: # about
				self["config"].instance.moveSelectionTo(167)
		if (2 <= position <= 4): # profiles
			self["config"].instance.moveSelectionTo(0)
		if (6 <= position <= 17): # system
			self["config"].instance.moveSelectionTo(2)
		if (18 <= position <= 35): # global colors
			self["config"].instance.moveSelectionTo(6)
		if (36 <= position <= 53): # infobar-look
			self["config"].instance.moveSelectionTo(18)
		if (54 <= position <= 60): # infobar-contents
			self["config"].instance.moveSelectionTo(36)
		if (62 <= position <= 64): # secondinfobar
			self["config"].instance.moveSelectionTo(54)
		if (72 <= position <= 80): # weather
			self["config"].instance.moveSelectionTo(62)
		if (82 <= position <= 84): # clock
			self["config"].instance.moveSelectionTo(72)
		if (90 <= position <= 94): # ecm infos
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				self["config"].instance.moveSelectionTo(72)
			else:
				self["config"].instance.moveSelectionTo(82)
		if (96 <= position <= 101): # views
			self["config"].instance.moveSelectionTo(90)
		if (103 <= position <= 105): # permanentclock
			self["config"].instance.moveSelectionTo(96)
		if (108 <= position <= 119): # channellist
			self["config"].instance.moveSelectionTo(103)
		if (121 <= position <= 123): # numberzap
			self["config"].instance.moveSelectionTo(108)
		if (126 <= position <= 129): # epgselection
			self["config"].instance.moveSelectionTo(121)
		if (131 <= position <= 135): # graphepg
			self["config"].instance.moveSelectionTo(126)
		if (137 <= position <= 139): # verticalepg
			self["config"].instance.moveSelectionTo(131)
		if (141 <= position <= 143): # timereditscreen
			self["config"].instance.moveSelectionTo(137)
		if (144 <= position <= 149): # emc
			self["config"].instance.moveSelectionTo(141)
		if (151 <= position <= 156): # movieselection
			self["config"].instance.moveSelectionTo(144)
		if (158 <= position <= 161): # player
			self["config"].instance.moveSelectionTo(151)
		if config.plugins.KravenVB.IBStyle.value == "box":
			if (162 <= position <= 163): # debug
				self["config"].instance.moveSelectionTo(158)
		else:
			if (162 <= position <= 165): # antialiasing
				self["config"].instance.moveSelectionTo(158)
			if (167 <= position <= 168): # debug
				self["config"].instance.moveSelectionTo(162)
		self.mylist()

	def categoryUp(self):
		position = self["config"].instance.getCurrentIndex()
		if position == 0: # about
			self["config"].instance.moveSelectionTo(2)
		if (2 <= position <= 4): # profiles
			self["config"].instance.moveSelectionTo(6)
		if (6 <= position <= 17): # system
			self["config"].instance.moveSelectionTo(18)
		if (18 <= position <= 35): # global colors
			self["config"].instance.moveSelectionTo(36)
		if (36 <= position <= 53): # infobar-look
			self["config"].instance.moveSelectionTo(54)
		if (54 <= position <= 60): # infobar-contents
			self["config"].instance.moveSelectionTo(62)
		if (62 <= position <= 64): # secondinfobar
			self["config"].instance.moveSelectionTo(72)
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			if (72 <= position <= 81): # weather
				self["config"].instance.moveSelectionTo(90)
		else:
			if (72 <= position <= 81): # weather
				self["config"].instance.moveSelectionTo(82)
		if (82 <= position <= 84): # clock
			self["config"].instance.moveSelectionTo(90)
		if (90 <= position <= 94): # ecm infos
			self["config"].instance.moveSelectionTo(96)
		if (96 <= position <= 101): # views
			self["config"].instance.moveSelectionTo(103)
		if (103 <= position <= 105): # permanentclock
			self["config"].instance.moveSelectionTo(108)
		if (108 <= position <= 119): # channellist
			self["config"].instance.moveSelectionTo(121)
		if (121 <= position <= 123): # numberzap
			self["config"].instance.moveSelectionTo(126)
		if (126 <= position <= 129): # epgselection
			self["config"].instance.moveSelectionTo(131)
		if (131 <= position <= 135): # graphepg
			self["config"].instance.moveSelectionTo(137)
		if (137 <= position <= 139): # verticalepg
			self["config"].instance.moveSelectionTo(141)
		if (141 <= position <= 143): # timereditscreen
			self["config"].instance.moveSelectionTo(144)
		if (144 <= position <= 149): # emc
			self["config"].instance.moveSelectionTo(151)
		if (151 <= position <= 156): # movieselection
			self["config"].instance.moveSelectionTo(158)
		if (158 <= position <= 161): # player
			self["config"].instance.moveSelectionTo(162)
		if config.plugins.KravenVB.IBStyle.value == "box":
			if (162 <= position <= 164): # debug
				self["config"].instance.moveSelectionTo(0)
		else:
			if (162 <= position <= 165): # antialiasing
				self["config"].instance.moveSelectionTo(167)
			if (167 <= position <= 168): # debug
				self["config"].instance.moveSelectionTo(0)
		self.mylist()

	def keyVirtualKeyBoardCallBack(self, callback):
		try:
			if callback:  
				self["config"].getCurrent()[1].value = callback
			else:
				pass
		except:
			pass

	def OK(self):
		option = self["config"].getCurrent()[1]
		if option in (config.plugins.KravenVB.weather_cityname,config.plugins.KravenVB.weather_gmcode):
			from Screens.VirtualKeyBoard import VirtualKeyBoard
			text = self["config"].getCurrent()[1].value
			if config.plugins.KravenVB.weather_search_over.value == 'name':
				title = _("Enter the city name of your location:")
			elif config.plugins.KravenVB.weather_search_over.value == 'gmcode':
				title = _("Enter the GM code for your location:")
			self.session.openWithCallback(self.keyVirtualKeyBoardCallBack, VirtualKeyBoard, title = title, text = text)
		elif option == config.plugins.KravenVB.customProfile:
			self.saveProfile(msg=True)
		elif option == config.plugins.KravenVB.defaultProfile:
			self.reset()

	def faq(self):
		from Plugins.SystemPlugins.MPHelp import PluginHelp, XMLHelpReader
		reader = XMLHelpReader(resolveFilename(SCOPE_PLUGINS, "Extensions/KravenVB/faq.xml"))
		KravenVBFaq = PluginHelp(*reader)
		KravenVBFaq.open(self.session)

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def getDataByKey(self, list, key):
		for item in list:
			if item["key"] == key:
				return item
		return list[0]

	def getFontStyleData(self, key):
		return self.getDataByKey(channelselFontStyles, key)

	def getFontSizeData(self, key):
		return self.getDataByKey(channelInfoFontSizes, key)

	def save(self):
		
		self.saveProfile(msg=False)
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		self.skinSearchAndReplace = []
					
		### Background
		self.skinSearchAndReplace.append(['name="Kravenbg" value="#00000000', 'name="Kravenbg" value="#00' + self.skincolorbackgroundcolor])

		### Background Transparency (global)
		self.skinSearchAndReplace.append(['name="Kravenbg" value="#00', 'name="Kravenbg" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value])

		### Background2 (non-transparent)
		if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
			self.skinSearchAndReplace.append(['name="Kravenbg2" value="#00000000', 'name="Kravenbg2" value="#00' + self.skincolorbackgroundcolor])
			if config.plugins.KravenVB.Unskinned.value == "unskinned-colors-on":
				self.skinSearchAndReplace.append(['name="background" value="#00000000', 'name="background" value="#00' + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg2" value="#00000000', 'name="Kravenbg2" value="#00' + config.plugins.KravenVB.BackgroundColor.value])
			if config.plugins.KravenVB.Unskinned.value == "unskinned-colors-on":
				self.skinSearchAndReplace.append(['name="background" value="#00000000', 'name="background" value="#00' + config.plugins.KravenVB.BackgroundColor.value])

		### Background3 (Menus Transparency)
		if config.plugins.KravenVB.Logo.value in ("logo","metrix-icons"):
			if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + config.plugins.KravenVB.BackgroundColor.value])
		else:
			if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#00' + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="Kravenbg3" value="#00000000', 'name="Kravenbg3" value="#00' + config.plugins.KravenVB.BackgroundColor.value])

		### Background4 (Channellist)
		if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
			self.skinSearchAndReplace.append(['name="Kravenbg4" value="#00000000', 'name="Kravenbg4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg4" value="#00000000', 'name="Kravenbg4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + config.plugins.KravenVB.BackgroundColor.value])

		### Background5 (Radio Channellist)
		if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
			self.skinSearchAndReplace.append(['name="Kravenbg5" value="#00000000', 'name="Kravenbg5" value="#' + "60" + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="Kravenbg5" value="#00000000', 'name="Kravenbg5" value="#' + "60" + config.plugins.KravenVB.BackgroundColor.value])

		### SIB Background
		if config.plugins.KravenVB.BackgroundColor.value in ("self","gradient","texture"):
			self.skinSearchAndReplace.append(['name="KravenSIBbg" value="#00000000', 'name="KravenSIBbg" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.skincolorbackgroundcolor])
		else:
			self.skinSearchAndReplace.append(['name="KravenSIBbg" value="#00000000', 'name="KravenSIBbg" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + config.plugins.KravenVB.BackgroundColor.value])

		### Background Grafiks
		if config.plugins.KravenVB.BackgroundColor.value in ("gradient","texture"):
			self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<ePixmap pixmap="KravenVB/graphics/globalbg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
			self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<ePixmap pixmap="KravenVB/graphics/nontransbg.png" position="0,0" size="1280,720" zPosition="-10" />'])
			self.skinSearchAndReplace.append(['<!-- menubg */-->', '<ePixmap pixmap="KravenVB/graphics/menubg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
			self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<ePixmap pixmap="KravenVB/graphics/channelbg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
			self.skinSearchAndReplace.append(['<!-- sibbg */-->', '<ePixmap pixmap="KravenVB/graphics/sibbg.png" position="0,0" size="1280,720" zPosition="-10" alphatest="blend" />'])
		else:
			self.skinSearchAndReplace.append(['<!-- globalbg */-->', '<eLabel backgroundColor="Kravenbg" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
			self.skinSearchAndReplace.append(['<!-- nontransbg */-->', '<eLabel backgroundColor="Kravenbg2" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
			self.skinSearchAndReplace.append(['<!-- menubg */-->', '<eLabel backgroundColor="Kravenbg3" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
			self.skinSearchAndReplace.append(['<!-- channelbg */-->', '<eLabel backgroundColor="Kravenbg4" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])
			self.skinSearchAndReplace.append(['<!-- sibbg */-->', '<eLabel backgroundColor="KravenSIBbg" position="0,0" size="1280,720" transparent="0" zPosition="-10" />'])

		### Channelname. Transparency 50%, color always grey
		self.skinSearchAndReplace.append(['name="KravenNamebg" value="#A01B1775', 'name="KravenNamebg" value="#7F7F7F7F'])

		### ECM. Transparency of infobar, color of text
		if config.plugins.KravenVB.IBStyle.value == "grad":
			self.skinSearchAndReplace.append(['name="KravenECMbg" value="#F1325698', 'name="KravenECMbg" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenVB.ECMLineAntialias.value)])
		else:
			self.skinSearchAndReplace.append(['name="KravenECMbg" value="#F1325698', 'name="KravenECMbg" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.skincolorinfobarcolor])

		### Infobar. Transparency of infobar, color of infobar
		self.skinSearchAndReplace.append(['name="KravenIBbg" value="#001B1775', 'name="KravenIBbg" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.skincolorinfobarcolor])

		### CoolTV. color of infobar or color of background, if ibar invisible
		if config.plugins.KravenVB.IBColor.value == "all-screens":
			if config.plugins.KravenVB.IBStyle.value == "grad":
				self.skinSearchAndReplace.append(['name="KravenIBCoolbg" value="#00000000', 'name="KravenIBCoolbg" value="#00' + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenVB.ScreensAntialias.value)])
			else:
				self.skinSearchAndReplace.append(['name="KravenIBCoolbg" value="#00000000', 'name="KravenIBCoolbg" value="#00' + self.skincolorinfobarcolor])
		else:
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBCoolbg"', 'backgroundColor="Kravenbg2"'])

		### Screens. Lower Transparency of infobar and background, color of infobar or color of background, if ibar invisible
		if config.plugins.KravenVB.IBColor.value == "all-screens":
			if config.plugins.KravenVB.IBStyle.value == "grad":
				self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + self.calcTransparency(config.plugins.KravenVB.InfobarColorTrans.value,config.plugins.KravenVB.BackgroundColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenVB.ScreensAntialias.value)])
				self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + self.calcTransparency(config.plugins.KravenVB.InfobarColorTrans.value,config.plugins.KravenVB.MenuColorTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenVB.ScreensAntialias.value)])
				self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + self.calcTransparency(config.plugins.KravenVB.InfobarColorTrans.value,config.plugins.KravenVB.ChannelSelectionTrans.value) + self.calcBrightness(self.skincolorinfobarcolor,config.plugins.KravenVB.ScreensAntialias.value)])
			else:
				self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + self.skincolorinfobarcolor])
				self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + self.skincolorinfobarcolor])
				self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + self.skincolorinfobarcolor])
		else:
			self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#00' + config.plugins.KravenVB.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#00' + config.plugins.KravenVB.MenuColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#00' + config.plugins.KravenVB.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])

		### Menu
		if self.gete2distroversion() == "VTi":
			self.skinSearchAndReplace.append(['render="KravenVBMenuPig"', 'render="KravenVBPig3"'])
		if config.plugins.KravenVB.Logo.value == "minitv":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<constant-widget name="Logo1"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<constant-widget name="Icons1"/>'])
		elif config.plugins.KravenVB.Logo.value == "logo":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<constant-widget name="Logo2"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<constant-widget name="Icons2"/>'])
		elif config.plugins.KravenVB.Logo.value == "metrix-icons":
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<constant-widget name="Logo3"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<constant-widget name="Icons3"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- Logo -->', '<constant-widget name="Logo4"/>'])
			self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', '<constant-widget name="Icons4"/>'])

		### Infobar. Background-Style
		if config.plugins.KravenVB.IBStyle.value == "box":

			### Infobar - Background
			self.skinSearchAndReplace.append(['<!--<eLabel position', '<eLabel position'])
			self.skinSearchAndReplace.append(['zPosition="-8" />-->', 'zPosition="-8" />'])

			### Infobar - Line
			self.skinSearchAndReplace.append(['name="KravenIBLine" value="#00ffffff', 'name="KravenIBLine" value="#' + config.plugins.KravenVB.IBLine.value])

			### Infobar
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-ib-top"/>', '<constant-widget name="box2-ib-top"/>'])
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-np-x1"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-x2-x3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-z1-z2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-zz1-zz4"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-zz2-zz3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box2-ib-zzz1"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-ib-top"/>', '<constant-widget name="texture-ib-top"/>'])
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-np-x1"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-x2-x3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-z1-z2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-zz1-zz4"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-zz2-zz3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="texture-ib-zzz1"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-ib-top"/>', '<constant-widget name="box-ib-top"/>'])
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-np-x1"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-x2-x3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-z1-z2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-zz1-zz4"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-zz2-zz3"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="box-ib-zzz1"/>'])

			### NetatmoBar - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-netatmo"/>', '<constant-widget name="box2-netatmo"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-netatmo"/>', '<constant-widget name="texture-netatmo"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-netatmo"/>', '<constant-widget name="box-netatmo"/>'])

			### SIB - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-sib"/>', '<constant-widget name="box2-sib"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-sib"/>', '<constant-widget name="texture-sib"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-sib"/>', '<constant-widget name="box-sib"/>'])

			### weather-big - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-big"/>', '<constant-widget name="box2-weather-big"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-big"/>', '<constant-widget name="texture-weather-big"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-big"/>', '<constant-widget name="box-weather-big"/>'])

			### weather-small - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-small"/>', '<constant-widget name="box2-weather-small"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-small"/>', '<constant-widget name="texture-weather-small"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-weather-small"/>', '<constant-widget name="box-weather-small"/>'])

			### weather-small - Position
			self.skinSearchAndReplace.append(['position="960,55" size="70,70"', 'position="1000,25" size="70,70"'])
			self.skinSearchAndReplace.append(['position="1030,55" size="115,70"', 'position="1070,25" size="115,70"'])
			self.skinSearchAndReplace.append(['position="1145,55" size="75,35"', 'position="1185,25" size="75,35"'])
			self.skinSearchAndReplace.append(['position="1145,90" size="75,35"', 'position="1185,60" size="75,35"'])

			### clock-android - Background
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2") and self.actClockstyle == "clock-android":
				self.skinSearchAndReplace.append(['position="0,576" size="1280,144"', 'position="0,566" size="1280,154"'])
				self.skinSearchAndReplace.append(['position="0,576" size="1280,2"', 'position="0,566" size="1280,2"'])
				self.skinSearchAndReplace.append(['position="0,580" size="1280,140"', 'position="0,566" size="1280,154"'])
				self.skinSearchAndReplace.append(['position="0,580" size="1280,2"', 'position="0,566" size="1280,2"'])

			### EMCMediaCenter, MoviePlayer, DVDPlayer - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-player"/>', '<constant-widget name="box2-player"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-player"/>', '<constant-widget name="texture-player"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-player"/>', '<constant-widget name="box-player"/>'])

			### EPGSelectionEPGBar - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-EPGBar"/>', '<constant-widget name="box2-EPGBar"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-EPGBar"/>', '<constant-widget name="texture-EPGBar"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-EPGBar"/>', '<constant-widget name="box-EPGBar"/>'])

			### ChannelSelectionRadio
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-csr"/>', '<constant-widget name="box2-csr"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-csr"/>', '<constant-widget name="texture-csr"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-csr"/>', '<constant-widget name="box-csr"/>'])

			### RadioInfoBar
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-rib"/>', '<constant-widget name="box2-rib"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-rib"/>', '<constant-widget name="texture-rib"/>'])
			else:
				self.skinSearchAndReplace.append(['<constant-widget name="gradient-rib"/>', '<constant-widget name="box-rib"/>'])

		else:
			### Infobar
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-np-x1"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-x2-x3"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-z1-z2"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-zz1-zz4"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-zz2-zz3"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', '<constant-widget name="gradient-ib-zzz1"/>'])

		### MediaPortal (player) box-style
		if config.plugins.KravenVB.MediaPortal.value == "mediaportal":
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				mpplayer = """<ePixmap pixmap="KravenVB/graphics/ibar5.png" position="0,610" size="1280,110" zPosition="-9" />
	  <eLabel position="0,610" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
				self.skinSearchAndReplace.append(['<!-- MediaPortal playercolor */-->', mpplayer])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				mpplayer1 = """<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,610" size="1280,110" zPosition="-9" />
	  <eLabel position="0,610" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
				self.skinSearchAndReplace.append(['<!-- MediaPortal playercolor */-->', mpplayer1])
			else:
				mpplayer2 = """<eLabel position="0,610" size="1280,110" backgroundColor="KravenIBbg" zPosition="-9" />
	  <eLabel position="0,610" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
				self.skinSearchAndReplace.append(['<!-- MediaPortal playercolor */-->', mpplayer2])

		### Font Colors
		self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#' + config.plugins.KravenVB.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#' + config.plugins.KravenVB.Font2.value])
		if config.plugins.KravenVB.Unskinned.value == "unskinned-colors-on":
			self.skinSearchAndReplace.append(['name="foreground" value="#00dddddd', 'name="foreground" value="#' + config.plugins.KravenVB.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont1" value="#00ffffff', 'name="KravenIBFont1" value="#' + config.plugins.KravenVB.IBFont1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont2" value="#00F0A30A', 'name="KravenIBFont2" value="#' + config.plugins.KravenVB.IBFont2.value])
		self.skinSearchAndReplace.append(['name="KravenPermanentClock" value="#00ffffff', 'name="KravenPermanentClock" value="#' + config.plugins.KravenVB.PermanentClockFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
		if config.plugins.KravenVB.EMCSelectionColors.value == "none":
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenVB.EMCSelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenVB.EMCSelectionBackground.value])
		self.skinSearchAndReplace.append(['name="selectedFG" value="#00ffffff', 'name="selectedFG" value="#' + config.plugins.KravenVB.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenMarked" value="#00ffffff', 'name="KravenMarked" value="#' + config.plugins.KravenVB.MarkedFont.value])
		self.skinSearchAndReplace.append(['name="KravenECM" value="#00ffffff', 'name="KravenECM" value="#' + config.plugins.KravenVB.ECMFont.value])
		self.skinSearchAndReplace.append(['name="KravenName" value="#00ffffff', 'name="KravenName" value="#' + config.plugins.KravenVB.ChannelnameFont.value])
		self.skinSearchAndReplace.append(['name="KravenButton" value="#00ffffff', 'name="KravenButton" value="#' + config.plugins.KravenVB.ButtonText.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid" value="#00ffffff', 'name="KravenAndroid" value="#' + config.plugins.KravenVB.Android.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid2" value="#00ffffff', 'name="KravenAndroid2" value="#' + config.plugins.KravenVB.Android2.value])
		self.skinSearchAndReplace.append(['name="KravenPrime" value="#0070AD11', 'name="KravenPrime" value="#' + config.plugins.KravenVB.PrimetimeFont.value])

		### Infobar (Serviceevent) Font-Size
		if config.plugins.KravenVB.IBFontSize.value == "size-22":
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,543" size="336,40"', 'font="Regular;22" position="603,551" size="336,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,640" size="336,40"', 'font="Regular;22" position="603,648" size="336,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,544" size="484,40"', 'font="Regular;22" position="603,552" size="484,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,644" size="484,40"', 'font="Regular;22" position="603,652" size="484,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="438,615" size="472,40"', 'font="Regular;22" position="438,620" size="472,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="510,667" size="437,40"', 'font="Regular;22" position="510,674" size="437,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,615" size="481,40"', 'font="Regular;22" position="430,623" size="481,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,667" size="481,40"', 'font="Regular;22" position="430,674" size="481,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,559" size="481,40"', 'font="Regular;22" position="430,567" size="481,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,650" size="481,40"', 'font="Regular;22" position="430,659" size="481,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,585" size="708,40"', 'font="Regular;22" position="199,593" size="708,27"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,637" size="708,40"', 'font="Regular;22" position="199,644" size="708,27"'])
		elif config.plugins.KravenVB.IBFontSize.value == "size-26":
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,543" size="336,40"', 'font="Regular;26" position="603,546" size="336,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,640" size="336,40"', 'font="Regular;26" position="603,643" size="336,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,544" size="484,40"', 'font="Regular;26" position="603,547" size="484,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="603,644" size="484,40"', 'font="Regular;26" position="603,647" size="484,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="438,615" size="472,40"', 'font="Regular;26" position="438,618" size="472,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="510,667" size="437,40"', 'font="Regular;26" position="510,670" size="437,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,615" size="481,40"', 'font="Regular;26" position="430,618" size="481,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,667" size="481,40"', 'font="Regular;26" position="430,670" size="481,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,559" size="481,40"', 'font="Regular;26" position="430,562" size="481,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,650" size="481,40"', 'font="Regular;26" position="430,653" size="481,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,585" size="708,40"', 'font="Regular;26" position="199,588" size="708,34"'])
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,637" size="708,40"', 'font="Regular;26" position="199,640" size="708,34"'])

		### ChannelSelection (Servicename, Servicenumber, Serviceinfo) Font-Size
		if self.gete2distroversion() == "VTi":
			if not self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
				if config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-16":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;16"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;16"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-18":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;18"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;18"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-20":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;20"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;20"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-22":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;22"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;22"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-24":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;24"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;24"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-26":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;26"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;26"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-28":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;28"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;28"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize.value == "size-30":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;25"', 'serviceNumberFont="Regular;30"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;25"', 'serviceNameFont="Regular;30"'])
				if config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-16":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;16"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-18":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;18"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-20":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;20"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-22":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;22"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-24":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;24"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-26":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;26"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-28":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;28"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize.value == "size-30":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;23"', 'serviceInfoFont="Regular;30"'])
			else:
				if config.plugins.KravenVB.ChannelSelectionServiceSize1.value == "size-16":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;20"', 'serviceNumberFont="Regular;16"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;20"', 'serviceNameFont="Regular;16"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize1.value == "size-18":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;20"', 'serviceNumberFont="Regular;18"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;20"', 'serviceNameFont="Regular;18"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize1.value == "size-22":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;20"', 'serviceNumberFont="Regular;22"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;20"', 'serviceNameFont="Regular;22"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize1.value == "size-24":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;20"', 'serviceNumberFont="Regular;24"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;20"', 'serviceNameFont="Regular;24"'])
				elif config.plugins.KravenVB.ChannelSelectionServiceSize1.value == "size-26":
					self.skinSearchAndReplace.append(['serviceNumberFont="Regular;20"', 'serviceNumberFont="Regular;26"'])
					self.skinSearchAndReplace.append(['serviceNameFont="Regular;20"', 'serviceNameFont="Regular;26"'])
				if config.plugins.KravenVB.ChannelSelectionInfoSize1.value == "size-16":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;20"', 'serviceInfoFont="Regular;16"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize1.value == "size-18":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;20"', 'serviceInfoFont="Regular;18"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize1.value == "size-22":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;20"', 'serviceInfoFont="Regular;22"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize1.value == "size-24":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;20"', 'serviceInfoFont="Regular;24"'])
				elif config.plugins.KravenVB.ChannelSelectionInfoSize1.value == "size-26":
					self.skinSearchAndReplace.append(['serviceInfoFont="Regular;20"', 'serviceInfoFont="Regular;26"'])

		### ChannelSelection (Event-Description) Font-Size and Primetime
		if self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv3"):
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSLEPG22"/>', '<constant-widget name="CSLEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSLEPG22"/>', '<constant-widget name="CSLEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSLEPG22"/>', '<constant-widget name="CSLEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv33":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSEPEPG22"/>', '<constant-widget name="CSEPEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSEPEPG22"/>', '<constant-widget name="CSEPEPG324"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSEPEPG22"/>', '<constant-widget name="CSEPEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv4":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSREPG22"/>', '<constant-widget name="CSREPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSREPG22"/>', '<constant-widget name="CSREPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSREPG22"/>', '<constant-widget name="CSREPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv2":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT2EPG22"/>', '<constant-widget name="CSMT2EPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT2EPG22"/>', '<constant-widget name="CSMT2EPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT2EPG22"/>', '<constant-widget name="CSMT2EPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv22":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT22EPG22"/>', '<constant-widget name="CSMT22EPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT22EPG22"/>', '<constant-widget name="CSMT22EPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSMT22EPG22"/>', '<constant-widget name="CSMT22EPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNEPG19"/>', '<constant-widget name="CSNEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNEPG19"/>', '<constant-widget name="CSNEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNEPG19"/>', '<constant-widget name="CSNEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile2":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSN2EPG19"/>', '<constant-widget name="CSN2EPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSN2EPG19"/>', '<constant-widget name="CSN2EPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSN2EPG19"/>', '<constant-widget name="CSN2EPG19Prime"/>'])
		elif self.actChannelselectionstyle in ("channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPG19"/>', '<constant-widget name="CSNMTEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPG19"/>', '<constant-widget name="CSNMTEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPG19"/>', '<constant-widget name="CSNMTEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile-minitv33":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPEPG19"/>', '<constant-widget name="CSNMTEPEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPEPG19"/>', '<constant-widget name="CSNMTEPEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNMTEPEPG19"/>', '<constant-widget name="CSNMTEPEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nopicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNPEPG22"/>', '<constant-widget name="CSNPEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNPEPG22"/>', '<constant-widget name="CSNPEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSNPEPG22"/>', '<constant-widget name="CSNPEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-xpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSXEPG22"/>', '<constant-widget name="CSXEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSXEPG22"/>', '<constant-widget name="CSXEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSXEPG22"/>', '<constant-widget name="CSXEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZEPG22"/>', '<constant-widget name="CSZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZEPG22"/>', '<constant-widget name="CSZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZEPG22"/>', '<constant-widget name="CSZEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zzpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZEPG22"/>', '<constant-widget name="CSZZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZEPG22"/>', '<constant-widget name="CSZZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZEPG22"/>', '<constant-widget name="CSZZEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zzzpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZZEPG22"/>', '<constant-widget name="CSZZZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZZEPG22"/>', '<constant-widget name="CSZZZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append(['<constant-widget name="CSZZZEPG22"/>', '<constant-widget name="CSZZZEPG22Prime"/>'])

		### ChannelSelection horizontal Primetime
		if self.gete2distroversion() == "VTi" and config.plugins.KravenVB.alternativeChannellist.value == "on" and config.plugins.KravenVB.ChannelSelectionHorStyle.value == "cshor-minitv" and config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
			self.skinSearchAndReplace.append(['<constant-widget name="CSHORMT"/>', '<constant-widget name="CSHORMTPrime"/>'])

		### ChannelSelection 'not available' Font
		self.skinSearchAndReplace.append(['name="KravenNotAvailable" value="#00FFEA04', 'name="KravenNotAvailable" value="#' + config.plugins.KravenVB.ChannelSelectionServiceNA.value])

		### GraphEPG selected background color
		if config.plugins.KravenVB.GMErunningbg.value == "global":
			self.skinSearchAndReplace.append(['name="KravenGMErunningbg" value="#00389416', 'name="KravenGMErunningbg" value="#' + config.plugins.KravenVB.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenGMErunningbg" value="#00389416', 'name="KravenGMErunningbg" value="#' + config.plugins.KravenVB.GMErunningbg.value])

		### Debug-Names
		if config.plugins.KravenVB.DebugNames.value == "screennames-on":
			self.skinSearchAndReplace.append(['<!--<text', '<eLabel backgroundColor="#00000000" font="Regular;15" foregroundColor="white" text'])

			debug = """<widget backgroundColor="#00000000" font="Regular;15" foregroundColor="white" render="Label" source="menu" position="70,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9">
	  <convert type="KravenVBMenuEntryID"></convert>
	</widget>
	<eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />"""
			self.skinSearchAndReplace.append(['<!-- KravenVBMenuEntryID-Converter -->', debug])

			debugpos1 = """ " position="70,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" />
	<eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />"""
			self.skinSearchAndReplace.append(['" position="70,0" />-->', debugpos1])

			debugpos2 = """ " position="42,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" />
	<eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />"""
			self.skinSearchAndReplace.append(['" position="42,0" />-->', debugpos2])

			debugpos3 = """ " position="40,0" size="500,18" halign="left" valign="center" transparent="1" zPosition="9" />
	<eLabel position="0,0" size="1280,18" backgroundColor="#00000000" zPosition="8" />"""
			self.skinSearchAndReplace.append(['" position="40,0" />-->', debugpos3])

		### Icons
		if config.plugins.KravenVB.IBColor.value == "only-infobar":
			if config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])
			if config.plugins.KravenVB.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-light/"])
		elif config.plugins.KravenVB.IBColor.value == "all-screens":
			if config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
			if config.plugins.KravenVB.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-dark/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["/infobar-icons/", "/icons-light/"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])

		### Weather-Server
		if config.plugins.KravenVB.weather_server.value == "_owm":
			self.skinSearchAndReplace.append(['KravenVBWeather', 'KravenVBWeather_owm'])
			if config.plugins.KravenVB.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo2; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenVBWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo2; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo2; 60" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="100,100" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="100,100" render="Label" font="Meteo2; 100" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])
		elif config.plugins.KravenVB.weather_server.value == "_accu":
			self.skinSearchAndReplace.append(['KravenVBWeather', 'KravenVBWeather_accu'])
			if config.plugins.KravenVB.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenVBWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo; 60" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="100,100" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="100,100" render="Label" font="Meteo; 1000" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])
		elif config.plugins.KravenVB.weather_server.value == "_realtek":
			self.skinSearchAndReplace.append(['KravenVBWeather', 'KravenVBWeather_realtek'])
			if config.plugins.KravenVB.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo; 40" halign="right" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenVBWetterPicon" alphatest="blend"', 'size="50,50" render="Label" font="Meteo; 45" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo; 60" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="100,100" render="KravenVBWetterPicon" alphatest="blend" path="WetterIcons"', 'size="100,100" render="Label" font="Meteo; 100" halign="center" valign="center" foregroundColor="KravenMeteo" noWrap="1"'])
				self.skinSearchAndReplace.append(['MeteoIcon</convert>', 'MeteoFont</convert>'])

		### Meteo-Font
		if config.plugins.KravenVB.MeteoColor.value == "meteo-dark":
			self.skinSearchAndReplace.append(['name="KravenMeteo" value="#00fff0e0"', 'name="KravenMeteo" value="#00000000"'])

		### Progress
		if config.plugins.KravenVB.Progress.value == "progress2":
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress18.png"',' pixmap="KravenVB/progress/progress18_2.png"'])
			self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenVB/progress/progress52.png"',' picServiceEventProgressbar="KravenVB/progress/progress52_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress170.png"',' pixmap="KravenVB/progress/progress170_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress200.png"',' pixmap="KravenVB/progress/progress200_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress220.png"',' pixmap="KravenVB/progress/progress220_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress248.png"',' pixmap="KravenVB/progress/progress248_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"',' pixmap="KravenVB/progress/progress300_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"',' pixmap="KravenVB/progress/progress328_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"',' pixmap="KravenVB/progress/progress370_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"',' pixmap="KravenVB/progress/progress380_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"',' pixmap="KravenVB/progress/progress410_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress480.png"',' pixmap="KravenVB/progress/progress480_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"',' pixmap="KravenVB/progress/progress581_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"',' pixmap="KravenVB/progress/progress599_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress708.png"',' pixmap="KravenVB/progress/progress708_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress749.png"',' pixmap="KravenVB/progress/progress749_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress858.png"',' pixmap="KravenVB/progress/progress858_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress888.png"',' pixmap="KravenVB/progress/progress888_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress990.png"',' pixmap="KravenVB/progress/progress990_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress1265.png"',' pixmap="KravenVB/progress/progress1265_2.png"'])
		elif not config.plugins.KravenVB.Progress.value == "progress":
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress18.png"'," "])
			self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenVB/progress/progress52.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress170.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress200.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress220.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress248.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress480.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress708.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress749.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress858.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress888.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress990.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress1265.png"'," "])
			self.skinSearchAndReplace.append(['name="KravenProgress" value="#00C3461B', 'name="KravenProgress" value="#' + config.plugins.KravenVB.Progress.value])

		### Border
		self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#' + config.plugins.KravenVB.Border.value])

		### MiniTV Border
		self.skinSearchAndReplace.append(['name="KravenBorder2" value="#003F3F3F', 'name="KravenBorder2" value="#' + config.plugins.KravenVB.MiniTVBorder.value])

		### NumberZap Border
		if not config.plugins.KravenVB.NumberZapExt.value == "none":
			self.skinSearchAndReplace.append(['name="KravenNZBorder" value="#00ffffff', 'name="KravenNZBorder" value="#' + config.plugins.KravenVB.NZBorder.value])

		### GraphEPG Border
		self.skinSearchAndReplace.append(['name="KravenGMEBorder" value="#00ffffff', 'name="KravenGMEBorder" value="#' + config.plugins.KravenVB.GMEBorder.value])

		### VerticalEPG Border
		self.skinSearchAndReplace.append(['name="KravenVEPGBorder" value="#00ffffff', 'name="KravenVEPGBorder" value="#' + config.plugins.KravenVB.VEPGBorder.value])

		### Line
		self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#' + config.plugins.KravenVB.Line.value])

		### Runningtext
		if config.plugins.KravenVB.RunningText.value == "none":
			self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
		if not config.plugins.KravenVB.RunningText.value == "none":
			self.skinSearchAndReplace.append(["startdelay=5000", config.plugins.KravenVB.RunningText.value])
			self.skinSearchAndReplace.append(["steptime=90", config.plugins.KravenVB.RunningTextSpeed.value])
			if config.plugins.KravenVB.RunningTextSpeed.value == "steptime=200":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=66"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=100":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=33"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=66":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=22"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=50":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=17"])

		### Scrollbar
		if self.gete2distroversion() == "VTi":
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="0"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="10"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="15"'])
		elif self.gete2distroversion() == "openatv":
			if config.plugins.KravenVB.ScrollBar2.value == "showOnDemand":
				self.skinSearchAndReplace.append(['scrollbarMode="showNever"', 'scrollbarMode="showOnDemand"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', ''])
			else:
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', ''])

		### Selectionborder
		if not config.plugins.KravenVB.SelectionBorder.value == "none":
			self.selectionbordercolor = config.plugins.KravenVB.SelectionBorder.value
			self.borset = ("borset_" + self.selectionbordercolor + ".png")
			self.skinSearchAndReplace.append(["borset.png", self.borset])

		### IB Color visible
		if config.plugins.KravenVB.IBColor.value == "only-infobar":
			self.skinSearchAndReplace.append(['backgroundColor="KravenMbg"', 'backgroundColor="Kravenbg"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont1"', 'foregroundColor="KravenFont1"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont2"', 'foregroundColor="KravenFont2"'])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-cs"/>', " "])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-cooltv"/>', " "])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-emc"/>', " "])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-wrr"/>', " "])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-split1"/>', " "])
			self.skinSearchAndReplace.append(['<constant-widget name="gradient-split2"/>', " "])
		else:
			self.skinSearchAndReplace.append(['backgroundColor="KravenMbg"', 'backgroundColor="KravenIBbg2"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont1"', 'foregroundColor="KravenIBFont1"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont2"', 'foregroundColor="KravenIBFont2"'])

			if config.plugins.KravenVB.IBStyle.value == "box":
				### Menu
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					menubox = """<ePixmap pixmap="KravenVB/graphics/ibar4.png" position="0,640" size="1280,80" zPosition="-9" alphatest="blend" />
	<eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	<ePixmap pixmap="KravenVB/graphics/ibaro.png" position="0,0" size="1280,59" zPosition="-9" alphatest="blend" />
	<eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
					self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menubox])

					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cs"/>', '<constant-widget name="box2-cs"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cooltv"/>', '<constant-widget name="box2-cooltv"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-emc"/>', '<constant-widget name="box2-emc"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-wrr"/>', '<constant-widget name="box2-wrr"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split1"/>', '<constant-widget name="box2-split1"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split2"/>', '<constant-widget name="box2-split2"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					menubox = """<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,640" size="1280,80" zPosition="-9" alphatest="blend" />
	<eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,0" size="1280,59" zPosition="-9" alphatest="blend" />
	<eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
					self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menubox])

					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cs"/>', '<constant-widget name="texture-cs"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cooltv"/>', '<constant-widget name="texture-cooltv"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-emc"/>', '<constant-widget name="texture-emc"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-wrr"/>', '<constant-widget name="texture-wrr"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split1"/>', '<constant-widget name="texture-split1"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split2"/>', '<constant-widget name="texture-split2"/>'])
				else:
					menubox = """<eLabel position="0,640" size="1280,80" backgroundColor="KravenIBbg2" zPosition="-9" />
	  <eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	  <eLabel position="0,0" size="1280,59" backgroundColor="KravenIBbg2" zPosition="-9" />
	  <eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
					self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menubox])

					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cs"/>', '<constant-widget name="box-cs"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-cooltv"/>', '<constant-widget name="box-cooltv"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-emc"/>', '<constant-widget name="box-emc"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-wrr"/>', '<constant-widget name="box-wrr"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split1"/>', '<constant-widget name="box-split1"/>'])
					self.skinSearchAndReplace.append(['<constant-widget name="gradient-split2"/>', '<constant-widget name="box-split2"/>'])

				### Title - Position
				self.skinSearchAndReplace.append(['position="70,12"','position="70,7"'])
				self.skinSearchAndReplace.append(['position="63,12"','position="63,7"'])
				self.skinSearchAndReplace.append(['position="42,12"','position="42,8"'])
				self.skinSearchAndReplace.append(['position="440,16"','position="440,11"'])

				### Clock - Position
				self.skinSearchAndReplace.append(['position="1138,22"','position="1138,17"'])

				### Clock (wbrFS_r_site) - Position
				self.skinSearchAndReplace.append(['position="244,22"','position="244,17"'])

				### Menü, OK, Exit - Position
				self.skinSearchAndReplace.append(['position="1095,670"','position="1095,675"'])
				self.skinSearchAndReplace.append(['position="1145,670"','position="1145,675"'])
				self.skinSearchAndReplace.append(['position="1195,670"','position="1195,675"'])

				### ColorButtons - Position
				self.skinSearchAndReplace.append(['position="65,692"','position="65,697"'])
				self.skinSearchAndReplace.append(['position="315,692"','position="315,697"'])
				self.skinSearchAndReplace.append(['position="565,692"','position="565,697"'])
				self.skinSearchAndReplace.append(['position="815,692"','position="815,697"'])

				### ColorButtons (ChannelSelection, CoolTV, EMC) - Position
				self.skinSearchAndReplace.append(['position="42,692"','position="42,697"'])
				self.skinSearchAndReplace.append(['position="292,692"','position="292,697"'])
				self.skinSearchAndReplace.append(['position="542,692"','position="542,697"'])
				self.skinSearchAndReplace.append(['position="792,692"','position="792,697"'])

				### ColorButton-Text - Position
				self.skinSearchAndReplace.append(['position="70,665"','position="70,670"'])
				self.skinSearchAndReplace.append(['position="320,665"','position="320,670"'])
				self.skinSearchAndReplace.append(['position="570,665"','position="570,670"'])
				self.skinSearchAndReplace.append(['position="820,665"','position="820,670"'])
				self.skinSearchAndReplace.append(['position="70,639"','position="70,644"'])
				self.skinSearchAndReplace.append(['position="320,639"','position="320,644"'])
				self.skinSearchAndReplace.append(['position="570,639"','position="570,644"'])
				self.skinSearchAndReplace.append(['position="820,639"','position="820,644"'])

				### ColorButton-Text (ChannelSelection, CoolTV, EMC) - Position
				self.skinSearchAndReplace.append(['position="47,665"','position="47,670"'])
				self.skinSearchAndReplace.append(['position="297,665"','position="297,670"'])
				self.skinSearchAndReplace.append(['position="547,665"','position="547,670"'])
				self.skinSearchAndReplace.append(['position="797,665"','position="797,670"'])

				### MQB - Position
				self.skinSearchAndReplace.append(['<ePixmap alphatest="blend" pixmap="KravenVB/buttons/key_grey1.png" position="65,642" size="200,5" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap alphatest="blend" pixmap="KravenVB/buttons/key_grey1.png" position="315,642" size="200,5" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap alphatest="blend" pixmap="KravenVB/buttons/key_grey1.png" position="565,642" size="200,5" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap alphatest="blend" pixmap="KravenVB/buttons/key_grey1.png" position="815,642" size="200,5" />'," "])
				self.skinSearchAndReplace.append(['position="105,615"','position="105,641"'])
				self.skinSearchAndReplace.append(['position="355,615"','position="355,641"'])
				self.skinSearchAndReplace.append(['position="605,615"','position="605,641"'])
				self.skinSearchAndReplace.append(['position="855,615"','position="855,641"'])
				self.skinSearchAndReplace.append(['position="62,615"','position="62,641"'])
				self.skinSearchAndReplace.append(['position="312,615"','position="312,641"'])
				self.skinSearchAndReplace.append(['position="562,615"','position="562,641"'])
				self.skinSearchAndReplace.append(['position="812,615"','position="812,641"'])

				### MediaPlayer - Position
				self.skinSearchAndReplace.append(['position="1037,666"','position="1037,671"'])

				### EPGSelection - Position
				self.skinSearchAndReplace.append(['position="820,16" render="Picon"','position="820,11" render="Picon"'])

			else:
				### Menu
				menugradient = """<ePixmap pixmap="KravenVB/graphics/ibar.png" position="0,550" size="1280,400" alphatest="blend" zPosition="-9" />
	  <ePixmap pixmap="KravenVB/graphics/ibaro.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />"""
				self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menugradient])

		self.skinSearchAndReplace.append(['backgroundColor="KravenSIBbg2"', 'backgroundColor="KravenIBbg2"'])
		self.skinSearchAndReplace.append(['foregroundColor="KravenSIBFont1"', 'foregroundColor="KravenIBFont1"'])
		self.skinSearchAndReplace.append(['foregroundColor="KravenSIBFont2"', 'foregroundColor="KravenIBFont2"'])

		### MediaPortal box-style
		if config.plugins.KravenVB.MediaPortal.value == "mediaportal" and config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
			mpbox = """<ePixmap pixmap="KravenVB/graphics/ibar4.png" position="0,640" size="1280,80" zPosition="-9" alphatest="blend" />
	  <eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	  <ePixmap pixmap="KravenVB/graphics/ibaro.png" position="0,0" size="1280,59" zPosition="-9" alphatest="blend" />
	  <eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
			self.skinSearchAndReplace.append(['<!-- MediaPortal ibarcolor */-->', mpbox])
		if config.plugins.KravenVB.MediaPortal.value == "mediaportal" and config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.InfobarBoxColor.value == "texture":
			mpbox1 = """<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,640" size="1280,80" zPosition="-9" alphatest="blend" />
	  <eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	  <ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,0" size="1280,59" zPosition="-9" alphatest="blend" />
	  <eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
			self.skinSearchAndReplace.append(['<!-- MediaPortal ibarcolor */-->', mpbox1])
		if config.plugins.KravenVB.MediaPortal.value == "mediaportal" and config.plugins.KravenVB.IBColor.value == "all-screens" and not config.plugins.KravenVB.InfobarBoxColor.value in ("gradient","texture"):
			mpbox2 = """<eLabel position="0,640" size="1280,80" backgroundColor="KravenIBbg" zPosition="-9" />
	  <eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	  <eLabel position="0,0" size="1280,59" backgroundColor="KravenIBbg" zPosition="-9" />
	  <eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
			self.skinSearchAndReplace.append(['<!-- MediaPortal ibarcolor */-->', mpbox2])

		### Clock Analog Style
		self.analogstylecolor = config.plugins.KravenVB.AnalogStyle.value
		self.analog = ("analog_" + self.analogstylecolor + ".png")
		self.skinSearchAndReplace.append(["analog.png", self.analog])

		### Header
		if config.usage.movielist_show_picon.value == True:
			self.skinSearchAndReplace.append(['<parameter name="MovieListMinimalVTITitle" value="27,0,620,27" />', '<parameter name="MovieListMinimalVTITitle" value="27,0,535,27" />'])
		if config.plugins.KravenVB.EPGListSize.value == "big":
			self.skinSearchAndReplace.append(['<parameter name="EPGlistFont1" value="Regular;22" />', '<parameter name="EPGlistFont1" value="Regular;26" />'])
		self.appendSkinFile(self.daten + "header_begin.xml")
		if not config.plugins.KravenVB.SelectionBorder.value == "none":
			self.appendSkinFile(self.daten + "header_middle.xml")
		self.appendSkinFile(self.daten + "header_end.xml")

		### Volume
		self.appendSkinFile(self.daten + config.plugins.KravenVB.Volume.value + ".xml")

		### ChannelSelection - VTi
		if self.gete2distroversion() == "VTi":
			if config.plugins.KravenVB.alternativeChannellist.value == "none":
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + ".xml")
				if self.actChannelselectionstyle in ("channelselection-style-minitv33","channelselection-style-nobile-minitv33","channelselection-style-minitv2","channelselection-style-minitv22"):
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = True
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = True
					config.usage.use_extended_pig_channelselection.save()
					config.usage.zap_pip.value = False
					config.usage.zap_pip.save()
					if config.plugins.KravenVB.ChannelSelectionMode.value == "zap":
						config.usage.servicelist_preview_mode.value = False
						config.usage.servicelist_preview_mode.save()
					else:
						config.usage.servicelist_preview_mode.value = True
						config.usage.servicelist_preview_mode.save()
				elif self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv4","channelselection-style-nobile-minitv"):
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = False
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = False
					config.usage.use_extended_pig_channelselection.save()
					if config.plugins.KravenVB.ChannelSelectionMode.value == "zap":
						config.usage.servicelist_preview_mode.value = False
						config.usage.servicelist_preview_mode.save()
					else:
						config.usage.servicelist_preview_mode.value = True
						config.usage.servicelist_preview_mode.save()
				elif self.actChannelselectionstyle in ("channelselection-style-minitv3","channelselection-style-nobile-minitv3"):
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = False
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = False
					config.usage.use_extended_pig_channelselection.save()
					config.usage.servicelist_preview_mode.value = False
					config.usage.servicelist_preview_mode.save()
				else:
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = False
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = False
					config.usage.use_extended_pig_channelselection.save()
				config.usage.servicelist_alternative_mode.value = False
				config.usage.servicelist_alternative_mode.save()
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ChannelSelectionHorStyle.value + ".xml")
				config.usage.servicelist_alternative_mode.value = True
				config.usage.servicelist_alternative_mode.save()
			if config.plugins.KravenVB.ChannellistPicon.value == "on":
				config.usage.servicelist_show_picon.value = "1"
				config.usage.servicelist_show_picon.save()
			else:
				config.usage.servicelist_show_picon.value = False
				config.usage.servicelist_show_picon.save()
		
		### ChannelSelection - openatv
		elif self.gete2distroversion() == "openatv":
			if self.actChannelselectionstyle in ("channelselection-style-nopicon","channelselection-style-xpicon","channelselection-style-zpicon","channelselection-style-zzpicon","channelselection-style-zzzpicon","channelselection-style-minitv3","channelselection-style-nobile-minitv3") or config.plugins.KravenVB.ChannelSelectionMode.value == "zap":
				config.usage.servicelistpreview_mode.value = False
			else:
				config.usage.servicelistpreview_mode.value = True
			config.usage.servicelistpreview_mode.save()
			if self.actChannelselectionstyle in ("channelselection-style-minitv2","channelselection-style-minitv22"): #DualTV
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + "-openatv.xml")
				config.plugins.KravenVB.PigStyle.value = "DualTV"
				config.plugins.KravenVB.PigStyle.save()
			elif self.actChannelselectionstyle in ("channelselection-style-minitv33","channelselection-style-nobile-minitv33"): #ExtPreview
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + "-openatv.xml")
				config.plugins.KravenVB.PigStyle.value = "ExtPreview"
				config.plugins.KravenVB.PigStyle.save()
			elif self.actChannelselectionstyle in ("channelselection-style-minitv3","channelselection-style-nobile-minitv3"): #Preview
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + "-openatv.xml")
				config.plugins.KravenVB.PigStyle.value = "Preview"
				config.plugins.KravenVB.PigStyle.save()
			else:
				self.skinSearchAndReplace.append(['render="KravenVBPig3"', 'render="Pig"'])
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + ".xml")

		### Infobox
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			if self.gete2distroversion() == "VTi":
				if config.plugins.KravenVB.Infobox.value == "cpu":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="  L:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBLayoutInfo">LoadAvg'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBServiceName2">OrbitalPos', 'convert  type="KravenVBCpuUsage">$0'])
				elif config.plugins.KravenVB.Infobox.value == "temp":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="U:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBTempFanInfo">FanInfo'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBServiceName2">OrbitalPos', 'convert  type="KravenVBTempFanInfo">TempInfo'])
			elif self.gete2distroversion() == "openatv":
				if config.plugins.KravenVB.Infobox2.value == "cpu":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="  L:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBLayoutInfo">LoadAvg'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBServiceName2">OrbitalPos', 'convert  type="KravenVBCpuUsage">$0'])
				elif config.plugins.KravenVB.Infobox2.value == "temp":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="U:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenIcon" />-->', 'foregroundColor="KravenIcon" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBTempFanInfo">FanInfo'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBServiceName2">OrbitalPos', 'convert  type="KravenVBTempFanInfo">TempInfo'])
				elif config.plugins.KravenVB.Infobox2.value == "db":
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert  type="KravenVBFrontendInfo">SNRdB'])

		### Record State
		try:
			f=open("/proc/stb/info/vumodel","r")
			vumodel=f.read().strip()
			f.close()
		except IOError:
			pass
		if vumodel.lower() == "ultimo":
			if not config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2","infobar-style-zz3"):
				if config.plugins.KravenVB.record4.value == "record-blink":
					self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
				else:
					self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
		else:
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				if config.plugins.KravenVB.record2.value == "record-blink+tuner-shine":
					self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
					self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
					self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
					self.skinSearchAndReplace.append(['>tunerblink</convert>', ' />'])
					self.skinSearchAndReplace.append(['source="session.FrontendInfo" zPosition="3"', 'source="session.FrontendInfo" zPosition="5"'])
				elif config.plugins.KravenVB.record2.value == "record-shine+tuner-blink":
					self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
					self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
					self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
					self.skinSearchAndReplace.append(['>tunerblink</convert>', '>Blink</convert>'])
				elif config.plugins.KravenVB.record2.value == "record+tuner-blink":
					self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
					self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
					self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
					self.skinSearchAndReplace.append(['>tunerblink</convert>', '>Blink</convert>'])
				elif config.plugins.KravenVB.record2.value == "record+tuner-shine":
					self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
					self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
					self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
					self.skinSearchAndReplace.append(['>tunerblink</convert>', ' />'])
					self.skinSearchAndReplace.append(['source="session.FrontendInfo" zPosition="3"', 'source="session.FrontendInfo" zPosition="5"'])
				elif config.plugins.KravenVB.record2.value == "record-blink+no-record-tuner":
					self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
				else:
					self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				if config.plugins.KravenVB.record.value == "record-blink":
					self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
				else:
					self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
					if config.plugins.KravenVB.record2.value == "record-blink+tuner-shine":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', ' />'])
						self.skinSearchAndReplace.append(['source="session.FrontendInfo" zPosition="3"', 'source="session.FrontendInfo" zPosition="5"'])
					elif config.plugins.KravenVB.record2.value == "record-shine+tuner-blink":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', '>Blink</convert>'])
					elif config.plugins.KravenVB.record2.value == "record+tuner-blink":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', '>Blink</convert>'])
					elif config.plugins.KravenVB.record2.value == "record+tuner-shine":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', ' />'])
						self.skinSearchAndReplace.append(['source="session.FrontendInfo" zPosition="3"', 'source="session.FrontendInfo" zPosition="5"'])
					elif config.plugins.KravenVB.record2.value == "record-blink+no-record-tuner":
						self.skinSearchAndReplace.append(['>recordblink</convert>', '>Blink</convert>'])
					else:
						self.skinSearchAndReplace.append(['>recordblink</convert>', ' />'])
				else:
					if config.plugins.KravenVB.record3.value == "tuner-blink":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', '>Blink</convert>'])
					elif config.plugins.KravenVB.record3.value == "tuner-shine":
						self.skinSearchAndReplace.append(['<!--  <widget', '<widget'])
						self.skinSearchAndReplace.append(['</widget>  -->', '</widget>'])
						self.skinSearchAndReplace.append(['>tunerblink</convert>', ' />'])
						self.skinSearchAndReplace.append(['source="session.FrontendInfo" zPosition="3"', 'source="session.FrontendInfo" zPosition="5"'])

		### Infobar_begin
		self.appendSkinFile(self.daten + "infobar-begin.xml")

		### Infobar typewriter effect
		if config.plugins.KravenVB.TypeWriter.value == "runningtext":
			self.skinSearchAndReplace.append(['render="KravenVBEmptyEpg"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',' + config.plugins.KravenVB.RunningTextSpeed.value + ',wrap=0,always=0,repeat=2,oneshot=1"'])

		### Infobar_main
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			if config.plugins.KravenVB.tuner2.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main2.xml")
			elif config.plugins.KravenVB.tuner2.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main4.xml")
			elif config.plugins.KravenVB.tuner2.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main8.xml")
			elif config.plugins.KravenVB.tuner2.value == "10-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main10.xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			if config.plugins.KravenVB.tuner2.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main2.xml")
			elif config.plugins.KravenVB.tuner2.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main4.xml")
			elif config.plugins.KravenVB.tuner2.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main8.xml")
			elif config.plugins.KravenVB.tuner2.value == "10-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main10.xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main8.xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main8.xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main8.xml")
		else:
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarStyle.value + "_main.xml")

		### Infobar_top
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
			elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")
			elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top3":
				self.appendSkinFile(self.daten + "infobar-x2-z1_top3.xml")

		### Channelname
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="42,500"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,450"', '"KravenName" position="42,450"'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="20,500"'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="20,474"'])
			self.skinSearchAndReplace.append(['"KravenName" position="20,450"', '"KravenName" position="20,414"'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
			self.skinSearchAndReplace.append(['"KravenName" position="20,510" size="1240,60"', '"KravenName" position="435,534" size="565,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			self.skinSearchAndReplace.append(['"KravenName" position="20,510" size="1240,60"', '"KravenName" position="446,474" size="754,50"'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")

		### clock-weather (icon size)
		if not config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" and self.actClockstyle == "clock-weather":
			if config.plugins.KravenVB.ClockIconSize.value == "size-128":
				self.skinSearchAndReplace.append(['position="1066,598" size="96,96"','position="1050,582" size="128,128"'])
				self.skinSearchAndReplace.append(['position="1066,608" size="96,96"','position="1050,592" size="128,128"'])
				self.skinSearchAndReplace.append(['position="1076,598" size="96,96"','position="1060,582" size="128,128"'])

		### clock-style_ib
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather2.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
				self.appendSkinFile(self.daten + "clock-classic-big2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-analog":
				self.appendSkinFile(self.daten + "clock-analog2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather2.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
				self.appendSkinFile(self.daten + "clock-classic-big3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather3.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")

		### infobar - ecm-info
		if config.plugins.KravenVB.ECMVisible.value in ("ib","ib+sib"):

			if config.plugins.KravenVB.FTA.value == "none":
				self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if config.plugins.KravenVB.tuner2.value == "8-tuner":
					self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="350,22"'])
				elif config.plugins.KravenVB.tuner2.value == "10-tuner":
					self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="495,22"'])
				self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				self.appendSkinFile(self.daten + "infobar-ecminfo-nopicon.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

		### system-info
		if config.plugins.KravenVB.IBStyle.value == "box":
			if config.plugins.KravenVB.SystemInfo.value == "systeminfo-small":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-small-bg"/>','<constant-widget name="systeminfo-small-bg-box2"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-small-bg"/>','<constant-widget name="systeminfo-small-bg-texture"/>'])
				self.appendSkinFile(self.daten + "systeminfo-small2.xml")
			elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-big":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-big-bg"/>','<constant-widget name="systeminfo-big-bg-box2"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-big-bg"/>','<constant-widget name="systeminfo-big-bg-texture"/>'])
				self.appendSkinFile(self.daten + "systeminfo-big2.xml")
			elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-bigsat-bg"/>','<constant-widget name="systeminfo-bigsat-bg-box2"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<constant-widget name="systeminfo-bigsat-bg"/>','<constant-widget name="systeminfo-bigsat-bg-texture"/>'])
				self.appendSkinFile(self.daten + "systeminfo-bigsat2.xml")
		else:
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SystemInfo.value + ".xml")

		### weather-style
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle3.value
			else:
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle2.value
		if self.actWeatherstyle != "netatmobar":
			self.appendSkinFile(self.daten + self.actWeatherstyle + ".xml")
		if self.actWeatherstyle == "none" and self.actClockstyle != "clock-android" and self.actClockstyle != "clock-weather" and config.plugins.KravenVB.SIB.value != "sib6" and config.plugins.KravenVB.SIB.value != "sib7" and config.plugins.KravenVB.PlayerClock.value != "player-android" and config.plugins.KravenVB.PlayerClock.value != "player-weather":
			config.plugins.KravenVB.refreshInterval.value = "0"
			config.plugins.KravenVB.refreshInterval.save()
		elif config.plugins.KravenVB.refreshInterval.value == "0":
			config.plugins.KravenVB.refreshInterval.value = config.plugins.KravenVB.refreshInterval.default
			config.plugins.KravenVB.refreshInterval.save()

		### Infobar_end - SIB_begin
		self.appendSkinFile(self.daten + "infobar-style_middle.xml")

		### clock-style - SIB
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather2.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
				self.appendSkinFile(self.daten + "clock-classic-big2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-analog":
				self.appendSkinFile(self.daten + "clock-analog2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip2.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather2.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
				self.appendSkinFile(self.daten + "clock-classic3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
				self.appendSkinFile(self.daten + "clock-classic-big3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
				self.appendSkinFile(self.daten + "clock-color3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
				self.appendSkinFile(self.daten + "clock-flip3.xml")
			elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
				self.appendSkinFile(self.daten + "clock-weather3.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")

		### secondinfobar - ecm-info
		if config.plugins.KravenVB.ECMVisible.value in ("sib","ib+sib"):
			if config.plugins.KravenVB.FTA.value == "none":
				self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
				self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if config.plugins.KravenVB.tuner2.value == "8-tuner":
					self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="350,22"'])
				elif config.plugins.KravenVB.tuner2.value == "10-tuner":
					self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="495,22"'])
				self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				self.appendSkinFile(self.daten + "infobar-ecminfo-nopicon.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

		### SIB_main + SIB-Fontsize
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			if config.plugins.KravenVB.tuner2.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main2.xml")
			elif config.plugins.KravenVB.tuner2.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main4.xml")
			elif config.plugins.KravenVB.tuner2.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main8.xml")
			elif config.plugins.KravenVB.tuner2.value == "10-tuner":
				self.appendSkinFile(self.daten + "infobar-style-nopicon_main10.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			if config.plugins.KravenVB.tuner2.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main2.xml")
			elif config.plugins.KravenVB.tuner2.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main4.xml")
			elif config.plugins.KravenVB.tuner2.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main8.xml")
			elif config.plugins.KravenVB.tuner2.value == "10-tuner":
				self.appendSkinFile(self.daten + "infobar-style-x1_main10.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
			self.appendSkinFile(self.daten + "infobar-style-x2_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
			self.appendSkinFile(self.daten + "infobar-style-x3_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			self.appendSkinFile(self.daten + "infobar-style-z1_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
			self.appendSkinFile(self.daten + "infobar-style-z2_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1199,189">', 'font="Regular2; 22" size="1199,162">']) # sib1-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,297">', 'font="Regular2; 22" size="1200,270">']) # sib4+sib6-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="700,297">', 'font="Regular2; 22" size="700,270">']) # sib5+sib7-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="470,297">', 'font="Regular2; 22" size="470,270">']) # sib5+sib7-small
			else:
				self.skinSearchAndReplace.append(['font="Regular2; 24" size="1199,186">', 'font="Regular2; 24" size="1199,155">']) # sib1
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,297">', 'font="Regular2; 26" size="1200,264">']) # sib4+sib6
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="700,297">', 'font="Regular2; 26" size="700,264">']) # sib5+sib7
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="470,297">', 'font="Regular2; 26" size="470,264">']) # sib5+sib7
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main8.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1199,189">', 'font="Regular2; 22" size="1199,162">']) # sib1-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,297">', 'font="Regular2; 22" size="1200,270">']) # sib4+sib6-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="700,297">', 'font="Regular2; 22" size="700,270">']) # sib5+sib7-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="470,297">', 'font="Regular2; 22" size="470,270">']) # sib5+sib7-small
			else:
				self.skinSearchAndReplace.append(['font="Regular2; 24" size="1199,186">', 'font="Regular2; 24" size="1199,155">']) # sib1
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,297">', 'font="Regular2; 26" size="1200,264">']) # sib4+sib6
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="700,297">', 'font="Regular2; 26" size="700,264">']) # sib5+sib7
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="470,297">', 'font="Regular2; 26" size="470,264">']) # sib5+sib7
			self.appendSkinFile(self.daten + "infobar-style-zz2_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1199,189">', 'font="Regular2; 22" size="1199,162">']) # sib1-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,297">', 'font="Regular2; 22" size="1200,270">']) # sib4+sib6-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="700,297">', 'font="Regular2; 22" size="700,270">']) # sib5+sib7-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="470,297">', 'font="Regular2; 22" size="470,270">']) # sib5+sib7-small
			else:
				self.skinSearchAndReplace.append(['font="Regular2; 24" size="1199,186">', 'font="Regular2; 24" size="1199,155">']) # sib1
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,297">', 'font="Regular2; 26" size="1200,264">']) # sib4+sib6
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="700,297">', 'font="Regular2; 26" size="700,264">']) # sib5+sib7
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="470,297">', 'font="Regular2; 26" size="470,264">']) # sib5+sib7
			self.appendSkinFile(self.daten + "infobar-style-zz3_main.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1199,189">', 'font="Regular2; 22" size="1199,162">']) # sib1-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,297">', 'font="Regular2; 22" size="1200,270">']) # sib4+sib6-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="700,297">', 'font="Regular2; 22" size="700,270">']) # sib5+sib7-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="470,297">', 'font="Regular2; 22" size="470,270">']) # sib5+sib7-small
			else:
				self.skinSearchAndReplace.append(['font="Regular2; 24" size="1199,186">', 'font="Regular2; 24" size="1199,155">']) # sib1
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,297">', 'font="Regular2; 26" size="1200,264">']) # sib4+sib6
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="700,297">', 'font="Regular2; 26" size="700,264">']) # sib5+sib7
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="470,297">', 'font="Regular2; 26" size="470,264">']) # sib5+sib7
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main8.xml")

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1199,189">', 'font="Regular2; 22" size="1199,135">']) # sib1-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="570,378">', 'font="Regular2; 22" size="570,324">']) # sib2-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,378">', 'font="Regular2; 22" size="1200,324">']) # sib3-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="1200,297">', 'font="Regular2; 22" size="1200,216">']) # sib4+sib6-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="700,297">', 'font="Regular2; 22" size="700,216">']) # sib5+sib7-small
				self.skinSearchAndReplace.append(['font="Regular2; 22" size="470,297">', 'font="Regular2; 22" size="470,216">']) # sib5+sib7-small
			else:
				self.skinSearchAndReplace.append(['font="Regular2; 24" size="1199,186">', 'font="Regular2; 24" size="1199,124">']) # sib1
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="570,396">', 'font="Regular2; 26" size="570,330">']) # sib2
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,396">', 'font="Regular2; 26" size="1200,330">']) # sib3
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="1200,297">', 'font="Regular2; 26" size="1200,231">']) # sib4+sib6
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="700,297">', 'font="Regular2; 26" size="700,231">']) # sib5+sib7
				self.skinSearchAndReplace.append(['font="Regular2; 26" size="470,297">', 'font="Regular2; 26" size="470,231">']) # sib5+sib7
			if config.plugins.KravenVB.tuner.value == "2-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main2.xml")
			elif config.plugins.KravenVB.tuner.value == "4-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main4.xml")
			elif config.plugins.KravenVB.tuner.value == "8-tuner":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main8.xml")

		if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB.value + "-small.xml")
		else:
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB.value + ".xml")
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/SecondInfoBar/plugin.py"):
			config.plugins.SecondInfoBar.HideNormalIB.value = True
			config.plugins.SecondInfoBar.HideNormalIB.save()

		### Main XML
		self.appendSkinFile(self.daten + "main.xml")

		if config.plugins.KravenVB.IBStyle.value == "grad":
			### Timeshift_begin
			self.appendSkinFile(self.daten + "timeshift-begin.xml")

			if self.actWeatherstyle in ("weather-big","weather-left"):
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.daten + "timeshift-begin-leftlow.xml")
				else:
					self.appendSkinFile(self.daten + "timeshift-begin-low.xml")
			elif self.actWeatherstyle == "weather-small":
				self.appendSkinFile(self.daten + "timeshift-begin-left.xml")
			else:
				self.appendSkinFile(self.daten + "timeshift-begin-high.xml")

			### Timeshift_Infobar_main
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				if config.plugins.KravenVB.tuner.value == "2-tuner":
					self.appendSkinFile(self.daten + "infobar-style-nopicon_main2.xml")
				elif config.plugins.KravenVB.tuner2.value == "4-tuner":
					self.appendSkinFile(self.daten + "infobar-style-nopicon_main4.xml")
				elif config.plugins.KravenVB.tuner2.value == "8-tuner":
					self.appendSkinFile(self.daten + "infobar-style-nopicon_main8.xml")
				elif config.plugins.KravenVB.tuner2.value == "10-tuner":
					self.appendSkinFile(self.daten + "infobar-style-nopicon_main10.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if config.plugins.KravenVB.tuner2.value == "2-tuner":
					self.appendSkinFile(self.daten + "infobar-style-x1_main2.xml")
				elif config.plugins.KravenVB.tuner2.value == "4-tuner":
					self.appendSkinFile(self.daten + "infobar-style-x1_main4.xml")
				elif config.plugins.KravenVB.tuner2.value == "8-tuner":
					self.appendSkinFile(self.daten + "infobar-style-x1_main8.xml")
				elif config.plugins.KravenVB.tuner2.value == "10-tuner":
					self.appendSkinFile(self.daten + "infobar-style-x1_main10.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
				if config.plugins.KravenVB.tuner.value == "2-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz1_main2.xml")
				elif config.plugins.KravenVB.tuner.value == "4-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz1_main4.xml")
				elif config.plugins.KravenVB.tuner.value == "8-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz1_main8.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				if config.plugins.KravenVB.tuner.value == "2-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz4_main2.xml")
				elif config.plugins.KravenVB.tuner.value == "4-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz4_main4.xml")
				elif config.plugins.KravenVB.tuner.value == "8-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zz4_main8.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				if config.plugins.KravenVB.tuner.value == "2-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zzz1_main2.xml")
				elif config.plugins.KravenVB.tuner.value == "4-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zzz1_main4.xml")
				elif config.plugins.KravenVB.tuner.value == "8-tuner":
					self.appendSkinFile(self.daten + "infobar-style-zzz1_main8.xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarStyle.value + "_main.xml")

			### Timeshift_Infobar_top
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
				elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")
				elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top3":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top3.xml")

			### Timeshift_Channelname
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="42,500"'])
				self.skinSearchAndReplace.append(['"KravenName" position="20,450"', '"KravenName" position="42,450"'])
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="20,500"'])
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4"):
				self.skinSearchAndReplace.append(['"KravenName" position="20,510"', '"KravenName" position="20,474"'])
				self.skinSearchAndReplace.append(['"KravenName" position="20,450"', '"KravenName" position="20,414"'])
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
				self.skinSearchAndReplace.append(['"KravenName" position="20,510" size="1240,60"', '"KravenName" position="435,534" size="565,50"'])
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.skinSearchAndReplace.append(['"KravenName" position="20,510" size="1240,60"', '"KravenName" position="446,474" size="754,50"'])
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")

			### Timeshift_clock-style_ib
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
					self.appendSkinFile(self.daten + "clock-classic3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
					self.appendSkinFile(self.daten + "clock-color3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
					self.appendSkinFile(self.daten + "clock-flip2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
					self.appendSkinFile(self.daten + "clock-weather2.xml")
				else:
					self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
				if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
					self.appendSkinFile(self.daten + "clock-classic2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
					self.appendSkinFile(self.daten + "clock-classic-big2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
					self.appendSkinFile(self.daten + "clock-color2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-analog":
					self.appendSkinFile(self.daten + "clock-analog2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
					self.appendSkinFile(self.daten + "clock-flip2.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
					self.appendSkinFile(self.daten + "clock-weather2.xml")
				else:
					self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
				if config.plugins.KravenVB.ClockStyle.value == "clock-classic":
					self.appendSkinFile(self.daten + "clock-classic3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-classic-big":
					self.appendSkinFile(self.daten + "clock-classic-big3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-color":
					self.appendSkinFile(self.daten + "clock-color3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-flip":
					self.appendSkinFile(self.daten + "clock-flip3.xml")
				elif config.plugins.KravenVB.ClockStyle.value == "clock-weather":
					self.appendSkinFile(self.daten + "clock-weather3.xml")
				else:
					self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")

			### timeshift - ecm-info
			if config.plugins.KravenVB.ECMVisible.value in ("ib","ib+sib"):
				if config.plugins.KravenVB.FTA.value == "none":
					self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

				if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

				if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
					if config.plugins.KravenVB.tuner2.value == "8-tuner":
						self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="350,22"'])
					elif config.plugins.KravenVB.tuner2.value == "10-tuner":
						self.skinSearchAndReplace.append(['position="273,693" size="403,22"', 'position="273,693" size="495,22"'])
					self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
					self.appendSkinFile(self.daten + "infobar-ecminfo-nopicon.xml")
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
					self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
					self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
				elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

			### Timeshift_system-info
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SystemInfo.value + ".xml")

			### Timeshift_weather-style
			if self.actWeatherstyle != "netatmobar":
				self.appendSkinFile(self.daten + self.actWeatherstyle + ".xml")

			### Timeshift_end
			self.appendSkinFile(self.daten + "timeshift-end.xml")

			### InfobarTunerState
			if self.actWeatherstyle in ("weather-big","weather-left","netatmobar"):
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.daten + "infobartunerstate-low.xml")
				else:
					self.appendSkinFile(self.daten + "infobartunerstate-mid.xml")
			else:
				self.appendSkinFile(self.daten + "infobartunerstate-high.xml")

		elif config.plugins.KravenVB.IBStyle.value == "box":
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append(['<constant-widget name="timeshift-bg"/>', '<constant-widget name="timeshift-bg-box2"/>'])
				self.skinSearchAndReplace.append(['<constant-widget name="ibts-bg"/>', '<constant-widget name="ibts-bg-box2"/>'])
				self.skinSearchAndReplace.append(['<constant-widget name="autoresolution-bg"/>', '<constant-widget name="autoresolution-bg-box2"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append(['<constant-widget name="timeshift-bg"/>', '<constant-widget name="timeshift-bg-texture"/>'])
				self.skinSearchAndReplace.append(['<constant-widget name="ibts-bg"/>', '<constant-widget name="ibts-bg-texture"/>'])
				self.skinSearchAndReplace.append(['<constant-widget name="autoresolution-bg"/>', '<constant-widget name="autoresolution-bg-texture"/>'])
			self.appendSkinFile(self.daten + "timeshift-ibts-ar.xml")

		### Players
		self.appendSkinFile(self.daten + "player-movie.xml")
		self.appendSkinFile(self.daten + config.plugins.KravenVB.PlayerClock.value + ".xml")
		self.appendSkinFile(self.daten + "screen_end.xml")
		self.appendSkinFile(self.daten + "player-emc.xml")
		self.appendSkinFile(self.daten + config.plugins.KravenVB.PlayerClock.value + ".xml")
		self.appendSkinFile(self.daten + "screen_end.xml")

		### PermanentClock
		if config.plugins.KravenVB.PermanentClock.value == "permanentclock-infobar-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="KravenIBbg" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append(['<constant-widget name="permanentclock-infobar-big"/>', '<constant-widget name="permanentclock-infobar-small"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-global-big":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="120,30"'])
			self.skinSearchAndReplace.append(['<constant-widget name="permanentclock-infobar-big"/>', '<constant-widget name="permanentclock-global-big"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-global-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append(['<constant-widget name="permanentclock-infobar-big"/>', '<constant-widget name="permanentclock-global-small"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-transparent-big":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="120,30"'])
			self.skinSearchAndReplace.append(['<constant-widget name="permanentclock-infobar-big"/>', '<constant-widget name="permanentclock-transparent-big"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-transparent-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append(['<constant-widget name="permanentclock-infobar-big"/>', '<constant-widget name="permanentclock-transparent-small"/>'])

		### Plugins
		self.appendSkinFile(self.daten + "plugins.xml")
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/PermanentTimeshift/plugin.py"):
			config.plugins.pts.showinfobar.value = False
			config.plugins.pts.showinfobar.save()

		### MSNWeatherPlugin XML
		if self.gete2distroversion() == "openatv":
			console1 = eConsoleAppContainer()
			if fileExists("/usr/lib/enigma2/python/Components/Converter/MSNWeather.pyo"):
				self.appendSkinFile(self.daten + "MSNWeatherPlugin.xml")
				if not fileExists("/usr/share/enigma2/KravenVB/msn_weather_icons/1.png"):
					console1.execute("wget -q http://coolskins.de/downloads/kraven/msn-icon.tar.gz -O /tmp/msn-icon.tar.gz; tar xf /tmp/msn-icon.tar.gz -C /usr/share/enigma2/KravenVB/")
			else:
				self.appendSkinFile(self.daten + "MSNWeatherPlugin2.xml")

		### NetatmoBar
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				if config.plugins.KravenVB.WeatherStyle3.value == "netatmobar":
					self.appendSkinFile(self.daten + "netatmobar.xml")

		### EMC (Event-Description) Font-Size
		if config.plugins.KravenVB.EMCStyle.value in ("emc-bigcover","emc-minitv"):
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcmbc22"/>', '<constant-widget name="emcmbc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value in ("emc-bigcover2","emc-minitv2"):
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcm2bc222"/>', '<constant-widget name="emcm2bc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-nocover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcnc22"/>', '<constant-widget name="emcnc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-nocover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcnc222"/>', '<constant-widget name="emcnc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-smallcover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcsc22"/>', '<constant-widget name="emcsc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-smallcover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcsc222"/>', '<constant-widget name="emcsc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-verybigcover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcvbc22"/>', '<constant-widget name="emcvbc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-verybigcover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="emcvbc222"/>', '<constant-widget name="emcvbc224"/>'])

		### EMC
		self.appendSkinFile(self.daten + config.plugins.KravenVB.EMCStyle.value + ".xml")

		### NumberZapExt
		self.appendSkinFile(self.daten + config.plugins.KravenVB.NumberZapExt.value + ".xml")
		if not config.plugins.KravenVB.NumberZapExt.value == "none":
			config.usage.numberzap_show_picon.value = True
			config.usage.numberzap_show_picon.save()
			config.usage.numberzap_show_servicename.value = True
			config.usage.numberzap_show_servicename.save()

		### PVRState
		if config.plugins.KravenVB.IBStyle.value == "box":
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<constant-widget name="pvrstate-bg"/>', '<constant-widget name="pvrstate-bg-box2"/>'])
				else:
					self.skinSearchAndReplace.append(['<constant-widget name="pvrstate2-bg"/>', '<constant-widget name="pvrstate2-bg-box2"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<constant-widget name="pvrstate-bg"/>', '<constant-widget name="pvrstate-bg-texture"/>'])
				else:
					self.skinSearchAndReplace.append(['<constant-widget name="pvrstate2-bg"/>', '<constant-widget name="pvrstate2-bg-texture"/>'])
			self.appendSkinFile(self.daten + config.plugins.KravenVB.PVRState.value + ".xml")

		### SplitScreen
		if self.gete2distroversion() == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SplitScreen.value + ".xml")

		### TimerEditScreen
		self.appendSkinFile(self.daten + config.plugins.KravenVB.TimerEditScreen.value + ".xml")

		### TimerListStyle
		if self.gete2distroversion() == "VTi":
			if config.plugins.KravenVB.TimerListStyle.value == "timerlist-standard":
				config.usage.timerlist_style.value = False
				config.usage.timerlist_style.save()
			elif config.plugins.KravenVB.TimerListStyle.value == "timerlist-1":
				config.usage.timerlist_style.value = "1"
				config.usage.timerlist_style.save()
			elif config.plugins.KravenVB.TimerListStyle.value == "timerlist-2":
				config.usage.timerlist_style.value = "2"
				config.usage.timerlist_style.save()
			elif config.plugins.KravenVB.TimerListStyle.value == "timerlist-3":
				config.usage.timerlist_style.value = "3"
				config.usage.timerlist_style.save()
			elif config.plugins.KravenVB.TimerListStyle.value == "timerlist-4":
				config.usage.timerlist_style.value = "4"
				config.usage.timerlist_style.save()
			elif config.plugins.KravenVB.TimerListStyle.value == "timerlist-5":
				config.usage.timerlist_style.value = "5"
				config.usage.timerlist_style.save()

		### EPGSelection
		if config.plugins.KravenVB.EPGListSize.value == "big":
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" itemHeight="30"', 'font="Regular;26" foregroundColor="KravenFont1" itemHeight="36"'])
		else:
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" itemHeight="30"', 'font="Regular;22" foregroundColor="KravenFont1" itemHeight="30"'])
		if config.plugins.KravenVB.EPGSelectionEPGSize.value == "big":
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,329" size="418,270"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,329" size="418,270"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,294" size="418,297"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,294" size="418,300"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,110" size="418,486"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,110" size="418,480"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,75" size="418,532"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,75" size="418,510"'])
		else:
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,329" size="418,270"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,329" size="418,270"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,294" size="418,297"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,294" size="418,297"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,110" size="418,486"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,110" size="418,486"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,75" size="418,532"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,75" size="418,532"'])
		self.appendSkinFile(self.daten + config.plugins.KravenVB.EPGSelection.value + ".xml")

		### CoolTVGuide
		self.appendSkinFile(self.daten + config.plugins.KravenVB.CoolTVGuide.value + ".xml")

		### GraphEPG (Event-Description) Font-Size
		if config.plugins.KravenVB.GMEDescriptionSize.value == "big":
			self.skinSearchAndReplace.append(['<constant-widget name="GE22"/>', '<constant-widget name="GE24"/>'])
			self.skinSearchAndReplace.append(['<constant-widget name="GEMTR22"/>', '<constant-widget name="GEMTR24"/>'])
			self.skinSearchAndReplace.append(['<constant-widget name="GEMTL22"/>', '<constant-widget name="GEMTL24"/>'])

		### GraphEPG
		if self.gete2distroversion() == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.GraphMultiEPG.value + ".xml")
		elif self.gete2distroversion() == "openatv":
			if config.plugins.KravenVB.GraphicalEPG.value == "text":
				config.epgselection.graph_type_mode.value = False
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = False
				config.epgselection.graph_pig.save()
			elif config.plugins.KravenVB.GraphicalEPG.value == "text-minitv":
				config.epgselection.graph_type_mode.value = False
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = "true"
				config.epgselection.graph_pig.save()
			elif config.plugins.KravenVB.GraphicalEPG.value == "graphical":
				config.epgselection.graph_type_mode.value = "graphics"
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = False
				config.epgselection.graph_pig.save()
			elif config.plugins.KravenVB.GraphicalEPG.value == "graphical-minitv":
				config.epgselection.graph_type_mode.value = "graphics"
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = "true"
				config.epgselection.graph_pig.save()

		### VerticalEPG
		if self.gete2distroversion() == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.VerticalEPG.value + ".xml")

		### MovieSelection (MovieList) Font-Colors
		if not fileExists("/usr/lib/enigma2/python/Plugins/Extensions/SerienFilm/plugin.py"):
			self.skinSearchAndReplace.append(['UnwatchedColor="unwatched"', 'UnwatchedColor="#' + config.plugins.KravenVB.UnwatchedColor.value + '"'])
			self.skinSearchAndReplace.append(['WatchingColor="watching"', 'WatchingColor="#' + config.plugins.KravenVB.WatchingColor.value + '"'])
			self.skinSearchAndReplace.append(['FinishedColor="finished"', 'FinishedColor="#' + config.plugins.KravenVB.FinishedColor.value + '"'])
		else:
			self.skinSearchAndReplace.append(['UnwatchedColor="unwatched" WatchingColor="watching" FinishedColor="finished"', ''])

		### MovieSelection (Event-Description) Font-Size
		if config.plugins.KravenVB.MovieSelection.value == "movieselection-no-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="msnc22"/>', '<constant-widget name="msnc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-small-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="mssc22"/>', '<constant-widget name="mssc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-big-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="msbc22"/>', '<constant-widget name="msbc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-minitv":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="msm22"/>', '<constant-widget name="msm24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-minitv-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append(['<constant-widget name="msmc22"/>', '<constant-widget name="msmc24"/>'])

		### MovieSelection
		self.appendSkinFile(self.daten + config.plugins.KravenVB.MovieSelection.value + ".xml")

		### SerienRecorder
		self.appendSkinFile(self.daten + config.plugins.KravenVB.SerienRecorder.value + ".xml")

		### MediaPortal
		console = eConsoleAppContainer()
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py"):
			if config.plugins.KravenVB.MediaPortal.value == "mediaportal":
				if config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					console.execute("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")

		### vti - atv
		if self.gete2distroversion() == "VTi":
			self.appendSkinFile(self.daten + "vti.xml")
		elif self.gete2distroversion() == "openatv":
			self.appendSkinFile(self.daten + "openatv.xml")

		### skin-user
		try:
			self.appendSkinFile(self.daten + "skin-user.xml")
		except:
			pass
		### skin-end
		self.appendSkinFile(self.daten + "skin-end.xml")

		xFile = open(self.dateiTMP, "w")
		for xx in self.skin_lines:
			xFile.writelines(xx)
		xFile.close()

		move(self.dateiTMP, self.datei)

		### Menu icons download - we do it here to give it some time
		if config.plugins.KravenVB.Logo.value in ("metrix-icons","minitv-metrix-icons"):
			self.installIcons(config.plugins.KravenVB.MenuIcons.value)

		### Get weather data to make sure the helper config values are not empty
		self.get_weather_data()

		# Make ibar graphics
		if config.plugins.KravenVB.BackgroundColor.value == "gradient":
			self.makeBGGradientpng()
		elif config.plugins.KravenVB.BackgroundColor.value == "texture":
			self.makeBGTexturepng()

		if config.plugins.KravenVB.IBStyle.value == "grad":
			if config.plugins.KravenVB.InfobarGradientColor.value == "texture":
				self.makeIbarTextureGradientpng(config.plugins.KravenVB.InfobarTexture.value,config.plugins.KravenVB.InfobarColorTrans.value) # ibars
				self.makeRectTexturepng(config.plugins.KravenVB.InfobarTexture.value, config.plugins.KravenVB.InfobarColorTrans.value, 905, 170, "shift") # timeshift bar
				self.makeRectTexturepng(config.plugins.KravenVB.InfobarTexture.value, config.plugins.KravenVB.InfobarColorTrans.value, 400, 200, "wsmall") # weather small
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-small":
					self.makeRectTexturepng(config.plugins.KravenVB.InfobarTexture.value, config.plugins.KravenVB.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
				elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-big":
					self.makeRectTexturepng(config.plugins.KravenVB.InfobarTexture.value, config.plugins.KravenVB.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
				else:
					self.makeRectTexturepng(config.plugins.KravenVB.InfobarTexture.value, config.plugins.KravenVB.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat
			else:
				self.makeIbarColorGradientpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value) # ibars
				self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 905, 170, "shift") # timeshift bar
				self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 200, "wsmall") # weather small
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-small":
					self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
				elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-big":
					self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
				else:
					self.makeRectColorpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat
		elif config.plugins.KravenVB.IBStyle.value == "box":
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.makeIBGradientpng()
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.makeIBTexturepng()

		if config.plugins.KravenVB.SerienRecorder.value == "serienrecorder":
			self.makeSRpng(self.skincolorbackgroundcolor) # serienrecorder
			
		# Thats it
		self.restart()

	def restart(self):
		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		"""
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def restartGUI(self, answer):
		if answer is True:
			config.skin.primary_skin.setValue("KravenVB/skin.xml")
			config.skin.save()
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		askExit = self.session.openWithCallback(self.doExit,MessageBox,_("Do you really want to exit without saving?"), MessageBox.TYPE_YESNO)
		askExit.setTitle(_("Exit"))

	def doExit(self,answer):
		if answer is True:
			for x in self["config"].list:
				if len(x) > 1:
						x[1].cancel()
				else:
						pass
			self.close()
		else:
			self.mylist()

	def gete2distroversion(self):
		try:
			from boxbranding import getImageDistro
			if getImageDistro() == "openatv":
				return "openatv"
			elif getImageDistro() == "VTi":
				return "VTi"
		except ImportError:
			return "VTi"

	def reset(self):
		askReset = self.session.openWithCallback(self.doReset,MessageBox,_("Do you really want to reset all values to the selected default profile?"), MessageBox.TYPE_YESNO)
		askReset.setTitle(_("Reset profile"))

	def doReset(self,answer):
		if answer is True:
			if config.plugins.KravenVB.defaultProfile.value == "default":
				for name in config.plugins.KravenVB.dict():
					if not name in ("customProfile","DebugNames"):
						item=(getattr(config.plugins.KravenVB,name))
						item.value=item.default
			else:
				self.loadProfile(loadDefault=True)
		self.mylist()

	def showColor(self,actcolor):
		c = self["Canvas"]
		c.fill(0,0,368,207,actcolor)
		c.flush()

	def showGradient(self,color1,color2):
		width=368
		height=207
		color1=color1[-6:]
		r1=int(color1[0:2],16)
		g1=int(color1[2:4],16)
		b1=int(color1[4:6],16)
		color2=color2[-6:]
		r2=int(color2[0:2],16)
		g2=int(color2[2:4],16)
		b2=int(color2[4:6],16)
		c = self["Canvas"]
		if color1!=color2:
			for pos in range(0,height):
				p=pos/float(height)
				r=r2*p+r1*(1-p)
				g=g2*p+g1*(1-p)
				b=b2*p+b1*(1-p)
				c.fill(0,pos,width,1,self.RGB(int(r),int(g),int(b)))
		else:
			c.fill(0,0,width,height,self.RGB(int(r1),int(g1),int(b1)))
		c.flush()

	def showText(self,fontsize,text):
		from enigma import gFont,RT_HALIGN_CENTER,RT_VALIGN_CENTER
		c = self["Canvas"]
		c.fill(0,0,368,207,self.RGB(0,0,0))
		c.writeText(0,0,368,207,self.RGB(255,255,255),self.RGB(0,0,0),gFont("Regular",fontsize),text,RT_HALIGN_CENTER+RT_VALIGN_CENTER)
		c.flush()

	def loadProfile(self,loadDefault=False):
		if loadDefault:
			profile=config.plugins.KravenVB.defaultProfile.value
			fname=self.profiles+"kraven_default_"+profile
		else:
			profile=config.plugins.KravenVB.customProfile.value
			fname=self.profiles+"kraven_profile_"+profile
		if profile and fileExists(fname):
			print ("KravenPlugin: Load profile "+fname)
			pFile=open(fname,"r")
			for line in pFile:
				try:
					line=line.split("|")
					name=line[0]
					value=line[1]
					type=line[2].strip('\n')
					if not (name in ("customProfile","DebugNames","weather_owm_latlon","weather_accu_latlon","weather_realtek_latlon","weather_accu_id","weather_foundcity","weather_gmcode","weather_cityname","weather_language","weather_server") or (loadDefault and name == "defaultProfile")):
						if type == "<type 'int'>":
							getattr(config.plugins.KravenVB,name).value=int(value)
						elif type == "<type 'hex'>":
							getattr(config.plugins.KravenVB,name).value=hex(value)
						elif type == "<type 'list'>":
							getattr(config.plugins.KravenVB,name).value=eval(value)
						else:
							getattr(config.plugins.KravenVB,name).value=str(value)
				except:
					pass
			pFile.close()
			# fix possible inconsistencies between boxes
			if self.gete2distroversion() == "VTi":
				if SystemInfo.get("NumVideoDecoders",1)>1:
					if config.plugins.KravenVB.ChannelSelectionStyle.value!=config.plugins.KravenVB.ChannelSelectionStyle.default:
						config.plugins.KravenVB.ChannelSelectionStyle2.value=config.plugins.KravenVB.ChannelSelectionStyle.value
						config.plugins.KravenVB.ChannelSelectionStyle.value=config.plugins.KravenVB.ChannelSelectionStyle.default
				else:
					if config.plugins.KravenVB.ChannelSelectionStyle2.value!=config.plugins.KravenVB.ChannelSelectionStyle2.default:
						if config.plugins.KravenVB.ChannelSelectionStyle2.value in ("channelselection-style-minitv33","channelselection-style-minitv2","channelselection-style-minitv22"):
							config.plugins.KravenVB.ChannelSelectionStyle.value="channelselection-style-minitv3"
						elif config.plugins.KravenVB.ChannelSelectionStyle2.value == "channelselection-style-nobile-minitv33":
							config.plugins.KravenVB.ChannelSelectionStyle.value="channelselection-style-nobile-minitv3"
						else:
							config.plugins.KravenVB.ChannelSelectionStyle.value=config.plugins.KravenVB.ChannelSelectionStyle2.value
						config.plugins.KravenVB.ChannelSelectionStyle2.value=config.plugins.KravenVB.ChannelSelectionStyle2.default
				if not fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py") and config.plugins.KravenVB.WeatherStyle3.value=="netatmobar":
					config.plugins.KravenVB.WeatherStyle3.value=config.plugins.KravenVB.WeatherStyle3.default
		elif not loadDefault:
			print ("KravenPlugin: Create profile "+fname)
			self.saveProfile(msg=False)

	def saveProfile(self,msg=True):
		profile=config.plugins.KravenVB.customProfile.value
		if profile:
			try:
				fname=self.profiles+"kraven_profile_"+profile
				print ("KravenPlugin: Save profile "+fname)
				pFile=open(fname,"w")
				for name in config.plugins.KravenVB.dict():
					if not name in ("customProfile","DebugNames","weather_owm_latlon","weather_accu_latlon","weather_realtek_latlon","weather_accu_id","weather_foundcity","weather_gmcode","weather_cityname","weather_language","weather_server"):
						value=getattr(config.plugins.KravenVB,name).value
						pFile.writelines(name+"|"+str(value)+"|"+str(type(value))+"\n")
				pFile.close()
				if msg:
					self.session.open(MessageBox,_("Profile ")+str(profile)+_(" saved successfully."), MessageBox.TYPE_INFO, timeout=5)
			except:
				self.session.open(MessageBox,_("Profile ")+str(profile)+_(" could not be saved!"), MessageBox.TYPE_INFO, timeout=15)

	def installIcons(self,author):

		pathname="http://coolskins.de/downloads/kraven/"
		instname="/usr/share/enigma2/Kraven-menu-icons/iconpackname"
		versname="Kraven-Menu-Icons-by-"+author+".packname"
		
		# Read iconpack version on box
		packinstalled = "not installed"
		if fileExists(instname):
			pFile=open(instname,"r")
			for line in pFile:
				packinstalled=line.strip('\n')
			pFile.close()
		print ("KravenPlugin: Iconpack on box is "+packinstalled)
		
		# Read iconpack version on server
		packonserver = "unknown"
		fullversname=pathname+versname
		sub=subprocess.Popen("wget -q "+fullversname+" -O /tmp/"+versname,shell=True)
		sub.wait()
		if fileExists("/tmp/"+versname):
			pFile=open("/tmp/"+versname,"r")
			for line in pFile:
				packonserver=line.strip('\n')
			pFile.close()
			popen("rm /tmp/"+versname)
			print ("KravenPlugin: Iconpack on server is "+packonserver)

			# Download an install icon pack, if needed
			if packinstalled != packonserver:
				packname=packonserver
				fullpackname=pathname+packname
				sub=subprocess.Popen("rm -rf /usr/share/enigma2/Kraven-menu-icons/*.*; rm -rf /usr/share/enigma2/Kraven-menu-icons; wget -q "+fullpackname+" -O /tmp/"+packname+"; tar xf /tmp/"+packname+" -C /usr/share/enigma2/",shell=True)
				sub.wait()
				popen("rm /tmp/"+packname)
				print ("KravenPlugin: Installed iconpack "+fullpackname)
			else:
				print ("KravenPlugin: No need to install other iconpack")

	def makeTexturePreview(self,style):
		width=368
		height=207
		inpath="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
		outpath="/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/"
		if fileExists(usrpath+style+".png"):
			bg=Image.open(usrpath+style+".png")
		elif fileExists(usrpath+style+".jpg"):
			bg=Image.open(usrpath+style+".jpg")
		elif fileExists(inpath+style+".png"):
			bg=Image.open(inpath+style+".png")
		elif fileExists(inpath+style+".jpg"):
			bg=Image.open(inpath+style+".jpg")
		bg_w,bg_h=bg.size
		image=Image.new("RGBA",(width,height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,height,bg_h):
				image.paste(bg,(i,j))
		image.save(outpath+"preview.jpg")
		
	def makeAlternatePreview(self,style,color):
		width=368
		height=207
		inpath="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
		outpath="/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/"
		if fileExists(usrpath+style+".png"):
			bg=Image.open(usrpath+style+".png")
		elif fileExists(usrpath+style+".jpg"):
			bg=Image.open(usrpath+style+".jpg")
		elif fileExists(inpath+style+".png"):
			bg=Image.open(inpath+style+".png")
		elif fileExists(inpath+style+".jpg"):
			bg=Image.open(inpath+style+".jpg")
		bg_w,bg_h=bg.size
		image=Image.new("RGBA",(width,height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,height,bg_h):
				image.paste(bg,(i,j))
		color=color[-6:]
		r=int(color[0:2],16)
		g=int(color[2:4],16)
		b=int(color[4:6],16)
		image.paste((int(r),int(g),int(b),255),(0,int(height/2),width,height))
		image.save(outpath+"preview.jpg")
		
	def makePreview(self):
		width=368
		height=208
		lineheight=3
		boxbarheight=40
		gradbarheight=80
		
		inpath="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
			
		# background
		if config.plugins.KravenVB.BackgroundColor.value == "texture":
			style=config.plugins.KravenVB.BackgroundTexture.value
			if fileExists(usrpath+style+".png"):
				bg=Image.open(usrpath+style+".png")
			elif fileExists(usrpath+style+".jpg"):
				bg=Image.open(usrpath+style+".jpg")
			elif fileExists(inpath+style+".png"):
				bg=Image.open(inpath+style+".png")
			elif fileExists(inpath+style+".jpg"):
				bg=Image.open(inpath+style+".jpg")
			bg_w,bg_h=bg.size
			img=Image.new("RGBA",(width,height),(0,0,0,0))
			for i in xrange(0,width,bg_w):
				for j in xrange(0,height,bg_h):
					img.paste(bg,(i,j))
		elif config.plugins.KravenVB.BackgroundColor.value == "gradient":
			c1=config.plugins.KravenVB.BackgroundGradientColorPrimary.value
			c2=config.plugins.KravenVB.BackgroundGradientColorSecondary.value
			c1=c1[-6:]
			r1=int(c1[0:2],16)
			g1=int(c1[2:4],16)
			b1=int(c1[4:6],16)
			c2=c2[-6:]
			r2=int(c2[0:2],16)
			g2=int(c2[2:4],16)
			b2=int(c2[4:6],16)
			if c1!=c2:
				img=Image.new("RGBA",(1,height))
				for pos in range(0,height):
					p=pos/float(height)
					r=r2*p+r1*(1-p)
					g=g2*p+g1*(1-p)
					b=b2*p+b1*(1-p)
					img.putpixel((0,pos),(int(r),int(g),int(b),255))
				img=img.resize((width,height))
			else:
				img=Image.new("RGBA",(width,height),(int(r1),int(g1),int(b1),255))
		else:
			c=self.skincolorbackgroundcolor
			c=c[-6:]
			r=int(c[0:2],16)
			g=int(c[2:4],16)
			b=int(c[4:6],16)
			img=Image.new("RGBA",(width,height),(int(r),int(g),int(b),255))
		
		# infobars
		if config.plugins.KravenVB.IBStyle.value=="grad":
			if config.plugins.KravenVB.InfobarGradientColor.value == "texture":
				style=config.plugins.KravenVB.InfobarTexture.value
				if fileExists(usrpath+style+".png"):
					bg=Image.open(usrpath+style+".png")
				elif fileExists(usrpath+style+".jpg"):
					bg=Image.open(usrpath+style+".jpg")
				elif fileExists(inpath+style+".png"):
					bg=Image.open(inpath+style+".png")
				elif fileExists(inpath+style+".jpg"):
					bg=Image.open(inpath+style+".jpg")
				bg_w,bg_h=bg.size
				ib=Image.new("RGBA",(width,gradbarheight),(0,0,0,0))
				for i in xrange(0,width,bg_w):
					for j in xrange(0,gradbarheight,bg_h):
						ib.paste(bg,(i,j))
			else:
				c=self.skincolorinfobarcolor
				c=c[-6:]
				r=int(c[0:2],16)
				g=int(c[2:4],16)
				b=int(c[4:6],16)
				ib=Image.new("RGBA",(width,gradbarheight),(int(r),int(g),int(b),255))
			trans=(255-int(config.plugins.KravenVB.InfobarColorTrans.value,16))/255.0
			gr=Image.new("L",(1,gradbarheight),int(255*trans))
			for pos in range(0,gradbarheight):
				gr.putpixel((0,pos),int(self.dexpGradient(gradbarheight,2.0,pos)*trans))
			gr=gr.resize(ib.size)
			img.paste(ib,(0,height-gradbarheight),gr)
			ib=ib.transpose(Image.ROTATE_180)
			gr=gr.transpose(Image.ROTATE_180)
			img.paste(ib,(0,0),gr)
		else: # config.plugins.KravenVB.IBStyle.value=="box":
			if config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				style=config.plugins.KravenVB.InfobarTexture.value
				if fileExists(usrpath+style+".png"):
					bg=Image.open(usrpath+style+".png")
				elif fileExists(usrpath+style+".jpg"):
					bg=Image.open(usrpath+style+".jpg")
				elif fileExists(inpath+style+".png"):
					bg=Image.open(inpath+style+".png")
				elif fileExists(inpath+style+".jpg"):
					bg=Image.open(inpath+style+".jpg")
				bg_w,bg_h=bg.size
				ib=Image.new("RGBA",(width,boxbarheight),(0,0,0,0))
				for i in xrange(0,width,bg_w):
					for j in xrange(0,boxbarheight,bg_h):
						ib.paste(bg,(i,j))
				img.paste(ib,(0,0))
				img.paste(ib,(0,height-boxbarheight))
			elif config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				c1=config.plugins.KravenVB.InfobarGradientColorPrimary.value
				c2=config.plugins.KravenVB.InfobarGradientColorSecondary.value
				c1=c1[-6:]
				r1=int(c1[0:2],16)
				g1=int(c1[2:4],16)
				b1=int(c1[4:6],16)
				c2=c2[-6:]
				r2=int(c2[0:2],16)
				g2=int(c2[2:4],16)
				b2=int(c2[4:6],16)
				if c1!=c2:
					ib=Image.new("RGBA",(1,boxbarheight))
					for pos in range(0,boxbarheight):
						p=pos/float(boxbarheight)
						r=r2*p+r1*(1-p)
						g=g2*p+g1*(1-p)
						b=b2*p+b1*(1-p)
						ib.putpixel((0,pos),(int(r),int(g),int(b),255))
					ib=ib.resize((width,boxbarheight))
					img.paste(ib,(0,height-boxbarheight))
					ib=ib.transpose(Image.ROTATE_180)
					img.paste(ib,(0,0))
				else:
					ib=Image.new("RGBA",(width,boxbarheight),(int(r1),int(g1),int(b1),255))
					img.paste(ib,(0,0))
					img.paste(ib,(0,height-boxbarheight))
			else:
				c=self.skincolorinfobarcolor
				c=c[-6:]
				r=int(c[0:2],16)
				g=int(c[2:4],16)
				b=int(c[4:6],16)
				ib=Image.new("RGBA",(width,boxbarheight),(int(r),int(g),int(b),255))
				img.paste(ib,(0,0))
				img.paste(ib,(0,height-boxbarheight))
			c=config.plugins.KravenVB.IBLine.value
			c=c[-6:]
			r=int(c[0:2],16)
			g=int(c[2:4],16)
			b=int(c[4:6],16)
			img.paste((int(r),int(g),int(b),255),(0,boxbarheight,width,boxbarheight+lineheight))
			img.paste((int(r),int(g),int(b),255),(0,height-boxbarheight-lineheight,width,height-boxbarheight))
				
		img.save("/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/preview.jpg")
		
	def makeIbarColorGradientpng(self, newcolor, newtrans):

		width = 1280 # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder

		ibarheight = 310 # height of ibar
		ibargradientstart = 50 # start of ibar gradient (from top)
		ibargradientsize = 100 # size of ibar gradient

		ibaroheight = 165 # height of ibaro
		ibarogradientstart = 65 # start of ibaro gradient (from top)
		ibarogradientsize = 100 # size of ibaro gradient

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		trans = (255-int(newtrans,16))/255.0

		img = Image.new("RGBA",(width,ibarheight),(r,g,b,0))
		gradient = Image.new("L",(1,ibarheight),int(255*trans))
		for pos in range(0,ibargradientstart):
			gradient.putpixel((0,pos),0)
		for pos in range(0,ibargradientsize):
			gradient.putpixel((0,ibargradientstart+pos),int(self.dexpGradient(ibargradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibar.png")

		img = Image.new("RGBA",(width,ibaroheight),(r,g,b,0))
		gradient = Image.new("L",(1,ibaroheight),0)
		for pos in range(0,ibarogradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibarogradientsize):
			gradient.putpixel((0,ibarogradientstart+ibarogradientsize-pos-1),int(self.dexpGradient(ibarogradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro.png")

	def makeIbarTextureGradientpng(self, style, trans):

		width = 1280 # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder

		ibarheight = 310 # height of ibar
		ibargradientstart = 50 # start of ibar gradient (from top)
		ibargradientsize = 100 # size of ibar gradient

		ibaroheight = 165 # height of ibaro
		ibarogradientstart = 65 # start of ibaro gradient (from top)
		ibarogradientsize = 100 # size of ibaro gradient

		trans = (255-int(trans,16))/255.0

		inpath="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
		if fileExists(usrpath+style+".png"):
			bg=Image.open(usrpath+style+".png")
		elif fileExists(usrpath+style+".jpg"):
			bg=Image.open(usrpath+style+".jpg")
		elif fileExists(inpath+style+".png"):
			bg=Image.open(inpath+style+".png")
		elif fileExists(inpath+style+".jpg"):
			bg=Image.open(inpath+style+".jpg")
		bg_w,bg_h=bg.size
		
		img=Image.new("RGBA",(width,ibarheight),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,ibarheight,bg_h):
				img.paste(bg,(i,j))
		gradient = Image.new("L",(1,ibarheight),int(255*trans))
		for pos in range(0,ibargradientstart):
			gradient.putpixel((0,pos),0)
		for pos in range(0,ibargradientsize):
			gradient.putpixel((0,ibargradientstart+pos),int(self.dexpGradient(ibargradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibar.png")

		img=Image.new("RGBA",(width,ibaroheight),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,ibaroheight,bg_h):
				img.paste(bg,(i,j))
		gradient = Image.new("L",(1,ibaroheight),0)
		for pos in range(0,ibarogradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibarogradientsize):
			gradient.putpixel((0,ibarogradientstart+ibarogradientsize-pos-1),int(self.dexpGradient(ibarogradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro.png")

	def makeRectColorpng(self, newcolor, newtrans, width, height, pngname):

		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		gradientsize = 80 # size of gradient

		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)

		trans = (255-int(newtrans,16))/255.0

		img = Image.new("RGBA",(width,height),(r,g,b,int(255*trans)))

		gradient = Image.new("RGBA",(1,gradientsize),(r,g,b,0))
		for pos in range(0,gradientsize):
			gradient.putpixel((0,pos),(r,g,b,int((self.dexpGradient(gradientsize,gradientspeed,pos))*trans)))

		hgradient = gradient.resize((width-2*gradientsize, gradientsize))
		img.paste(hgradient, (gradientsize,0,width-gradientsize,gradientsize))
		hgradient = hgradient.transpose(Image.ROTATE_180)
		img.paste(hgradient, (gradientsize,height-gradientsize,width-gradientsize,height))

		vgradient = gradient.transpose(Image.ROTATE_90)
		vgradient = vgradient.resize((gradientsize,height-2*gradientsize))
		img.paste(vgradient, (0,gradientsize,gradientsize,height-gradientsize))
		vgradient = vgradient.transpose(Image.ROTATE_180)
		img.paste(vgradient, (width-gradientsize,gradientsize,width,height-gradientsize))

		corner = Image.new("RGBA",(gradientsize,gradientsize),(r,g,b,0))
		for xpos in range(0,gradientsize):
			for ypos in range(0,gradientsize):
				dist = int(round((xpos**2+ypos**2)**0.503))
				corner.putpixel((xpos,ypos),(r,g,b,int((self.dexpGradient(gradientsize,gradientspeed,gradientsize-dist-1))*trans)))
		corner = corner.filter(ImageFilter.BLUR)
		img.paste(corner, (width-gradientsize,height-gradientsize,width,height))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (width-gradientsize,0,width,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0,0,gradientsize,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		img.paste(corner, (0,height-gradientsize,gradientsize,height))

		img.save("/usr/share/enigma2/KravenVB/graphics/"+pngname+".png")

	def makeRectTexturepng(self, style, trans, width, height, pngname):

		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder
		gradientsize = 80 # size of gradient

		trans = (255-int(trans,16))/255.0

		inpath="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
		if fileExists(usrpath+style+".png"):
			bg=Image.open(usrpath+style+".png")
		elif fileExists(usrpath+style+".jpg"):
			bg=Image.open(usrpath+style+".jpg")
		elif fileExists(inpath+style+".png"):
			bg=Image.open(inpath+style+".png")
		elif fileExists(inpath+style+".jpg"):
			bg=Image.open(inpath+style+".jpg")
		bg_w,bg_h=bg.size
		
		img=Image.new("RGBA",(width,height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,height,bg_h):
				img.paste(bg,(i,j))

		mask=Image.new("L",(width,height),255*trans)
		
		gradient = Image.new("L",(1,gradientsize),0)
		for pos in range(0,gradientsize):
			gradient.putpixel((0,pos),int((self.dexpGradient(gradientsize,gradientspeed,pos))*trans))

		hgradient = gradient.resize((width-2*gradientsize, gradientsize))
		mask.paste(hgradient, (gradientsize,0,width-gradientsize,gradientsize))
		hgradient = hgradient.transpose(Image.ROTATE_180)
		mask.paste(hgradient, (gradientsize,height-gradientsize,width-gradientsize,height))

		vgradient = gradient.transpose(Image.ROTATE_90)
		vgradient = vgradient.resize((gradientsize,height-2*gradientsize))
		mask.paste(vgradient, (0,gradientsize,gradientsize,height-gradientsize))
		vgradient = vgradient.transpose(Image.ROTATE_180)
		mask.paste(vgradient, (width-gradientsize,gradientsize,width,height-gradientsize))

		corner = Image.new("L",(gradientsize,gradientsize),0)
		for xpos in range(0,gradientsize):
			for ypos in range(0,gradientsize):
				dist = int(round((xpos**2+ypos**2)**0.503))
				corner.putpixel((xpos,ypos),int((self.dexpGradient(gradientsize,gradientspeed,gradientsize-dist-1))*trans))
		corner = corner.filter(ImageFilter.BLUR)
		mask.paste(corner, (width-gradientsize,height-gradientsize,width,height))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (width-gradientsize,0,width,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (0,0,gradientsize,gradientsize))
		corner = corner.transpose(Image.ROTATE_90)
		mask.paste(corner, (0,height-gradientsize,gradientsize,height))
		
		img.putalpha(mask)

		img.save("/usr/share/enigma2/KravenVB/graphics/"+pngname+".png")

	def makeBGGradientpng(self):
		self.makeGradientpng("globalbg",1280,720,config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value,config.plugins.KravenVB.BackgroundColorTrans.value)
		self.makeGradientpng("nontransbg",1280,720,config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value,"00")
		self.makeGradientpng("menubg",1280,720,config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value,config.plugins.KravenVB.MenuColorTrans.value)
		self.makeGradientpng("channelbg",1280,720,config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value,config.plugins.KravenVB.ChannelSelectionTrans.value)
		self.makeGradientpng("sibbg",1280,720,config.plugins.KravenVB.BackgroundGradientColorPrimary.value,config.plugins.KravenVB.BackgroundGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
			
	def makeIBGradientpng(self):
		width=1280
		#Ibar
		ibarheights=[
			("infobar-style-nopicon",165),
			("infobar-style-x1",165),
			("infobar-style-zz1",198),
			("infobar-style-zz2",185),
			("infobar-style-zz3",185),
			("infobar-style-zz4",198),
			("infobar-style-zzz1",247)
			]
		for pair in ibarheights:
			if config.plugins.KravenVB.InfobarStyle.value == pair[0]:
				self.makeGradientpng("ibar",width,pair[1],config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-android":
				self.makeGradientpng("ibar",width,154,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
			else:
				self.makeGradientpng("ibar",width,144,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
			if config.plugins.KravenVB.ClockStyle.value == "clock-android":
				self.makeGradientpng("ibar",width,154,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
			else:
				self.makeGradientpng("ibar",width,140,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		self.makeGradientpng("ibar2",width,60,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		self.makeGradientpng("ibar3",width,70,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		self.makeGradientpng("ibar4",width,80,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		self.makeGradientpng("ibar5",width,110,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		self.makeGradientpng("ibar6",width,206,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		#Ibaro
		ibaroheights=[
			("ibaro",59),
			("ibaro2",70),
			("ibaro3",115)
			]
		for pair in ibaroheights:
			self.makeGradientpng(pair[0],width,pair[1],config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarColorTrans.value)

		#Sysinfo
		if config.plugins.KravenVB.InfoStyle.value == "primary":
			FirstColor=config.plugins.KravenVB.InfobarGradientColorPrimary.value
			SecondColor=config.plugins.KravenVB.InfobarGradientColorPrimary.value
		elif config.plugins.KravenVB.InfoStyle.value == "secondary":
			FirstColor=config.plugins.KravenVB.InfobarGradientColorSecondary.value
			SecondColor=config.plugins.KravenVB.InfobarGradientColorSecondary.value
		else:
			FirstColor=config.plugins.KravenVB.InfobarGradientColorPrimary.value
			SecondColor=config.plugins.KravenVB.InfobarGradientColorSecondary.value
		if config.plugins.KravenVB.SystemInfo.value == "systeminfo-small":
			self.makeGradientpng("info",300,80,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)
		elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-big":
			self.makeGradientpng("info",300,170,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)
		elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
			self.makeGradientpng("info",300,260,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)
		
		#Timeshift
		self.makeGradientpng("shift",785,62,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)

		#InfobarTunerState
		self.makeGradientpng("ibts",1280,32,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)

		#AutoResolution
		self.makeGradientpng("autoresolution",252,62,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)

		#PVRState
		if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
			self.makeGradientpng("pvrstate",220,90,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)
		elif config.plugins.KravenVB.PVRState.value in ("pvrstate-center-small","pvrstate-left-small"):
			self.makeGradientpng("pvrstate",110,45,FirstColor,SecondColor,config.plugins.KravenVB.InfobarColorTrans.value)

		#Weather-small
		if config.plugins.KravenVB.WeatherStyle.value == "weather-small":
			self.makeGradientpng("wsmall",300,120,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarColorTrans.value)

	def makeGradientpng(self,name,width,height,color1,color2,trans):
		path="/usr/share/enigma2/KravenVB/graphics/"
		width=int(width)
		height=int(height)
		color1=color1[-6:]
		r1=int(color1[0:2],16)
		g1=int(color1[2:4],16)
		b1=int(color1[4:6],16)
		color2=color2[-6:]
		r2=int(color2[0:2],16)
		g2=int(color2[2:4],16)
		b2=int(color2[4:6],16)
		trans=255-int(trans,16)
		gradient=Image.new("RGBA",(1,height))
		for pos in range(0,height):
			p=pos/float(height)
			r=r2*p+r1*(1-p)
			g=g2*p+g1*(1-p)
			b=b2*p+b1*(1-p)
			gradient.putpixel((0,pos),(int(r),int(g),int(b),int(trans)))
		gradient=gradient.resize((width,height))
		gradient.save(path+name+".png")

	def makeBGTexturepng(self):
		self.makeTexturepng("globalbg",1280,720,config.plugins.KravenVB.BackgroundTexture.value,config.plugins.KravenVB.BackgroundColorTrans.value)
		self.makeTexturepng("nontransbg",1280,720,config.plugins.KravenVB.BackgroundTexture.value,"00")
		self.makeTexturepng("menubg",1280,720,config.plugins.KravenVB.BackgroundTexture.value,config.plugins.KravenVB.MenuColorTrans.value)
		self.makeTexturepng("channelbg",1280,720,config.plugins.KravenVB.BackgroundTexture.value,config.plugins.KravenVB.ChannelSelectionTrans.value)
		self.makeTexturepng("sibbg",1280,720,config.plugins.KravenVB.BackgroundTexture.value,config.plugins.KravenVB.InfobarColorTrans.value)
			
	def makeIBTexturepng(self):
		self.makeTexturepng("ibtexture",1280,720,config.plugins.KravenVB.InfobarTexture.value,config.plugins.KravenVB.InfobarColorTrans.value)
			
	def makeTexturepng(self,name,width,height,style,trans):
		width=int(width)
		height=int(height)
		trans=255-int(trans,16)
		path="/usr/share/enigma2/KravenVB/textures/"
		usrpath="/usr/share/enigma2/Kraven-user-icons/"
		outpath="/usr/share/enigma2/KravenVB/graphics/"
		if fileExists(usrpath+style+".png"):
			bg=Image.open(usrpath+style+".png")
		elif fileExists(usrpath+style+".jpg"):
			bg=Image.open(usrpath+style+".jpg")
		elif fileExists(path+style+".png"):
			bg=Image.open(path+style+".png")
		elif fileExists(path+style+".jpg"):
			bg=Image.open(path+style+".jpg")
		bg_w,bg_h=bg.size
		image=Image.new("RGBA",(width,height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,height,bg_h):
				image.paste(bg,(i,j))
		alpha=Image.new("L",(width,height),trans)
		image.putalpha(alpha)
		image.save(outpath+name+".png")

	def makeBackpng(self):
		# this makes a transparent png
		# not needed above, use it manually
		width = 1280 # width of the png file
		height = 720 # height of the png file
		img = Image.new("RGBA",(width,height),(0,0,0,0))
		img.save("/usr/share/enigma2/KravenVB/backg.png")

	def makeSRpng(self,newcolor):
		if config.plugins.KravenVB.SerienRecorder.value == "serienrecorder":
			width = 600 # width of the png file
			height = 390 # height of the png file

			newcolor = newcolor[-6:]
			r = int(newcolor[0:2], 16)
			g = int(newcolor[2:4], 16)
			b = int(newcolor[4:6], 16)
		
			img = Image.new("RGBA",(width,height),(r,g,b,255))
			img.save("/usr/share/enigma2/KravenVB/graphics/popup_bg.png")
		else:
			pass

	def dexpGradient(self,len,spd,pos):
		if pos < 0:
			pos = 0
		if pos > len-1:
			pos = len-1
		a = ((len/2)**spd)*2.0
		if pos <= len/2:
			f = (pos**spd)
		else:
			f = a-((len-pos)**spd)
		e = int((f/a)*255)
		return e

	def calcBrightness(self,color,factor):
		f = int(int(factor)*25.5-255)
		color = color[-6:]
		r = int(color[0:2],16)+f
		g = int(color[2:4],16)+f
		b = int(color[4:6],16)+f
		if r<0:
			r=0
		if g<0:
			g=0
		if b<0:
			b=0
		if r>255:
			r=255
		if g>255:
			g=255
		if b>255:
			b=255
		return str(hex(r)[2:4]).zfill(2)+str(hex(g)[2:4]).zfill(2)+str(hex(b)[2:4]).zfill(2)

	def calcTransparency(self,trans1,trans2):
		t1 = int(trans1,16)
		t2 = int(trans2,16)
		return str(hex(min(t1,t2))[2:4]).zfill(2)

	def hexRGB(self,color):
		color = color[-6:]
		r = int(color[0:2],16)
		g = int(color[2:4],16)
		b = int(color[4:6],16)
		return (r<<16)|(g<<8)|b

	def RGB(self,r,g,b):
		return (r<<16)|(g<<8)|b

	def get_weather_data(self):

			self.city = ''
			self.lat = ''
			self.lon = ''
			self.zipcode = ''
			self.accu_id = ''
			self.woe_id = ''
			self.gm_code = ''
			self.preview_text = ''
			self.preview_warning = ''

			if config.plugins.KravenVB.weather_search_over.value == 'ip':
			  self.get_latlon_by_ip()
			elif config.plugins.KravenVB.weather_search_over.value == 'name':
			  self.get_latlon_by_name()
			elif config.plugins.KravenVB.weather_search_over.value == 'gmcode':
			  self.get_latlon_by_gmcode()

			self.generate_owm_accu_realtek_string()
			if config.plugins.KravenVB.weather_server.value == '_accu':
			  self.get_accu_id_by_latlon()

			self.actCity=self.preview_text+self.preview_warning
			config.plugins.KravenVB.weather_foundcity.value=self.city
			config.plugins.KravenVB.weather_foundcity.save()

	def get_latlon_by_ip(self):
		try:
			res = requests.get('http://ip-api.com/json/?lang=de&fields=status,city,lat,lon', timeout=1)
			data = res.json()

			if data['status']=='success':
				self.city = data['city']
				self.lat = data['lat']
				self.lon = data['lon']
				self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
			else:
				self.preview_text = _('No data for IP')

		except:
			self.preview_text = _('No data for IP')

	def get_latlon_by_name(self):
		try:
			name = config.plugins.KravenVB.weather_cityname.getValue()
			res = requests.get('http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % str(name), timeout=1)
			data = res.json()

			for entry in data['results'][0]['address_components']:
				if entry['types'][0]=='locality':
					self.city = entry['long_name']
					break
					
			self.lat = data['results'][0]['geometry']['location']['lat']
			self.lon = data['results'][0]['geometry']['location']['lng']

			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.get_latlon_by_ip()
			self.preview_warning = _('\n\nNo data for search string,\nfallback to IP')

	def get_latlon_by_gmcode(self):
		try:
			gmcode = config.plugins.KravenVB.weather_gmcode.value
			res = requests.get('http://wxdata.weather.com/wxdata/weather/local/%s?cc=*' % str(gmcode), timeout=1)
			data = fromstring(res.text)

			self.city = data[1][0].text.split(',')[0]
			self.lat = data[1][2].text
			self.lon = data[1][3].text

			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
		except:
			self.get_latlon_by_ip()
			self.preview_warning = _('\n\nNo data for GM code,\nfallback to IP')

	def get_accu_id_by_latlon(self):
		try:
			res = requests.get('http://realtek.accu-weather.com/widget/realtek/weather-data.asp?%s' % config.plugins.KravenVB.weather_realtek_latlon.value, timeout=1)
			cityId = re.search('cityId>(.+?)</cityId', str(res.text)).groups(1)
			self.accu_id = str(cityId[0])
			config.plugins.KravenVB.weather_accu_id.value = str(self.accu_id)
			config.plugins.KravenVB.weather_accu_id.save()
		except:
			self.preview_warning = '\n\n'+_('No Accu ID found')
		if self.accu_id is None or self.accu_id=='':
			self.preview_warning = '\n\n'+_('No Accu ID found')

	def generate_owm_accu_realtek_string(self):
		config.plugins.KravenVB.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.KravenVB.weather_language.value))
		config.plugins.KravenVB.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenVB.weather_language.value))
		config.plugins.KravenVB.weather_realtek_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenVB.weather_language.value))
		config.plugins.KravenVB.weather_owm_latlon.save()
		config.plugins.KravenVB.weather_accu_latlon.save()
		config.plugins.KravenVB.weather_realtek_latlon.save()

