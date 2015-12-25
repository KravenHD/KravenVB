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
from os import environ, listdir, remove, rename, system
from shutil import move, rmtree
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from Components.SystemInfo import SystemInfo
from PIL import Image, ImageFilter
import gettext, time
from enigma import ePicLoad, getDesktop, eConsoleAppContainer, eTimer
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

#############################################################

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

config.plugins.KravenVB = ConfigSubsection()
config.plugins.KravenVB.weather_city = ConfigNumber(default="676757")
config.plugins.KravenVB.Primetime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))
config.plugins.KravenVB.InfobarSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.InfobarSelfColorB = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorR = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorG = ConfigSlider(default=0, increment=15, limits=(0,255))
config.plugins.KravenVB.BackgroundSelfColorB = ConfigSlider(default=75, increment=15, limits=(0,255))
				
config.plugins.KravenVB.customProfile = ConfigSelection(default="1", choices = [
				("1", _("1")),
				("2", _("2")),
				("3", _("3")),
				("4", _("4")),
				("5", _("5"))
				])
				
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
				
config.plugins.KravenVB.MenuColorTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])
				
config.plugins.KravenVB.MenuColorTransNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for MiniTV"))
				])
				
config.plugins.KravenVB.BackgroundColorTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])
				
config.plugins.KravenVB.InfobarColorTrans = ConfigSelection(default="00", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])
				
config.plugins.KravenVB.BackgroundColor = ConfigSelection(default="self", choices = [
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
				("ffffff", _("white")),
				("self", _("self"))
				])
				
config.plugins.KravenVB.InfobarColor = ConfigSelection(default="self", choices = [
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
				("999998", _("grey")),
				("3F3F3E", _("grey dark")),
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
				("ffffff", _("white")),
				("self", _("self"))
				])
				
config.plugins.KravenVB.SelectionBackground = ConfigSelection(default="000050EF", choices = [
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
				])
				
config.plugins.KravenVB.Font1 = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.Font2 = ConfigSelection(default="00F0A30A", choices = [
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
				])
				
config.plugins.KravenVB.IBFont1 = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.IBFont2 = ConfigSelection(default="00F0A30A", choices = [
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
				])
				
config.plugins.KravenVB.SelectionFont = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.MarkedFont = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.ECMFont = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.ChannelnameFont = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.PrimetimeFont = ConfigSelection(default="0070AD11", choices = [
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
				])
				
config.plugins.KravenVB.ButtonText = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.Border = ConfigSelection(default="00ffffff", choices = [
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
				("00000000", _("black")),
				("00330400", _("red dark")),
				("00647687", _("steel")),
				("00262C33", _("steel dark")),
				("006C0AAB", _("violet")),
				("001F0333", _("violet dark")),
				("00ffffff", _("white"))
				])
				
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
				
config.plugins.KravenVB.Line = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.SelectionBorder = ConfigSelection(default="none", choices = [
				("none", _("off")),
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
				])
				
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
				("infobar-channelname-small-x1", _("Name small")),
				("infobar-channelname-number-small-x1", _("Name & Number small")),
				("infobar-channelname-x1", _("Name big")),
				("infobar-channelname-number-x1", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName2 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-x2", _("Name small")),
				("infobar-channelname-number-small-x2", _("Name & Number small")),
				("infobar-channelname-x2", _("Name big")),
				("infobar-channelname-number-x2", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName3 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-z1", _("Name small")),
				("infobar-channelname-number-small-z1", _("Name & Number small")),
				("infobar-channelname-z1", _("Name big")),
				("infobar-channelname-number-z1", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName4 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-zz1", _("Name small")),
				("infobar-channelname-number-small-zz1", _("Name & Number small")),
				("infobar-channelname-zz1", _("Name big")),
				("infobar-channelname-number-zz1", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName5 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-zz2", _("Name")),
				("infobar-channelname-number-zz2", _("Name & Number"))
				])
				
config.plugins.KravenVB.InfobarChannelName6 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-zz4", _("Name small")),
				("infobar-channelname-number-small-zz4", _("Name & Number small")),
				("infobar-channelname-zz4", _("Name big")),
				("infobar-channelname-number-zz4", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName7 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-zzz1", _("Name")),
				("infobar-channelname-number-zzz1", _("Name & Number"))
				])
				
config.plugins.KravenVB.InfobarChannelName8 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-x3", _("Name small")),
				("infobar-channelname-number-small-x3", _("Name & Number small")),
				("infobar-channelname-x3", _("Name big")),
				("infobar-channelname-number-x3", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName9 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-small-z2", _("Name small")),
				("infobar-channelname-number-small-z2", _("Name & Number small")),
				("infobar-channelname-z2", _("Name big")),
				("infobar-channelname-number-z2", _("Name & Number big"))
				])
				
config.plugins.KravenVB.InfobarChannelName10 = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("infobar-channelname-zz3", _("Name")),
				("infobar-channelname-number-zz3", _("Name & Number"))
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
				
config.plugins.KravenVB.ChannelSelectionModeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for this channellist style"))
				])
				
config.plugins.KravenVB.ChannelSelectionTrans = ConfigSelection(default="32", choices = [
				("00", _("0%")),
				("0C", _("5%")),
				("18", _("10%")),
				("32", _("20%")),
				("58", _("35%")),
				("7E", _("50%"))
				])
				
config.plugins.KravenVB.ChannelSelectionTransNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for this channellist style"))
				])
				
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
				
config.plugins.KravenVB.ChannelSelectionServiceSizeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for Nobile-Styles"))
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
				
config.plugins.KravenVB.ChannelSelectionInfoSizeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available for Nobile-Styles"))
				])
				
config.plugins.KravenVB.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-xpicon", _("X-Picons")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-zzpicon", _("ZZ-Picons")),
				("numberzapext-zzzpicon", _("ZZZ-Picons"))
				])
				
config.plugins.KravenVB.CoolTVGuide = ConfigSelection(default="cooltv-minitv", choices = [
				("cooltv-minitv", _("MiniTV")),
				("cooltv-picon", _("Picon"))
				])
				
config.plugins.KravenVB.MovieSelection = ConfigSelection(default="movieselection-no-cover", choices = [
				("movieselection-no-cover", _("no Cover")),
				("movieselection-small-cover", _("small Cover")),
				("movieselection-big-cover", _("big Cover")),
				("movieselection-minitv", _("MiniTV"))
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
				
config.plugins.KravenVB.RunningText = ConfigSelection(default="startdelay=4000", choices = [
				("movetype=none", _("off")),
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
				("clock-analog", _("Analog")),
				("clock-android", _("Android")),
				("clock-color", _("colored"))
				])

config.plugins.KravenVB.ClockStyle2 = ConfigSelection(default="clock-classic2", choices = [
				("clock-classic2", _("standard")),
				("clock-classic-big2", _("standard big")),
				("clock-analog", _("Analog")),
				("clock-android", _("Android")),
				("clock-color2", _("colored"))
				])

config.plugins.KravenVB.ClockStyle3 = ConfigSelection(default="clock-classic3", choices = [
				("clock-classic3", _("standard")),
				("clock-classic-big3", _("standard big")),
				("clock-analog", _("Analog")),
				("clock-android", _("Android")),
				("clock-color3", _("colored"))
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
				
config.plugins.KravenVB.ECMLine1 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact"))
				])
				
config.plugins.KravenVB.ECMLine2 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
				("VeryShortCaid", _("short with CAID")),
				("VeryShortReader", _("short with source")),
				("ShortReader", _("compact")),
				("Normal", _("balanced")),
				("Long", _("extensive")),
				("VeryLong", _("complete"))
				])
				
