# -*- coding: utf-8 -*-


import urllib2
import ssl
import time
from Config import *
import logging
import sys


class RpiRemoteControl(object):
                                                                                    # BBC HD 15
    channelDictIPTV = {'TVP 1 HD': "1", 'TVP 2 HD': "2", 'TVP Polonia': "10", 'BBC HD': "1", \
                       'TVP Historia' : "445", 'TVP 1 HD DTT' : "901", 'TVP 2 HD DTT' : "902", \
                       'TVP Historia DTT' : "905", 'TVP Polonia DTT' : "906", \
                       'HBO HD' : "266", 'HBO 2 HD' : "267", 'HBO Comedy HD' : "268"}
                                                                                  # BBC HD 44
    channelDictDTH = {'TVP 1 HD': "1", 'TVP 2 HD': "2", 'TVP Polonia': "10", 'BBC HD': "342", \
                       'TVP Historia' : "445", 'TVP 1 HD DTT' : "260", 'TVP 2 HD DTT' : "261", \
                       'TVP Historia DTT' : "264", 'TVP Polonia DTT' : "265", \
                       'HBO HD' : "266", 'HBO 2 HD' : "267", 'HBO Comedy HD' : "268"}
    '''
    channelDictDTH = {'TVP 1 HD': "455", 'TVP 2 HD': "455", 'TVP Polonia': "455", 'BBC HD': "455", \
                       'TVP Historia' : "455", 'TVP 1 HD DTT' : "455", 'TVP 2 HD DTT' : "455", \
                       'TVP Historia DTT' : "455", 'TVP Polonia DTT' : "455", \
                       'HBO HD' : "455", 'HBO 2 HD' : "455", 'HBO Comedy HD' : "455"}
    '''
    channelDictRFOG = {'TVP 1 HD': "1", 'TVP 2 HD': "2", 'TVP Polonia': "10", 'BBC HD': "15", \
                       'TVP Historia' : "445", 'TVP 1 HD DTT' : "901", 'TVP 2 HD DTT' : "902", \
                       'TVP Historia DTT' : "905", 'TVP Polonia DTT' : "906", \
                       'HBO HD' : "266", 'HBO 2 HD' : "267", 'HBO Comedy HD' : "268"}

    def __init__(self):
        self.logger = logging.getLogger('NewTvTesting.RpiRemoteControl')            
        self.__list = None
            
        if(Env.ZONE == "IPTV" or Env.ZONE == "FTTH"):
            self.__list = RpiRemoteControl.channelDictIPTV
        elif(Env.ZONE == "DTH"):
            self.__list = RpiRemoteControl.channelDictDTH
        elif(Env.ZONE == "RFTV"):            
            self.__list = RpiRemoteControl.channelDictRFOG
        else:
            raise BaseException("Current technology not known.")
    
    @property 
    def getChannelTVP1HD(self):
        return self.__list['TVP 1 HD']
    @property
    def getChannelTVP2HD(self):
        return self.__list['TVP 2 HD']
    @property
    def getChannelTVPPolonia(self):
        return self.__list['TVP Polonia']
    @property
    def getChannelBBCHD(self):
        return self.__list['BBC HD']
    @property
    def getChannelTVPHistoria(self):
        return self.__list['TVP Historia']
    @property
    def getChannelTVP1HD_dtt(self):
        return self.__list['TVP 1 HD DTT']
    @property
    def getChannelTVP2HD_dtt(self):
        return self.__list['TVP 2 HD DTT']
    @property
    def getChannelTVPHistoria_dtt(self):
        return self.__list['TVP Historia DTT']
    @property
    def getChannelTVPPolonia_dtt(self):
        return self.__list['TVP Polonia DTT']
    @property
    def getChannelHBOHD(self):
        return self.__list['HBO HD']
    @property
    def getChannelHBO2HD(self):
        return self.__list['HBO 2 HD']
    @property
    def getChannelHBOComedyHD(self):
        return self.__list['HBO Comedy HD']

    def close(self):
        pass

    def sendUrl(self, url):

        # python < 2.7.9
        response = urllib2.urlopen(url)
        return response

        # python >= 2.7.9
