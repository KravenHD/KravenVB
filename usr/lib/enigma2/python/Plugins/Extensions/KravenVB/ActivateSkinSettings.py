# -*- coding: utf-8 -*-

#  Activate Skin Settings Code
#
#  Coded/Modified/Adapted by Team Kraven
#  Based on VTi and/or OpenATV image source code
#
#  This code is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ 
#  or send a letter to Creative Commons, 559 Nathan 
#  Abbott Way, Stanford, California 94305, USA.
#
#  If you think this license infringes any rights,
#  please contact Team Kraven at info@coolskins.de

from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock, ConfigSlider, ConfigBoolean
from Components.SystemInfo import SystemInfo
from Components.PluginComponent import plugins
from shutil import move, rmtree
from os import environ, listdir, remove, rename, system, popen, path
from PIL import Image, ImageFilter
from boxbranding import getBoxType
from copy import deepcopy
import time, subprocess, re, requests
from Tools.Directories import fileExists

try:
	from boxbranding import getImageDistro
	if getImageDistro() in ("openatv","teamblue"):
		from lxml import etree
		from xml.etree.cElementTree import fromstring
except ImportError:
	brand = False
	from xml import etree
	from xml.etree.cElementTree import fromstring

#######################################################################

ColorSelfList = [
	("F0A30A", _("amber")),
	("B27708", _("amber dark")),
	("1B1775", _("blue")),
	("0E0C3F", _("blue dark")),
	("7D5929", _("brown")),
	("3F2D15", _("brown dark")),
	("0050EF", _("cobalt")),
	("001F59", _("cobalt dark")),
	("1BA1E2", _("cyan")),
	("0F5B7F", _("cyan dark")),
	("FFEA04", _("yellow")),
	("999999", _("grey")),
	("3F3F3F", _("grey dark")),
	("70AD11", _("green")),
	("213305", _("green dark")),
	("A19181", _("Kraven")),
	("28150B", _("Kraven dark")),
	("6D8764", _("olive")),
	("313D2D", _("olive dark")),
	("C3461B", _("orange")),
	("892E13", _("orange dark")),
	("F472D0", _("pink")),
	("723562", _("pink dark")),
	("E51400", _("red")),
	("330400", _("red dark")),
	("000000", _("black")),
	("008A00", _("emerald")),
	("647687", _("steel")),
	("262C33", _("steel dark")),
	("6C0AAB", _("violet")),
	("1F0333", _("violet dark")),
	("ffffff", _("white")),
	("self", _("self"))
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
	("008A00", _("emerald")),
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

BorderSelfList = deepcopy(ColorSelfList)
BorderSelfList.append(("none", _("off")))

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
config.plugins.KravenVB.InfobarAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenVB.ECMLineAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenVB.ScreensAntialias = ConfigSlider(default=10, increment=1, limits=(0,20))
config.plugins.KravenVB.SelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.SelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.SelfColorB = ConfigSlider(default=75, increment=15, limits=(0,255))

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
				
config.plugins.KravenVB.refreshInterval = ConfigSelection(default="60", choices = [
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

config.plugins.KravenVB.BackgroundListColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)
config.plugins.KravenVB.BackgroundSelfColor = ConfigText(default="000000")
config.plugins.KravenVB.BackgroundColor = ConfigText(default="000000")

config.plugins.KravenVB.BackgroundAlternateListColor = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.BackgroundAlternateSelfColor = ConfigText(default="000000")
config.plugins.KravenVB.BackgroundAlternateColor = ConfigText(default="000000")

config.plugins.KravenVB.InfobarGradientListColor = ConfigSelection(default="self", choices = BackgroundSelfTextureList)
config.plugins.KravenVB.InfobarGradientSelfColor = ConfigText(default="000000")
config.plugins.KravenVB.InfobarGradientColor = ConfigText(default="000000")

config.plugins.KravenVB.InfobarBoxListColor = ConfigSelection(default="self", choices = BackgroundSelfGradientTextureList)
config.plugins.KravenVB.InfobarBoxSelfColor = ConfigText(default="000000")
config.plugins.KravenVB.InfobarBoxColor = ConfigText(default="000000")

config.plugins.KravenVB.InfobarAlternateListColor = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.InfobarAlternateSelfColor = ConfigText(default="000000")
config.plugins.KravenVB.InfobarAlternateColor = ConfigText(default="000000")

config.plugins.KravenVB.BackgroundGradientListColorPrimary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.BackgroundGradientSelfColorPrimary = ConfigText(default="000000")
config.plugins.KravenVB.BackgroundGradientColorPrimary = ConfigText(default="000000")

config.plugins.KravenVB.BackgroundGradientListColorSecondary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.BackgroundGradientSelfColorSecondary = ConfigText(default="000000")
config.plugins.KravenVB.BackgroundGradientColorSecondary = ConfigText(default="000000")

config.plugins.KravenVB.InfobarGradientListColorPrimary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.InfobarGradientSelfColorPrimary = ConfigText(default="000000")
config.plugins.KravenVB.InfobarGradientColorPrimary = ConfigText(default="000000")

config.plugins.KravenVB.InfobarGradientListColorSecondary = ConfigSelection(default="000000", choices = BackgroundSelfList)
config.plugins.KravenVB.InfobarGradientSelfColorSecondary = ConfigText(default="000000")
config.plugins.KravenVB.InfobarGradientColorSecondary = ConfigText(default="000000")

config.plugins.KravenVB.SelectionBackgroundList = ConfigSelection(default="0050EF", choices = ColorSelfList)
config.plugins.KravenVB.SelectionBackgroundSelf = ConfigText(default="0050EF")
config.plugins.KravenVB.SelectionBackground = ConfigText(default="0050EF")

config.plugins.KravenVB.Font1List = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.Font1Self = ConfigText(default="ffffff")
config.plugins.KravenVB.Font1 = ConfigText(default="ffffff")

config.plugins.KravenVB.Font2List = ConfigSelection(default="F0A30A", choices = ColorSelfList)
config.plugins.KravenVB.Font2Self = ConfigText(default="F0A30A")
config.plugins.KravenVB.Font2 = ConfigText(default="F0A30A")

config.plugins.KravenVB.IBFont1List = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.IBFont1Self = ConfigText(default="ffffff")
config.plugins.KravenVB.IBFont1 = ConfigText(default="ffffff")

config.plugins.KravenVB.IBFont2List = ConfigSelection(default="F0A30A", choices = ColorSelfList)
config.plugins.KravenVB.IBFont2Self = ConfigText(default="F0A30A")
config.plugins.KravenVB.IBFont2 = ConfigText(default="F0A30A")

config.plugins.KravenVB.PermanentClockFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.PermanentClockFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.PermanentClockFont = ConfigText(default="ffffff")

config.plugins.KravenVB.SelectionFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.SelectionFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.SelectionFont = ConfigText(default="ffffff")

config.plugins.KravenVB.MarkedFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.MarkedFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.MarkedFont = ConfigText(default="ffffff")

config.plugins.KravenVB.ECMFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.ECMFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.ECMFont = ConfigText(default="ffffff")

config.plugins.KravenVB.ChannelnameFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.ChannelnameFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.ChannelnameFont = ConfigText(default="ffffff")

config.plugins.KravenVB.PrimetimeFontList = ConfigSelection(default="70AD11", choices = ColorSelfList)
config.plugins.KravenVB.PrimetimeFontSelf = ConfigText(default="70AD11")
config.plugins.KravenVB.PrimetimeFont = ConfigText(default="70AD11")

config.plugins.KravenVB.ButtonTextList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.ButtonTextSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.ButtonText = ConfigText(default="ffffff")

config.plugins.KravenVB.AndroidList = ConfigSelection(default="000000", choices = ColorSelfList)
config.plugins.KravenVB.AndroidSelf = ConfigText(default="000000")
config.plugins.KravenVB.Android = ConfigText(default="000000")

config.plugins.KravenVB.BorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.BorderSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.Border = ConfigText(default="ffffff")

config.plugins.KravenVB.ProgressList = ConfigSelection(default="C3461B", choices = [
				("F0A30A", _("amber")),
				("B27708", _("amber dark")),
				("1B1775", _("blue")),
				("0E0C3F", _("blue dark")),
				("7D5929", _("brown")),
				("3F2D15", _("brown dark")),
				("progress", _("colorfull")),
				("progress2", _("colorfull2")),
				("0050EF", _("cobalt")),
				("001F59", _("cobalt dark")),
				("1BA1E2", _("cyan")),
				("0F5B7F", _("cyan dark")),
				("FFEA04", _("yellow")),
				("999999", _("grey")),
				("3F3F3F", _("grey dark")),
				("70AD11", _("green")),
				("213305", _("green dark")),
				("A19181", _("Kraven")),
				("28150B", _("Kraven dark")),
				("6D8764", _("olive")),
				("313D2D", _("olive dark")),
				("C3461B", _("orange")),
				("892E13", _("orange dark")),
				("F472D0", _("pink")),
				("723562", _("pink dark")),
				("E51400", _("red")),
				("330400", _("red dark")),
				("000000", _("black")),
				("008A00", _("emerald")),
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white")),
				("self", _("self"))
				])
config.plugins.KravenVB.ProgressSelf = ConfigText(default="C3461B")
config.plugins.KravenVB.Progress = ConfigText(default="C3461B")

config.plugins.KravenVB.LineList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.LineSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.Line = ConfigText(default="ffffff")

config.plugins.KravenVB.IBLineList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.IBLineSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.IBLine = ConfigText(default="ffffff")

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

config.plugins.KravenVB.SelectionBorderList = ConfigSelection(default="ffffff", choices = BorderSelfList)
config.plugins.KravenVB.SelectionBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.SelectionBorder = ConfigText(default="ffffff")

config.plugins.KravenVB.MiniTVBorderList = ConfigSelection(default="3F3F3F", choices = ColorSelfList)
config.plugins.KravenVB.MiniTVBorderSelf = ConfigText(default="3F3F3F")
config.plugins.KravenVB.MiniTVBorder = ConfigText(default="3F3F3F")

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

config.plugins.KravenVB.ChannelSelectionStyle = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
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
				("channelselection-style-nobile-minitv3", _("Nobile Preview")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenVB.ChannelSelectionStyle2 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
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
				("channelselection-style-nobile-minitv33", _("Nobile Extended Preview")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenVB.ChannelSelectionStyle3 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-nopicon2", _("no Picon2")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-minitv-picon", _("MiniTV Picon"))
				])

config.plugins.KravenVB.ChannellistEPGList = ConfigSelection(default="channellistepglist-off", choices = [
				("channellistepglist-on", _("on")),
				("channellistepglist-off", _("off"))
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

config.plugins.KravenVB.ChannelSelectionServiceNAList = ConfigSelection(default="FFEA04", choices = ColorSelfList)
config.plugins.KravenVB.ChannelSelectionServiceNASelf = ConfigText(default="FFEA04")
config.plugins.KravenVB.ChannelSelectionServiceNA = ConfigText(default="FFEA04")

config.plugins.KravenVB.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-xpicon", _("X-Picons")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-zzpicon", _("ZZ-Picons")),
				("numberzapext-zzzpicon", _("ZZZ-Picons"))
				])

config.plugins.KravenVB.NZBorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.NZBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.NZBorder = ConfigText(default="ffffff")

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

config.plugins.KravenVB.GMESelFgList = ConfigSelection(default="ffffff", choices = [
				("global", _("global selection fontcolor")),
				("ffffff", _("white")),
				("F0A30A", _("amber")),
				("self", _("self"))
				])
config.plugins.KravenVB.GMESelFgSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.GMESelFg = ConfigText(default="ffffff")

config.plugins.KravenVB.GMESelBgList = ConfigSelection(default="389416", choices = [
				("global", _("global selection background")),
				("389416", _("green")),
				("0064c7", _("blue")),
				("self", _("self"))
				])
config.plugins.KravenVB.GMESelBgSelf = ConfigText(default="389416")
config.plugins.KravenVB.GMESelBg = ConfigText(default="389416")

config.plugins.KravenVB.GMENowFgList = ConfigSelection(default="F0A30A", choices = [
				("global", _("global selection fontcolor")),
				("ffffff", _("white")),
				("F0A30A", _("amber")),
				("self", _("self"))
				])
config.plugins.KravenVB.GMENowFgSelf = ConfigText(default="F0A30A")
config.plugins.KravenVB.GMENowFg = ConfigText(default="F0A30A")

config.plugins.KravenVB.GMENowBgList = ConfigSelection(default="0064c7", choices = [
				("global", _("global selection background")),
				("389416", _("green")),
				("0064c7", _("blue")),
				("self", _("self"))
				])
config.plugins.KravenVB.GMENowBgSelf = ConfigText(default="0064c7")
config.plugins.KravenVB.GMENowBg = ConfigText(default="0064c7")

config.plugins.KravenVB.GMEBorderList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.GMEBorderSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.GMEBorder = ConfigText(default="ffffff")

config.plugins.KravenVB.VerticalEPG = ConfigSelection(default="verticalepg-minitv", choices = [
				("verticalepg-minitv", _("MiniTV right")),
				("verticalepg-minitv2", _("MiniTV left")),
				("verticalepg-description", _("description")),
				("verticalepg-full", _("full"))
				])

config.plugins.KravenVB.VerticalEPG2 = ConfigSelection(default="verticalepg-full", choices = [
				("verticalepg-minitv3", _("MiniTV")),
				("verticalepg-full", _("full"))
				])