config.plugins.KravenVB.ECMLine3 = ConfigSelection(default="ShortReader", choices = [
				("none", _("off")),
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
				
config.plugins.KravenVB.SIB = ConfigSelection(default="infobar-style-x1_end2", choices = [
				("infobar-style-x1_end", _("top/bottom")),
				("infobar-style-x1_end2", _("left/right")),
				("infobar-style-x1_end3", _("single")),
				("infobar-style-x1_end4", _("MiniTV")),
				("infobar-style-x1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB1 = ConfigSelection(default="infobar-style-x2_end2", choices = [
				("infobar-style-x2_end", _("top/bottom")),
				("infobar-style-x2_end2", _("left/right")),
				("infobar-style-x2_end3", _("single")),
				("infobar-style-x2_end4", _("MiniTV")),
				("infobar-style-x2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB2 = ConfigSelection(default="infobar-style-x3_end2", choices = [
				("infobar-style-x3_end", _("top/bottom")),
				("infobar-style-x3_end2", _("left/right")),
				("infobar-style-x3_end3", _("single")),
				("infobar-style-x3_end4", _("MiniTV")),
				("infobar-style-x3_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB3 = ConfigSelection(default="infobar-style-z1_end2", choices = [
				("infobar-style-z1_end", _("top/bottom")),
				("infobar-style-z1_end2", _("left/right")),
				("infobar-style-z1_end3", _("single")),
				("infobar-style-z1_end4", _("MiniTV")),
				("infobar-style-z1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB4 = ConfigSelection(default="infobar-style-z2_end2", choices = [
				("infobar-style-z2_end", _("top/bottom")),
				("infobar-style-z2_end2", _("left/right")),
				("infobar-style-z2_end3", _("single")),
				("infobar-style-z2_end4", _("MiniTV")),
				("infobar-style-z2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB5 = ConfigSelection(default="infobar-style-zz1_end2", choices = [
				("infobar-style-zz1_end", _("top/bottom")),
				("infobar-style-zz1_end2", _("left/right")),
				("infobar-style-zz1_end3", _("single")),
				("infobar-style-zz1_end4", _("MiniTV")),
				("infobar-style-zz1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB6 = ConfigSelection(default="infobar-style-zz2_end2", choices = [
				("infobar-style-zz2_end", _("top/bottom")),
				("infobar-style-zz2_end2", _("left/right")),
				("infobar-style-zz2_end3", _("single")),
				("infobar-style-zz2_end4", _("MiniTV")),
				("infobar-style-zz2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB7 = ConfigSelection(default="infobar-style-zz3_end2", choices = [
				("infobar-style-zz3_end", _("top/bottom")),
				("infobar-style-zz3_end2", _("left/right")),
				("infobar-style-zz3_end3", _("single")),
				("infobar-style-zz3_end4", _("MiniTV")),
				("infobar-style-zz3_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB8 = ConfigSelection(default="infobar-style-zz4_end2", choices = [
				("infobar-style-zz4_end", _("top/bottom")),
				("infobar-style-zz4_end2", _("left/right")),
				("infobar-style-zz4_end3", _("single")),
				("infobar-style-zz4_end4", _("MiniTV")),
				("infobar-style-zz4_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB9 = ConfigSelection(default="infobar-style-zzz1_end2", choices = [
				("infobar-style-zzz1_end", _("top/bottom")),
				("infobar-style-zzz1_end2", _("left/right")),
				("infobar-style-zzz1_end3", _("single")),
				("infobar-style-zzz1_end4", _("MiniTV")),
				("infobar-style-zzz1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.IBtop = ConfigSelection(default="infobar-x2-z1_top2", choices = [
				("infobar-x2-z1_top", _("Icons + 4 Tuner + Resolution + Infobox")),
				("infobar-x2-z1_top2", _("Icons + REC + 2 Tuner + Resolution + Infobox"))
				])
				
config.plugins.KravenVB.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("cpu", _("CPU + Load")),
				("temp", _("Temperature + Fan"))
				])
				
config.plugins.KravenVB.IBColor = ConfigSelection(default="all-screens", choices = [
				("all-screens", _("in all Screens")),
				("only-infobar", _("only Infobar, SecondInfobar & Players"))
				])
				
config.plugins.KravenVB.About = ConfigSelection(default="about", choices = [
				("about", _(" "))
				])
				
config.plugins.KravenVB.About2 = ConfigSelection(default="about", choices = [
				("about", _("press OK for the FAQs"))
				])
				
config.plugins.KravenVB.ClockStyleNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenVB.AnalogStyleNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for Clock Analog"))
				])
				
config.plugins.KravenVB.IBtopNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenVB.InfoboxNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available in this style"))
				])
				
config.plugins.KravenVB.IBColorNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("not available when scrollbars activated"))
				])
				
config.plugins.KravenVB.Logo = ConfigSelection(default="minitv", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV"))
				])
				
config.plugins.KravenVB.DebugNames = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("screennames-on", _("on"))
				])
				
config.plugins.KravenVB.WeatherView = ConfigSelection(default="meteo", choices = [
				("icon", _("Icon")),
				("meteo", _("Meteo"))
				])
				
config.plugins.KravenVB.WeatherViewNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when weather activated"))
				])

config.plugins.KravenVB.MeteoColor = ConfigSelection(default="meteo-light", choices = [
				("meteo-light", _("light")),
				("meteo-dark", _("dark"))
				])
				
config.plugins.KravenVB.MeteoColorNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for Meteo-Style"))
				])
				
config.plugins.KravenVB.Primetimeavailable = ConfigSelection(default="primetime-on", choices = [
				("primetime-off", _("off")),
				("primetime-on", _("on"))
				])
				
config.plugins.KravenVB.PrimetimeNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Primetime is activated"))
				])
				
config.plugins.KravenVB.PrimetimeFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Primetime is activated"))
				])

config.plugins.KravenVB.ChannelnameFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when activated"))
				])
				
config.plugins.KravenVB.FTANA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when ECM-Infos are activated"))
				])
				
config.plugins.KravenVB.ECMFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when ECM-Infos are activated"))
				])
				
config.plugins.KravenVB.RunningTextSpeedNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available when Running Text is activated"))
				])
				
config.plugins.KravenVB.EMCSelectionColors = ConfigSelection(default="emc-colors-on", choices = [
				("none", _("off")),
				("emc-colors-on", _("on"))
				])
				
config.plugins.KravenVB.EMCSelectionBackground = ConfigSelection(default="00213305", choices = [
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
				])
				
config.plugins.KravenVB.EMCSelectionBackgroundNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for 'Custom EMC-Selection-Colors'"))
				])
				
config.plugins.KravenVB.EMCSelectionFont = ConfigSelection(default="00ffffff", choices = [
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
				])
				
config.plugins.KravenVB.EMCSelectionFontNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for 'Custom EMC-Selection-Colors'"))
				])
				
config.plugins.KravenVB.ColorNA = ConfigSelection(default="not-available", choices = [
				("not-available", _("only available for self-colors"))
				])
				
#######################################################################

