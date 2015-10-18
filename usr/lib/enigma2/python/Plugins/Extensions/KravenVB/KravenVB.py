#######################################################################
#
# KravenVB by Team Kraven
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
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger, ConfigClock
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext, time
from enigma import ePicLoad, getDesktop, eConsoleAppContainer
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
config.plugins.KravenVB.refreshInterval = ConfigNumber(default="10")
config.plugins.KravenVB.Primetime = ConfigClock(default=time.mktime((0, 0, 0, 20, 15, 0, 0, 0, 0)))
				
config.plugins.KravenVB.Volume = ConfigSelection(default="volume-border", choices = [
				("volume-original", _("original")),
				("volume-border", _("with Border")),
				("volume-left", _("left")),
				("volume-right", _("right")),
				("volume-top", _("top")),
				("volume-center", _("center"))
				])
				
config.plugins.KravenVB.BackgroundColorTrans = ConfigSelection(default="00", choices = [
				("00", _("off")),
				("0A", _("low")),
				("4A", _("medium")),
				("8C", _("high"))
				])
				
config.plugins.KravenVB.Background = ConfigSelection(default="000000", choices = [
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
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
				])
				
config.plugins.KravenVB.SkinColorInfobar = ConfigSelection(default="000000", choices = [
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
				("647687", _("steel")),
				("262C33", _("steel dark")),
				("6C0AAB", _("violet")),
				("1F0333", _("violet dark")),
				("ffffff", _("white"))
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
				
config.plugins.KravenVB.Progress = ConfigSelection(default="00C3461B", choices = [
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
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right"))
				])
							
config.plugins.KravenVB.ChannelSelectionStyle2 = ConfigSelection(default="channelselection-style-minitv", choices = [
				("channelselection-style-nopicon", _("no Picon")),
				("channelselection-style-zpicon", _("Z-Picons")),
				("channelselection-style-xpicon", _("X-Picons")),
				("channelselection-style-zzpicon", _("ZZ-Picons")),
				("channelselection-style-zzzpicon", _("ZZZ-Picons")),
				("channelselection-style-nobile", _("Nobile")),
				("channelselection-style-nobile2", _("Nobile 2")),
				("channelselection-style-nobile-minitv", _("Nobile MiniTV")),
				("channelselection-style-minitv", _("MiniTV left")),
				("channelselection-style-minitv4", _("MiniTV right")),
				("channelselection-style-minitv2", _("MiniTV/PIP")),
				("channelselection-style-minitv22", _("MiniTV/PIP 2")),
				("channelselection-style-minitv3", _("PIP"))
				])
				
config.plugins.KravenVB.NumberZapExt = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("numberzapext-zpicon", _("Z-Picons")),
				("numberzapext-xpicon", _("X-Picons")),
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
				("startdelay=10000", _("10 sec"))
				])
				
config.plugins.KravenVB.ScrollBar = ConfigSelection(default="scrollbarWidth=10", choices = [
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
				
config.plugins.KravenVB.ECMInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("ecm-info-on", _("on"))
				])
				
config.plugins.KravenVB.SystemInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("systeminfo-big", _("big")),
				("systeminfo-small", _("small"))
				])
				
config.plugins.KravenVB.SatInfo = ConfigSelection(default="none", choices = [
				("none", _("off")),
				("satinfo", _("on"))
				])
				