config.plugins.KravenVB.MovieSelection = ConfigSelection(default="movieselection-no-cover", choices = [
				("movieselection-no-cover", _("no Cover")),
				("movieselection-no-cover2", _("no Cover2")),
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
				("emc-minitv2", _("MiniTV2")),
				("emc-full", _("full"))
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

config.plugins.KravenVB.ClockStyleNoInternet = ConfigSelection(default="clock-classic", choices = [
				("clock-classic", _("standard")),
				("clock-classic-big", _("standard big")),
				("clock-analog", _("analog")),
				("clock-color", _("colored")),
				("clock-flip", _("flip"))
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

config.plugins.KravenVB.WeatherStyleNoInternet = ConfigSelection(default="none", choices = [
				("none", _("off"))
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

config.plugins.KravenVB.TunerBusyList = ConfigSelection(default="CCCC00", choices = [
				("CCCC00", _("yellow")),
				("self", _("self"))
				])
config.plugins.KravenVB.TunerBusySelf = ConfigText(default="CCCC00")
config.plugins.KravenVB.TunerBusy = ConfigText(default="CCCC00")

config.plugins.KravenVB.TunerLiveList = ConfigSelection(default="00B400", choices = [
				("00B400", _("green")),
				("self", _("self"))
				])
config.plugins.KravenVB.TunerLiveSelf = ConfigText(default="00B400")
config.plugins.KravenVB.TunerLive = ConfigText(default="00B400")

config.plugins.KravenVB.TunerRecordList = ConfigSelection(default="FF0C00", choices = [
				("FF0C00", _("red")),
				("self", _("self"))
				])
config.plugins.KravenVB.TunerRecordSelf = ConfigText(default="FF0C00")
config.plugins.KravenVB.TunerRecord = ConfigText(default="FF0C00")

config.plugins.KravenVB.TunerXtremeBusyList = ConfigSelection(default="1BA1E2", choices = [
				("1BA1E2", _("cyan")),
				("self", _("self"))
				])
config.plugins.KravenVB.TunerXtremeBusySelf = ConfigText(default="1BA1E2")
config.plugins.KravenVB.TunerXtremeBusy = ConfigText(default="1BA1E2")

config.plugins.KravenVB.ShowUnusedTuner = ConfigSelection(default="on", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenVB.ShowAgcSnr = ConfigSelection(default="none", choices = [
				("on", _("on")),
				("none", _("off"))
				])

config.plugins.KravenVB.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("tunerinfo", _("Tunerinfo")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenVB.Infobox2 = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("db", _("Tuner/Satellite + dB")),
				("tunerinfo", _("Tunerinfo")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenVB.Infobox3 = ConfigSelection(default="cpu", choices = [
				("tunerinfo", _("Tunerinfo")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
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

config.plugins.KravenVB.LogoNoInternet = ConfigSelection(default="minitv", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV"))
				])

config.plugins.KravenVB.MainmenuFontsize = ConfigSelection(default="mainmenu-big", choices = [
				("mainmenu-small", _("small")),
				("mainmenu-middle", _("middle")),
				("mainmenu-big", _("big"))
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

config.plugins.KravenVB.EMCSelectionBackgroundList = ConfigSelection(default="213305", choices = ColorSelfList)
config.plugins.KravenVB.EMCSelectionBackgroundSelf = ConfigText(default="213305")
config.plugins.KravenVB.EMCSelectionBackground = ConfigText(default="213305")

config.plugins.KravenVB.EMCSelectionFontList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.EMCSelectionFontSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.EMCSelectionFont = ConfigText(default="ffffff")

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

config.plugins.KravenVB.FileCommander = ConfigSelection(default="filecommander-hor", choices = [
				("filecommander-hor", _("horizontal")),
				("filecommander-ver", _("vertical"))
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
				("_accu", _("Accuweather"))
				])

config.plugins.KravenVB.weather_search_over = ConfigSelection(default="ip", choices = [
				("ip", _("Auto (IP)")),
				("name", _("Search String"))
				])

config.plugins.KravenVB.weather_search_over2 = ConfigSelection(default="ip", choices = [
				("ip", _("Auto (IP)")),
				("name", _("Search String")),
				("gmcode", _("GM Code"))
				])

config.plugins.KravenVB.weather_owm_latlon = ConfigText(default = "")
config.plugins.KravenVB.weather_accu_latlon = ConfigText(default = "")
config.plugins.KravenVB.weather_accu_apikey = ConfigText(default = "")
config.plugins.KravenVB.weather_accu_id = ConfigText(default = "")
config.plugins.KravenVB.weather_foundcity = ConfigText(default = "")

config.plugins.KravenVB.PlayerClock = ConfigSelection(default="player-classic", choices = [
				("player-classic", _("standard")),
				("player-android", _("android")),
				("player-flip", _("flip")),
				("player-weather", _("weather icon"))
				])

config.plugins.KravenVB.Android2List = ConfigSelection(default="000000", choices = ColorSelfList)
config.plugins.KravenVB.Android2Self = ConfigText(default="000000")
config.plugins.KravenVB.Android2 = ConfigText(default="000000")

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

config.plugins.KravenVB.CategoryVarious = ConfigSelection(default="category", choices = [
				("category", _(" "))
				])

config.plugins.KravenVB.Unskinned = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("unskinned-colors-on", _("on"))
				])

config.plugins.KravenVB.UnwatchedColorList = ConfigSelection(default="ffffff", choices = ColorSelfList)
config.plugins.KravenVB.UnwatchedColorSelf = ConfigText(default="ffffff")
config.plugins.KravenVB.UnwatchedColor = ConfigText(default="ffffff")

config.plugins.KravenVB.WatchingColorList = ConfigSelection(default="0050EF", choices = ColorSelfList)
config.plugins.KravenVB.WatchingColorSelf = ConfigText(default="0050EF")
config.plugins.KravenVB.WatchingColor = ConfigText(default="0050EF")

config.plugins.KravenVB.FinishedColorList = ConfigSelection(default="70AD11", choices = ColorSelfList)
config.plugins.KravenVB.FinishedColorSelf = ConfigText(default="70AD11")
config.plugins.KravenVB.FinishedColor = ConfigText(default="70AD11")

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

config.plugins.KravenVB.TBna = ConfigSelection(default="na", choices = [
				("na", _("not available for teamBlue"))
				])

config.plugins.KravenVB.KravenIconVPosition = ConfigSelection(default="vposition0", choices = [
				("vposition-3", _("-3")),
				("vposition-2", _("-2")),
				("vposition-1", _("-1")),
				("vposition0", _("0")),
				("vposition+1", _("+1")),
				("vposition+2", _("+2")),
				("vposition+3", _("+3"))
				])

config.plugins.KravenVB.InfobarSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorB = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorB = ConfigSlider(default=75, increment=15, limits=(0,255))

#############################################################

class ActivateSkinSettings:

	def __init__(self):
		self.datei = "/usr/share/enigma2/KravenVB/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/comp/"
		self.picPath = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/"
		self.profiles = "/etc/enigma2/"
		self.BoxName=self.getBoxName()
		self.E2DistroVersion=self.getE2DistroVersion()
		self.Templates=self.getTemplates()
		self.Tuners=self.getTuners()
		self.InternetAvailable=self.getInternetAvailable()

	def WriteSkin(self, silent=False):
		#silent = True  -> returned 0 or 1 (no gui mode)
		#silent = False -> returned some optional code for messages or another things in gui mode

		#error codes for silent mode 
		#0:"No Error"
		#1:"Error occurred"

		self.silent = silent

		if self.silent:
			if config.skin.primary_skin.value != "KravenVB/skin.xml":
				print 'KravenVB is not the primary skin. No restore action needed!'
				return 0
			self.E2settings = open("/etc/enigma2/settings", "r").read()

		return self.save()

	def calcBackgrounds(self, bg = None):
		if config.plugins.KravenVB.BackgroundColor.value == "gradient":
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundGradientColorPrimary.value
		elif config.plugins.KravenVB.BackgroundColor.value == "texture":
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundAlternateColor.value
		else:
			self.skincolorbackgroundcolor = config.plugins.KravenVB.BackgroundColor.value
		if config.plugins.KravenVB.IBStyle.value == "grad":
			if config.plugins.KravenVB.InfobarGradientColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarGradientColor.value
		else:
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarGradientColorPrimary.value
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarAlternateColor.value
			else:
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarBoxColor.value

		if bg == 'background':
			return self.skincolorbackgroundcolor
		elif bg == 'infobar':
			return self.skincolorinfobarcolor

	def save(self):
		#refresh internet
		if not self.silent:
			self.InternetAvailable=self.getInternetAvailable()

		#clock
		self.actClockstyle="none"
		if self.InternetAvailable:
			self.actClockstyle=config.plugins.KravenVB.ClockStyle.value
		else:
			self.actClockstyle=config.plugins.KravenVB.ClockStyleNoInternet.value

		#weather
		self.actWeatherstyle="none"
		if self.InternetAvailable:
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zzz1"):
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle.value
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle3.value
				else:
					self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle2.value

		#channelselection
		self.actChannelselectionstyle="none"
		if self.E2DistroVersion == "VTi":
			if config.plugins.KravenVB.alternativeChannellist.value == "none":
				if SystemInfo.get("NumVideoDecoders",1) > 1:
					self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle2.value
				else:
					self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle.value
		elif self.E2DistroVersion == "openatv":
			if SystemInfo.get("NumVideoDecoders",1) > 1:
				self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle2.value
			else:
				self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle.value
		elif self.E2DistroVersion == "teamblue":
			self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle3.value

		### Calculate Backgrounds
		self.calcBackgrounds()

		self.skin_lines = []
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
		if self.InternetAvailable:
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
		else:
			if config.plugins.KravenVB.LogoNoInternet.value == "logo":
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

		### Background graphics
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
			self.skinSearchAndReplace.append(['name="KravenIBbg2" value="#00000000', 'name="KravenIBbg2" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg3" value="#00000000', 'name="KravenIBbg3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + self.skincolorbackgroundcolor])
			self.skinSearchAndReplace.append(['name="KravenIBbg4" value="#00000000', 'name="KravenIBbg4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])

		### Menu
		if self.E2DistroVersion == "VTi":
			if not self.actChannelselectionstyle in ("channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-nobile-minitv33","channelselection-style-minitv3","channelselection-style-nobile-minitv3"):
				self.skinSearchAndReplace.append(['render="KravenVBMenuPig"', 'render="Pig"'])
			else:
				self.skinSearchAndReplace.append(['render="KravenVBMenuPig"', 'render="KravenVBPig3"'])
		elif self.E2DistroVersion == "openatv":
			if not self.actChannelselectionstyle in ("channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-nobile-minitv33","channelselection-style-minitv3","channelselection-style-nobile-minitv3"):
				self.skinSearchAndReplace.append(['render="KravenVBMenuPig"', 'render="Pig"'])
		elif self.E2DistroVersion == "teamblue":
			self.skinSearchAndReplace.append(['render="KravenVBMenuPig"', 'render="Pig"'])
		if self.InternetAvailable:
			if config.plugins.KravenVB.Logo.value == "minitv":
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo1"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons1"/>'])
			elif config.plugins.KravenVB.Logo.value == "logo":
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo2"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons2"/>'])
			elif config.plugins.KravenVB.Logo.value == "metrix-icons":
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo3"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons3"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo4"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons4"/>'])
		else:
			if config.plugins.KravenVB.LogoNoInternet.value == "minitv":
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo1"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons1"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Logo -->', self.Templates + 'name="Logo2"/>'])
				self.skinSearchAndReplace.append(['<!-- Metrix-Icons -->', self.Templates + 'name="Icons2"/>'])

		### Logo
		if self.E2DistroVersion == "VTi":
			system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/logo-vti.tar.gz -C /usr/share/enigma2/KravenVB/")
		elif self.E2DistroVersion == "openatv":
			system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/logo-openatv.tar.gz -C /usr/share/enigma2/KravenVB/")
		elif self.E2DistroVersion == "teamblue":
			system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/logo-teamblue.tar.gz -C /usr/share/enigma2/KravenVB/")

		### Mainmenu Fontsize
		if config.plugins.KravenVB.MainmenuFontsize.value == "mainmenu-small":
			self.skinSearchAndReplace.append([self.Templates + 'name="mainmenu-big"/>', self.Templates + 'name="mainmenu-small"/>'])
		elif config.plugins.KravenVB.MainmenuFontsize.value == "mainmenu-middle":
			self.skinSearchAndReplace.append([self.Templates + 'name="mainmenu-big"/>', self.Templates + 'name="mainmenu-middle"/>'])

		### Infobar. Background-Style
		if config.plugins.KravenVB.IBStyle.value == "box":

			### Infobar - Background
			self.skinSearchAndReplace.append(['<!--<eLabel position', '<eLabel position'])
			self.skinSearchAndReplace.append(['zPosition="-8" />-->', 'zPosition="-8" />'])

			### Infobar - Line
			self.skinSearchAndReplace.append(['name="KravenIBLine" value="#00ffffff', 'name="KravenIBLine" value="#00' + config.plugins.KravenVB.IBLine.value])

			### Infobar
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', self.Templates + 'name="infobar-style-x2-z1-topbar-box2"/>'])

				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-x2-x3-box2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-z1-z2-box2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-box2"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-zz2-zz3-box2"/>'])

			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', self.Templates + 'name="infobar-style-x2-z1-topbar-texture"/>'])

				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-x2-x3-texture"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-z1-z2-texture"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-texture"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-zz2-zz3-texture"/>'])

			else:
				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
					self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', self.Templates + 'name="infobar-style-x2-z1-topbar-box"/>'])

				if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-x2-x3-box"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-z1-z2-box"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zzz1"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-box"/>'])
				elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
					self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-zz2-zz3-box"/>'])

			### NetatmoBar - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="infobar-style-x2-z1-netatmobar-gradient"/>', self.Templates + 'name="infobar-style-x2-z1-netatmobar-box2"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="infobar-style-x2-z1-netatmobar-gradient"/>', self.Templates + 'name="infobar-style-x2-z1-netatmobar-texture"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="infobar-style-x2-z1-netatmobar-gradient"/>', self.Templates + 'name="infobar-style-x2-z1-netatmobar-box"/>'])

			### SIB - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-sib"/>', self.Templates + 'name="box2-sib"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-sib"/>', self.Templates + 'name="texture-sib"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-sib"/>', self.Templates + 'name="box-sib"/>'])

			### clock-android - ibar-Position
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2") and self.actClockstyle == "clock-android":
				self.skinSearchAndReplace.append(['position="0,576" size="1280,144"', 'position="0,566" size="1280,154"'])
				self.skinSearchAndReplace.append(['position="0,576" size="1280,2"', 'position="0,566" size="1280,2"'])
				self.skinSearchAndReplace.append(['position="0,580" size="1280,140"', 'position="0,566" size="1280,154"'])
				self.skinSearchAndReplace.append(['position="0,580" size="1280,2"', 'position="0,566" size="1280,2"'])

			### EMCMediaCenter, MoviePlayer, DVDPlayer - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-player"/>', self.Templates + 'name="box2-player"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-player"/>', self.Templates + 'name="texture-player"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-player"/>', self.Templates + 'name="box-player"/>'])

			### EPGSelectionEPGBar - Background
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-EPGBar"/>', self.Templates + 'name="box2-EPGBar"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-EPGBar"/>', self.Templates + 'name="texture-EPGBar"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-EPGBar"/>', self.Templates + 'name="box-EPGBar"/>'])

			### ChannelSelectionRadio
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-csr"/>', self.Templates + 'name="box2-csr"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-csr"/>', self.Templates + 'name="texture-csr"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-csr"/>', self.Templates + 'name="box-csr"/>'])

			### RadioInfoBar
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-rib"/>', self.Templates + 'name="box2-rib"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-rib"/>', self.Templates + 'name="texture-rib"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-rib"/>', self.Templates + 'name="box-rib"/>'])

			### GraphicalInfoBarEPG, QuickEPG
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibepg"/>', self.Templates + 'name="box2-ibepg"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibepg"/>', self.Templates + 'name="texture-ibepg"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibepg"/>', self.Templates + 'name="box-ibepg"/>'])

			### InfoBarEventView
			if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibev"/>', self.Templates + 'name="box2-ibev"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibev"/>', self.Templates + 'name="texture-ibev"/>'])
			else:
				self.skinSearchAndReplace.append([self.Templates + 'name="gradient-ibev"/>', self.Templates + 'name="box-ibev"/>'])

		else:
			### Infobar
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				self.skinSearchAndReplace.append(['<!-- Infobar topbarbackground -->', self.Templates + 'name="infobar-style-x2-z1-topbar-gradient"/>'])

			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-x2-x3-gradient"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-z1-z2-gradient"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-zz1","infobar-style-zzz1"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-gradient"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ibar -->', self.Templates + 'name="infobar-style-zz2-zz3-gradient"/>'])

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
		self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#00' + config.plugins.KravenVB.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#00' + config.plugins.KravenVB.Font2.value])
		if config.plugins.KravenVB.Unskinned.value == "unskinned-colors-on":
			self.skinSearchAndReplace.append(['name="foreground" value="#00dddddd', 'name="foreground" value="#00' + config.plugins.KravenVB.Font1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont1" value="#00ffffff', 'name="KravenIBFont1" value="#00' + config.plugins.KravenVB.IBFont1.value])
		self.skinSearchAndReplace.append(['name="KravenIBFont2" value="#00F0A30A', 'name="KravenIBFont2" value="#00' + config.plugins.KravenVB.IBFont2.value])
		self.skinSearchAndReplace.append(['name="KravenPermanentClock" value="#00ffffff', 'name="KravenPermanentClock" value="#00' + config.plugins.KravenVB.PermanentClockFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#00' + config.plugins.KravenVB.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#00' + config.plugins.KravenVB.SelectionBackground.value])
		if config.plugins.KravenVB.EMCSelectionColors.value == "none":
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#00' + config.plugins.KravenVB.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#00' + config.plugins.KravenVB.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#00' + config.plugins.KravenVB.EMCSelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#00' + config.plugins.KravenVB.EMCSelectionBackground.value])
		self.skinSearchAndReplace.append(['name="selectedFG" value="#00ffffff', 'name="selectedFG" value="#00' + config.plugins.KravenVB.SelectionFont.value])
		self.skinSearchAndReplace.append(['name="KravenMarked" value="#00ffffff', 'name="KravenMarked" value="#00' + config.plugins.KravenVB.MarkedFont.value])
		self.skinSearchAndReplace.append(['name="KravenECM" value="#00ffffff', 'name="KravenECM" value="#00' + config.plugins.KravenVB.ECMFont.value])
		self.skinSearchAndReplace.append(['name="KravenName" value="#00ffffff', 'name="KravenName" value="#00' + config.plugins.KravenVB.ChannelnameFont.value])
		self.skinSearchAndReplace.append(['name="KravenButton" value="#00ffffff', 'name="KravenButton" value="#00' + config.plugins.KravenVB.ButtonText.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid" value="#00ffffff', 'name="KravenAndroid" value="#00' + config.plugins.KravenVB.Android.value])
		self.skinSearchAndReplace.append(['name="KravenAndroid2" value="#00ffffff', 'name="KravenAndroid2" value="#00' + config.plugins.KravenVB.Android2.value])
		self.skinSearchAndReplace.append(['name="KravenPrime" value="#0070AD11', 'name="KravenPrime" value="#00' + config.plugins.KravenVB.PrimetimeFont.value])

		### Infobar (Serviceevent) Font-Size
		if config.plugins.KravenVB.IBFontSize.value == "size-22":
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,553" size="500,38"', 'font="Regular;22" position="545,560" size="500,27"']) # ZZ1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,643" size="393,38"', 'font="Regular;22" position="545,650" size="393,27"']) # ZZ1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,526" size="500,38"', 'font="Regular;22" position="545,533" size="500,27"']) # ZZZ1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,616" size="393,38"', 'font="Regular;22" position="545,623" size="393,27"']) # ZZZ1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="438,614" size="472,38"', 'font="Regular;22" position="438,621" size="472,27"']) # ZZ2, ZZ3 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="510,666" size="437,38"', 'font="Regular;22" position="510,673" size="437,27"']) # ZZ3 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,614" size="481,38"', 'font="Regular;22" position="430,621" size="481,27"']) # X2, X3, Z1, Z2 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,666" size="481,38"', 'font="Regular;22" position="430,673" size="481,27"']) # X2, X3, Z1, Z2 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,558" size="481,38"', 'font="Regular;22" position="430,565" size="481,27"']) # X1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,649" size="481,38"', 'font="Regular;22" position="430,656" size="481,27"']) # X1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,584" size="708,38"', 'font="Regular;22" position="199,591" size="708,27"']) # no picon now
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,636" size="708,38"', 'font="Regular;22" position="199,643" size="708,27"']) # no picon next
		elif config.plugins.KravenVB.IBFontSize.value == "size-26":
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,553" size="500,38"', 'font="Regular;26" position="545,556" size="500,33"']) # ZZ1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,643" size="393,38"', 'font="Regular;26" position="545,646" size="393,33"']) # ZZ1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,526" size="500,38"', 'font="Regular;26" position="545,529" size="500,33"']) # ZZZ1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="545,616" size="393,38"', 'font="Regular;26" position="545,619" size="393,33"']) # ZZZ1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="438,614" size="472,38"', 'font="Regular;26" position="438,617" size="472,33"']) # ZZ2, ZZ3 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="510,666" size="437,38"', 'font="Regular;26" position="510,669" size="437,33"']) # ZZ3 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,614" size="481,38"', 'font="Regular;26" position="430,617" size="481,33"']) # X2, X3, Z1, Z2 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,666" size="481,38"', 'font="Regular;26" position="430,669" size="481,33"']) # X2, X3, Z1, Z2 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,558" size="481,38"', 'font="Regular;26" position="430,561" size="481,33"']) # X1 now
			self.skinSearchAndReplace.append(['font="Regular;30" position="430,649" size="481,38"', 'font="Regular;26" position="430,652" size="481,33"']) # X1 next
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,584" size="708,38"', 'font="Regular;26" position="199,587" size="708,33"']) # no picon now
			self.skinSearchAndReplace.append(['font="Regular;30" position="199,636" size="708,38"', 'font="Regular;26" position="199,639" size="708,33"']) # no picon next

		### ChannelSelection (Servicename, Servicenumber, Serviceinfo) Font-Size
		if self.E2DistroVersion == "VTi":
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
				self.skinSearchAndReplace.append([self.Templates + 'name="CSLEPG22"/>', self.Templates + 'name="CSLEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSLEPG22"/>', self.Templates + 'name="CSLEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSLEPG22"/>', self.Templates + 'name="CSLEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv33":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSEPEPG22"/>', self.Templates + 'name="CSEPEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSEPEPG22"/>', self.Templates + 'name="CSEPEPG324"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSEPEPG22"/>', self.Templates + 'name="CSEPEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv4":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSREPG22"/>', self.Templates + 'name="CSREPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSREPG22"/>', self.Templates + 'name="CSREPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSREPG22"/>', self.Templates + 'name="CSREPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv2":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT2EPG22"/>', self.Templates + 'name="CSMT2EPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT2EPG22"/>', self.Templates + 'name="CSMT2EPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT2EPG22"/>', self.Templates + 'name="CSMT2EPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv22":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT22EPG22"/>', self.Templates + 'name="CSMT22EPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT22EPG22"/>', self.Templates + 'name="CSMT22EPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMT22EPG22"/>', self.Templates + 'name="CSMT22EPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNEPG19"/>', self.Templates + 'name="CSNEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNEPG19"/>', self.Templates + 'name="CSNEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNEPG19"/>', self.Templates + 'name="CSNEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile2":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSN2EPG19"/>', self.Templates + 'name="CSN2EPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSN2EPG19"/>', self.Templates + 'name="CSN2EPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSN2EPG19"/>', self.Templates + 'name="CSN2EPG19Prime"/>'])
		elif self.actChannelselectionstyle in ("channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPG19"/>', self.Templates + 'name="CSNMTEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPG19"/>', self.Templates + 'name="CSNMTEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPG19"/>', self.Templates + 'name="CSNMTEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nobile-minitv33":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPEPG19"/>', self.Templates + 'name="CSNMTEPEPG22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPEPG19"/>', self.Templates + 'name="CSNMTEPEPG22"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize1.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNMTEPEPG19"/>', self.Templates + 'name="CSNMTEPEPG19Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nopicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNPEPG22"/>', self.Templates + 'name="CSNPEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNPEPG22"/>', self.Templates + 'name="CSNPEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNPEPG22"/>', self.Templates + 'name="CSNPEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-nopicon2":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNP2EPG22"/>', self.Templates + 'name="CSNP2EPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNP2EPG22"/>', self.Templates + 'name="CSNP2EPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSNP2EPG22"/>', self.Templates + 'name="CSNP2EPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-xpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSXEPG22"/>', self.Templates + 'name="CSXEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSXEPG22"/>', self.Templates + 'name="CSXEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSXEPG22"/>', self.Templates + 'name="CSXEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZEPG22"/>', self.Templates + 'name="CSZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZEPG22"/>', self.Templates + 'name="CSZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZEPG22"/>', self.Templates + 'name="CSZEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zzpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZEPG22"/>', self.Templates + 'name="CSZZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZEPG22"/>', self.Templates + 'name="CSZZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZEPG22"/>', self.Templates + 'name="CSZZEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-zzzpicon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZZEPG22"/>', self.Templates + 'name="CSZZZEPG24Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZZEPG22"/>', self.Templates + 'name="CSZZZEPG24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSZZZEPG22"/>', self.Templates + 'name="CSZZZEPG22Prime"/>'])
		elif self.actChannelselectionstyle == "channelselection-style-minitv-picon":
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMTP22"/>', self.Templates + 'name="CSMTP22Prime"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "none" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMTP22"/>', self.Templates + 'name="CSMTP24"/>'])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-on" and config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
				self.skinSearchAndReplace.append([self.Templates + 'name="CSMTP22"/>', self.Templates + 'name="CSMTP24Prime"/>'])

		### ChannelSelection horizontal Primetime
		if self.E2DistroVersion == "VTi" and config.plugins.KravenVB.alternativeChannellist.value == "on" and config.plugins.KravenVB.ChannelSelectionHorStyle.value == "cshor-minitv" and config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
			self.skinSearchAndReplace.append([self.Templates + 'name="CSHORMT"/>', self.Templates + 'name="CSHORMTPrime"/>'])

		### ChannelSelection 'not available' Font
		self.skinSearchAndReplace.append(['name="KravenNotAvailable" value="#00FFEA04', 'name="KravenNotAvailable" value="#00' + config.plugins.KravenVB.ChannelSelectionServiceNA.value])

		### GraphMultiEPG colors
		if config.plugins.KravenVB.GMESelFg.value == "global":
			self.skinSearchAndReplace.append(['name="KravenGMESelFg" value="#00ffffff', 'name="KravenGMESelFg" value="#00' + config.plugins.KravenVB.SelectionFont.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenGMESelFg" value="#00ffffff', 'name="KravenGMESelFg" value="#00' + config.plugins.KravenVB.GMESelFg.value])
		if config.plugins.KravenVB.GMESelBg.value == "global":
			self.skinSearchAndReplace.append(['name="KravenGMESelBg" value="#00389416', 'name="KravenGMESelBg" value="#00' + config.plugins.KravenVB.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenGMESelBg" value="#00389416', 'name="KravenGMESelBg" value="#00' + config.plugins.KravenVB.GMESelBg.value])
		if config.plugins.KravenVB.GMENowFg.value == "global":
			self.skinSearchAndReplace.append(['name="KravenGMENowFg" value="#00F0A30A', 'name="KravenGMENowFg" value="#00' + config.plugins.KravenVB.SelectionFont.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenGMENowFg" value="#00F0A30A', 'name="KravenGMENowFg" value="#00' + config.plugins.KravenVB.GMENowFg.value])
		if config.plugins.KravenVB.GMENowBg.value == "global":
			self.skinSearchAndReplace.append(['name="KravenGMENowBg" value="#00389416', 'name="KravenGMENowBg" value="#00' + config.plugins.KravenVB.SelectionBackground.value])
		else:
			self.skinSearchAndReplace.append(['name="KravenGMENowBg" value="#00389416', 'name="KravenGMENowBg" value="#00' + config.plugins.KravenVB.GMENowBg.value])
		self.skinSearchAndReplace.append(['name="KravenGMEBorder" value="#00ffffff', 'name="KravenGMEBorder" value="#00' + config.plugins.KravenVB.GMEBorder.value])

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
				self.skinSearchAndReplace.append(["infobar-icons", "icons-dark"])
			elif config.plugins.KravenVB.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["infobar-icons", "icons-light"])
		elif config.plugins.KravenVB.IBColor.value == "all-screens":
			if config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["/global-icons/", "/icons-light/"])
			if config.plugins.KravenVB.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenIcon" value="#00fff0e0"', 'name="KravenIcon" value="#00000000"'])
				self.skinSearchAndReplace.append(["infobar-icons", "icons-dark"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-dark/"])
			elif config.plugins.KravenVB.IconStyle.value == "icons-light":
				self.skinSearchAndReplace.append(["infobar-icons", "icons-light"])
				self.skinSearchAndReplace.append(["/infobar-global-icons/", "/icons-light/"])

		if config.plugins.KravenVB.IconStyle2.value == "icons-light2":
			system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/icons-white.tar.gz -C /usr/share/enigma2/KravenVB/")
		else:
			system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/icons-black.tar.gz -C /usr/share/enigma2/KravenVB/")

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
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress270.png"',' pixmap="KravenVB/progress/progress270_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"',' pixmap="KravenVB/progress/progress300_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"',' pixmap="KravenVB/progress/progress328_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"',' pixmap="KravenVB/progress/progress370_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"',' pixmap="KravenVB/progress/progress380_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"',' pixmap="KravenVB/progress/progress410_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress480.png"',' pixmap="KravenVB/progress/progress480_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"',' pixmap="KravenVB/progress/progress581_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"',' pixmap="KravenVB/progress/progress599_2.png"'])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress657.png"',' pixmap="KravenVB/progress/progress657_2.png"'])
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
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress270.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress480.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress657.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress708.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress749.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress858.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress888.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress990.png"'," "])
			self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress1265.png"'," "])
			self.skinSearchAndReplace.append(['name="KravenProgress" value="#00C3461B', 'name="KravenProgress" value="#00' + config.plugins.KravenVB.Progress.value])

		### Border
		self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#00' + config.plugins.KravenVB.Border.value])

		### MiniTV Border
		self.skinSearchAndReplace.append(['name="KravenBorder2" value="#003F3F3F', 'name="KravenBorder2" value="#00' + config.plugins.KravenVB.MiniTVBorder.value])

		### NumberZap Border
		if not config.plugins.KravenVB.NumberZapExt.value == "none":
			self.skinSearchAndReplace.append(['name="KravenNZBorder" value="#00ffffff', 'name="KravenNZBorder" value="#00' + config.plugins.KravenVB.NZBorder.value])

		### Line
		self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#00' + config.plugins.KravenVB.Line.value])

		### Runningtext
		if config.plugins.KravenVB.RunningText.value == "none":
			self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
		else:
			self.skinSearchAndReplace.append(["startdelay=5000", config.plugins.KravenVB.RunningText.value])
			
			# vertical RunningText
			self.skinSearchAndReplace.append(["steptime=90", config.plugins.KravenVB.RunningTextSpeed.value])
			
			# horizontal RunningText
			if config.plugins.KravenVB.RunningTextSpeed.value == "steptime=200":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=66"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=100":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=33"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=66":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=22"])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=50":
				self.skinSearchAndReplace.append(["steptime=80", "steptime=17"])

		### Scrollbar
		if self.E2DistroVersion == "VTi":
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="0"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="10"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="15"'])
		elif self.E2DistroVersion in ("openatv","teamblue"):
			if config.plugins.KravenVB.ScrollBar2.value == "showOnDemand":
				self.skinSearchAndReplace.append(['scrollbarMode="showNever"', 'scrollbarMode="showOnDemand"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', ''])
			else:
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', ''])
					
		### Scrollbar - showNever
		self.skinSearchAndReplace.append(['scrollbarMode="never"', 'scrollbarMode="showNever"'])

		### Selectionborder
		if not config.plugins.KravenVB.SelectionBorderList.value == "none":
			self.makeborsetpng(config.plugins.KravenVB.SelectionBorder.value)

		### IB Color visible
		if config.plugins.KravenVB.IBColor.value == "only-infobar":
			self.skinSearchAndReplace.append(['backgroundColor="KravenMbg"', 'backgroundColor="Kravenbg"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont1"', 'foregroundColor="KravenFont1"'])
			self.skinSearchAndReplace.append(['foregroundColor="KravenMFont2"', 'foregroundColor="KravenFont2"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cs"/>', " "])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cooltv"/>', " "])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-emc"/>', " "])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-wrr"/>', " "])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split1"/>', " "])
			self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split2"/>', " "])
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

					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cs"/>', self.Templates + 'name="box2-cs"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cooltv"/>', self.Templates + 'name="box2-cooltv"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-emc"/>', self.Templates + 'name="box2-emc"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-wrr"/>', self.Templates + 'name="box2-wrr"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split1"/>', self.Templates + 'name="box2-split1"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split2"/>', self.Templates + 'name="box2-split2"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					menubox = """<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,640" size="1280,80" zPosition="-9" alphatest="blend" />
	<eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	<ePixmap pixmap="KravenVB/graphics/ibtexture.png" position="0,0" size="1280,59" zPosition="-9" alphatest="blend" />
	<eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
					self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menubox])

					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cs"/>', self.Templates + 'name="texture-cs"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cooltv"/>', self.Templates + 'name="texture-cooltv"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-emc"/>', self.Templates + 'name="texture-emc"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-wrr"/>', self.Templates + 'name="texture-wrr"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split1"/>', self.Templates + 'name="texture-split1"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split2"/>', self.Templates + 'name="texture-split2"/>'])
				else:
					menubox = """<eLabel position="0,640" size="1280,80" backgroundColor="KravenIBbg2" zPosition="-9" />
	  <eLabel position="0,640" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />
	  <eLabel position="0,0" size="1280,59" backgroundColor="KravenIBbg2" zPosition="-9" />
	  <eLabel position="0,58" size="1280,2" backgroundColor="KravenIBLine" zPosition="-8" />"""
					self.skinSearchAndReplace.append(['<!-- Menu ibar -->', menubox])

					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cs"/>', self.Templates + 'name="box-cs"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-cooltv"/>', self.Templates + 'name="box-cooltv"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-emc"/>', self.Templates + 'name="box-emc"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-wrr"/>', self.Templates + 'name="box-wrr"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split1"/>', self.Templates + 'name="box-split1"/>'])
					self.skinSearchAndReplace.append([self.Templates + 'name="gradient-split2"/>', self.Templates + 'name="box-split2"/>'])

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
	  <ePixmap pixmap="KravenVB/graphics/ibaro2.png" position="0,0" size="1280,165" alphatest="blend" zPosition="-9" />"""
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

		### Tuner
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zzz1"):

			### Tuner Colors
			self.skinSearchAndReplace.append(['name="KravenTunerBusy" value="#00CCCC00', 'name="KravenTunerBusy" value="#00' + config.plugins.KravenVB.TunerBusy.value])
			self.skinSearchAndReplace.append(['name="KravenTunerLive" value="#0000B400', 'name="KravenTunerLive" value="#00' + config.plugins.KravenVB.TunerLive.value])
			self.skinSearchAndReplace.append(['name="KravenTunerRecord" value="#00FF0C00', 'name="KravenTunerRecord" value="#00' + config.plugins.KravenVB.TunerRecord.value])
			self.skinSearchAndReplace.append(['name="KravenTunerXtremeBusy" value="#001BA1E2', 'name="KravenTunerXtremeBusy" value="#00' + config.plugins.KravenVB.TunerXtremeBusy.value])

			### Show unused Tuners
			if config.plugins.KravenVB.ShowUnusedTuner.value == "none":
				self.skinSearchAndReplace.append([',ShowUnused', ''])

			### Set align for Tuners
			if not config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append([',RightAlign2', ''])
				self.skinSearchAndReplace.append([',RightAlign4', ''])
				self.skinSearchAndReplace.append([',RightAlign8', ''])

		### SecondInfobar Font- and Textsize
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
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

		### Clock Analog Style
		self.analogstylecolor = config.plugins.KravenVB.AnalogStyle.value
		self.analog = ("analog_" + self.analogstylecolor + ".png")
		self.skinSearchAndReplace.append(["analog.png", self.analog])

		### HelpMenu
		if self.E2DistroVersion in ("openatv","teamblue"):
			self.skinSearchAndReplace.append(['skin_default/rc_vu_1.png,skin_default/rc_vu_2.png,skin_default/rc_vu_3.png,skin_default/rc_vu_4.png,skin_default/rc_vu_5.png', 'skin_default/rc.png,skin_default/rcold.png'])

		### KravenIconVPosition
		if self.E2DistroVersion in ("openatv","teamblue"):
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
				self.skinSearchAndReplace.append([',687" name="KravenIconVPosition"', ',685"'])
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append([',692" name="KravenIconVPosition"', ',690"'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
				self.skinSearchAndReplace.append([',690" name="KravenIconVPosition"', ',688"'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				self.skinSearchAndReplace.append([',23" name="KravenIconVPosition"', ',21"'])
			self.skinSearchAndReplace.append([',680" name="KravenIconVPosition"', ',678"']) # Players
		else:
			VPos_list = [23, 680, 687, 690, 692]
			for i in VPos_list:
				VPos_old = str(i)
				if config.plugins.KravenVB.KravenIconVPosition.value == "vposition-3":
					VPos_new = str(i -3)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition-2":
					VPos_new = str(i -2)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition-1":
					VPos_new = str(i -1)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition0":
					VPos_new = str(i)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition+1":
					VPos_new = str(i +1)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition+2":
					VPos_new = str(i +2)
				elif config.plugins.KravenVB.KravenIconVPosition.value == "vposition+3":
					VPos_new = str(i +3)
				self.skinSearchAndReplace.append([',' + VPos_old + '" name="KravenIconVPosition"', ',' + VPos_new + '"'])

		### Channellist-EPGList - VTi
		if self.E2DistroVersion == "VTi" and config.plugins.KravenVB.alternativeChannellist.value == "none":
			if config.plugins.KravenVB.ChannellistEPGList.value == "channellistepglist-on":
				if self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
					self.skinSearchAndReplace.append(['alias name="EPGListChannelList0" font="Regular" size="23"', 'alias name="EPGListChannelList0" font="Regular" size="19"'])
					self.skinSearchAndReplace.append(['alias name="EPGListChannelList1" font="Regular" size="23"', 'alias name="EPGListChannelList1" font="Regular" size="19"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistText0" value="2,1,32,28"', 'parameter name="EPGServicelistText0" value="2,1,26,25"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistText1" value="34,1,66,28"', 'parameter name="EPGServicelistText1" value="28,1,54,25"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistText2" value="110,1,62,28"', 'parameter name="EPGServicelistText2" value="92,1,50,25"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecImage" value="170,5,20,20"', 'parameter name="EPGServicelistRecImage" value="146,4,20,20"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecText" value="187,1,600,28"', 'parameter name="EPGServicelistRecText" value="163,1,600,25"'])
					self.skinSearchAndReplace.append(['parameter name="EPGServicelistNonRecText" value="170,1,600,28"', 'parameter name="EPGServicelistNonRecText" value="146,1,600,25"'])
					if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
						self.skinSearchAndReplace.append(['<!--ChannellistEPGList-P', '<widget'])
						self.skinSearchAndReplace.append(['ChannellistEPGList-P-->', '/>'])
					else:
						self.skinSearchAndReplace.append(['<!--ChannellistEPGList-NP', '<widget'])
						self.skinSearchAndReplace.append(['ChannellistEPGList-NP-->', '/>'])
				elif self.actChannelselectionstyle == "channelselection-style-minitv22":
					if config.plugins.KravenVB.ChannelSelectionEPGSize2.value == "small":
						self.skinSearchAndReplace.append(['alias name="EPGListChannelList0" font="Regular" size="23"', 'alias name="EPGListChannelList0" font="Regular" size="21"'])
						self.skinSearchAndReplace.append(['alias name="EPGListChannelList1" font="Regular" size="23"', 'alias name="EPGListChannelList1" font="Regular" size="21"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText0" value="2,1,32,28"', 'parameter name="EPGServicelistText0" value="2,1,28,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText1" value="34,1,66,28"', 'parameter name="EPGServicelistText1" value="30,1,58,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText2" value="110,1,62,28"', 'parameter name="EPGServicelistText2" value="98,1,54,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecImage" value="170,5,20,20"', 'parameter name="EPGServicelistRecImage" value="154,4,20,20"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecText" value="187,1,600,28"', 'parameter name="EPGServicelistRecText" value="171,1,600,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistNonRecText" value="170,1,600,28"', 'parameter name="EPGServicelistNonRecText" value="154,1,600,25"'])
						if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-SP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-SP-->', '/>'])
						else:
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-SNP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-SNP-->', '/>'])
					else:
						if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-BP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-BP-->', '/>'])
						else:
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-BNP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-BNP-->', '/>'])
				else:
					if config.plugins.KravenVB.ChannelSelectionEPGSize3.value == "small":
						self.skinSearchAndReplace.append(['alias name="EPGListChannelList0" font="Regular" size="23"', 'alias name="EPGListChannelList0" font="Regular" size="21"'])
						self.skinSearchAndReplace.append(['alias name="EPGListChannelList1" font="Regular" size="23"', 'alias name="EPGListChannelList1" font="Regular" size="21"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText0" value="2,1,32,28"', 'parameter name="EPGServicelistText0" value="2,1,28,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText1" value="34,1,66,28"', 'parameter name="EPGServicelistText1" value="30,1,58,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistText2" value="110,1,62,28"', 'parameter name="EPGServicelistText2" value="98,1,54,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecImage" value="170,5,20,20"', 'parameter name="EPGServicelistRecImage" value="154,4,20,20"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistRecText" value="187,1,600,28"', 'parameter name="EPGServicelistRecText" value="171,1,600,25"'])
						self.skinSearchAndReplace.append(['parameter name="EPGServicelistNonRecText" value="170,1,600,28"', 'parameter name="EPGServicelistNonRecText" value="154,1,600,25"'])
						if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-SP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-SP-->', '/>'])
						else:
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-SNP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-SNP-->', '/>'])
					else:
						if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-BP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-BP-->', '/>'])
						else:
							self.skinSearchAndReplace.append(['<!--ChannellistEPGList-BNP', '<widget'])
							self.skinSearchAndReplace.append(['ChannellistEPGList-BNP-->', '/>'])
			else:
				self.skinSearchAndReplace.append(['<!--ChannellistSingleEpgList', '<widget'])
				self.skinSearchAndReplace.append(['ChannellistSingleEpgList-->', 'widget>'])
		elif self.E2DistroVersion in ("openatv","teamblue"):
			self.skinSearchAndReplace.append(['<!--ChannellistSingleEpgList', '<widget'])
			self.skinSearchAndReplace.append(['ChannellistSingleEpgList-->', 'widget>'])

		### NumericalTextInputHelpDialog (HelpWindow)
		if self.E2DistroVersion in ("VTi","teamblue"):
			self.skinSearchAndReplace.append(['<widget name="HelpWindow" position="900,346" size="261,262" zPosition="98" transparent="1" alphatest="blend" />', ' '])

		### delete Font-Shadow if Channelname is inside the box
		if config.plugins.KravenVB.IBStyle.value == "box" and config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3","infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['backgroundColor="KravenNamebg"', 'backgroundColor="KravenIBbg"'])

		### Infobar - ecm-info
		if config.plugins.KravenVB.FTA.value == "none":
			self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

		### EPGSelection EPGList
		if self.E2DistroVersion == "VTi":
			if config.plugins.KravenVB.EPGListSize.value == "big":
				self.skinSearchAndReplace.append(['alias name="EPGList0" font="Regular" size="22"', 'alias name="EPGList0" font="Regular" size="24"']) # EPGList (Fontsize)
				self.skinSearchAndReplace.append(['alias name="EPGList1" font="Regular" size="22"', 'alias name="EPGList1" font="Regular" size="24"'])
				
				self.skinSearchAndReplace.append(['font="Regular;22" itemHeight="EPGSelection"', 'itemHeight="36"']) # EPGSelection (itemHeight)
				self.skinSearchAndReplace.append(['parameter name="EPGlistText1" value="2,1,32,27"', 'parameter name="EPGlistText1" value="2,3,40,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistText2" value="39,1,162,27"', 'parameter name="EPGlistText2" value="46,3,180,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistRecImage" value="214,5,20,20"', 'parameter name="EPGlistRecImage" value="240,8,20,20"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistRecText" value="240,1,466,27"', 'parameter name="EPGlistRecText" value="266,3,440,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistNonRecText" value="214,1,492,27"', 'parameter name="EPGlistNonRecText" value="240,3,466,30"'])
				
				self.skinSearchAndReplace.append(['itemHeight="EPGSearch"', 'itemHeight="72"']) # EPGSearch (itemHeight)
				self.skinSearchAndReplace.append(['parameter name="EPGlistText3" value="214,1,492,27"', 'parameter name="EPGlistText3" value="240,2,466,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGSearchItemHeightBig" value="60"', 'parameter name="EPGSearchItemHeightBig" value="72"'])
				self.skinSearchAndReplace.append(['parameter name="EPGSearchItemHeightDefault" value="30"', 'parameter name="EPGSearchItemHeightDefault" value="36"'])
				
				self.skinSearchAndReplace.append(['itemHeight="EPGSelectionMulti"', 'itemHeight="36"']) # EPGSelectionMulti (itemHeight)
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiRecIcon" value="2,5,20,20"', 'parameter name="EPGlistMultiRecIcon" value="2,8,20,20"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiRecText" value="26,1,123,27"', 'parameter name="EPGlistMultiRecText" value="26,3,148,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiNonRecText" value="3,1,146,27"', 'parameter name="EPGlistMultiNonRecText" value="2,3,176,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiBeginText1" value="155,2,185,27"', 'parameter name="EPGlistMultiBeginText1" value="184,3,222,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiBeginText2" value="346,2,832,27"', 'parameter name="EPGlistMultiBeginText2" value="412,3,766,30"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiProgress" value="210,11,33,8"', 'parameter name="EPGlistMultiProgress" value="240,13,33,10"'])
				self.skinSearchAndReplace.append(['parameter name="EPGlistMultiProgressText" value="250,2,928,27"', 'parameter name="EPGlistMultiProgressText" value="280,3,898,30"'])
				
				self.skinSearchAndReplace.append(['parameter name="EPGlistEPGBarText1" value="27,1,469,27"', 'parameter name="EPGlistEPGBarText1" value="27,0,469,30"']) # EPGSelectionEPGBar_HD
				self.skinSearchAndReplace.append(['parameter name="EPGlistEPGBarText2" value="2,1,494,27"', 'parameter name="EPGlistEPGBarText2" value="2,0,494,30"'])
				
			else:
				self.skinSearchAndReplace.append(['font="Regular;22" itemHeight="EPGSelection"', 'itemHeight="30"']) # EPGSelection (itemHeight)
				self.skinSearchAndReplace.append(['itemHeight="EPGSearch"', 'itemHeight="60"']) # EPGSearch (itemHeight)
				self.skinSearchAndReplace.append(['itemHeight="EPGSelectionMulti"', 'itemHeight="30"']) # EPGSelectionMulti (itemHeight)
				
		elif self.E2DistroVersion == "openatv":
			if config.plugins.KravenVB.EPGListSize.value == "big":
				self.skinSearchAndReplace.append(['font="Regular;22" itemHeight="EPGSelection"', 'font="Regular;24" itemHeight="36"']) # EPGSelection (Fontsize and itemHeight)
				self.skinSearchAndReplace.append(['font="Regular;22" itemHeight="EPGSearch"', 'font="Regular;24" itemHeight="36"']) # EPGSearch (Fontsize and itemHeight)
				self.skinSearchAndReplace.append(['font="Regular;22" itemHeight="EPGSelectionMulti"', 'font="Regular;24" itemHeight="36"']) # EPGSelectionMulti (Fontsize and itemHeight)
			else:
				self.skinSearchAndReplace.append(['itemHeight="EPGSelection"', 'itemHeight="30"']) # EPGSelection (itemHeight)
				self.skinSearchAndReplace.append(['itemHeight="EPGSearch"', 'itemHeight="30"']) # EPGSearch (itemHeight)
				self.skinSearchAndReplace.append(['itemHeight="EPGSelectionMulti"', 'itemHeight="30"']) # EPGSelectionMulti (itemHeight)
				
		elif self.E2DistroVersion == "teamblue":
			if config.plugins.KravenVB.EPGListSize.value == "big":
				self.skinSearchAndReplace.append(['teamBlueEPGListSkinParameter="EPGSelection_EPGSearch"', 'setEventItemFont="Regular;26" setEventTimeFont="Regular;21" setTimeWidth="104" setIconDistance="8" setIconShift="0" setColWidths="58,138" setColGap="10" itemHeight="35" position="70,80" size="708,525"']) # EPGSelection, EPGSearch
				self.skinSearchAndReplace.append(['teamBlueEPGListSkinParameter="EPGSelectionMulti"', 'setEventItemFont="Regular;26" setEventTimeFont="Regular;21" setTimeWidth="104" setIconDistance="8" setIconShift="0" setColWidths="230,115" setColGap="10" itemHeight="35" position="50,135" size="1180,350"']) # EPGSelectionMulti
			else:
				self.skinSearchAndReplace.append(['teamBlueEPGListSkinParameter="EPGSelection_EPGSearch"', 'setEventItemFont="Regular;22" setEventTimeFont="Regular;18" setTimeWidth="90" setIconDistance="8" setIconShift="0" setColWidths="50,120" setColGap="10" itemHeight="30" position="70,80" size="708,540"']) # EPGSelection, EPGSearch
				self.skinSearchAndReplace.append(['teamBlueEPGListSkinParameter="EPGSelectionMulti"', 'setEventItemFont="Regular;22" setEventTimeFont="Regular;18" setTimeWidth="90" setIconDistance="8" setIconShift="0" setColWidths="200,100" setColGap="10" itemHeight="30" position="50,135" size="1180,360"']) # EPGSelectionMulti

		### Infobar typewriter effect
		if config.plugins.KravenVB.TypeWriter.value == "runningtext":
			self.skinSearchAndReplace.append(['render="KravenVBEmptyEpg"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',' + config.plugins.KravenVB.RunningTextSpeed.value + ',wrap=0,always=0,repeat=2,oneshot=1"'])
		elif config.plugins.KravenVB.TypeWriter.value == "none":
			self.skinSearchAndReplace.append(['render="KravenVBEmptyEpg"', 'render="KravenVBEmptyEpg2"'])

		### VTi MovieList-Picon
		if self.E2DistroVersion == "VTi":
			if (not self.silent and config.usage.movielist_show_picon.value == True) or (self.silent and 'config.usage.movielist_show_picon=true' in self.E2settings):
				self.skinSearchAndReplace.append(['<parameter name="MovieListMinimalVTITitle" value="27,0,620,27" />', '<parameter name="MovieListMinimalVTITitle" value="27,0,535,27" />'])

		### Header begin
		self.appendSkinFile(self.daten + "header-begin.xml")

		### Listselection-Border
		if not config.plugins.KravenVB.SelectionBorderList.value == "none":
			self.appendSkinFile(self.daten + "selectionborder.xml")

		### Header end
		self.appendSkinFile(self.daten + "header-end.xml")

		### Skinparameter
		self.appendSkinFile(self.daten + 'skinparameter_' + self.E2DistroVersion + '.xml')

		### Templates - constant-widgets / panels
		if self.E2DistroVersion == "teamblue":
			self.skinSearchAndReplace.append(['<constant-widgets>', '<!--/* Templates -->']) # customize template.xml for teamBlue - remove constant-widgets begin
			self.skinSearchAndReplace.append(['</constant-widgets>', '<!-- Templates */-->']) # customize template.xml for teamBlue - remove constant-widgets end
			self.skinSearchAndReplace.append(['constant-panels', 'screen']) # customize template-screens for teamBlue
			self.skinSearchAndReplace.append(['<constant-widget ', self.Templates]) # customize panels in xmls for teamBlue
		elif self.E2DistroVersion in ("VTi","openatv"):
			self.skinSearchAndReplace.append(['constant-panels', 'constant-widget']) # customize constant-widgets for VTi and openATV

		### Templates xml
		self.appendSkinFile(self.daten + 'templates-main.xml')
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
			self.appendSkinFile(self.daten + 'templates-' + config.plugins.KravenVB.InfobarStyle.value + '.xml')
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.appendSkinFile(self.daten + 'templates-infobar-style-x2-x3-z1-z2.xml')
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			self.appendSkinFile(self.daten + 'templates-infobar-style-zz1-zzz1.xml')
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
			self.appendSkinFile(self.daten + 'templates-infobar-style-zz2-zz3.xml')

		### ChannelSelection - horizontal RunningText
		if not self.BoxName == "solo2":
			if config.plugins.KravenVB.RunningTextSpeed.value == "steptime=200":
				self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',steptime=66,wrap=0,always=0,repeat=2,oneshot=1"'])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=100":
				self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',steptime=33,wrap=0,always=0,repeat=2,oneshot=1"'])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=66":
				self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',steptime=22,wrap=0,always=0,repeat=2,oneshot=1"'])
			elif config.plugins.KravenVB.RunningTextSpeed.value == "steptime=50":
				self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenVBRunningText" options="movetype=running,startpoint=0,' + config.plugins.KravenVB.RunningText.value + ',steptime=17,wrap=0,always=0,repeat=2,oneshot=1"'])
		else:
			self.skinSearchAndReplace.append(['render="RunningTextEmptyEpg2"', 'render="KravenVBEmptyEpg2"'])

		### ChannelSelection - VTi
		if self.E2DistroVersion == "VTi":
			self.skinSearchAndReplace.append(['name="giopet"', ' '])
			if config.plugins.KravenVB.alternativeChannellist.value == "none":
				self.appendSkinFile(self.daten + self.actChannelselectionstyle + ".xml")
				if not self.silent and self.actChannelselectionstyle in ("channelselection-style-minitv33","channelselection-style-nobile-minitv33","channelselection-style-minitv2","channelselection-style-minitv22"):
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
				elif not self.silent and self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv4","channelselection-style-nobile-minitv","channelselection-style-minitv-picon"):
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
				elif not self.silent and self.actChannelselectionstyle in ("channelselection-style-minitv3","channelselection-style-nobile-minitv3"):
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = False
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = False
					config.usage.use_extended_pig_channelselection.save()
					config.usage.servicelist_preview_mode.value = False
					config.usage.servicelist_preview_mode.save()
				elif not self.silent:
					config.usage.use_pig.value = True
					config.usage.use_pig.save()
					config.usage.use_extended_pig.value = False
					config.usage.use_extended_pig.save()
					config.usage.use_extended_pig_channelselection.value = False
					config.usage.use_extended_pig_channelselection.save()
				if not self.silent:
					config.usage.servicelist_alternative_mode.value = False
					config.usage.servicelist_alternative_mode.save()
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ChannelSelectionHorStyle.value + ".xml")
				if not self.silent:
					config.usage.servicelist_alternative_mode.value = True
					config.usage.servicelist_alternative_mode.save()
		
		### ChannelSelection - openatv
		elif self.E2DistroVersion == "openatv":
			if not self.silent:
				config.usage.servicelist_mode.value = "standard"
				config.usage.servicelist_mode.save()
			self.skinSearchAndReplace.append(['name="giopet"', 'fieldMargins="15" nonplayableMargins="15" itemsDistances="8" progressBarWidth="52" progressPercentWidth="80" progressbarHeight="10"'])
			if not self.silent and (self.actChannelselectionstyle in ("channelselection-style-nopicon","channelselection-style-nopicon2","channelselection-style-xpicon","channelselection-style-zpicon","channelselection-style-zzpicon","channelselection-style-zzzpicon","channelselection-style-minitv3","channelselection-style-nobile-minitv3") or config.plugins.KravenVB.ChannelSelectionMode.value == "zap"):
				config.usage.servicelistpreview_mode.value = False
			elif not self.silent:
				config.usage.servicelistpreview_mode.value = True
			if not self.silent:
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
		
		### ChannelSelection - teamblue
		elif self.E2DistroVersion == "teamblue":
			self.skinSearchAndReplace.append(['name="giopet"', ''])
			self.skinSearchAndReplace.append(['render="KravenVBPig3"', 'render="Pig"'])
			self.appendSkinFile(self.daten + self.actChannelselectionstyle + ".xml")

		### Infobar Clock
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->',self.Templates + 'name="infobar-style-x2-x3-z1-z2-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->',self.Templates + 'name="infobar-style-zz2-zz3-' + self.actClockstyle + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<!-- Infobar clockstyle -->',self.Templates + 'name="infobar-style-zz1-zzz1-' + self.actClockstyle + '"/>'])

		### Infobar Channelname
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon" and not config.plugins.KravenVB.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="infobar-style-nopicon-' + config.plugins.KravenVB.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" and not config.plugins.KravenVB.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="infobar-style-x1-' + config.plugins.KravenVB.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2") and not config.plugins.KravenVB.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="infobar-style-x2-x3-z1-z2-' + config.plugins.KravenVB.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" and not config.plugins.KravenVB.InfobarChannelName.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-' + config.plugins.KravenVB.InfobarChannelName.value + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3") and not config.plugins.KravenVB.InfobarChannelName2.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="infobar-style-zz2-zz3-' + config.plugins.KravenVB.InfobarChannelName2.value + '"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1" and not config.plugins.KravenVB.InfobarChannelName2.value == "none":
			self.skinSearchAndReplace.append(['<!-- Infobar channelname -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-' + config.plugins.KravenVB.InfobarChannelName2.value + '"/>'])

		### Infobar/SIB - ecm-info
		if config.plugins.KravenVB.ECMVisible.value in ("ib","ib+sib"):
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-ecminfo"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->',self.Templates + 'name="infobar-style-x2-x3-z1-z2-ecminfo"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->',self.Templates + 'name="infobar-style-zz2-zz3-ecminfo"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar ecminfo -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-ecminfo"/>'])

		if config.plugins.KravenVB.ECMVisible.value in ("sib","ib+sib"):
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-ecminfo"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->',self.Templates + 'name="infobar-style-x2-x3-z1-z2-ecminfo"/>'])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz2","infobar-style-zz3"):
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->',self.Templates + 'name="infobar-style-zz2-zz3-ecminfo"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- SIB ecminfo -->',self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-ecminfo"/>'])

		### Infobar weather-style
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-nopicon","infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zzz1"):
			self.actWeatherstyle = config.plugins.KravenVB.WeatherStyle.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				self.actWeatherstyle = config.plugins.KravenVB.WeatherStyle3.value
			else:
				self.actWeatherstyle = config.plugins.KravenVB.WeatherStyle2.value

		if self.actWeatherstyle == "weather-small":
			if config.plugins.KravenVB.IBStyle.value == "box":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="box2-weather-small"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="texture-weather-small"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="box-weather-small"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', self.Templates + 'name="weather-small2"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="gradient-weather-small"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', self.Templates + 'name="weather-small"/>'])

		elif self.actWeatherstyle == "weather-left":
			self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', self.Templates + 'name="weather-left"/>'])

		elif self.actWeatherstyle == "weather-big":
			if config.plugins.KravenVB.IBStyle.value == "box":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="box2-weather-big"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="texture-weather-big"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="box-weather-big"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar weatherbackground -->', self.Templates + 'name="gradient-weather-big"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar weatherstyle -->', self.Templates + 'name="weather-big"/>'])

		if config.plugins.KravenVB.refreshInterval.value == "0":
			config.plugins.KravenVB.refreshInterval.value = config.plugins.KravenVB.refreshInterval.default
			config.plugins.KravenVB.refreshInterval.save()

		### Infobar system-info
		if not config.plugins.KravenVB.SystemInfo.value == "none":
			if config.plugins.KravenVB.IBStyle.value == "box":
				if config.plugins.KravenVB.InfobarBoxColor.value == "gradient":
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->',self.Templates + 'name="box2-' + config.plugins.KravenVB.SystemInfo.value + '"/>'])
				elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->',self.Templates + 'name="texture-' + config.plugins.KravenVB.SystemInfo.value + '"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', self.Templates + 'name="box-' + config.plugins.KravenVB.SystemInfo.value + '"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfo -->', self.Templates + 'name="' + config.plugins.KravenVB.SystemInfo.value + '2"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfobackground -->', self.Templates + 'name="gradient-' + config.plugins.KravenVB.SystemInfo.value + '"/>'])
				self.skinSearchAndReplace.append(['<!-- Infobar systeminfo -->', self.Templates + 'name="' + config.plugins.KravenVB.SystemInfo.value + '"/>'])

		### Infobar
		# mainstyles
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar mainstyles -->', self.Templates + 'name="infobar-style-x2-x3-z1-z2"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- Infobar mainstyles -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '"/>'])

		# picon
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3"):
			self.skinSearchAndReplace.append(['<!-- Infobar picon -->', self.Templates + 'name="infobar-style-x2-x3-picon"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-z1","infobar-style-z2"):
			self.skinSearchAndReplace.append(['<!-- Infobar picon -->', self.Templates + 'name="infobar-style-z1-z2-picon"/>'])
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			if config.plugins.KravenVB.ShowAgcSnr.value == "on":
				self.skinSearchAndReplace.append(['<!-- Infobar picon -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-agc-snr"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar picon -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-picon"/>'])

		# tuners / some icons / Infobox
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-nopicon":
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', self.Templates + 'name="' + config.plugins.KravenVB.InfobarStyle.value + '-' + self.Tuners + '"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar icons -->', self.Templates + 'name="infobar-style-nopicon-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', self.Templates + 'name="infobar-style-nopicon-infobox-' + config.plugins.KravenVB.Infobox3.value + '"/>'])

		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', self.Templates + 'name="infobar-style-x1-' + self.Tuners + '"/>'])
			if self.E2DistroVersion == "VTi":
				self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', self.Templates + 'name="infobar-style-x1-infobox-' + config.plugins.KravenVB.Infobox.value + '"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', self.Templates + 'name="infobar-style-x1-infobox-' + config.plugins.KravenVB.Infobox2.value + '"/>'])

		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			self.skinSearchAndReplace.append(['<!-- Infobar topbaricons -->', self.Templates + 'name="infobar-style-x2-z1-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar topbartuners -->', self.Templates + 'name="infobar-style-x2-z1-' + self.Tuners + '"/>'])
			if self.E2DistroVersion == "VTi":
				self.skinSearchAndReplace.append(['<!-- Infobar topbarinfobox -->', self.Templates + 'name="infobar-style-x2-z1-infobox-' + config.plugins.KravenVB.Infobox.value + '"/>'])
			else:
				self.skinSearchAndReplace.append(['<!-- Infobar topbarinfobox -->', self.Templates + 'name="infobar-style-x2-z1-infobox-' + config.plugins.KravenVB.Infobox2.value + '"/>'])

		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			self.skinSearchAndReplace.append(['<!-- Infobar icons -->', self.Templates + 'name="infobar-style-zz1-zzz1-icons"/>'])
			self.skinSearchAndReplace.append(['<!-- Infobar tuners -->', self.Templates + 'name="infobar-style-zz1-zzz1-' + self.Tuners + '"/>'])
			self.actInfobox = ''
			if config.plugins.KravenVB.ShowAgcSnr.value == "on":
				self.actInfobox = config.plugins.KravenVB.Infobox3.value
			else:
				if self.E2DistroVersion == "VTi":
					self.actInfobox = config.plugins.KravenVB.Infobox.value
				else:
					self.actInfobox = config.plugins.KravenVB.Infobox2.value
			self.skinSearchAndReplace.append(['<!-- Infobar infobox -->', self.Templates + 'name="infobar-style-zz1-zzz1-infobox-' + self.actInfobox + '"/>'])

		### SecondInfobar
		if config.plugins.KravenVB.SIBFont.value == "sibfont-small":
			self.skinSearchAndReplace.append(['<!-- SIB style -->',self.Templates + 'name="' + config.plugins.KravenVB.SIB.value + '-small"/>'])
		else:
			self.skinSearchAndReplace.append(['<!-- SIB style -->',self.Templates + 'name="' + config.plugins.KravenVB.SIB.value + '"/>'])

		if config.plugins.KravenVB.SIB.value in ("sib4","sib5","sib6","sib7"):
			self.skinSearchAndReplace.append(['<!-- SIB extra -->',self.Templates + 'name="' + config.plugins.KravenVB.SIB.value + '-extra"/>'])

		### Players clockstyle
		self.skinSearchAndReplace.append(['<!-- Player clockstyle -->',self.Templates + 'name="' + config.plugins.KravenVB.PlayerClock.value + '"/>'])

		### Volume
		self.skinSearchAndReplace.append(['<!-- Volume style -->',self.Templates + 'name="' + config.plugins.KravenVB.Volume.value + '"/>'])
		if config.plugins.KravenVB.Volume.value == "volume-left":
			self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"','screen name="Volume" position="10,130" size="28,360"'])
		elif config.plugins.KravenVB.Volume.value == "volume-right":
			self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"','screen name="Volume" position="1240,130" size="28,360"'])
		elif config.plugins.KravenVB.Volume.value == "volume-top":
			self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"','screen name="Volume" position="center,25" size="400,28"'])
		elif config.plugins.KravenVB.Volume.value == "volume-center":
			self.skinSearchAndReplace.append(['screen name="Volume" position="47,38" size="330,80"','screen name="Volume" position="548,286" size="184,184"'])

		### PVRState
		if config.plugins.KravenVB.IBStyle.value == "box":
			if config.plugins.KravenVB.InfobarBoxColor.value in ("gradient","texture") and not config.plugins.KravenVB.PVRState.value == "pvrstate-off":
				if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate-box-' + config.plugins.KravenVB.InfobarBoxColor.value + '"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate2-box-' + config.plugins.KravenVB.InfobarBoxColor.value + '"/>'])
			if not config.plugins.KravenVB.InfobarBoxColor.value in ("gradient","texture") and not config.plugins.KravenVB.PVRState.value == "pvrstate-off":
				if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate-bg"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate2-bg"/>'])
		else:
			if not config.plugins.KravenVB.PVRState.value == "pvrstate-off":
				if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate-bg"/>'])
				else:
					self.skinSearchAndReplace.append(['<!-- PVRState background -->', self.Templates + 'name="pvrstate2-bg"/>'])

		if not config.plugins.KravenVB.PVRState.value == "pvrstate-off":
			self.skinSearchAndReplace.append(['<!-- PVRState style -->', self.Templates + 'name="' + config.plugins.KravenVB.PVRState.value + '"/>'])
			if config.plugins.KravenVB.PVRState.value == "pvrstate-center-big":
				self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="220,90"'])
			elif config.plugins.KravenVB.PVRState.value == "pvrstate-center-small":
				self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="center,center" size="110,45"'])
			elif config.plugins.KravenVB.PVRState.value == "pvrstate-left-small":
				self.skinSearchAndReplace.append(['screen name="PVRState" position="0,0" size="0,0"', 'screen name="PVRState" position="30,20" size="110,45"'])

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
				self.skinSearchAndReplace.append([self.Templates + 'name="timeshift-bg"/>', self.Templates + 'name="timeshift-bg-box2"/>'])
				self.skinSearchAndReplace.append([self.Templates + 'name="ibts-bg"/>', self.Templates + 'name="ibts-bg-box2"/>'])
				self.skinSearchAndReplace.append([self.Templates + 'name="autoresolution-bg"/>', self.Templates + 'name="autoresolution-bg-box2"/>'])
			elif config.plugins.KravenVB.InfobarBoxColor.value == "texture":
				self.skinSearchAndReplace.append([self.Templates + 'name="timeshift-bg"/>', self.Templates + 'name="timeshift-bg-texture"/>'])
				self.skinSearchAndReplace.append([self.Templates + 'name="ibts-bg"/>', self.Templates + 'name="ibts-bg-texture"/>'])
				self.skinSearchAndReplace.append([self.Templates + 'name="autoresolution-bg"/>', self.Templates + 'name="autoresolution-bg-texture"/>'])
			self.appendSkinFile(self.daten + "timeshift-ibts-ar.xml")

		### PermanentClock
		if config.plugins.KravenVB.PermanentClock.value == "permanentclock-infobar-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="KravenIBbg" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="permanentclock-infobar-big"/>', self.Templates + 'name="permanentclock-infobar-small"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-global-big":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="120,30"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="permanentclock-infobar-big"/>', self.Templates + 'name="permanentclock-global-big"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-global-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="Kravenbg" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="permanentclock-infobar-big"/>', self.Templates + 'name="permanentclock-global-small"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-transparent-big":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="120,30"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="permanentclock-infobar-big"/>', self.Templates + 'name="permanentclock-transparent-big"/>'])
		elif config.plugins.KravenVB.PermanentClock.value == "permanentclock-transparent-small":
			self.skinSearchAndReplace.append(['backgroundColor="KravenIBbg" name="PermanentClockScreen" size="120,30"', 'backgroundColor="transparent" name="PermanentClockScreen" size="80,20"'])
			self.skinSearchAndReplace.append([self.Templates + 'name="permanentclock-infobar-big"/>', self.Templates + 'name="permanentclock-transparent-small"/>'])

		### Plugins
		self.appendSkinFile(self.daten + "plugins.xml")

		### MSNWeatherPlugin XML
		if self.E2DistroVersion in ("openatv","teamblue"):
			if fileExists("/usr/lib/enigma2/python/Components/Converter/MSNWeather.pyo"):
				self.appendSkinFile(self.daten + "MSNWeatherPlugin.xml")
				if self.InternetAvailable and not fileExists("/usr/share/enigma2/KravenVB/msn_weather_icons/1.png"):
					system("wget -q http://picons.mynonpublic.com/msn-icon.tar.gz -O /tmp/msn-icon.tar.gz; tar xf /tmp/msn-icon.tar.gz -C /usr/share/enigma2/KravenVB/")
			else:
				self.appendSkinFile(self.daten + "MSNWeatherPlugin2.xml")

		### NetatmoBar
		if self.InternetAvailable:
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					if config.plugins.KravenVB.WeatherStyle3.value == "netatmobar":
						self.appendSkinFile(self.daten + "netatmobar.xml")

		### EMC (Event-Description) Font-Size
		if config.plugins.KravenVB.EMCStyle.value in ("emc-bigcover","emc-minitv"):
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcmbc22"/>', self.Templates + 'name="emcmbc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value in ("emc-bigcover2","emc-minitv2"):
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcm2bc222"/>', self.Templates + 'name="emcm2bc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-nocover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcnc22"/>', self.Templates + 'name="emcnc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-nocover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcnc222"/>', self.Templates + 'name="emcnc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-smallcover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcsc22"/>', self.Templates + 'name="emcsc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-smallcover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcsc222"/>', self.Templates + 'name="emcsc224"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-verybigcover":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcvbc22"/>', self.Templates + 'name="emcvbc24"/>'])
		elif config.plugins.KravenVB.EMCStyle.value == "emc-verybigcover2":
			if config.plugins.KravenVB.EMCEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="emcvbc222"/>', self.Templates + 'name="emcvbc224"/>'])

		### EMC (MovieList) Font-Colors
		self.skinSearchAndReplace.append(['UnwatchedColor="unwatched"', 'UnwatchedColor="#00' + config.plugins.KravenVB.UnwatchedColor.value + '"'])
		self.skinSearchAndReplace.append(['WatchingColor="watching"', 'WatchingColor="#00' + config.plugins.KravenVB.WatchingColor.value + '"'])
		self.skinSearchAndReplace.append(['FinishedColor="finished"', 'FinishedColor="#00' + config.plugins.KravenVB.FinishedColor.value + '"'])

		### EMC
		self.appendSkinFile(self.daten + config.plugins.KravenVB.EMCStyle.value + ".xml")

		### NumberZapExt
		self.appendSkinFile(self.daten + config.plugins.KravenVB.NumberZapExt.value + ".xml")
		if self.E2DistroVersion in ("VTi","openatv") and not self.silent and not config.plugins.KravenVB.NumberZapExt.value == "none":
			config.usage.numberzap_show_picon.value = True
			config.usage.numberzap_show_picon.save()
			config.usage.numberzap_show_servicename.value = True
			config.usage.numberzap_show_servicename.save()

		### SplitScreen
		if self.E2DistroVersion == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SplitScreen.value + ".xml")

		### FileCommander
		if self.E2DistroVersion == "openatv":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.FileCommander.value + ".xml")

		### TimerEditScreen
		if self.E2DistroVersion == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.TimerEditScreen.value + ".xml")
		elif self.E2DistroVersion in ("openatv","teamblue"):
			self.appendSkinFile(self.daten + "timer-openatv.xml")

		### TimerListStyle
		if not self.silent and self.E2DistroVersion == "VTi":
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

		### EPGSelection EPGSize
		if config.plugins.KravenVB.EPGSelectionEPGSize.value == "big":
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,329" size="418,270"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,329" size="418,270"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,294" size="418,297"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,294" size="418,300"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,115" size="418,486"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,115" size="418,480"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,80" size="418,532"', 'font="Regular;24" foregroundColor="KravenFont1" position="820,80" size="418,510"'])
		else:
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,329" size="418,270"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,329" size="418,270"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,294" size="418,297"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,294" size="418,297"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,115" size="418,486"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,115" size="418,486"'])
			self.skinSearchAndReplace.append(['font="Regular;22" foregroundColor="EPGSelection" position="820,80" size="418,532"', 'font="Regular;22" foregroundColor="KravenFont1" position="820,80" size="418,532"'])

		### EPGSelection xml
		if self.E2DistroVersion in ("VTi","openatv"):
			self.appendSkinFile(self.daten + config.plugins.KravenVB.EPGSelection.value + ".xml")
		elif self.E2DistroVersion == "teamblue":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.EPGSelection.value + "_teamblue.xml")

		### CoolTVGuide
		self.appendSkinFile(self.daten + config.plugins.KravenVB.CoolTVGuide.value + ".xml")

		### GraphMultiEPG (Event-Description) Font-Size
		if config.plugins.KravenVB.GMEDescriptionSize.value == "big":
			self.skinSearchAndReplace.append([self.Templates + 'name="GE22"/>', self.Templates + 'name="GE24"/>'])
			self.skinSearchAndReplace.append([self.Templates + 'name="GEMTR22"/>', self.Templates + 'name="GEMTR24"/>'])
			self.skinSearchAndReplace.append([self.Templates + 'name="GEMTL22"/>', self.Templates + 'name="GEMTL24"/>'])

		### GraphMultiEPG
		if self.E2DistroVersion == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.GraphMultiEPG.value + ".xml")
		elif self.E2DistroVersion == "openatv":
			if not self.silent and config.plugins.KravenVB.GraphicalEPG.value == "text":
				config.epgselection.graph_type_mode.value = False
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = False
				config.epgselection.graph_pig.save()
			elif not self.silent and config.plugins.KravenVB.GraphicalEPG.value == "text-minitv":
				config.epgselection.graph_type_mode.value = False
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = True
				config.epgselection.graph_pig.save()
			elif not self.silent and config.plugins.KravenVB.GraphicalEPG.value == "graphical":
				config.epgselection.graph_type_mode.value = "graphics"
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = False
				config.epgselection.graph_pig.save()
			elif not self.silent and config.plugins.KravenVB.GraphicalEPG.value == "graphical-minitv":
				config.epgselection.graph_type_mode.value = "graphics"
				config.epgselection.graph_type_mode.save()
				config.epgselection.graph_pig.value = True
				config.epgselection.graph_pig.save()
		elif self.E2DistroVersion == "teamblue":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.GraphMultiEPG.value + "_teamblue.xml")

		### VerticalEPG
		if self.E2DistroVersion == "VTi":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.VerticalEPG.value + ".xml")
		elif self.E2DistroVersion == "openatv":
			if not self.silent and config.plugins.KravenVB.VerticalEPG2.value == "verticalepg-full":
				config.epgselection.vertical_pig.value = False
				config.epgselection.vertical_pig.save()
			elif not self.silent and config.plugins.KravenVB.VerticalEPG2.value == "verticalepg-minitv3":
				config.epgselection.graph_pig.value = True
				config.epgselection.graph_pig.save()

		### MovieSelection (MovieList) Font-Size - teamblue
		if self.E2DistroVersion == "teamblue":
			self.skinSearchAndReplace.append(['name="MovieList-teamblue"', 'fontName="Regular" fontSizesOriginal="22,20,20" fontSizesCompact="22,20" fontSizesMinimal="22,20" itemHeights="90,54,30" pbarShift="7" pbarHeight="16" pbarLargeWidth="48" partIconeShiftMinimal="5" partIconeShiftCompact="5" partIconeShiftOriginal="5" spaceIconeText="4" iconsWidth="25" trashShift="3" dirShift="3" spaceRight="2" columnsOriginal="200,220" columnsCompactDescription="140,160,180" compactColumn="220" treeDescription="180"'])
		elif self.E2DistroVersion in ("VTi","openatv"):
			self.skinSearchAndReplace.append([' name="MovieList-teamblue" ', ' '])

		### MovieSelection (Event-Description) Font-Size
		if config.plugins.KravenVB.MovieSelection.value == "movieselection-no-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="msnc22"/>', self.Templates + 'name="msnc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-no-cover2":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="msnc222"/>', self.Templates + 'name="msnc224"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-small-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="mssc22"/>', self.Templates + 'name="mssc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-big-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="msbc22"/>', self.Templates + 'name="msbc24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-minitv":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="msm22"/>', self.Templates + 'name="msm24"/>'])
		elif config.plugins.KravenVB.MovieSelection.value == "movieselection-minitv-cover":
			if config.plugins.KravenVB.MovieSelectionEPGSize.value == "big":
				self.skinSearchAndReplace.append([self.Templates + 'name="msmc22"/>', self.Templates + 'name="msmc24"/>'])

		### MovieSelection
		self.appendSkinFile(self.daten + config.plugins.KravenVB.MovieSelection.value + ".xml")

		### SerienRecorder
		if config.plugins.KravenVB.SerienRecorder.value == "serienrecorder":
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SerienRecorder.value + ".xml")

		### MediaPortal
		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/skin.xml"):
			system("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/skin.xml")

		if self.E2DistroVersion in ("VTi","openatv"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenVB.MediaPortal.value == "mediaportal":
				if config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")

		elif self.E2DistroVersion == "teamblue":
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.py") and config.plugins.KravenVB.MediaPortal.value == "mediaportal":
				if config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_IB_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_box_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-light" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-light_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "grad":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_IB_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")
				elif config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle.value == "icons-dark" and config.plugins.KravenVB.IBStyle.value == "box":
					system("tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/MediaPortal_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/; tar xf /usr/lib/enigma2/python/Plugins/Extensions/KravenVB/data/Player_box_icons-dark_teamblue.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/simpleplayer/")

		if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB/MP_skin.xml") and not config.plugins.KravenVB.MediaPortal.value == "mediaportal":
			system("rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/skins_720/KravenVB")

		### vti - openatv - teamblue
		if self.E2DistroVersion == "VTi":
			self.appendSkinFile(self.daten + "vti.xml")
		elif self.E2DistroVersion == "openatv":
			self.appendSkinFile(self.daten + "openatv.xml")
		elif self.E2DistroVersion == "teamblue":
			self.appendSkinFile(self.daten + "teamblue.xml")

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
		if self.InternetAvailable:
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
		return 0

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

	def getBoxName(self):
		if fileExists("/proc/stb/info/vumodel"):
			file = open('/proc/stb/info/vumodel', 'r')
			boxname = file.readline().strip()
			file.close()
			return boxname
		else:
			try:
				from boxbranding import getMachineName
				return getMachineName()
			except ImportError:
				return "unknown"

	def getE2DistroVersion(self):
		try:
			from boxbranding import getImageDistro
			if getImageDistro() == "openatv":
				return "openatv"
			elif getImageDistro() == "teamblue":
				return "teamblue"
			elif getImageDistro() == "VTi":
				return "VTi"
		except ImportError:
			return "VTi"

	def getTemplates(self): # customize panels in plugin for teamBlue
		try:
			from boxbranding import getImageDistro
			if getImageDistro() == "openatv":
				return "<constant-widget "
			elif getImageDistro() == "teamblue":
				return "<panel "
			elif getImageDistro() == "VTi":
				return "<constant-widget "
		except ImportError:
			return "<constant-widget "

	def getTuners(self):
		from Components.Sources.TunerInfo import TunerInfo
		tinfo = TunerInfo()
		tuners = tinfo.getTunerAmount()
		if tuners is 1:
			return "1-tuner"
		elif tuners is 2:
			return "2-tuner"
		elif (3 <= tuners <= 4):
			return "4-tuner"
		elif (5 <= tuners):
			return "8-tuner"
		else:
			return "1-tuner"

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None, xShift=0, yShift=0):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		 
		xShift, yShift:
		 (optional) apply positive or negative change to all position tags in skin file
		"""

		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		if xShift != 0 or yShift != 0:		
			tempFileLines = []
			for skinLine in file_lines:
				startPos = skinLine.find(' position="')
				if startPos >=0:
					begLine = skinLine[:startPos+11]
					endLine = skinLine[startPos+11:]
					endPos = endLine.find('" ')
					position = endLine[:endPos]
					endLine  = endLine[endPos:]
					xpos = position.split(",")[0]
					ypos = position.split(",")[1]
					if xpos.isdigit() and ypos.isdigit():
						position = str(int(xpos) + xShift) + "," + str(int(ypos) + yShift)
					skinLine = begLine + position + endLine
				tempFileLines.append(skinLine)
			file_lines = tempFileLines		

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def getInternetAvailable(self):
		import ping
		r = ping.doOne("8.8.8.8",1.5)
		if r != None and r <= 1.5:
			return True
		else:
			return False

	def installIcons(self,author):

		if self.InternetAvailable==False: 
			return

		if self.E2DistroVersion == "VTi":
			print "VTI Image found. Use VTI Server"
			pathname="http://coolskins.de/downloads/kraven/"
		elif self.E2DistroVersion == "openatv":
			print "ATV Image found. Use ATV Server"
			pathname="http://picons.mynonpublic.com/"
		elif self.E2DistroVersion == "teamblue":
			print "teamBlue Image found. Use ATV Server"
			pathname="http://picons.mynonpublic.com/"
		else:
			print "No Icons found. Aborted"
			return

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

	def makeIbarColorGradientpng(self, newcolor, newtrans):

		width = 1280 # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder

		ibarheight = 310 # height of ibar
		ibargradientstart = 50 # start of ibar gradient (from top)
		ibargradientsize = 100 # size of ibar gradient

		ibaroheight = 165 # height of ibaro
		ibarogradientstart = 65 # start of ibaro gradient (from top)
		ibarogradientsize = 100 # size of ibaro gradient

		ibaro2height = 125 # height of ibaro2
		ibaro2gradientstart = 25 # start of ibaro2 gradient (from top)
		ibaro2gradientsize = 100 # size of ibaro2 gradient

		ibaro3height = 145 # height of ibaro3
		ibaro3gradientstart = 45 # start of ibaro3 gradient (from top)
		ibaro3gradientsize = 100 # size of ibaro3 gradient

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

		img = Image.new("RGBA",(width,ibaro2height),(r,g,b,0))
		gradient = Image.new("L",(1,ibaro2height),0)
		for pos in range(0,ibaro2gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro2gradientsize):
			gradient.putpixel((0,ibaro2gradientstart+ibaro2gradientsize-pos-1),int(self.dexpGradient(ibaro2gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro2.png")

		img = Image.new("RGBA",(width,ibaro3height),(r,g,b,0))
		gradient = Image.new("L",(1,ibaro3height),0)
		for pos in range(0,ibaro3gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro3gradientsize):
			gradient.putpixel((0,ibaro3gradientstart+ibaro3gradientsize-pos-1),int(self.dexpGradient(ibaro3gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro3.png")

	def makeIbarTextureGradientpng(self, style, trans):

		width = 1280 # width of the png file
		gradientspeed = 2.0 # look of the gradient. 1 is flat (linear), higher means rounder

		ibarheight = 310 # height of ibar
		ibargradientstart = 50 # start of ibar gradient (from top)
		ibargradientsize = 100 # size of ibar gradient

		ibaroheight = 165 # height of ibaro
		ibarogradientstart = 65 # start of ibaro gradient (from top)
		ibarogradientsize = 100 # size of ibaro gradient

		ibaro2height = 125 # height of ibaro2
		ibaro2gradientstart = 25 # start of ibaro2 gradient (from top)
		ibaro2gradientsize = 100 # size of ibaro2 gradient

		ibaro3height = 145 # height of ibaro3
		ibaro3gradientstart = 45 # start of ibaro3 gradient (from top)
		ibaro3gradientsize = 100 # size of ibaro3 gradient

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

		img = Image.new("RGBA",(width,ibarheight),(0,0,0,0))
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

		img = Image.new("RGBA",(width,ibaroheight),(0,0,0,0))
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

		img = Image.new("RGBA",(width,ibaro2height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,ibaroheight,bg_h):
				img.paste(bg,(i,j))
		gradient = Image.new("L",(1,ibaro2height),0)
		for pos in range(0,ibaro2gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro2gradientsize):
			gradient.putpixel((0,ibaro2gradientstart+ibaro2gradientsize-pos-1),int(self.dexpGradient(ibaro2gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro2.png")

		img = Image.new("RGBA",(width,ibaro3height),(0,0,0,0))
		for i in xrange(0,width,bg_w):
			for j in xrange(0,ibaroheight,bg_h):
				img.paste(bg,(i,j))
		gradient = Image.new("L",(1,ibaro3height),0)
		for pos in range(0,ibaro3gradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibaro3gradientsize):
			gradient.putpixel((0,ibaro3gradientstart+ibaro3gradientsize-pos-1),int(self.dexpGradient(ibaro3gradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/graphics/ibaro3.png")

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
		self.makeGradientpng("ibar7",width,285,config.plugins.KravenVB.InfobarGradientColorPrimary.value,config.plugins.KravenVB.InfobarGradientColorSecondary.value,config.plugins.KravenVB.InfobarColorTrans.value)
		#Ibaro
		ibaroheights=[
			("ibaro",59),
			("ibaro2",70),
			("ibaro3",115),
			("ibaro4",150)
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

	def makeborsetpng(self,newcolor):
		width = 2
		height = 2
		newcolor = newcolor[-6:]
		r = int(newcolor[0:2], 16)
		g = int(newcolor[2:4], 16)
		b = int(newcolor[4:6], 16)
		img = Image.new("RGBA",(width,height),(r,g,b,255))
		img.save("/usr/share/enigma2/KravenVB/graphics/borset.png")

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

	def get_weather_data(self):

			self.city = ''
			self.lat = ''
			self.lon = ''
			self.accu_id = ''
			self.gm_code = ''
			self.preview_text = ''
			self.preview_warning = ''

			if config.plugins.KravenVB.weather_server.value == '_accu':
				if config.plugins.KravenVB.weather_search_over.value == 'ip':
					self.get_accu_by_ip()
				elif config.plugins.KravenVB.weather_search_over.value == 'name':
					self.get_accu_by_name()
			elif config.plugins.KravenVB.weather_server.value == '_owm':
				if config.plugins.KravenVB.weather_search_over2.value == 'ip':
					self.get_owm_by_ip()
				elif config.plugins.KravenVB.weather_search_over2.value == 'name':
					self.get_owm_by_name()
				elif config.plugins.KravenVB.weather_search_over2.value == 'gmcode':
					self.get_owm_by_gmcode()

			self.actCity=self.preview_text+self.preview_warning

	def get_owm_by_ip(self):

		if self.InternetAvailable==False: 
			return
		
		try:
			res = requests.get('http://ip-api.com/json/?lang=de&fields=status,city,lat,lon', timeout=1)
			data = res.json()

			if data['status']=='success':
				self.city = data['city']
				self.lat = data['lat']
				self.lon = data['lon']
				self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
				config.plugins.KravenVB.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.KravenVB.weather_language.value))
				config.plugins.KravenVB.weather_owm_latlon.save()
				config.plugins.KravenVB.weather_foundcity.value = self.city
				config.plugins.KravenVB.weather_foundcity.save()
			else:
				self.preview_text = _('No data for IP')
		except:
			self.preview_text = _('No data for IP')

	def get_owm_by_gmcode(self):

		if self.InternetAvailable==False: 
			return
		
		try:
			gmcode = config.plugins.KravenVB.weather_gmcode.value
			res = requests.get('http://wxdata.weather.com/wxdata/weather/local/%s?cc=%s' % str(gmcode), timeout=1)
			data = fromstring(res.text)

			self.city = data[1][0].text.split(',')[0]
			self.lat = data[1][2].text
			self.lon = data[1][3].text

			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
			config.plugins.KravenVB.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.KravenVB.weather_language.value))
			config.plugins.KravenVB.weather_owm_latlon.save()
			config.plugins.KravenVB.weather_foundcity.value = self.city
			config.plugins.KravenVB.weather_foundcity.save()
		except:
			self.get_owm_by_ip()
			self.preview_warning = _('\n\nNo data for GM code,\nfallback to IP')

	def get_owm_by_name(self):

		if self.InternetAvailable==False: 
			return
		
		try:
			searchterm = config.plugins.KravenVB.weather_cityname.getValue()
			res = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?appid=60e502f04cdafb43a8ca88f82c39c033&q=%s' % str(searchterm), timeout=1)
			data = res.json()

			if data['cod'] == '401':
				self.preview_warning = _('API authorization failed')
			elif data['cod'] == '404':
				self.preview_warning = _('Search term not found')
			elif data['cod'] == '429':
				self.preview_warning = _('API requests exceeded')
			elif data['cod'] == '200':
				self.city = data['city']['name']
				self.lat  = data['city']['coord']['lat']
				self.lon  = data['city']['coord']['lon']
				
			self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
			config.plugins.KravenVB.weather_owm_latlon.value = 'lat=%s&lon=%s&units=metric&lang=%s' % (str(self.lat),str(self.lon),str(config.plugins.KravenVB.weather_language.value))
			config.plugins.KravenVB.weather_owm_latlon.save()
			config.plugins.KravenVB.weather_foundcity.value = self.city
			config.plugins.KravenVB.weather_foundcity.save()

		except:
			self.get_owm_by_ip()
			self.preview_warning = _('\n\nNo data for search term,\nfallback to IP')

	def get_accu_by_ip(self):

		if self.InternetAvailable==False: 
			return
		
		try:
			res = requests.get('http://ip-api.com/json/?lang=de&fields=status,city', timeout=1)
			data = res.json()

			if data['status'] == 'success':
				city = data['city']
				apikey = config.plugins.KravenVB.weather_accu_apikey.value
				language = config.plugins.KravenVB.weather_language.value
				res1 = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?q=%s&apikey=%s&language=%s' % (str(city),str(apikey),str(language)), timeout=1)
				data1 = res1.json()
			
				if 'Code' in data1:
					if data1['Code'] == 'ServiceUnavailable':
						self.preview_warning = _('API requests exceeded')
					elif data1['Code'] == 'Unauthorized':
						self.preview_warning = _('API authorization failed')
				else:
					self.accu_id = data1[0]['Key']
					self.city = data1[0]['LocalizedName']
					self.lat = data1[0]['GeoPosition']['Latitude']
					self.lon = data1[0]['GeoPosition']['Longitude']
					self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
					config.plugins.KravenVB.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenVB.weather_language.value))
					config.plugins.KravenVB.weather_accu_latlon.save()
					config.plugins.KravenVB.weather_accu_id.value = str(self.accu_id)
					config.plugins.KravenVB.weather_accu_id.save()
					config.plugins.KravenVB.weather_foundcity.value = str(self.city)
					config.plugins.KravenVB.weather_foundcity.save()
			else:
				self.preview_text = _('No data for IP')
		except:
			self.preview_warning = _('No Accu ID found')

	def get_accu_by_name(self):

		if self.InternetAvailable==False: 
			return
		
		try:
			city = config.plugins.KravenVB.weather_cityname.getValue()
			apikey = config.plugins.KravenVB.weather_accu_apikey.value
			language = config.plugins.KravenVB.weather_language.value
			
			res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search?q=%s&apikey=%s&language=%s' % (str(city),str(apikey),str(language)), timeout=1)
			data = res.json()
			
			if 'Code' in data:
				if data['Code'] == 'ServiceUnavailable':
					self.preview_warning = _('API requests exceeded')
				elif data['Code'] == 'Unauthorized':
					self.preview_warning = _('API authorization failed')
			else:
				self.accu_id = data[0]['Key']
				self.city = data[0]['LocalizedName']
				self.lat = data[0]['GeoPosition']['Latitude']
				self.lon = data[0]['GeoPosition']['Longitude']
				self.preview_text = str(self.city) + '\nLat: ' + str(self.lat) + '\nLong: ' + str(self.lon)
				config.plugins.KravenVB.weather_accu_latlon.value = 'lat=%s&lon=%s&metric=1&language=%s' % (str(self.lat), str(self.lon), str(config.plugins.KravenVB.weather_language.value))
				config.plugins.KravenVB.weather_accu_latlon.save()
				config.plugins.KravenVB.weather_accu_id.value = str(self.accu_id)
				config.plugins.KravenVB.weather_accu_id.save()
				config.plugins.KravenVB.weather_foundcity.value = str(self.city)
				config.plugins.KravenVB.weather_foundcity.save()
		except:
			self.preview_warning = _('No Accu ID found')