class KravenVB(ConfigListScreen, Screen):
	skin = """
<screen name="KravenVB-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <widget font="Regular; 20" halign="left" valign="center" source="key_red" position="70,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_green" position="320,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_yellow" position="570,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget font="Regular; 20" halign="left" valign="center" source="key_blue" position="820,665" size="220,26" render="Label" backgroundColor="#00000000" foregroundColor="#00ffffff" transparent="1" zPosition="1" />
  <widget name="config" position="70,80" size="708,540" itemHeight="30" font="Regular;24" transparent="1" enableWrapAround="1" scrollbarMode="showAlways" scrollbarWidth="6" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,15" size="708,46" text="KravenVB - Konfigurationstool" font="Regular; 35" valign="center" halign="left" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="847,218" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="847,427" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="845,218" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel position="1215,218" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap pixmap="KravenVB/buttons/key_red1.png" position="65,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_green1.png" position="315,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_yellow1.png" position="565,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_blue1.png" position="815,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1138,22" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="830,70" size="402,46" text="KravenVB" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="830,125" size="402,34" text="for VTi-Image" font="Regular; 26" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <eLabel position="845,165" size="372,40" text="Version: 3.5.1" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <widget name="helperimage" position="847,220" size="368,207" zPosition="1" backgroundColor="#00000000" />
  <widget source="Canvas" render="Canvas" position="847,220" size="368,207" zPosition="-1" backgroundColor="#00000000" />
  <widget source="help" render="Label" position="847,450" size="368,196" font="Regular;20" backgroundColor="#00000000" foregroundColor="#00f0a30a" halign="center" valign="top" transparent="1" />
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
		self.profiles = "/etc/"
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
			"red": self.exit,
			"green": self.save,
			"yellow": self.saveProfile,
			"blue": self.reset,
			"cancel": self.exit,
			"pageup": self.pageUp,
			"papedown": self.pageDown,
			"ok": self.faq
		}, -1)
		
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save skin"))
		self["key_yellow"] = StaticText(_("Save profile"))
		self["key_blue"] = StaticText(_("Reset profile"))
		
		self.UpdatePicture()
		
		self.timer = eTimer()
		self.timer.callback.append(self.updateMylist)
		self.onLayoutFinish.append(self.updateMylist)
		
		self.lastProfile="0"
		
		self.actClockstyle=""
		self.actWeatherstyle=""
		self.actChannelselectionstyle=""

	def mylist(self):
		self.timer.start(100, True)

	def updateMylist(self):
		list = []
		list.append(getConfigListEntry(_("About"), config.plugins.KravenVB.About2, _("The KravenVB skin will be generated by this plugin according to your preferences. Make your settings and watch the changes in the preview window above. When finished, save your skin by pressing the green button and restart the GUI.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("PROFILES _____________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Active Profile"), config.plugins.KravenVB.customProfile, _("Select the profile you want to work with. Profiles are saved automatically on switching them or by pressing the yellow button. New profiles will be generated based on the actual one. Profiles are interchangeable between boxes.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("SYSTEM _______________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Icons (except Infobar)"), config.plugins.KravenVB.IconStyle2, _("Choose between light and dark icons in system screens. The icons in the infobars are not affected.")))
		list.append(getConfigListEntry(_("Running Text (Delay)"), config.plugins.KravenVB.RunningText, _("Choose the start delay for running text.")))
		if config.plugins.KravenVB.RunningText.value in ("startdelay=2000","startdelay=4000","startdelay=6000","startdelay=8000","startdelay=10000","startdelay=15000","startdelay=20000"):
			list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenVB.RunningTextSpeed, _("Choose the speed for running text.")))
		elif config.plugins.KravenVB.RunningText.value == "movetype=none":
			list.append(getConfigListEntry(_("Running Text (Speed)"), config.plugins.KravenVB.RunningTextSpeedNA, _("This option is not available because running text is deactivated.")))
		list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenVB.ScrollBar, _("Choose the width of scrollbars in lists or deactivate scrollbars completely. Active scrollbars deactivate the option \"show the infobar background in all screens (bicolored background)\".")))
		if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
			list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenVB.IBColor, _("Choose whether you want to see the infobar background in all screens (bicolored background).")))
		elif config.plugins.KravenVB.ScrollBar.value in ("scrollbarWidth=5","scrollbarWidth=10","scrollbarWidth=15"):
			list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenVB.IBColorNA, _("This option is not available because scrollbars are activated.")))
		list.append(getConfigListEntry(_("Menus"), config.plugins.KravenVB.Logo, _("Choose between MiniTV or Kraven logo in system menus.")))
		if config.plugins.KravenVB.Logo.value == "logo":
			list.append(getConfigListEntry(_("Menu-Transparency"), config.plugins.KravenVB.MenuColorTrans, _("Choose the degree of background transparency for system menu screens.")))
		else:
			list.append(getConfigListEntry(_("Menu-Transparency"), config.plugins.KravenVB.MenuColorTransNA, _("This option is not available because MiniTV for system menus is activated.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("GLOBAL COLORS ________________________________________________________"), config.plugins.KravenVB.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenVB.BackgroundColor, _("Choose the background color for all screens. You can choose from a list of predefined colors or create your own color using RGB sliders.")))
		if config.plugins.KravenVB.BackgroundColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.BackgroundSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.BackgroundSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.BackgroundSelfColorB, _("Set the intensity of this basic color with the slider.")))
		else:
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.ColorNA, _(" ")))
		list.append(getConfigListEntry(_("Background-Transparency"), config.plugins.KravenVB.BackgroundColorTrans, _("Choose the degree of background transparency for all screens except system menus and channellists.")))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenVB.SelectionBackground, _("Choose the background color of selection bars.")))
		list.append(getConfigListEntry(_("Listselection-Border"), config.plugins.KravenVB.SelectionBorder, _("Choose the border color of selection bars or deactivate borders completely.")))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenVB.Progress, _("Choose the color of progress bars.")))
		list.append(getConfigListEntry(_("Progress-Border"), config.plugins.KravenVB.Border, _("Choose the border color of progress bars.")))
		list.append(getConfigListEntry(_("Lines"), config.plugins.KravenVB.Line, _("Choose the color of all lines. This affects dividers as well as the line in the center of some progress bars.")))
		list.append(getConfigListEntry(_("Primary-Font"), config.plugins.KravenVB.Font1, _("Choose the color of the primary font. The primary font is used for list items, textboxes and other important information.")))
		list.append(getConfigListEntry(_("Secondary-Font"), config.plugins.KravenVB.Font2, _("Choose the color of the secondary font. The secondary font is used for headers, labels and other additional information.")))
		list.append(getConfigListEntry(_("Selection-Font"), config.plugins.KravenVB.SelectionFont, _("Choose the color of the font in selection bars.")))
		list.append(getConfigListEntry(_("Marking-Font"), config.plugins.KravenVB.MarkedFont, _("Choose the font color of marked list items.")))
		list.append(getConfigListEntry(_("Colorbutton-Font"), config.plugins.KravenVB.ButtonText, _("Choose the font color of the color button labels.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("INFOBAR ______________________________________________________________"), config.plugins.KravenVB.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Infobar-Style"), config.plugins.KravenVB.InfobarStyle, _("Choose from different infobar styles. Please note that not every style provides every feature. Therefore some features might be unavailable for the chosen style.")))
		list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenVB.InfobarColor, _("Choose the background color of the infobars. You can choose from a list of predefined colors or create your own color using RGB sliders.")))
		if config.plugins.KravenVB.InfobarColor.value == "self":
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.InfobarSelfColorR, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.InfobarSelfColorG, _("Set the intensity of this basic color with the slider.")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.InfobarSelfColorB, _("Set the intensity of this basic color with the slider.")))
		else:
			list.append(getConfigListEntry(_("          red"), config.plugins.KravenVB.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          green"), config.plugins.KravenVB.ColorNA, _(" ")))
			list.append(getConfigListEntry(_("          blue"), config.plugins.KravenVB.ColorNA, _(" ")))
		list.append(getConfigListEntry(_("Infobar-Transparency"), config.plugins.KravenVB.InfobarColorTrans, _("Choose the degree of background transparency for the infobars.")))
		list.append(getConfigListEntry(_("Primary-Infobar-Font"), config.plugins.KravenVB.IBFont1, _("Choose the color of the primary infobar font.")))
		list.append(getConfigListEntry(_("Secondary-Infobar-Font"), config.plugins.KravenVB.IBFont2, _("Choose the color of the secondary infobar font.")))
		list.append(getConfigListEntry(_("Infobar-Icons"), config.plugins.KravenVB.IconStyle, _("Choose between light and dark infobar icons.")))
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenVB.IBtop, _("Choose from different options to display tuner and recording state.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenVB.IBtopNA, _("This option is not available for the selected infobar style.")))
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox, _("Choose which informations will be shown in the info box.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.InfoboxNA, _("This option is not available for the selected infobar style.")))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName.value == "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName2, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName2.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName3, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName3.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName4, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName4.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName5, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName5.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName6, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName6.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName7, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName7.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName8, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName8.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName9, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName9.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName10, _("Choose from different options to show the channel name and number in the infobar.")))
			if config.plugins.KravenVB.InfobarChannelName10.value ==  "none":
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFontNA, _("This option is not available because displaying channel name and number is deactivated.")))
			else:
				list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont, _("Choose the font color of channel name and number")))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenVB.ClockStyle.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle2, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenVB.ClockStyle2.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle3, _("Choose from different options to show the clock in the infobar.")))
			self.actClockstyle=config.plugins.KravenVB.ClockStyle3.value
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyleNA, _("This option is not available for the selected infobar style.")))
			self.actClockstyle="none"
		if self.actClockstyle == "clock-analog":
			list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenVB.AnalogStyle, _("Choose from different colors for the analog type clock in the infobar.")))
		else:
			list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenVB.AnalogStyleNA, _("This option is not available for the selected clock type.")))
		list.append(getConfigListEntry(_("System-Infos"), config.plugins.KravenVB.SystemInfo, _("Choose from different additional windows with system informations or deactivate them completely.")))
		list.append(getConfigListEntry(_("ECM INFOS ____________________________________________________________"), config.plugins.KravenVB.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenVB.ECMLine1, _("Choose from different options to display the ECM informations.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenVB.ECMLine2, _("Choose from different options to display the ECM informations.")))
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenVB.ECMLine3, _("Choose from different options to display the ECM informations.")))
		if config.plugins.KravenVB.ECMLine1.value == "none" or config.plugins.KravenVB.ECMLine2.value == "none" or config.plugins.KravenVB.ECMLine3.value == "none":
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenVB.FTANA, _("This option is not available because displaying ECM information is deactivated.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFontNA, _("This option is not available because displaying ECM information is deactivated.")))
		else:
			list.append(getConfigListEntry(_("Show 'free to air'"), config.plugins.KravenVB.FTA, _("Choose whether 'free to air' is displayed or not for unencrypted channels.")))
			list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFont, _("Choose the font color of the ECM information.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("WEATHER ______________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle, _("Choose from different options to show the weather in the infobar.")))
			self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle.value
		elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
				list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle3, _("Activate or deactivate displaying the weather in the infobar.")))
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle3.value
			else:
				list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle2, _("Activate or deactivate displaying the weather in the infobar.")))
				self.actWeatherstyle=config.plugins.KravenVB.WeatherStyle2.value
		list.append(getConfigListEntry(_("Weather-ID"), config.plugins.KravenVB.weather_city, _("Specify the weather ID for your location. You can find it at https://weather.yahoo.com. Just enter your ZIP or city and get your weather. The number at the end of the URL is your ID.")))
		list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.KravenVB.refreshInterval, _("Choose the frequency of loading weather data from the internet. Please note that it can take some time to show the weather after a reboot.")))
		if self.actWeatherstyle != "none":
			list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenVB.WeatherView, _("Choose between graphical weather symbols and Meteo symbols.")))
		else:
			list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenVB.WeatherViewNA, _("This option is not available because weather is deactivated.")))
		if config.plugins.KravenVB.WeatherView.value == "meteo":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenVB.MeteoColor, _("Choose between light and dark Meteo symbols.")))
		elif config.plugins.KravenVB.WeatherView.value == "icon":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenVB.MeteoColorNA, _("This option is not available because Meteo symbols are not selected.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("CHANNELLIST __________________________________________________________"), config.plugins.KravenVB.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		if SystemInfo.get("NumVideoDecoders",1) > 1:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle2, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle2.value
		else:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle, _("Choose from different styles for the channel selection screen.")))
			self.actChannelselectionstyle=config.plugins.KravenVB.ChannelSelectionStyle.value
		if self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv22","channelselection-style-minitv33","channelselection-style-minitv4","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv33"):
			list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenVB.ChannelSelectionMode, _("Choose between direct zapping (1xOK) and zapping after preview (2xOK).")))
		else:
			list.append(getConfigListEntry(_("Channellist-Mode"), config.plugins.KravenVB.ChannelSelectionModeNA, _("This option is only available for MiniTV, Extended Preview and DualTV channellist styles.")))
		if not self.actChannelselectionstyle in ("channelselection-style-minitv","channelselection-style-minitv2","channelselection-style-minitv3","channelselection-style-minitv4","channelselection-style-minitv22","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3"):
			list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenVB.ChannelSelectionTrans, _("Choose the degree of background transparency for the channellists.")))
		else:
			list.append(getConfigListEntry(_("Channellist-Transparenz"), config.plugins.KravenVB.ChannelSelectionTransNA, _("This option is not available for MiniTV, Preview and DualTV channellist styles.")))
		if self.actChannelselectionstyle in ("channelselection-style-nobile","channelselection-style-nobile2","channelselection-style-nobile-minitv","channelselection-style-nobile-minitv3","channelselection-style-nobile-minitv33"):
			list.append(getConfigListEntry(_("Servicenumber/-name Fontsize"), config.plugins.KravenVB.ChannelSelectionServiceSizeNA, _("This option is not available for Nobile-Styles.")))
			list.append(getConfigListEntry(_("Serviceinfo Fontsize"), config.plugins.KravenVB.ChannelSelectionInfoSizeNA, _("This option is not available for Nobile-Styles.")))
		else:
			list.append(getConfigListEntry(_("Servicenumber/-name Fontsize"), config.plugins.KravenVB.ChannelSelectionServiceSize, _("Choose the font size of channelnumber and channelname.")))
			list.append(getConfigListEntry(_("Serviceinfo Fontsize"), config.plugins.KravenVB.ChannelSelectionInfoSize, _("Choose the font size of serviceinformation.")))
		list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenVB.Primetimeavailable, _("Choose whether primetime program information is displayed or not.")))
		if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.Primetime, _("Specify the time for your primetime.")))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFont, _("Choose the font color of the primetime information.")))
		elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-off":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.PrimetimeNA, _("This option is not available because displaying primetime information is deactivated.")))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFontNA, _("This option is not available because displaying primetime information is deactivated.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("ENHANCED MOVIE CENTER ________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("EMC-Style"), config.plugins.KravenVB.EMCStyle, _("Choose from different styles for EnhancedMovieCenter.")))
		list.append(getConfigListEntry(_("Custom EMC-Selection-Colors"), config.plugins.KravenVB.EMCSelectionColors, _("Choose whether you want to customize the selection-colors for EnhancedMovieCenter.")))
		if config.plugins.KravenVB.EMCSelectionColors.value == "emc-colors-on":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenVB.EMCSelectionBackground, _("Choose the background color of selection bars for EnhancedMovieCenter.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenVB.EMCSelectionFont, _("Choose the color of the font in selection bars for EnhancedMovieCenter.")))
		elif config.plugins.KravenVB.EMCSelectionColors.value == "none":
			list.append(getConfigListEntry(_("EMC-Listselection"), config.plugins.KravenVB.EMCSelectionBackgroundNA, _("This option is not available because 'Custom EMC-Selection-Colors' is deactivated.")))
			list.append(getConfigListEntry(_("EMC-Selection-Font"), config.plugins.KravenVB.EMCSelectionFontNA, _("This option is not available because 'Customize EMC-Selection-Colors' is deactivated.")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("VIEWS ________________________________________________________________"), config.plugins.KravenVB.About, _(" ")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenVB.Volume, _("Choose from different styles for the volume display.")))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenVB.CoolTVGuide, _("Choose from different styles for CoolTVGuide.")))
		list.append(getConfigListEntry(_("MovieSelection"), config.plugins.KravenVB.MovieSelection, _("Choose from different styles for MovieSelection.")))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB1, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB2, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB3, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB4, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB5, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB6, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB7, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB8, _("Choose from different styles for SecondInfobar.")))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB9, _("Choose from different styles for SecondInfobar.")))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.KravenVB.NumberZapExt, _("Choose from different styles for ExtNumberZap")))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("DEBUG ________________________________________________________________"), ))
		list.append(getConfigListEntry(_(" "), ))
		list.append(getConfigListEntry(_("Screennames"), config.plugins.KravenVB.DebugNames, _("Activate or deactivate small screen names for debugging purposes.")))
		
		self["config"].list = list
		self["config"].l.setList(list)
		self.updateHelp()
		self["helperimage"].hide()
		self.ShowPicture()
		
		option = self["config"].getCurrent()[1]
		
		if option == config.plugins.KravenVB.customProfile:
			if config.plugins.KravenVB.customProfile.value==self.lastProfile:
				self.saveProfile(msg=False)
			else:
				self.loadProfile()
				self.lastProfile=config.plugins.KravenVB.customProfile.value
		
		if option == config.plugins.KravenVB.BackgroundColor:
			if config.plugins.KravenVB.BackgroundColor.value in ("self"):
				self.showColor(self.RGB(int(config.plugins.KravenVB.BackgroundSelfColorR.value), int(config.plugins.KravenVB.BackgroundSelfColorG.value), int(config.plugins.KravenVB.BackgroundSelfColorB.value)))
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.BackgroundColor.value))
		elif option in (config.plugins.KravenVB.BackgroundSelfColorR,config.plugins.KravenVB.BackgroundSelfColorG,config.plugins.KravenVB.BackgroundSelfColorB):
			self.showColor(self.RGB(int(config.plugins.KravenVB.BackgroundSelfColorR.value), int(config.plugins.KravenVB.BackgroundSelfColorG.value), int(config.plugins.KravenVB.BackgroundSelfColorB.value)))
		elif option == config.plugins.KravenVB.SelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionBackground.value))
		elif option == config.plugins.KravenVB.EMCSelectionBackground:
			self.showColor(self.hexRGB(config.plugins.KravenVB.EMCSelectionBackground.value))
		elif option == config.plugins.KravenVB.Progress:
			if config.plugins.KravenVB.Progress.value in ("progress", "progress2"):
				self["helperimage"].show()
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.Progress.value))
		elif option == config.plugins.KravenVB.Border:
			self.showColor(self.hexRGB(config.plugins.KravenVB.Border.value))
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
		elif option == config.plugins.KravenVB.SelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.SelectionFont.value))
		elif option == config.plugins.KravenVB.EMCSelectionFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.EMCSelectionFont.value))
		elif option == config.plugins.KravenVB.MarkedFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.MarkedFont.value))
		elif option == config.plugins.KravenVB.ButtonText:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ButtonText.value))
		elif option == config.plugins.KravenVB.InfobarColor:
			if config.plugins.KravenVB.InfobarColor.value in ("self"):
				self.showColor(self.RGB(int(config.plugins.KravenVB.InfobarSelfColorR.value), int(config.plugins.KravenVB.InfobarSelfColorG.value), int(config.plugins.KravenVB.InfobarSelfColorB.value)))
			else:
				self.showColor(self.hexRGB(config.plugins.KravenVB.InfobarColor.value))
		elif option in (config.plugins.KravenVB.InfobarSelfColorR,config.plugins.KravenVB.InfobarSelfColorG,config.plugins.KravenVB.InfobarSelfColorB):
			self.showColor(self.RGB(int(config.plugins.KravenVB.InfobarSelfColorR.value), int(config.plugins.KravenVB.InfobarSelfColorG.value), int(config.plugins.KravenVB.InfobarSelfColorB.value)))
		elif option == config.plugins.KravenVB.ChannelnameFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ChannelnameFont.value))
		elif option == config.plugins.KravenVB.ECMFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.ECMFont.value))
		elif option ==  config.plugins.KravenVB.PrimetimeFont:
			self.showColor(self.hexRGB(config.plugins.KravenVB.PrimetimeFont.value))
		else:
			self["helperimage"].show()

	def updateHelp(self):
		cur = self["config"].getCurrent()
		if cur:
			self["help"].text = cur[2]

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			if returnValue in ("infobar-style-x1_end","infobar-style-x2_end","infobar-style-x3_end","infobar-style-z1_end","infobar-style-z2_end","infobar-style-zz1_end","infobar-style-zz2_end","infobar-style-zz3_end","infobar-style-zz4_end","infobar-style-zzz1_end"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB.jpg"
			elif returnValue in ("infobar-style-x1_end2","infobar-style-x2_end2","infobar-style-x3_end2","infobar-style-z1_end2","infobar-style-z2_end2","infobar-style-zz1_end2","infobar-style-zz2_end2","infobar-style-zz3_end2","infobar-style-zz4_end2","infobar-style-zzz1_end2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB1.jpg"
			elif returnValue in ("infobar-style-x1_end3","infobar-style-x2_end3","infobar-style-x3_end3","infobar-style-z1_end3","infobar-style-z2_end3","infobar-style-zz1_end3","infobar-style-zz2_end3","infobar-style-zz3_end3","infobar-style-zz4_end3","infobar-style-zzz1_end3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB2.jpg"
			elif returnValue in ("infobar-style-x1_end4","infobar-style-x2_end4","infobar-style-x3_end4","infobar-style-z1_end4","infobar-style-z2_end4","infobar-style-zz1_end4","infobar-style-zz2_end4","infobar-style-zz3_end4","infobar-style-zz4_end4","infobar-style-zzz1_end4"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB3.jpg"
			elif returnValue in ("infobar-style-x1_end5","infobar-style-x2_end5","infobar-style-x3_end5","infobar-style-z1_end5","infobar-style-z2_end5","infobar-style-zz1_end5","infobar-style-zz2_end5","infobar-style-zz3_end5","infobar-style-zz4_end5","infobar-style-zzz1_end5"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB4.jpg"
			elif returnValue in ("clock-classic","clock-classic2","clock-classic3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-classic.jpg"
			elif returnValue in ("clock-classic-big","clock-classic-big2","clock-classic-big3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-classic-big.jpg"
			elif returnValue in ("clock-color","clock-color2","clock-color3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-color.jpg"
			elif returnValue in ("startdelay=2000","startdelay=4000","startdelay=6000","startdelay=8000","startdelay=10000","startdelay=15000","startdelay=20000"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/running-delay.jpg"
			elif returnValue in ("steptime=200","steptime=100","steptime=66","steptime=50"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/running-speed.jpg"
			elif returnValue in ("about","about2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/about.png"
			elif returnValue == ("meteo-light"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/meteo.jpg"
			elif returnValue == ("progress"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull.jpg"
			elif returnValue == ("progress2"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull2.jpg"
			elif returnValue in ("size-16","size-18","size-20","size-22","size-24","size-26","size-28","size-30"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/size.jpg"
			elif returnValue == ("channelselection-style-nobile-minitv3"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/channelselection-style-nobile-minitv.jpg"
			elif returnValue in ("00","0"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/none.jpg"
			elif returnValue in ("zap","preview"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/modus.jpg"
			elif returnValue in ("0C","18","32","58","7E"):
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/transparent.jpg"
			else:
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
			self.PicLoad.startDecode(self.picPath)
			self.picPath = None
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
		pass

	def keyUp(self):
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
		
		if True:
			self.skinSearchAndReplace = []
			
			### Background
			if config.plugins.KravenVB.BackgroundColor.value == "self":
				self.skincolorbackgroundcolor = str(hex(config.plugins.KravenVB.BackgroundSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.BackgroundSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.BackgroundSelfColorB.value)[2:4]).zfill(2)
				self.skinSearchAndReplace.append(['name="KravenBackground" value="#00000000', 'name="KravenBackground" value="#00' + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="KravenBackground" value="#00000000', 'name="KravenBackground" value="#00' + config.plugins.KravenVB.BackgroundColor.value])
			
			### Background Transparency (global)
			self.skinSearchAndReplace.append(['name="KravenBackground" value="#00', 'name="KravenBackground" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value])
			
			### Background2 (non-transparent)
			if config.plugins.KravenVB.BackgroundColor.value == "self":
				self.skinSearchAndReplace.append(['name="KravenBackground2" value="#00000000', 'name="KravenBackground2" value="#00' + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="KravenBackground2" value="#00000000', 'name="KravenBackground2" value="#00' + config.plugins.KravenVB.BackgroundColor.value])
			
			### Background3 (Menus Transparency)
			if config.plugins.KravenVB.Logo.value == "logo":
				if config.plugins.KravenVB.BackgroundColor.value == "self":
					self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + self.skincolorbackgroundcolor])
				else:
					self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#' + config.plugins.KravenVB.MenuColorTrans.value + config.plugins.KravenVB.BackgroundColor.value])
			else:
				if config.plugins.KravenVB.BackgroundColor.value == "self":
					self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#00' + self.skincolorbackgroundcolor])
				else:
					self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#00' + config.plugins.KravenVB.BackgroundColor.value])
			
			### Background4 (Channellist)
			if config.plugins.KravenVB.BackgroundColor.value == "self":
				self.skinSearchAndReplace.append(['name="KravenBackground4" value="#00000000', 'name="KravenBackground4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + self.skincolorbackgroundcolor])
			else:
				self.skinSearchAndReplace.append(['name="KravenBackground4" value="#00000000', 'name="KravenBackground4" value="#' + config.plugins.KravenVB.ChannelSelectionTrans.value + config.plugins.KravenVB.BackgroundColor.value])
			
			### Infobar Backgrounds
			if config.plugins.KravenVB.InfobarColor.value == "self":
				self.skincolorinfobarcolor = str(hex(config.plugins.KravenVB.InfobarSelfColorR.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorG.value)[2:4]).zfill(2) + str(hex(config.plugins.KravenVB.InfobarSelfColorB.value)[2:4]).zfill(2)
				self.skinSearchAndReplace.append(['name="KravenInfobarBackground" value="#001B1775', 'name="KravenInfobarBackground" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.skincolorinfobarcolor])
				self.skinSearchAndReplace.append(['name="KravenNameBackground" value="#A01B1775', 'name="KravenNameBackground" value="#7E' + self.skincolorinfobarcolor])
				self.skinSearchAndReplace.append(['name="KravenIbarBackground" value="#4A1B1775', 'name="KravenIbarBackground" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + self.skincolorinfobarcolor])
			else:
				self.skincolorinfobarcolor = config.plugins.KravenVB.InfobarColor.value
				self.skinSearchAndReplace.append(['name="KravenInfobarBackground" value="#001B1775', 'name="KravenInfobarBackground" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + config.plugins.KravenVB.InfobarColor.value])
				self.skinSearchAndReplace.append(['name="KravenNameBackground" value="#A01B1775', 'name="KravenNameBackground" value="#7E' + config.plugins.KravenVB.InfobarColor.value])
				self.skinSearchAndReplace.append(['name="KravenIbarBackground" value="#4A1B1775', 'name="KravenIbarBackground" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + config.plugins.KravenVB.InfobarColor.value])
			
			### Selection Background
			if config.plugins.KravenVB.EMCSelectionColors.value == "none":
				self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
				self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
			elif config.plugins.KravenVB.EMCSelectionColors.value == "emc-colors-on":
				self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
				self.skinSearchAndReplace.append(['name="KravenEMCSelection" value="#000050EF', 'name="KravenEMCSelection" value="#' + config.plugins.KravenVB.EMCSelectionBackground.value])
			
			### Menu (Logo/MiniTV)
			if config.plugins.KravenVB.Logo.value == "minitv":
				self.skinSearchAndReplace.append(['<panel name="menu" />', '<eLabel backgroundColor="KravenBackground3" position="0,0" size="1280,720" transparent="0" zPosition="-10" /><widget backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="938,334" render="Label" size="65,80" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%H</convert></widget><eLabel backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="995,334" size="15,80" text=":" transparent="1" valign="center" zPosition="1" /><widget backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="1005,334" render="Label" size="65,80" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%M</convert></widget><eLabel backgroundColor="KravenBackground3" font="Regular; 32" foregroundColor="KravenFont1" halign="center" position="1061,348" size="15,60" text=":" transparent="1" valign="center" zPosition="1" /><widget backgroundColor="KravenBackground3" font="Regular; 32" foregroundColor="KravenFont1" halign="center" position="1071,348" render="Label" size="50,60" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%S</convert></widget><widget backgroundColor="KravenBackground3" font="Regular; 18" foregroundColor="KravenFont1" halign="center" position="928,404" render="Label" size="203,30" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%A</convert></widget><widget backgroundColor="KravenBackground3" font="Regular; 18" foregroundColor="KravenFont1" halign="center" position="928,429" render="Label" size="203,30" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%e. %B</convert></widget><ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" /><ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" /><widget source="session.VideoPicture" render="KravenVBPig3" position="822,80" size="416,234" zPosition="3" backgroundColor="transparent" /><eLabel backgroundColor="#00000000" position="822,80" size="416,234" transparent="0" zPosition="2" /><eLabel backgroundColor="#001F1F1F" position="822,80" size="416,3" transparent="0" zPosition="4" /><eLabel backgroundColor="#001F1F1F" position="822,311" size="416,3" transparent="0" zPosition="4" /><eLabel backgroundColor="#001F1F1F" position="822,80" size="3,234" transparent="0" zPosition="4" /><eLabel backgroundColor="#001F1F1F" position="1235,80" size="3,234" transparent="0" zPosition="4" /><ePixmap backgroundColor="KravenBackground3" pixmap="KravenVB/logo2.png" position="980,489" size="100,100" alphatest="blend" />'])
			elif config.plugins.KravenVB.Logo.value == "logo":
				self.skinSearchAndReplace.append(['<panel name="menu" />', '<eLabel backgroundColor="KravenBackground3" position="0,0" size="1280,720" transparent="0" zPosition="-10" /><ePixmap backgroundColor="KravenBackground3" pixmap="KravenVB/logo.png" position="930,100" size="200,200" alphatest="blend" /><widget backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="938,334" render="Label" size="65,80" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%H</convert></widget><eLabel backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="995,334" size="15,80" text=":" transparent="1" valign="center" zPosition="1" /><widget backgroundColor="KravenBackground3" font="Regular; 43" foregroundColor="KravenFont1" halign="center" position="1005,334" render="Label" size="65,80" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%M</convert></widget><eLabel backgroundColor="KravenBackground3" font="Regular; 32" foregroundColor="KravenFont1" halign="center" position="1061,348" size="15,60" text=":" transparent="1" valign="center" zPosition="1" /><widget backgroundColor="KravenBackground3" font="Regular; 32" foregroundColor="KravenFont1" halign="center" position="1071,348" render="Label" size="50,60" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%S</convert></widget><widget backgroundColor="KravenBackground3" font="Regular; 18" foregroundColor="KravenFont1" halign="center" position="928,404" render="Label" size="203,30" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%A</convert></widget><widget backgroundColor="KravenBackground3" font="Regular; 18" foregroundColor="KravenFont1" halign="center" position="928,429" render="Label" size="203,30" source="global.CurrentTime" transparent="1" valign="center" zPosition="1"><convert type="ClockToText">Format:%e. %B</convert></widget><ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" /><ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />'])
			
			### Font Colors
			self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#' + config.plugins.KravenVB.Font1.value])
			self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#' + config.plugins.KravenVB.Font2.value])
			self.skinSearchAndReplace.append(['name="KravenIBFont1" value="#00ffffff', 'name="KravenIBFont1" value="#' + config.plugins.KravenVB.IBFont1.value])
			self.skinSearchAndReplace.append(['name="KravenIBFont2" value="#00F0A30A', 'name="KravenIBFont2" value="#' + config.plugins.KravenVB.IBFont2.value])
			if config.plugins.KravenVB.EMCSelectionColors.value == "none":
				self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
				self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
			elif config.plugins.KravenVB.EMCSelectionColors.value == "emc-colors-on":
				self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
				self.skinSearchAndReplace.append(['name="KravenEMCSelFont" value="#00ffffff', 'name="KravenEMCSelFont" value="#' + config.plugins.KravenVB.EMCSelectionFont.value])
			self.skinSearchAndReplace.append(['name="selectedFG" value="#00ffffff', 'name="selectedFG" value="#' + config.plugins.KravenVB.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenMarkedFont" value="#00ffffff', 'name="KravenMarkedFont" value="#' + config.plugins.KravenVB.MarkedFont.value])
			self.skinSearchAndReplace.append(['name="KravenECMFont" value="#00ffffff', 'name="KravenECMFont" value="#' + config.plugins.KravenVB.ECMFont.value])
			self.skinSearchAndReplace.append(['name="KravenChannelnameFont" value="#00ffffff', 'name="KravenChannelnameFont" value="#' + config.plugins.KravenVB.ChannelnameFont.value])
			self.skinSearchAndReplace.append(['name="KravenButtonText" value="#00ffffff', 'name="KravenButtonText" value="#' + config.plugins.KravenVB.ButtonText.value])
			
			### ChannelSelection Font-Size
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
			
			### Primetime
			if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
				self.skinSearchAndReplace.append(['<!--<widget', '<widget'])
				self.skinSearchAndReplace.append(['</widget>-->', '</widget>'])
				self.skinSearchAndReplace.append(['name="KravenPrimetimeFont" value="#0070AD11', 'name="KravenPrimetimeFont" value="#' + config.plugins.KravenVB.PrimetimeFont.value])
			elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-off":
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgList" size="362,54"', 'render="KravenVBSingleEpgList" size="362,81"'])
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgList" size="400,54"', 'render="KravenVBSingleEpgList" size="400,81"'])
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgList" size="505,27"', 'render="KravenVBSingleEpgList" size="505,54"'])
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgList" size="778,81"', 'render="KravenVBSingleEpgList" size="778,108"'])
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgListNobile" size="339,572"', 'render="KravenVBSingleEpgListNobile" size="339,594"'])
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgList" size="474,308"', 'render="KravenVBSingleEpgList" size="474,330"'])
			
			### Debug-Names
			if config.plugins.KravenVB.DebugNames.value == "screennames-on":
				self.skinSearchAndReplace.append(['<!--<eLabel backgroundColor="#00000000" font="Regular;13" foregroundColor="red"', '<eLabel backgroundColor="#00000000" font="Regular;15" foregroundColor="red"'])
				self.skinSearchAndReplace.append(['position="70,0" size="500,16" halign="left" valign="center" transparent="1" />-->', 'position="70,0" size="500,19" halign="left" valign="top" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,17" backgroundColor="#00000000" zPosition="8" />'])
				self.skinSearchAndReplace.append(['position="42,0" size="500,16" halign="left" valign="center" transparent="1" />-->', 'position="42,0" size="500,19" halign="left" valign="top" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,17" backgroundColor="#00000000" zPosition="8" />'])
				self.skinSearchAndReplace.append(['position="40,0" size="500,16" halign="left" valign="center" transparent="1" />-->', 'position="40,0" size="500,19" halign="left" valign="top" transparent="1" zPosition="9" /><eLabel position="0,0" size="1280,17" backgroundColor="#00000000" zPosition="8" />'])
			
			### Icons
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0" and config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-dark/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-dark/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-dark/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-dark/icons/key_ok"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/icons", "KravenVB/icons-dark/icons"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0" and config.plugins.KravenVB.IBColor.value == "only-infobar" and config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/icons/key_ok"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0" and config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/infobar/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/infobar/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/infobar/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/infobar/key_ok"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/icons", "KravenVB/icons-dark/icons"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0" and config.plugins.KravenVB.IBColor.value == "all-screens" and config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/infobar/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/infobar/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/infobar/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/infobar/key_ok"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=5" and config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-dark/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-dark/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-dark/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-dark/icons/key_ok"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/icons", "KravenVB/icons-dark/icons"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10" and config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-dark/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-dark/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-dark/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-dark/icons/key_ok"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/icons", "KravenVB/icons-dark/icons"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15" and config.plugins.KravenVB.IconStyle2.value == "icons-dark2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-dark/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-dark/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-dark/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-dark/icons/key_ok"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/icons", "KravenVB/icons-dark/icons"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=5" and config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/icons/key_ok"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10" and config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/icons/key_ok"])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15" and config.plugins.KravenVB.IconStyle2.value == "icons-light2":
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_epg", "KravenVB/icons-light/icons/key_epg"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_exit", "KravenVB/icons-light/icons/key_exit"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_menu", "KravenVB/icons-light/icons/key_menu"])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/key_ok", "KravenVB/icons-light/icons/key_ok"])
			
			### Infobar-Icons
			if config.plugins.KravenVB.IconStyle.value == "icons-dark":
				self.skinSearchAndReplace.append(['name="KravenButtonStyleFont" value="#00fff0e0"', 'name="KravenButtonStyleFont" value="#00000000"'])
				self.skinSearchAndReplace.append(["KravenVB/icons-light/infobar", "KravenVB/icons-dark/infobar"])
			
			### Weather-View
			if config.plugins.KravenVB.WeatherView.value == "meteo":
				self.skinSearchAndReplace.append(['size="50,50" render="KravenVBPiconUni" alphatest="blend" path="WetterIcons"', 'size="50,50" render="Label" font="Meteo; 40" halign="right" valign="center" foregroundColor="KravenMeteoFont" backgroundColor="KravenInfobarBackground" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="50,50" path="WetterIcons" render="KravenVBPiconUni" alphatest="blend"', 'size="50,50" render="Label" font="Meteo; 45" halign="center" valign="center" foregroundColor="KravenMeteoFont" backgroundColor="KravenInfobarBackground" noWrap="1"'])
				self.skinSearchAndReplace.append(['size="70,70" render="KravenVBPiconUni" alphatest="blend" path="WetterIcons"', 'size="70,70" render="Label" font="Meteo; 70" halign="center" valign="center" foregroundColor="KravenMeteoFont" backgroundColor="KravenInfobarBackground" noWrap="1"'])
				self.skinSearchAndReplace.append(['convert  type="KravenVBWeather">currentWeatherPicon', 'convert  type="KravenVBWeather">currentWeatherCode'])
				self.skinSearchAndReplace.append(['convert  type="KravenVBWeather">forecastTomorrowPicon', 'convert  type="KravenVBWeather">forecastTomorrowCode'])
				self.skinSearchAndReplace.append(['convert  type="KravenVBWeather">forecastTomorrow1Picon', 'convert  type="KravenVBWeather">forecastTomorrow1Code'])
				self.skinSearchAndReplace.append(['convert  type="KravenVBWeather">forecastTomorrow2Picon', 'convert  type="KravenVBWeather">forecastTomorrow2Code'])
				self.skinSearchAndReplace.append(['convert  type="KravenVBWeather">forecastTomorrow3Picon', 'convert  type="KravenVBWeather">forecastTomorrow3Code'])
			
			### Meteo-Font
			if config.plugins.KravenVB.MeteoColor.value == "meteo-dark":
				self.skinSearchAndReplace.append(['name="KravenMeteoFont" value="#00fff0e0"', 'name="KravenMeteoFont" value="#00000000"'])
			
			### Progress
			if config.plugins.KravenVB.Progress.value == "progress2":
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress18.png"',' pixmap="KravenVB/progress/progress18_2.png"'])
				self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenVB/progress/progress52.png"',' picServiceEventProgressbar="KravenVB/progress/progress52_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress170.png"',' pixmap="KravenVB/progress/progress170_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress220.png"',' pixmap="KravenVB/progress/progress220_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress248.png"',' pixmap="KravenVB/progress/progress248_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"',' pixmap="KravenVB/progress/progress300_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"',' pixmap="KravenVB/progress/progress328_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"',' pixmap="KravenVB/progress/progress370_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"',' pixmap="KravenVB/progress/progress380_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"',' pixmap="KravenVB/progress/progress410_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"',' pixmap="KravenVB/progress/progress581_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"',' pixmap="KravenVB/progress/progress599_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress749.png"',' pixmap="KravenVB/progress/progress749_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress858.png"',' pixmap="KravenVB/progress/progress858_2.png"'])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress990.png"',' pixmap="KravenVB/progress/progress990_2.png"'])
			elif not config.plugins.KravenVB.Progress.value == "progress":
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress18.png"'," "])
				self.skinSearchAndReplace.append([' picServiceEventProgressbar="KravenVB/progress/progress52.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress170.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress220.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress248.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress300.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress328.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress370.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress380.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress410.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress581.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress599.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress749.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress858.png"'," "])
				self.skinSearchAndReplace.append([' pixmap="KravenVB/progress/progress990.png"'," "])
				self.skinSearchAndReplace.append(['name="KravenProgress" value="#00C3461B', 'name="KravenProgress" value="#' + config.plugins.KravenVB.Progress.value])
			
			### Border
			self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#' + config.plugins.KravenVB.Border.value])
			
			### Line
			self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#' + config.plugins.KravenVB.Line.value])
			
			### Runningtext
			if config.plugins.KravenVB.RunningText.value == "movetype=none":
				self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
			if not config.plugins.KravenVB.RunningText.value == "movetype=none":
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
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="0"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="10"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="15"'])
			
			### Selectionborder
			if not config.plugins.KravenVB.SelectionBorder.value == "none":
				self.selectionbordercolor = config.plugins.KravenVB.SelectionBorder.value
				self.borset = ("borset_" + self.selectionbordercolor + ".png")
				self.skinSearchAndReplace.append(["borset.png", self.borset])
			
			### IB Color visible
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				if config.plugins.KravenVB.IBColor.value == "only-infobar":
					if config.plugins.KravenVB.BackgroundColor.value == "self":
						self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
					else:
						self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.BackgroundColor.value])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="380,400" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="380,443" alphatest="blend" zPosition="-9" />'," "])
				elif config.plugins.KravenVB.IBColor.value == "all-screens":
					self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.InfobarColorTrans.value + "797979"])
					self.skinSearchAndReplace.append(['backgroundColor="KravenInfobar2Background" font="Regular2;34" foregroundColor="KravenFont2"', 'backgroundColor="KravenInfobar2Background" font="Regular2;34" foregroundColor="KravenIBFont2"'])
					self.skinSearchAndReplace.append(['position="1138,22" size="100,28" foregroundColor="KravenFont1"', 'position="1138,22" size="100,28" foregroundColor="KravenIBFont1"'])
			elif config.plugins.KravenVB.ScrollBar.value in ("scrollbarWidth=5","scrollbarWidth=10","scrollbarWidth=15"):
				if config.plugins.KravenVB.BackgroundColor.value == "self":
					self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + self.skincolorbackgroundcolor])
				else:
					self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.BackgroundColor.value])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibar.png" position="0,570" size="380,400" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/ibaro.png" position="0,-60" size="380,443" alphatest="blend" zPosition="-9" />'," "])
			
			### Clock Analog Style
			self.analogstylecolor = config.plugins.KravenVB.AnalogStyle.value
			self.analog = ("analog_" + self.analogstylecolor + ".png")
			self.skinSearchAndReplace.append(["analog.png", self.analog])
			
			### Header
			self.appendSkinFile(self.daten + "header_begin.xml")
			if not config.plugins.KravenVB.SelectionBorder.value == "none":
				self.appendSkinFile(self.daten + "header_middle.xml")
			self.appendSkinFile(self.daten + "header_end.xml")
			
			### Volume
			self.appendSkinFile(self.daten + config.plugins.KravenVB.Volume.value + ".xml")
			
			### ChannelSelection
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

			### Infobox
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x1","infobar-style-x2","infobar-style-z1","infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				if config.plugins.KravenVB.Infobox.value == "cpu":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="  L:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenButtonStyleFont" />-->', 'foregroundColor="KravenButtonStyleFont" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBLayoutInfo">LoadAvg'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBExtServiceInfo">OrbitalPosition', 'convert  type="KravenVBCpuUsage">$0'])
				elif config.plugins.KravenVB.Infobox.value == "temp":
					self.skinSearchAndReplace.append(['<!--<eLabel text="  S:"', '<eLabel text="U:"'])
					self.skinSearchAndReplace.append(['foregroundColor="KravenButtonStyleFont" />-->', 'foregroundColor="KravenButtonStyleFont" />'])
					self.skinSearchAndReplace.append(['  source="session.FrontendStatus', ' source="session.CurrentService'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert type="KravenVBTempFanInfo">FanInfo'])
					self.skinSearchAndReplace.append(['convert  type="KravenVBExtServiceInfo">OrbitalPosition', 'convert  type="KravenVBTempFanInfo">TempInfo'])

			### Infobar_begin
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + "infobar-begin-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				self.appendSkinFile(self.daten + "infobar-begin-zz1.xml")
			else:
				self.appendSkinFile(self.daten + "infobar-begin.xml")

			### Infobar_main
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarStyle.value + "_main.xml")

			### Infobar_top
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
				elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")

			### Channelname
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName3.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName4.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName5.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName6.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName7.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName8.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName9.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName10.value + ".xml")

			### clock-style_ib
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zzz1"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle3.value + ".xml")
				
			### FTA
			if config.plugins.KravenVB.FTA.value == "none":
				self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

			### ecm-contents
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if not config.plugins.KravenVB.ECMLine1.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

			### ecm-info
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if not config.plugins.KravenVB.ECMLine1.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

			### system-info
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SystemInfo.value + ".xml")

			### weather-style
			self.appendSkinFile(self.daten + self.actWeatherstyle + ".xml")
			if self.actWeatherstyle == "none" and self.actClockstyle != "clock-android":
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
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1""infobar-style-zzz1"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle3.value + ".xml")

			### SIB_main
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + "infobar-style-x1_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
				self.appendSkinFile(self.daten + "infobar-style-x2_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB1.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
				self.appendSkinFile(self.daten + "infobar-style-x3_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + "infobar-style-z1_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB3.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
				self.appendSkinFile(self.daten + "infobar-style-z2_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB4.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
				self.appendSkinFile(self.daten + "infobar-style-zz1_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB5.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + "infobar-style-zz2_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB6.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + "infobar-style-zz3_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB7.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				self.appendSkinFile(self.daten + "infobar-style-zz4_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB8.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + "infobar-style-zzz1_main.xml")
				self.appendSkinFile(self.daten + config.plugins.KravenVB.SIB9.value + ".xml")
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/SecondInfoBar/plugin.py"):
				config.plugins.SecondInfoBar.HideNormalIB.value = True
				config.plugins.SecondInfoBar.HideNormalIB.save()

			### Main XML
			self.appendSkinFile(self.daten + "main.xml")

			### Timeshift_begin
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + "timeshift-begin-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1", "infobar-style-zz4", "infobar-style-zzz1"):
				self.appendSkinFile(self.daten + "timeshift-begin-zz1.xml")
			else:
				self.appendSkinFile(self.daten + "timeshift-begin.xml")
				
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1","weather-big"):
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.daten + "timeshift-begin-leftlow.xml")
				else:
					self.appendSkinFile(self.daten + "timeshift-begin-low.xml")
			elif config.plugins.KravenVB.WeatherStyle.value == "weather-small":
				self.appendSkinFile(self.daten + "timeshift-begin-left.xml")
			else:
				self.appendSkinFile(self.daten + "timeshift-begin-high.xml")

			### Timeshift_Infobar_main
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarStyle.value + "_main.xml")

			### Timeshift_Infobar_top
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top.xml")
				elif config.plugins.KravenVB.IBtop.value == "infobar-x2-z1_top2":
					self.appendSkinFile(self.daten + "infobar-x2-z1_top2.xml")

			### Timeshift_Channelname
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName3.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName4.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName5.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName6.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName7.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName8.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName9.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarChannelName10.value + ".xml")

			### Timeshift_clock-style_ib
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2","infobar-style-zz2","infobar-style-zz3"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1""infobar-style-zzz1"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle3.value + ".xml")
				
			### Timeshift_FTA
			if config.plugins.KravenVB.FTA.value == "none":
				self.skinSearchAndReplace.append(['FTAVisible</convert>', 'FTAInvisible</convert>'])

			### Timeshift_ecm-contents
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if not config.plugins.KravenVB.ECMLine1.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine1.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-x3","infobar-style-z1","infobar-style-z2"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine2.value])
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.skinSearchAndReplace.append(['<convert type="KravenVBECMLine">ShortReader', '<convert type="KravenVBECMLine">' + config.plugins.KravenVB.ECMLine3.value])

			### Timeshift_ecm-info
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if not config.plugins.KravenVB.ECMLine1.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x3","infobar-style-z2"):
				if not config.plugins.KravenVB.ECMLine2.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-zz1","infobar-style-zz4","infobar-style-zzz1"):
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				if not config.plugins.KravenVB.ECMLine3.value == "none":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

			### Timeshift_system-info
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SystemInfo.value + ".xml")

			### Timeshift_weather-style
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x1","infobar-style-x3","infobar-style-z2","infobar-style-zz1","infobar-style-zz2","infobar-style-zz3","infobar-style-zz4","infobar-style-zzz1"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.WeatherStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					if config.plugins.KravenVB.WeatherStyle3.value == "weather-left":
						self.appendSkinFile(self.daten + "weather-left.xml")
				else:
					self.appendSkinFile(self.daten + config.plugins.KravenVB.WeatherStyle2.value + ".xml")

			### Timeshift_end
			self.appendSkinFile(self.daten + "timeshift-end.xml")
			
			### Plugins XML
			self.appendSkinFile(self.daten + "plugins.xml")
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/PermanentTimeshift/plugin.py"):
				config.plugins.pts.showinfobar.value = False
				config.plugins.pts.showinfobar.save()
			
			### InfobarTunerState
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1","weather-big"):
				if config.plugins.KravenVB.SystemInfo.value == "systeminfo-bigsat":
					self.appendSkinFile(self.daten + "infobartunerstate-low.xml")
				else:
					self.appendSkinFile(self.daten + "infobartunerstate-mid.xml")
			else:
				self.appendSkinFile(self.daten + "infobartunerstate-high.xml")

			### NetatmoBar XML
			if config.plugins.KravenVB.InfobarStyle.value in ("infobar-style-x2","infobar-style-z1"):
				if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/Netatmo/plugin.py"):
					if config.plugins.KravenVB.WeatherStyle3.value == "netatmobar":
						self.appendSkinFile(self.daten + "netatmobar.xml")

			### EMCSTYLE
			self.appendSkinFile(self.daten + config.plugins.KravenVB.EMCStyle.value + ".xml")			

			### NumberZapExtStyle
			self.appendSkinFile(self.daten + config.plugins.KravenVB.NumberZapExt.value + ".xml")
			if not config.plugins.KravenVB.NumberZapExt.value == "none":
				config.usage.numberzap_show_picon.value = True
				config.usage.numberzap_show_picon.save()
				config.usage.numberzap_show_servicename.value = True
				config.usage.numberzap_show_servicename.save()

			### cooltv XML
			self.appendSkinFile(self.daten + config.plugins.KravenVB.CoolTVGuide.value + ".xml")

			### MovieSelection XML
			self.appendSkinFile(self.daten + config.plugins.KravenVB.MovieSelection.value + ".xml")

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

			#system('rm -rf ' + self.dateiTMP)

		self.makeIbarpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value) # ibars

		if config.plugins.KravenVB.SystemInfo.value == "systeminfo-small":
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 185, "info") # sysinfo small
		elif config.plugins.KravenVB.SystemInfo.value == "systeminfo-big":
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 275, "info") # sysinfo big
		else:
			self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 375, "info") # sysinfo bigsat

		self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 905, 170, "shift") # timeshift bar
		
		self.makeRectpng(self.skincolorinfobarcolor, config.plugins.KravenVB.InfobarColorTrans.value, 400, 200, "wsmall") # weather small
			
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

	def reset(self):
		askReset = self.session.openWithCallback(self.doReset,MessageBox,_("Do you really want to reset all values to their defaults?"), MessageBox.TYPE_YESNO)
		askReset.setTitle(_("Reset profile"))

	def doReset(self,answer):
		if answer is True:
			for name in config.plugins.KravenVB.dict():
				if name is not "customProfile":
					item=(getattr(config.plugins.KravenVB,name))
					item.value=item.default
		self.mylist()

	def showColor(self,actcolor):
		c = self["Canvas"]
		c.fill(0, 0, 368, 207, actcolor)
		c.flush()

	def loadProfile(self):
		profile=config.plugins.KravenVB.customProfile.value
		if profile:
			fname=self.profiles+"kraven_profile_"+profile
			if fileExists(fname):
				print ("KravenPlugin: Load profile "+str(profile))
				pFile=open(fname,"r")
				for line in pFile:
					try:
						line=line.split("|")
						name=line[0]
						value=line[1]
						type=line[2].strip('\n')
						if name != "customProfile":
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
			else:
				print ("KravenPlugin: Create profile "+str(profile))
				self.saveProfile(msg=False)

	def saveProfile(self,msg=True):
		profile=config.plugins.KravenVB.customProfile.value
		if profile:
			print ("KravenPlugin: Save profile "+str(profile))
			try:
				fname=self.profiles+"kraven_profile_"+profile
				pFile=open(fname,"w")
				for name in config.plugins.KravenVB.dict():
					if name != "customProfile":
						value=getattr(config.plugins.KravenVB,name).value
						pFile.writelines(name+"|"+str(value)+"|"+str(type(value))+"\n")
				pFile.close()
				if msg:
					self.session.open(MessageBox,_("Profile ")+str(profile)+_(" saved successfully."), MessageBox.TYPE_INFO, timeout=5)
			except:
				self.session.open(MessageBox,_("Profile ")+str(profile)+_(" could not be saved!"), MessageBox.TYPE_INFO, timeout=15)

	def makeIbarpng(self, newcolor, newtrans):
		
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
		img.save("/usr/share/enigma2/KravenVB/ibar.png")
		
		img = Image.new("RGBA",(width,ibaroheight),(r,g,b,0))
		gradient = Image.new("L",(1,ibaroheight),0)
		for pos in range(0,ibarogradientstart):
			gradient.putpixel((0,pos),int(255*trans))
		for pos in range(0,ibarogradientsize):
			gradient.putpixel((0,ibarogradientstart+ibarogradientsize-pos-1),int(self.dexpGradient(ibarogradientsize,gradientspeed,pos)*trans))
		alpha = gradient.resize(img.size)
		img.putalpha(alpha)
		img.save("/usr/share/enigma2/KravenVB/ibaro.png")
			
	def makeRectpng(self, newcolor, newtrans, width, height, pngname):
		
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

		img.save("/usr/share/enigma2/KravenVB/"+pngname+".png")
			
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
		
	def makeBackpng(self):
		# this makes a transparent png
		# not needed above, use it manually
		width = 1280 # width of the png file
		height = 720 # height of the png file
		img = Image.new("RGBA",(width,height),(0,0,0,0))
		img.save("/usr/share/enigma2/KravenVB/backg.png")
			
	def hexRGB(self,color):
		color = color[-6:]
		r = int(color[0:2], 16)
		g = int(color[2:4], 16)
		b = int(color[4:6], 16)
		return (r<<16)|(g<<8)|b

	def RGB(self,r,g,b):
		return (r<<16)|(g<<8)|b
