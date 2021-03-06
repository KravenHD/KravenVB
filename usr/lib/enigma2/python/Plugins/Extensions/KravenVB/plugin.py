# -*- coding: utf-8 -*-

#  Plugin Code
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

from Plugins.Plugin import PluginDescriptor
from enigma import getDesktop
from Components.Language import language
from os import environ
import gettext
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
import KravenVB

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

def main(session, **kwargs):
	reload(KravenVB)
	try:
		session.open(KravenVB.KravenVB)
	except:
		import traceback
		traceback.print_exc()

def main_menu(menuid):
	if menuid == "system":
		return [("KravenVB", main, _("Configuration tool for KravenVB"), 27)]
	else:
		return []

def Plugins(**kwargs):
	screenwidth = getDesktop(0).size().width()
	try:
		from boxbranding import getImageDistro
		if getImageDistro() == "openatv":
			list = []
			list.append(PluginDescriptor(name="Setup KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_MENU, fnc = main_menu))
			if screenwidth and screenwidth == 1920:
				list.append(PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main))
			else:
				list.append(PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main))
			return list
		else:
			if screenwidth and screenwidth == 1920:
				return [PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
			else:
				return [PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]
	except ImportError:
		if screenwidth and screenwidth == 1920:
			return [PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='pluginfhd.png', fnc=main)]
		else:
			return [PluginDescriptor(name="KravenVB", description=_("Configuration tool for KravenVB"), where = PluginDescriptor.WHERE_PLUGINMENU, icon='plugin.png', fnc=main)]
