from pluginDefault import PluginDefault
from plugins.alarm.plugin import PluginAlarm
from plugins.anime.plugin import PluginAnime
from plugins.remote.plugin import PluginRemote

class PluginFactory:

    def getPlugin(subject, typeS):
        themeName= subject.split(".")[0]    
        if themeName== "alarm":
            return PluginAlarm(subject, typeS)
        elif themeName== "remote":
            return PluginRemote(subject, typeS)
        elif themeName == "anime":
            return PluginAnime(subject, typeS)
        return PluginDefault(subject, typeS)