#       ctx = ssl.create_default_context()
#       ctx.check_hostname = False
#       ctx.verify_mode = ssl.CERT_NONE
#       response = urllib2.urlopen(url, context = ctx)
#       return response

    def sendNumberSequence(self, number):
        """Send number sequence, e.g "1111"
        @author: Marcin Gmurczyk
        """        
        number = str(number)
        self.logger.debug("  >>   sendNumberSequence >" + number + "<")
        for x in range(len(number)):
            self.sendUrl(Rpi.URL_RPI_KEY + "KEY_" + number[x])
            time.sleep(0.5)
        time.sleep(2.5)

    def sendKeys(self, keys):
        for key in keys:
            self.logger.debug("  >>   remote control key >" + key + "<")
            self.sendUrl(Rpi.URL_RPI_KEY + key)
            if key == "KEY_MENU" or key == "KEY_OK" or key == "KEY_STOP" or key == "KEY_BACK":
                time.sleep(4)
            elif key == "KEY_CHANNELUP" or key == "KEY_CHANNELDOWN":
                time.sleep(6)
            elif key == "KEY_PLAY"or key == "KEY_INFO" or key == "KEY_GUIDE":
                time.sleep(5)
            else:
                time.sleep(0.2)

    def zap(self, channel):
        self.logger.debug("  >>   remote control zap " + str(channel))
        # time.sleep(6) ###norbi
        self.sendUrl(Rpi.URL_RPI_ZAP + str(channel))
        time.sleep(6)

    def sendWord(self, word):
        self.logger.debug("  >>   remote control word >" + word + "<")
        for c in word:
            for index in range(0, Remote.LETTERS[c][1]):
                self.sendUrl(
                    Rpi.URL_RPI_KEY + "KEY_" + str(Remote.LETTERS[c][0]))
                time.sleep(0.3)
            time.sleep(2.5)

    def sendDateHourMin(self, date):
        HourTxt = str(date.hour)
        MinTxt = str(date.minute)
        if len(HourTxt) == 2:
            self.sendKeys(["KEY_" + HourTxt[0], "KEY_" + HourTxt[1]])
        else:
            self.sendKeys(["KEY_0", "KEY_" + HourTxt[0]])

        if len(MinTxt) == 2:
            self.sendKeys(["KEY_" + MinTxt[0], "KEY_" + MinTxt[1]])
        else:
            self.sendKeys(["KEY_0", "KEY_" + MinTxt[0]])

    def hardReset(self):
        self.sendUrl(Rpi.URL_RPI_RESET)

    def getStbStatus(self):
        try:
            response = self.sendUrl(Rpi.URL_RPI_STATUS)
            return response.read()
        except:
            # raise
            return "KO"

    def startLogs(self):
        self.sendUrl(Rpi.URL_RPI_START_LOGS)

    def stopLogs(self):
        self.sendUrl(Rpi.URL_RPI_STOP_LOGS)

    def getLogs(self):
        return self.sendUrl(Rpi.URL_RPI_GET_LOGS).read()
    
#    def runCommand(self):
#        return self.sendUrl(Rpi.URL_RPI_RUN_COMMAND).read()
    
    def getFrontPanel(self):
        """Return the front panel value.
        @author: Tomasz Stasiuk
        """
        stb=str(Env.STB)
        print stb
        if stb == "UHD86" or stb =="UHD88":
        
            getFrontPanel1 = self.sendUrl(Rpi.URL_RPI_GET_FRONT_PANEL).read()
            getFrontPanel2 = str(getFrontPanel1.split(':', 7)[6])
            getFrontPanel3 = str(getFrontPanel2.split('+', 2)[0])
            getFrontPanel4 = str(getFrontPanel3.split())
            getFrontPanel5 = str(getFrontPanel4.split("'", 1)[1])
            getFrontPanel = str(getFrontPanel5.split("'", 1)[0])
            return getFrontPanel
    
        else:
            return "WHD80"
