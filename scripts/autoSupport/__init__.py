import ts3lib, ts3defines, datetime
from ts3plugin import ts3plugin
from os import path

class color(object):
    DEFAULT = "[color=white]"
    DEBUG = "[color=grey]"
    INFO = "[color=lightblue]"
    SUCCESS = "[color=green]"
    WARNING = "[color=orange]"
    ERROR = "[color=red]"
    FATAL = "[color=darkred]"
    ENDMARKER = "[/color]"

class autoSupport(ts3plugin):
    name = "Auto Support"
    apiVersion = 21
    requestAutoload = False
    version = "1.0"
    author = "Bluscream, SadPixel"
    description = "Requested by SadPixel"
    offersConfigure = False
    commandKeyword = "sup"
    infoTitle = None
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Toggle Auto Support", ""),
                (ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 1, "Force Stop Supporting", "")]
    hotkeys = [("autosupport", "Toggle Auto Support")]
    debug = True
    enabled = False
    supserver = "a5BUMeIEbvaQEVzU85UP8UY+6DY=" # BergwerkLabs
    supchanmain = 368144 # » Support | Warteraum
    supchans = [355971,355972,355972]
    supbot = "Z1OUM2IvRvIpdmKIyFV3tZQXkq4=" # bergwerkLABS | Support
    insupport = 0
    cursupchan = 0
    oldchan = 0

    def __init__(self):
        ts3lib.logMessage(self.name + " script for pyTSon by " + self.author + " loaded from \"" + __file__ + "\".", ts3defines.LogLevel.LogLevel_INFO, "Python Script", 0)
        if self.debug: ts3lib.printMessageToCurrentTab('[{:%Y-%m-%d %H:%M:%S}]'.format( datetime.datetime.now()) + " [color=orange]" + self.name + "[/color] Plugin for pyTSon by " + self.author + " loaded.")

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL:
            if menuItemID == 0: self.toggle()
            elif menuItemID == 1: self.stop(schid)

    def onHotkeyEvent(self, keyword):
        if keyword == "autosupport": self.toggle()

    def processCommand(self, schid, command):
        cmd = command.lower().split(" ")[0]
        if cmd == "toggle":  self.toggle();return True
        elif cmd == "on": self.toggle(True);return True
        elif cmd == "off":self.toggle(False);return True
        elif cmd == "stop":self.stop(schid);return True

    def toggle(self, state=None):
        if state: self.enabled = True
        elif state == False: self.enabled = False
        else: self.enabled = not self.enabled
        if self.enabled: ts3lib.printMessageToCurrentTab("{0} {1}enabled{2}.".format(self.name, color.SUCCESS, color.ENDMARKER));return True
        else: ts3lib.printMessageToCurrentTab("{0} {1}disabled{2}.".format(self.name, color.ERROR, color.ENDMARKER)); return False

    def stop(self, schid):
        (error, ownid) = ts3lib.getClientID(schid)
        ts3lib.requestClientMove(schid, ownid, self.oldchan, "")
        if self.debug: ts3lib.printMessageToCurrentTab("Not longer in support with client #{0} in channel #{1}".format(self.insupport, self.cursupchan))
        self.insupport == 0;self.cursupchan == 0;self.oldchan = 0

    def onConnectStatusChangeEvent(self, schid, newStatus, errorNumber):
        if newStatus == ts3defines.ConnectStatus.STATUS_CONNECTION_ESTABLISHED:
            (error, uid) = ts3lib.getServerVariableAsString(schid, ts3defines.VirtualServerProperties.VIRTUALSERVER_UNIQUE_IDENTIFIER)
            if uid == self.supserver: self.toggle(True)

    def onClientMoveMovedEvent(self, schid, clientID, oldChannelID, newChannelID, visibility, moverID, moverName, moverUniqueIdentiﬁer, moveMessage):
        (error, ownid) = ts3lib.getClientID(schid)
        if self.debug: ts3lib.printMessageToCurrentTab("insupport: {0} | cursupchan: {1} | oldchan: {2}".format(self.insupport,self.cursupchan, self.oldchan))
        if self.insupport == 0 and moverUniqueIdentiﬁer == self.supbot and newChannelID == self.supchanmain:
            for c in self.supchans:
                (error, clients) = ts3lib.getChannelClientList(schid, c)
                if len(clients) > 0: continue
                else:
                    ts3lib.requestClientMove(schid, clientID, c, "")
                    (error, ownchan) = ts3lib.getChannelOfClient(schid, ownid)
                    ts3lib.requestClientMove(schid, ownid, c, "")
                    self.insupport = clientID;self.cursupchan = c;self.oldchan = ownchan
                    if self.debug: ts3lib.printMessageToCurrentTab("Now in support with client #{0} in channel #{1}".format(clientID, c))
                    return
            ts3lib.printMessageToCurrentTab("No free support channel found for client #{0}! Please try manually.".format(clientID))
        elif self.insupport == clientID and oldChannelID == self.cursupchan and moverID == ownid:
            ts3lib.requestClientMove(schid, ownid, self.oldchan, "")
            if self.debug: ts3lib.printMessageToCurrentTab("Not longer in support with client #{0} in channel #{1}".format(self.insupport, self.cursupchan))
            self.insupport == 0;self.cursupchan == 0;self.oldchan = 0

    def onClientMoveEvent(self, schid, clientID, oldChannelID, newChannelID, visibility, moveMessage):
        if clientID == self.insupport and oldChannelID == self.cursupchan:
            (error, ownid) = ts3lib.getClientID(schid)
            ts3lib.requestClientMove(schid, ownid, self.oldchan, "")
            if self.debug: ts3lib.printMessageToCurrentTab("Not longer in support with client #{0} in channel #{1}".format(self.insupport, self.cursupchan))
            self.insupport == 0;self.cursupchan == 0;self.oldchan = 0

    def onClientKickFromChannelEvent(self, schid, clientID, oldChannelID, newChannelID, visibility, kickerID, kickerName, kickerUniqueIdentiﬁer, kickMessage):
        (error, ownid) = ts3lib.getClientID(schid)
        if self.insupport == clientID and oldChannelID == self.cursupchan and kickerID == ownid:
            ts3lib.requestClientMove(schid, ownid, self.oldchan, "")
            if self.debug: ts3lib.printMessageToCurrentTab("Not longer in support with client #{0} in channel #{1}".format(self.insupport, self.cursupchan))
            self.insupport == 0;self.cursupchan == 0;self.oldchan = 0