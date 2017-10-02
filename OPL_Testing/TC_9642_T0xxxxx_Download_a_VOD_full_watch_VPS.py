# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from datetime import datetime, timedelta


class TC_9642_T0xxxxx_Download_a_VOD_full_watch_VPS(TC_OPL_template):

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
            self.assertTrue(False, 'ERR: test vod download process in IPTV or FTTH')
        time.sleep(3)

        ''' step 1 '''
        self.logStepBeginning("STEP 1 - deactivate parental control")
        self.rc.sendKeys(["KEY_BACK"])
        self.rc.sendKeys(["KEY_BACK"])
        self.rc.sendKeys(["KEY_TV"])
        self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive),'ERR: SET ParentalControl')   
        self.logStepResults("STEP 1 - deactivate parental control")

        ''' step 2 '''
        self.logStepBeginning("STEP 2 - finding in VOD catalog  no watched video and play ")
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
        title = self.page.getInfoFromVodPage().title
        time.sleep(2)
        lenght = self.page.getInfoFromVodPage().length        
        self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(),"ERR: play vod")
        time.sleep(10)
        self.logStepResults("STEP 2 - finding in VOD catalog  no watched video and play  ")


        ''' step 3 '''
        self.logStepBeginning("STEP 3 - watching video unit the end ")
        time.sleep(4)

        currentDate = datetime.now()

        startHourTxt = int(currentDate.hour)
        startMinTxt = int(currentDate.minute)

        endDate = currentDate + lenght
        endHourTxt = int(endDate.hour)
        endMinTxt = int(endDate.minute)

        timeSleep=((endHourTxt-startHourTxt)*3600+(endMinTxt-startMinTxt)*60)
        print timeSleep
        print title
        time.sleep(timeSleep)
        time.sleep(720)
        titleEnd = self.page.getInfoFromVodPage().title
        if not titleEnd==title:
            self.assertTrue(False, ' ERR: not this same title watched last VOD ')
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.logStepResults("STEP 3 - watching video unit the end ")

        ''' step 4 '''
        self.logStepBeginning("STEP 4 - checking a downloading VOD on My video catalog ")
        time.sleep(4)
        self.assertTrue(self.page.goToVodMyVideos(), 'ERR: do not go to VOD my videos')
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(title), 'ERR: do not finding rented and full downloading last VOD')
        time.sleep(2)
        self.logStepResults("STEP 4 - checking a download VOD on My video catalog ")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")