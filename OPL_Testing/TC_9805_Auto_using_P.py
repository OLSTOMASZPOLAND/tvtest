# -*- coding: utf-8 -*-

import time
from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta
from wheel.signatures import assertTrue

 

 

class TC_9805_Auto_using_P(TC_OPL_template):

    """          
    Implementation of the HP QC test ID 9805_Auto_using_P+_P-
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

            ''' prestep '''
    
            self.logStepResults("AT_THE_BEGINNING")
            time.sleep(3)
        
        
        
            ''' step '''
            self.logStepBeginning("STEP 1- Turn off all favorite channels")
            self.page.cleanTurnOffAllFavoriteChannels()
            self.logStepResults("STEP 1- Turn off all favorite channels")
        
            ''' step '''
            self.logStepBeginning("STEP 2 - add Favorite channels (1,2,3)")   
            self.rc.sendKeys(["KEY_1"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo),'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            self.rc.sendKeys(["KEY_2"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo), 'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            self.rc.sendKeys(["KEY_3"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo), 'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            
            self.logStepResults("STEP 2 - add Favorite channels (1,2,3)")
            
            ''' step '''
            self.logStepBeginning("STEP 3 - zap to channel 1 and open favorite list channels")
            numberchannel = u"1".encode('utf-8')
            time.sleep(2)
            self.assertTrue(self.page.zapToChannel(numberchannel),'  >>   ERR: with zap to '+ numberchannel)
            time.sleep(2)
            frontpanel = self.rc.getFrontPanel()
            time.sleep(2)
            if frontpanel!="WHD80":
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            time.sleep(4)    
            self.rc.sendKeys(["KEY_LIST"])
            time.sleep(4)
            lista = self.page.findInPage(Description.favoriteInList)
            l=1
            if not (lista==True):
                while (l<20):
                    l=l+1
                    self.rc.sendKeys(["KEY_LEFT"])
                    time.sleep(4)
                    lista = self.page.findInPage(Description.favoriteInList)
                    if (lista==True):
                        l=20
            time.sleep(5)
            self.rc.sendKeys(["KEY_Back"])
            
            self.logStepResults("STEP 3 - zap to channel 1 and open favorite list channels")
            
            ''' step '''
            self.logStepBeginning("STEP 4 - P+(1)")
            time.sleep(2)
            self.rc.sendKeys(["KEY_CHANNELUP"])
            time.sleep(2)
            numberchannel = u"2".encode('utf-8')
            frontpanel = self.rc.getFrontPanel()
            time.sleep(3)
            if frontpanel!="WHD80":
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logStepResults("STEP 4 - P+(1)")
            
            
            ''' step '''
            self.logStepBeginning("STEP 5 - P+(2)")
            time.sleep(2)
            self.rc.sendKeys(["KEY_CHANNELUP"])
            time.sleep(2)
            numberchannel = u"3".encode('utf-8')
            frontpanel = self.rc.getFrontPanel()
            if frontpanel!="WHD80":
                time.sleep(3)
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logStepResults("STEP 5 - P+(2)")
            
            ''' step '''
            self.logStepBeginning("STEP 6 - P+(3)")
            time.sleep(2)
            self.rc.sendKeys(["KEY_CHANNELUP"])
            time.sleep(2)
            numberchannel = u"1".encode('utf-8')
            frontpanel = self.rc.getFrontPanel()
            time.sleep(3)
            if frontpanel!="WHD80":
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logStepResults("STEP 6 - P+(3)")
            
            ''' step '''
            self.logStepBeginning("STEP 7 - P-(1)")
            time.sleep(2)
            self.rc.sendKeys(["KEY_CHANNELDOWN"])
            time.sleep(2)
            numberchannel = u"3".encode('utf-8')
            frontpanel = self.rc.getFrontPanel()
            time.sleep(3)
            if frontpanel!="WHD80":
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logStepResults("STEP 7 - P-(1)")
    
            ''' step '''
            self.logStepBeginning("STEP 8 - P-(2)")
            time.sleep(2)
            self.rc.sendKeys(["KEY_CHANNELDOWN"])
            time.sleep(3)
            numberchannel = u"2".encode('utf-8')
            frontpanel = self.rc.getFrontPanel()
            time.sleep(3)
            if frontpanel!="WHD80":
                if (frontpanel != str(numberchannel)):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logStepResults("STEP 8 - P-(2)")
            
            ''' step '''
            self.logStepBeginning("STEP 9 - Check live")
            
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
            time.sleep(3)
            display = motionDetection()
            if not (display==True):
                time.sleep(10)
                display = motionDetection()
                if not (display==True):
                    self.assertTrue(False, "  >>  No video stream")
            self.rc.sendKeys(["KEY_BACK"])
            self.logStepResults("STEP 9 - Check live")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            time.sleep(5)
            self.page.checkStbStatusIfKoReboot()
            self.page.cleanTurnOffAllFavoriteChannels()
            