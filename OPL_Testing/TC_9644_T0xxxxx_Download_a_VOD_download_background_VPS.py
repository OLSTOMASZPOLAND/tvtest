# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta





class TC_9644_T0xxxxx_Download_a_VOD_download_background_VPS(TC_OPL_template):

    """             

    @author: Marek Szlachetka
    """



    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)



    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        if (Env.ZONE=="IPTV" or Env.ZONE=="FTTH"):
            self.assertTrue(False, 'ERR: test vod download proces in IPTV or FTTH')
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

        ''' step 1 '''
        self.logStepBeginning("STEP 1 - deactivate parental control")
        self.rc.sendKeys(["KEY_BACK"])
        self.rc.sendKeys(["KEY_BACK"])
        self.rc.sendKeys(["KEY_TV"])
        self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive),'ERR: SET ParentalControl')  
        self.logStepResults("STEP 1 - deactivate parental control")

        ''' step 2 '''
        self.logStepBeginning("STEP 2 - finding in VOD catalog  no watched video ")
        time.sleep(2)
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "ERR: Entering VOD Catalog")
        time.sleep(10)
        self.rc.sendKeys(["KEY_OK"])
        status3 = False
        status2=False
        i = 0
        while (i<20):
            i=i+1
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_UP"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            status3 = self.page.findInPage(Menu.vodRent)
            time.sleep(2)
            title = self.page.getInfoFromVodPage().title
            if "2h" in title:
                status2=True
                
            if "2d" in title:
                status2=True
                
            if "1d" in title:
                status2=True   
                             
            if status3==True and status2==True: 
                i=20        
            if i==19:
                self.assertTrue(False, 'ERR: no available searching VOD ')
            status2=False
            
        time.sleep(5)
        self.logStepResults("STEP 2 - finding in VOD catalog  no watched video  ")

        ''' step 3 '''
        self.logStepBeginning("STEP 3 - Rent VOD ")
        time.sleep(4)
        self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen(), 'ERR: Do not go to '+Menu.vodRent)
        self.logStepResults("STEP 3 - Rent VOD  ")


        ''' step 4 '''
        self.logStepBeginning("STEP 4 - checking a downloading VOD on video presentation ")
        time.sleep(4)
        status5 = self.page.findInPage('trwa pobieranie')
        title = self.page.getInfoFromVodPage().title
        i=0
        if status5==True:
            while (i<30):
                i=i+1
                time.sleep(300)
                self.rc.sendKeys(["KEY_BACK"])
                time.sleep(4)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(4)
                status5 = self.page.findInPage('trwa pobieranie')
                status6 = self.page.findInPage('pobieranie wstrzymane')
                if status6==True:
                        self.assertTrue(False, 'ERR: pobieranie wstrzymane') 
                if status5==False:
                    i=30
                if i==29:
                    self.assertTrue(False, 'ERR: do not download after 145 min') 
        time.sleep(8)
        self.assertTrue(self.page.actionSelect(Menu.vodResume), 'ERR: no finding PLAY function')
        time.sleep(2)
        status7 = self.page.findInPage('kontrola rodzicielska')
        if status7==True:
                self.rc.sendNumberSequence(Env.PARENTAL_CODE)
                self.rc.sendKeys(["KEY_OK"])
        time.sleep(4)
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

        self.logStepResults("STEP 4 - checking a downloading VOD on video presentation ")

        ''' step 5 '''
        self.logStepBeginning("STEP 5 - checking a downloading VOD on My video catalog ")
        time.sleep(4)
        self.assertTrue(self.page.goToVodMyVideos(), 'ERR: do not go to VOD my videos')
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(title), 'ERR: do not finding rented and full downloading last VOD')
        time.sleep(2)
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.logStepResults("STEP 5 - checking a download VOD on My video catalog ")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")