config.plugins.KravenVB.SIB = ConfigSelection(default="infobar-style-x1_end", choices = [
				("infobar-style-x1_end", _("top/bottom")),
				("infobar-style-x1_end2", _("left/right")),
				("infobar-style-x1_end3", _("single")),
				("infobar-style-x1_end4", _("MiniTV")),
				("infobar-style-x1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB1 = ConfigSelection(default="infobar-style-x2_end", choices = [
				("infobar-style-x2_end", _("top/bottom")),
				("infobar-style-x2_end2", _("left/right")),
				("infobar-style-x2_end3", _("single")),
				("infobar-style-x2_end4", _("MiniTV")),
				("infobar-style-x2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB2 = ConfigSelection(default="infobar-style-x3_end", choices = [
				("infobar-style-x3_end", _("top/bottom")),
				("infobar-style-x3_end2", _("left/right")),
				("infobar-style-x3_end3", _("single")),
				("infobar-style-x3_end4", _("MiniTV")),
				("infobar-style-x3_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB3 = ConfigSelection(default="infobar-style-z1_end", choices = [
				("infobar-style-z1_end", _("top/bottom")),
				("infobar-style-z1_end2", _("left/right")),
				("infobar-style-z1_end3", _("single")),
				("infobar-style-z1_end4", _("MiniTV")),
				("infobar-style-z1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB4 = ConfigSelection(default="infobar-style-z2_end", choices = [
				("infobar-style-z2_end", _("top/bottom")),
				("infobar-style-z2_end2", _("left/right")),
				("infobar-style-z2_end3", _("single")),
				("infobar-style-z2_end4", _("MiniTV")),
				("infobar-style-z2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB5 = ConfigSelection(default="infobar-style-zz1_end", choices = [
				("infobar-style-zz1_end", _("top/bottom")),
				("infobar-style-zz1_end2", _("left/right")),
				("infobar-style-zz1_end3", _("single")),
				("infobar-style-zz1_end4", _("MiniTV")),
				("infobar-style-zz1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB6 = ConfigSelection(default="infobar-style-zz2_end", choices = [
				("infobar-style-zz2_end", _("top/bottom")),
				("infobar-style-zz2_end2", _("left/right")),
				("infobar-style-zz2_end3", _("single")),
				("infobar-style-zz2_end4", _("MiniTV")),
				("infobar-style-zz2_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB7 = ConfigSelection(default="infobar-style-zz3_end", choices = [
				("infobar-style-zz3_end", _("top/bottom")),
				("infobar-style-zz3_end2", _("left/right")),
				("infobar-style-zz3_end3", _("single")),
				("infobar-style-zz3_end4", _("MiniTV")),
				("infobar-style-zz3_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB8 = ConfigSelection(default="infobar-style-zz4_end", choices = [
				("infobar-style-zz4_end", _("top/bottom")),
				("infobar-style-zz4_end2", _("left/right")),
				("infobar-style-zz4_end3", _("single")),
				("infobar-style-zz4_end4", _("MiniTV")),
				("infobar-style-zz4_end5", _("Weather"))
				])
				
config.plugins.KravenVB.SIB9 = ConfigSelection(default="infobar-style-zzz1_end", choices = [
				("infobar-style-zzz1_end", _("top/bottom")),
				("infobar-style-zzz1_end2", _("left/right")),
				("infobar-style-zzz1_end3", _("single")),
				("infobar-style-zzz1_end4", _("MiniTV")),
				("infobar-style-zzz1_end5", _("Weather"))
				])
				
config.plugins.KravenVB.IBtop = ConfigSelection(default="infobar-x2-z1_top", choices = [
				("infobar-x2-z1_top", _("Icons + 4 Tuner + Resolution + Infobox")),
				("infobar-x2-z1_top2", _("Icons + REC + 2 Tuner + Resolution + Infobox"))
				])
				
config.plugins.KravenVB.Infobox = ConfigSelection(default="sat", choices = [
				("sat", _("Tuner/Satellite + SNR")),
				("db", _("Tuner/Satellite + dB")),
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
				
config.plugins.KravenVB.Logo = ConfigSelection(default="logo", choices = [
				("logo", _("Logo")),
				("minitv", _("MiniTV"))
				])
				
config.plugins.KravenVB.DebugNames = ConfigSelection(default="screennames-off", choices = [
				("screennames-off", _("off")),
				("screennames-on", _("on"))
				])
				
config.plugins.KravenVB.WeatherView = ConfigSelection(default="icon", choices = [
				("icon", _("Icon")),
				("meteo", _("Meteo"))
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
				
#######################################################################

class KravenVB(ConfigListScreen, Screen):
	skin = """
<screen name="KravenVB-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#00000000">
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="70,665" size="220,26" text="Cancel" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="320,665" size="220,26" text="Save" transparent="1" />
  <eLabel font="Regular; 20" foregroundColor="#00ffffff" backgroundColor="#00000000" halign="left" valign="center" position="570,665" size="220,26" text="Reboot" transparent="1" />
  <widget name="config" position="70,70" size="708,570" itemHeight="30" font="Regular;24" transparent="1" enableWrapAround="1" scrollbarMode="showOnDemand" scrollbarWidth="5" zPosition="1" backgroundColor="#00000000" />
  <eLabel position="70,15" size="708,46" text="KravenVB - Konfigurationstool" font="Regular; 35" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="847,278" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="847,487" size="368,2" backgroundColor="#00f0a30a" />
  <eLabel position="845,278" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel position="1215,278" size="2,211" backgroundColor="#00f0a30a" />
  <eLabel backgroundColor="#00000000" position="0,0" size="1280,720" transparent="0" zPosition="-9" />
  <ePixmap pixmap="KravenVB/buttons/key_red1.png" position="65,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_green1.png" position="315,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <ePixmap pixmap="KravenVB/buttons/key_yellow1.png" position="565,692" size="200,5" backgroundColor="#00000000" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1154,16" size="100,28" font="Regular;26" halign="right" backgroundColor="#00000000" transparent="1" valign="center" foregroundColor="#00ffffff">
    <convert type="ClockToText">Default</convert>
  </widget>
  <eLabel position="830,80" size="402,46" text="KravenVB" font="Regular; 36" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00f0a30a" name="," />
  <eLabel position="830,130" size="402,46" text="for VTi-Image" font="Regular; 26" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <eLabel position="845,180" size="372,46" text="Version: 2.5.0" font="Regular; 30" valign="center" halign="center" transparent="1" backgroundColor="#00000000" foregroundColor="#00ffffff" name="," />
  <ePixmap backgroundColor="#00000000" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/about.png" position="847,280" size="368,207" zPosition="-9" />
  <widget name="helperimage" position="847,280" size="368,207" zPosition="1" backgroundColor="#00000000" />
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
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		
		list = []
		ConfigListScreen.__init__(self, list)
		
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions", "KravenVBConfigActions"],
		{
			"left": self.keyLeft,
			"down": self.keyDown,
			"up": self.keyUp,
			"right": self.keyRight,
			"red": self.exit,
			"yellow": self.reboot,
			"blue": self.showInfo,
			"green": self.save,
			"cancel": self.exit,
			"nextBouquet": self.pageUp,
			"prevBouquet": self.pageDown
		}, -1)
		
		self.UpdatePicture()
		self.onLayoutFinish.append(self.mylist)

	def mylist(self):		
		list = []
		list.append(getConfigListEntry(_("About"), config.plugins.KravenVB.About))
		list.append(getConfigListEntry(_("______________________ System __________________________________"), ))
		list.append(getConfigListEntry(_("Icons (except Infobar)"), config.plugins.KravenVB.IconStyle2))
		list.append(getConfigListEntry(_("Running Text (Delay)"), config.plugins.KravenVB.RunningText))
		list.append(getConfigListEntry(_("Scrollbars"), config.plugins.KravenVB.ScrollBar))
		list.append(getConfigListEntry(_("Menus"), config.plugins.KravenVB.Logo))
		list.append(getConfigListEntry(_("______________________ Global-Colors ___________________________"), ))
		list.append(getConfigListEntry(_("Background"), config.plugins.KravenVB.Background))
		list.append(getConfigListEntry(_("Background-Transparency"), config.plugins.KravenVB.BackgroundColorTrans))
		list.append(getConfigListEntry(_("Listselection"), config.plugins.KravenVB.SelectionBackground))
		list.append(getConfigListEntry(_("Listselection-Border"), config.plugins.KravenVB.SelectionBorder))
		list.append(getConfigListEntry(_("Progress-/Volumebar"), config.plugins.KravenVB.Progress))
		list.append(getConfigListEntry(_("Progress-Border"), config.plugins.KravenVB.Border))
		list.append(getConfigListEntry(_("Lines"), config.plugins.KravenVB.Line))
		list.append(getConfigListEntry(_("Primary-Font"), config.plugins.KravenVB.Font1))
		list.append(getConfigListEntry(_("Secondary-Font"), config.plugins.KravenVB.Font2))
		list.append(getConfigListEntry(_("Selection-Font"), config.plugins.KravenVB.SelectionFont))
		list.append(getConfigListEntry(_("Marking-Font"), config.plugins.KravenVB.MarkedFont))
		list.append(getConfigListEntry(_("Colorbutton-Font"), config.plugins.KravenVB.ButtonText))
		list.append(getConfigListEntry(_("______________________ Weather _________________________________"), ))
		list.append(getConfigListEntry(_("Weather-ID"), config.plugins.KravenVB.weather_city))
		list.append(getConfigListEntry(_("Refresh interval (in minutes)"), config.plugins.KravenVB.refreshInterval))
		list.append(getConfigListEntry(_("Weather-Style"), config.plugins.KravenVB.WeatherView))
		if config.plugins.KravenVB.WeatherView.value == "meteo":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenVB.MeteoColor))
		elif config.plugins.KravenVB.WeatherView.value == "icon":
			list.append(getConfigListEntry(_("Meteo-Color"), config.plugins.KravenVB.MeteoColorNA))
		list.append(getConfigListEntry(_("______________________ Infobar _________________________________"), ))
		list.append(getConfigListEntry(_("Infobar-Style"), config.plugins.KravenVB.InfobarStyle))
		list.append(getConfigListEntry(_("Infobar-Background"), config.plugins.KravenVB.SkinColorInfobar))
		if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
			list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenVB.IBColor))
		elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=5" or config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10" or config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
			list.append(getConfigListEntry(_("Show Infobar-Background"), config.plugins.KravenVB.IBColorNA))
		list.append(getConfigListEntry(_("Infobar-Icons"), config.plugins.KravenVB.IconStyle))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenVB.IBtop))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Tuner number/Record"), config.plugins.KravenVB.IBtopNA))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.Infobox))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("Infobox-Contents"), config.plugins.KravenVB.InfoboxNA))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Weather"), config.plugins.KravenVB.WeatherStyle2))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName2))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName3))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName4))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName5))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName6))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName7))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName8))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName9))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("Channelname/-number"), config.plugins.KravenVB.InfobarChannelName10))
		list.append(getConfigListEntry(_("Channelname/-number-Font"), config.plugins.KravenVB.ChannelnameFont))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle2))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyle3))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("Clock-Style"), config.plugins.KravenVB.ClockStyleNA))
		if config.plugins.KravenVB.ClockStyle.value == "clock-analog" or config.plugins.KravenVB.ClockStyle2.value == "clock-analog" or config.plugins.KravenVB.ClockStyle3.value == "clock-analog":
			list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenVB.AnalogStyle))
		elif config.plugins.KravenVB.ClockStyle.value == "clock-classic" or config.plugins.KravenVB.ClockStyle.value == "clock-classic-big" or config.plugins.KravenVB.ClockStyle.value == "clock-android" or config.plugins.KravenVB.ClockStyle.value == "clock-color" or config.plugins.KravenVB.ClockStyle2.value == "clock-classic2" or config.plugins.KravenVB.ClockStyle2.value == "clock-classic-big2" or config.plugins.KravenVB.ClockStyle2.value == "clock-android" or config.plugins.KravenVB.ClockStyle2.value == "clock-color2" or config.plugins.KravenVB.ClockStyle3.value == "clock-classic3" or config.plugins.KravenVB.ClockStyle3.value == "clock-classic3" or config.plugins.KravenVB.ClockStyle3.value == "clock-android" or config.plugins.KravenVB.ClockStyle3.value == "clock-color3":
			list.append(getConfigListEntry(_("Analog-Clock-Color"), config.plugins.KravenVB.AnalogStyleNA))
		list.append(getConfigListEntry(_("System-Infos"), config.plugins.KravenVB.SystemInfo))
		list.append(getConfigListEntry(_("Satellite-Infos"), config.plugins.KravenVB.SatInfo))
		list.append(getConfigListEntry(_("ECM-Infos"), config.plugins.KravenVB.ECMInfo))
		list.append(getConfigListEntry(_("ECM-Font"), config.plugins.KravenVB.ECMFont))
		list.append(getConfigListEntry(_("______________________ Channellist _____________________________"), ))
		if fileExists("/usr/lib/enigma2/python/Components/Converter/MiniTVDisplay.py") and fileExists("/usr/lib/enigma2/python/Components/Renderer/MiniTV.py"):
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle2))
		else:
			list.append(getConfigListEntry(_("Channellist-Style"), config.plugins.KravenVB.ChannelSelectionStyle))
		list.append(getConfigListEntry(_("Primetime"), config.plugins.KravenVB.Primetimeavailable))
		if config.plugins.KravenVB.Primetimeavailable.value == "primetime-on":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.Primetime))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFont))
		elif config.plugins.KravenVB.Primetimeavailable.value == "primetime-off":
			list.append(getConfigListEntry(_("Primetime-Time"), config.plugins.KravenVB.PrimetimeNA))
			list.append(getConfigListEntry(_("Primetime-Font"), config.plugins.KravenVB.PrimetimeFontNA))
		list.append(getConfigListEntry(_("______________________ Views ___________________________________"), ))
		list.append(getConfigListEntry(_("Volume"), config.plugins.KravenVB.Volume))
		list.append(getConfigListEntry(_("CoolTVGuide"), config.plugins.KravenVB.CoolTVGuide))
		list.append(getConfigListEntry(_("EnhancedMovieCenter"), config.plugins.KravenVB.EMCStyle))
		list.append(getConfigListEntry(_("MovieSelection"), config.plugins.KravenVB.MovieSelection))
		if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB1))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB2))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB3))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB4))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB5))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB6))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB7))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB8))
		elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
			list.append(getConfigListEntry(_("SecondInfobar"), config.plugins.KravenVB.SIB9))
		list.append(getConfigListEntry(_("ExtNumberZap"), config.plugins.KravenVB.NumberZapExt))
		list.append(getConfigListEntry(_("______________________ Debug ___________________________________"), ))
		list.append(getConfigListEntry(_("Screennames"), config.plugins.KravenVB.DebugNames))
		
		self["config"].list = list
		self["config"].l.setList(list)
		
		self.ShowPicture()

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			if returnValue == "infobar-style-x1_end" or returnValue == "infobar-style-x2_end" or returnValue == "infobar-style-x3_end" or returnValue == "infobar-style-z1_end" or returnValue == "infobar-style-z2_end" or returnValue == "infobar-style-zz1_end" or returnValue == "infobar-style-zz2_end" or returnValue == "infobar-style-zz3_end" or returnValue == "infobar-style-zz4_end" or returnValue == "infobar-style-zzz1_end":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB.jpg"
			elif returnValue == "infobar-style-x1_end2" or returnValue == "infobar-style-x2_end2" or returnValue == "infobar-style-x3_end2" or returnValue == "infobar-style-z1_end2" or returnValue == "infobar-style-z2_end2" or returnValue == "infobar-style-zz1_end2" or returnValue == "infobar-style-zz2_end2" or returnValue == "infobar-style-zz3_end2" or returnValue == "infobar-style-zz4_end2" or returnValue == "infobar-style-zzz1_end2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB1.jpg"
			elif returnValue == "infobar-style-x1_end3" or returnValue == "infobar-style-x2_end3" or returnValue == "infobar-style-x3_end3" or returnValue == "infobar-style-z1_end3" or returnValue == "infobar-style-z2_end3" or returnValue == "infobar-style-zz1_end3" or returnValue == "infobar-style-zz2_end3" or returnValue == "infobar-style-zz3_end3" or returnValue == "infobar-style-zz4_end3" or returnValue == "infobar-style-zzz1_end3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB2.jpg"
			elif returnValue == "infobar-style-x1_end4" or returnValue == "infobar-style-x2_end4" or returnValue == "infobar-style-x3_end4" or returnValue == "infobar-style-z1_end4" or returnValue == "infobar-style-z2_end4" or returnValue == "infobar-style-zz1_end4" or returnValue == "infobar-style-zz2_end4" or returnValue == "infobar-style-zz3_end4" or returnValue == "infobar-style-zz4_end4" or returnValue == "infobar-style-zzz1_end4":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB3.jpg"
			elif returnValue == "infobar-style-x1_end5" or returnValue == "infobar-style-x2_end5" or returnValue == "infobar-style-x3_end5" or returnValue == "infobar-style-z1_end5" or returnValue == "infobar-style-z2_end5" or returnValue == "infobar-style-zz1_end5" or returnValue == "infobar-style-zz2_end5" or returnValue == "infobar-style-zz3_end5" or returnValue == "infobar-style-zz4_end5" or returnValue == "infobar-style-zzz1_end5":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/SIB4.jpg"
			elif returnValue == "clock-classic" or returnValue == "clock-classic2" or returnValue == "clock-classic3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-classic.jpg"
			elif returnValue == "clock-classic-big" or returnValue == "clock-classic-big2" or returnValue == "clock-classic-big3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-classic-big.jpg"
			elif returnValue == "clock-color" or returnValue == "clock-color2" or returnValue == "clock-color3":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/clock-color.jpg"
			elif returnValue == "00":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/none.jpg"
			elif returnValue == "startdelay=2000" or returnValue == "startdelay=4000" or returnValue == "startdelay=6000" or returnValue == "startdelay=8000" or returnValue == "startdelay=10000":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/running-delay.jpg"
			elif returnValue == "F0A30A" or returnValue == "00F0A30A":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/amber.jpg"
			elif returnValue == "B27708" or returnValue == "00B27708":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/amber_dark.jpg"
			elif returnValue == "1B1775" or returnValue == "001B1775":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/blue.jpg"
			elif returnValue == "0E0C3F" or returnValue == "000E0C3F":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/blue_dark.jpg"
			elif returnValue == "7D5929" or returnValue == "007D5929":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/brown.jpg"
			elif returnValue == "3F2D15" or returnValue == "003F2D15":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/brown_dark.jpg"
			elif returnValue == "progress":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull.jpg"
			elif returnValue == "progress2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/colorfull2.jpg"
			elif returnValue == "0050EF" or returnValue == "000050EF":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/cobalt.jpg"
			elif returnValue == "001F59" or returnValue == "00001F59":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/cobalt_dark.jpg"
			elif returnValue == "1BA1E2" or returnValue == "001BA1E2":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/cyan.jpg"
			elif returnValue == "0F5B7F" or returnValue == "000F5B7F":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/cyan_dark.jpg"
			elif returnValue == "FFEA04" or returnValue == "00FFEA04":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/yellow.jpg"
			elif returnValue == "999999" or returnValue == "00999999":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/grey.jpg"
			elif returnValue == "3F3F3F" or returnValue == "003F3F3F":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/grey_dark.jpg"
			elif returnValue == "70AD11" or returnValue == "0070AD11":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/green.jpg"
			elif returnValue == "213305" or returnValue == "00213305":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/green_dark.jpg"
			elif returnValue == "A19181" or returnValue == "00A19181":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/kraven.jpg"
			elif returnValue == "28150B" or returnValue == "0028150B":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/kraven_dark.jpg"
			elif returnValue == "6D8764" or returnValue == "006D8764":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/olive.jpg"
			elif returnValue == "313D2D" or returnValue == "00313D2D":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/olive_dark.jpg"
			elif returnValue == "C3461B" or returnValue == "00C3461B":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/orange.jpg"
			elif returnValue == "892E13" or returnValue == "00892E13":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/orange_dark.jpg"
			elif returnValue == "F472D0" or returnValue == "00F472D0":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/pink.jpg"
			elif returnValue == "723562" or returnValue == "00723562":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/pink_dark.jpg"
			elif returnValue == "E51400" or returnValue == "00E51400":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/red.jpg"
			elif returnValue == "330400" or returnValue == "00330400":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/red_dark.jpg"
			elif returnValue == "000000" or returnValue == "00000000":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/black.jpg"
			elif returnValue == "647687" or returnValue == "00647687":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/steel.jpg"
			elif returnValue == "262C33" or returnValue == "00262C33":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/steel_dark.jpg"
			elif returnValue == "6C0AAB" or returnValue == "006C0AAB":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/violet.jpg"
			elif returnValue == "1F0333" or returnValue == "001F0333":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/violet_dark.jpg"
			elif returnValue == "ffffff" or returnValue == "00ffffff":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/white.jpg"
			elif returnValue == "about":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/about.png"
			elif returnValue == "meteo-light":
				path = "/usr/lib/enigma2/python/Plugins/Extensions/KravenVB/images/meteo.jpg"
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
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
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
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.mylist()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.mylist()

	def pageUp(self):
		self["config"].instance.moveSelection(self["config"].instance.pageUp)
		self.mylist()

	def pageDown(self):
		self["config"].instance.moveSelection(self["config"].instance.pageDown)
		self.mylist()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

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
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			# global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(['name="KravenBackground" value="#00', 'name="KravenBackground" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value])
			self.skinSearchAndReplace.append(['name="KravenBackground" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + "000000", 'name="KravenBackground" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.Background.value])
			self.skinSearchAndReplace.append(['name="KravenInfobarBackground" value="#001B1775', 'name="KravenInfobarBackground" value="#00' + config.plugins.KravenVB.SkinColorInfobar.value])
			self.skinSearchAndReplace.append(['name="KravenNameBackground" value="#A01B1775', 'name="KravenNameBackground" value="#A0' + config.plugins.KravenVB.SkinColorInfobar.value])
			self.skinSearchAndReplace.append(['name="KravenIbarBackground" value="#4A1B1775', 'name="KravenIbarBackground" value="#4A' + config.plugins.KravenVB.SkinColorInfobar.value])
			self.skinSearchAndReplace.append(['name="KravenSelection" value="#000050EF', 'name="KravenSelection" value="#' + config.plugins.KravenVB.SelectionBackground.value])
			self.skinSearchAndReplace.append(['name="KravenFont1" value="#00ffffff', 'name="KravenFont1" value="#' + config.plugins.KravenVB.Font1.value])
			self.skinSearchAndReplace.append(['name="KravenFont2" value="#00F0A30A', 'name="KravenFont2" value="#' + config.plugins.KravenVB.Font2.value])
			self.skinSearchAndReplace.append(['name="KravenSelFont" value="#00ffffff', 'name="KravenSelFont" value="#' + config.plugins.KravenVB.SelectionFont.value])
			self.skinSearchAndReplace.append(['name="KravenMarkedFont" value="#00ffffff', 'name="KravenMarkedFont" value="#' + config.plugins.KravenVB.MarkedFont.value])
			self.skinSearchAndReplace.append(['name="KravenECMFont" value="#00ffffff', 'name="KravenECMFont" value="#' + config.plugins.KravenVB.ECMFont.value])
			self.skinSearchAndReplace.append(['name="KravenChannelnameFont" value="#00ffffff', 'name="KravenChannelnameFont" value="#' + config.plugins.KravenVB.ChannelnameFont.value])
			self.skinSearchAndReplace.append(['name="KravenButtonText" value="#00ffffff', 'name="KravenButtonText" value="#' + config.plugins.KravenVB.ButtonText.value])
			
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
				self.skinSearchAndReplace.append(['render="KravenVBSingleEpgListNobile" size="474,308"', 'render="KravenVBSingleEpgListNobile" size="474,330"'])
			
			### MiniTV-Screens Background
			if config.plugins.KravenVB.BackgroundColorTrans.value == "0A" or config.plugins.KravenVB.BackgroundColorTrans.value == "4A" or config.plugins.KravenVB.BackgroundColorTrans.value == "8C":
				self.skinSearchAndReplace.append(['name="KravenBackground2" value="#00000000', 'name="KravenBackground2" value="#00' + config.plugins.KravenVB.Background.value])
			elif config.plugins.KravenVB.BackgroundColorTrans.value == "00":
				self.skinSearchAndReplace.append(['name="KravenBackground2" value="#00000000', 'name="KravenBackground2" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.Background.value])
			
			### Menu (Logo, MiniTV)
			if config.plugins.KravenVB.Logo.value == "minitv":
				self.skinSearchAndReplace.append(['<ePixmap backgroundColor="KravenBackground3" pixmap="KravenVB/logo.png" position="930,100" size="200,200" alphatest="blend" />', '<widget source="session.VideoPicture" render="Pig" position="822,80" size="416,234" zPosition="3" backgroundColor="transparent" /><ePixmap backgroundColor="KravenBackground3" pixmap="KravenVB/logo2.png" position="980,489" size="100,100" alphatest="blend" />'])
				self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#00' + config.plugins.KravenVB.Background.value])
			elif config.plugins.KravenVB.Logo.value == "logo":
				self.skinSearchAndReplace.append(['name="KravenBackground3" value="#00000000', 'name="KravenBackground3" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.Background.value])
			
			### Debug-Names
			if config.plugins.KravenVB.DebugNames.value == "screennames-on":
				self.skinSearchAndReplace.append(['<!--<eLabel backgroundColor="KravenInfobar2Background" font="Regular;13" foregroundColor="red"', '<eLabel backgroundColor="KravenInfobar2Background" font="Regular;15" foregroundColor="red"'])
				self.skinSearchAndReplace.append(['position="70,0" size="500,16" halign="left" valign="center" transparent="1" />-->', 'position="70,0" size="500,19" halign="left" valign="top" transparent="1" />'])
			
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
			
			self.skinSearchAndReplace.append(['name="KravenBorder" value="#00ffffff', 'name="KravenBorder" value="#' + config.plugins.KravenVB.Border.value])
			self.skinSearchAndReplace.append(['name="KravenLine" value="#00ffffff', 'name="KravenLine" value="#' + config.plugins.KravenVB.Line.value])
			
			if config.plugins.KravenVB.RunningText.value == "movetype=none":
				self.skinSearchAndReplace.append(["movetype=running", "movetype=none"])
			if not config.plugins.KravenVB.RunningText.value == "movetype=none":
				self.skinSearchAndReplace.append(["startdelay=5000", config.plugins.KravenVB.RunningText.value])
			
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				self.skinSearchAndReplace.append(['scrollbarMode="showOnDemand"', 'scrollbarMode="showNever"'])
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="0"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="10"'])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
				self.skinSearchAndReplace.append(['scrollbarWidth="5"', 'scrollbarWidth="15"'])
			
			if not config.plugins.KravenVB.SelectionBorder.value == "none":
				self.selectionbordercolor = config.plugins.KravenVB.SelectionBorder.value
				self.borset = ("borset_" + self.selectionbordercolor + ".png")
				self.skinSearchAndReplace.append(["borset.png", self.borset])
			
			self.skincolorinfobarcolor = config.plugins.KravenVB.SkinColorInfobar.value
			self.ibar = ("ibar_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibar.png", self.ibar])
			
			self.skincolorinfobarcolor = config.plugins.KravenVB.SkinColorInfobar.value
			self.ibar = ("ibaro_" + self.skincolorinfobarcolor + ".png")
			self.skinSearchAndReplace.append(["ibaro.png", self.ibar])
			
			### IB Color visible
			if config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=0":
				if config.plugins.KravenVB.IBColor.value == "only-infobar":
					self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.Background.value])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibar_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibaro_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibar_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,570" size="380,400" alphatest="blend" zPosition="-9" />'," "])
					self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibaro_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,-60" size="380,443" alphatest="blend" zPosition="-9" />'," "])
				elif config.plugins.KravenVB.IBColor.value == "all-screens":
					self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#00' + config.plugins.KravenVB.SkinColorInfobar.value])
			elif config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=5" or config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=10" or config.plugins.KravenVB.ScrollBar.value == "scrollbarWidth=15":
				self.skinSearchAndReplace.append(['name="KravenInfobar2Background" value="#00000000', 'name="KravenInfobar2Background" value="#' + config.plugins.KravenVB.BackgroundColorTrans.value + config.plugins.KravenVB.Background.value])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibar_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,570" size="1280,400" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibaro_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,-60" size="1280,443" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibar_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,570" size="380,400" alphatest="blend" zPosition="-9" />'," "])
				self.skinSearchAndReplace.append(['<ePixmap pixmap="KravenVB/header-kraven/ibaro_' + config.plugins.KravenVB.SkinColorInfobar.value + '.png" position="0,-60" size="380,443" alphatest="blend" zPosition="-9" />'," "])
			
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
			if fileExists("/usr/lib/enigma2/python/Components/Converter/MiniTVDisplay.py") and fileExists("/usr/lib/enigma2/python/Components/Renderer/MiniTV.py"):
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ChannelSelectionStyle2.value + ".xml")
			else:
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ChannelSelectionStyle.value + ".xml")

			### Infobox
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
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
				elif config.plugins.KravenVB.Infobox.value == "db":
					self.skinSearchAndReplace.append(['convert  type="KravenVBFrontendInfo">SNR', 'convert  type="KravenVBFrontendInfo">SNRdB'])

			### Infobar_begin
			self.appendSkinFile(self.daten + "infobar-begin.xml")

			### Infobar_main
			self.appendSkinFile(self.daten + config.plugins.KravenVB.InfobarStyle.value + "_main.xml")

			### Infobar_top
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
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
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle3.value + ".xml")

			### ecm-info
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-x3.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz1.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz2.xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				if config.plugins.KravenVB.ECMInfo.value == "ecm-info-on":
					self.appendSkinFile(self.daten + "infobar-ecminfo-zz3.xml")

			### system-info
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SystemInfo.value + ".xml")

			### sat-info
			self.appendSkinFile(self.daten + config.plugins.KravenVB.SatInfo.value + ".xml")

			### weather-style
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz4" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.WeatherStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.WeatherStyle2.value + ".xml")

			### Infobar_end - SIB_begin
			self.appendSkinFile(self.daten + "infobar-style_middle.xml")

			### clock-style - SIB
			if config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x1":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-x3" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-z2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz2" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz3":
				self.appendSkinFile(self.daten + config.plugins.KravenVB.ClockStyle2.value + ".xml")
			elif config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zz1" or config.plugins.KravenVB.InfobarStyle.value == "infobar-style-zzz1":
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

			### Main XML
			self.appendSkinFile(self.daten + "main.xml")

			### Plugins XML
			self.appendSkinFile(self.daten + "plugins.xml")

			### EMCSTYLE
			self.appendSkinFile(self.daten + config.plugins.KravenVB.EMCStyle.value + ".xml")			

			### NumberZapExtStyle
			self.appendSkinFile(self.daten + config.plugins.KravenVB.NumberZapExt.value + ".xml")

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
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

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
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()
