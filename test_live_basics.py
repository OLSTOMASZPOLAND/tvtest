# -*- coding: utf-8 -*-
import unittest
import time
import logging
from fuzzywuzzy import fuzz
  
from NewTvTesting.ResidentAppPage import *
from NewTvTesting.RemoteControl import *
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.DataSet import *


class TestLiveBasics(unittest.TestCase):


    def setUp(self):

        self.logger = logging.getLogger('NewTvTesting')
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)
        formatter = logging.Formatter('%(levelname)s :: %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)

        self.page = WebKitPage()
        rc = RpiRemoteControl()

        status = self.page.getStatus()
        if status.getStbStatus() == "KO":
            self.logger.warning("Hard Reset")
            #rc.hardReset()
            #time.sleep(180)
            status = self.page.getStatus()
        scene = status.getScene()
        if scene == "TOOLBOX" or scene == "ZAPPING_BANNER":
            rc.sendKeys(["KEY_BACK"])
        elif scene == "PORTAL" or scene == "UNKNOWN":
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])
        if status.findDialogBox():
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])

        self.test_passed = False
        

    def tearDown(self):

        self.logger.info(self.shortDescription())
        self.page.close()
        self.logger.removeHandler(self.handler)
        self.handler.close()

        if not self.test_passed:
            print("Error " + self.id())
            output = self.id() + time.strftime("%c")
            if Env.VIDEO:
                screenshot(Env.SCREENSHOTS_DIR + output + ".png")

    def test_a_zapping(self):
        '''Zapping'''
  
        self.logger.info(" ")
        self.logger.info("  ***************")
        self.logger.info("      Zapping ?")
        self.logger.info("  ***************")
        self.logger.info(" ")
  
  
        rc = RpiRemoteControl()
  
  
  
  
  
        ''' DTT desactivation '''
        time.sleep(10)
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_myAccount)
        else:
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
        self.assertTrue(self.page.actionSelect(Menu.tvSettings))
        self.assertTrue(self.page.actionSelect(Menu.dttChannels))
        self.assertTrue(self.page.actionSelect(Menu.dttDesactivation))
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])
  
  
  
  
        '''zapping num'''
        rc.zap(LiveData.TV1.getLcn())
        time.sleep(15)
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.assertTrue(pg.getLcn() == LiveData.TV1.getLcn(),"wrong lcn")
        self.assertTrue(pg.getChannelName() == LiveData.TV1.getFirstChannel_DttOff().name,"wrong channel name")
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"no motion - zapping num")
  
  
        '''zapping p+'''
        rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(15)
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.logger.info( " channel name from JSON : "+ LiveData.TV2.getFirstChannel_DttOff().name )
        self.assertTrue(pg.getLcn() == LiveData.TV2.getLcn(),"wrong lcn")    
        self.assertTrue(pg.getChannelName() == LiveData.TV2.getFirstChannel_DttOff().name,"wrong channel name")
      
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"no motion - zapping p+")
  
        '''zapping banner'''
        rc.sendKeys(["KEY_INFO"])
        self.page.actionSelectInLiveBanner(LiveData.TV5.getLcn())
        time.sleep(15)
  
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.assertTrue(pg.getLcn() == LiveData.TV5.getLcn(),"wrong lcn")
        self.assertTrue(pg.getChannelName() == LiveData.TV5.getFirstChannel_DttOff().name,"wrong channel name")
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"no motion - zapping banner")
  
        '''zapping num 2 digits'''
        rc.zap(LiveData.TV15.getLcn())
        time.sleep(15)
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.assertTrue(pg.getLcn() == LiveData.TV15.getLcn(),"wrong lcn")
        self.assertTrue(pg.getChannelName() == LiveData.TV15.getFirstChannel_DttOff().name,"wrong channel name")
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"no motion - zapping 2 digits")
  
        '''zapping mosaic'''
        rc.sendKeys(["KEY_0"])
        time.sleep(5)
        rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN"])
        pgMosaic = self.page.getInfoFromMosaicFocus()
        pgMosaic.display()
        rc.sendKeys(["KEY_OK"])
        time.sleep(15)
  
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.assertTrue(pg.getLcn() == pgMosaic.getLcn(),"wrong lcn")
        self.assertTrue(pg.getChannelName() == pgMosaic.getChannelName(),"wrong channel name")
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"no motion - zapping mosaic")
  
        rc.zap(LiveData.TV1.getLcn())
  
  
        self.test_passed = True

    def test_b_timeShifting(self):
 
        '''Time Shifting'''
        self.logger.info(" ")
        self.logger.info("  ********************")
        self.logger.info("      Time Shifting")
        self.logger.info("  ********************")
        self.logger.info(" ")
 
        rc = RpiRemoteControl()
 
        if Env.VIDEO:
            rc.zap(LiveData.TV1.getLcn())
            time.sleep(15)
            self.assertTrue(motionDetection(),u"step 1 - play expected")
            rc.sendKeys(["KEY_PLAY"])
            time.sleep(TimeShifting.LENGTH_1*60)
            self.assertFalse(motionDetection(),u"step 2 -pause expected")
            time.sleep(30)
            rc.sendKeys(["KEY_PLAY"])
            time.sleep(5)
            self.assertTrue(motionDetection(),u"step 3 -play expected")
            time.sleep(30)
            rc.sendKeys(["KEY_PLAY"])
            time.sleep(TimeShifting.LENGTH_2*60)
            self.assertFalse(motionDetection(),u"step 4 - pause expected")
            time.sleep(30)
 
            rc.zap(LiveData.TV2.getLcn())
            self.assertTrue(motionDetection(),u"step 5 - play expected")
 
        self.test_passed = True

#      def test_c_language(self):
#  
#         '''Language selection'''
#         self.logger.info(" ")
#         self.logger.info("  ********************")
#         self.logger.info("      Language")
#         self.logger.info("  ********************")
#         self.logger.info(" ")
#  
#         rc = RpiRemoteControl()
#  
#         rc.zap(LiveData.TV45.getLcn())
#         rc.sendKeys(["KEY_MENU"])
#         if Env.STB == "NEWBOX":
#             rc.sendKeys(Menu.tab_myAccount)
#         else:
#             self.assertTrue(self.page.actionSelect(Menu.myAccount))
#         self.assertTrue(self.page.actionSelect(Menu.mySettings))
#         self.assertTrue(self.page.actionSelect(Menu.language))
#         self.assertTrue(self.page.actionSelect(Menu.orginalSoundtrack))
#         time.sleep(3)
#  
#         rc.sendKeys(["KEY_CHANNELUP"])
#         time.sleep(15)
#         rc.sendKeys(["KEY_OK"])
#         self.assertTrue(self.page.actionSelect(Menu.toolboxOriginalSoundtrack))
#         self.assertTrue(self.page.actionSelect(Menu.toolbox_2_nativeSoundtrack))
#  
#         time.sleep(5)
#  
#         rc.sendKeys(["KEY_OK"])
#         self.assertTrue(self.page.findInList(Menu.toolboxNativeSoundtrack))
#  
#         self.test_passed = True
# 
    def test_d_favorites(self):
  
        '''Favorite channels'''
        self.logger.info(" ")
        self.logger.info("  ************************")
        self.logger.info("      Favorite channels")
        self.logger.info("  ************************")
        self.logger.info(" ")
  
        rc = RpiRemoteControl()
  
        rc.zap(LiveData.TV1.getLcn())
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_myAccount)
        else:
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
        self.assertTrue(self.page.actionSelect(Menu.mySettings))
        self.assertTrue(self.page.actionSelect(Menu.myChannels))
  
        items = self.page.getList()
        self.assertFalse(items == None, "Favourites page loading error")
  
        for channel in items:
            if channel.selected:
                rc.sendKeys(["KEY_OK"])
            rc.sendKeys(["KEY_DOWN"])
  
        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
  
        ''' FAV1 selection via Toolbox'''
  
        rc.zap(LiveData.TV2.getLcn())
        time.sleep(15)
        rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo))
        self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes))
  
        ''' FAV2 selection via menu'''
  
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_myAccount)
        else:
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
        self.assertTrue(self.page.actionSelect(Menu.mySettings))
        self.assertTrue(self.page.actionSelect(Menu.myChannels))
  
        items = self.page.getList()
        self.assertFalse(items == None, "Favourites page loading error")
        for index, channel in enumerate(items):
            if index == LiveData.TV2.lcn-1:
                self.assertTrue(channel.selected==True)
            if index == LiveData.TV5.lcn-1:
                rc.sendKeys(["KEY_OK"])
            rc.sendKeys(["KEY_DOWN"])
  
        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
  
        ''' checking'''
  
        rc.zap(LiveData.TV5.getLcn())
        time.sleep(15)
        rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.findInList(Menu.toolboxFavouriteChannelsYes))
        rc.sendKeys(["KEY_BACK"])
  
        rc.sendKeys(["KEY_INFO"])
        pg = self.page.getInfoFromLiveBanner()
        pg.display()
        self.assertTrue(pg.getFavorite())
        rc.sendKeys(["KEY_BACK"])
  
        self.test_passed = True
# 
#     def test_e_rights(self):
# 
#         '''No Right panel'''
#         self.logger.info(" ")
#         self.logger.info("  ********************")
#         self.logger.info("      No Right panel")
#         self.logger.info("  ********************")
#         self.logger.info(" ")
# 
#         rc = RpiRemoteControl()
#         rc.zap(LiveData.TVnoright.lcn)
# 
#         status = self.page.getStatus()
#         self.assertTrue(status.findNoRightPanel(),"no right panel")
# 
#         if Env.VIDEO:
#             self.assertFalse(motionDetection(),u"no motion expected")
# 
#         self.test_passed = True
# 
#     def test_f_subtitles(self):
#         '''Subtitles'''
#         self.logger.info(" ")
#         self.logger.info("  ********************")
#         self.logger.info("      Subtitles")
#         self.logger.info("  ********************")
#         self.logger.info(" ")
# 
#         rc = RpiRemoteControl()
#         rc.zap(LiveData.TV1.getLcn())
#         rc.sendKeys(["KEY_MENU"])
#         if Env.STB == "NEWBOX":
#             rc.sendKeys(Menu.tab_myAccount)
#         else:
#             self.assertTrue(self.page.actionSelect(Menu.myAccount))
#         self.assertTrue(self.page.actionSelect(Menu.myPreferences))
#         self.assertTrue(self.page.actionSelect(Menu.subtitles))
#         self.assertTrue(self.page.actionSelect(Menu.hearingImpairedSubtitles))
# 
#         rc.sendKeys(["KEY_CHANNELUP"])
#         time.sleep(15)
#         rc.sendKeys(["KEY_OK"])
#         self.assertTrue(self.page.actionSelect(Menu.toolboxHearingImpairesSubtitles))
#         self.assertTrue(self.page.actionSelect(Menu.toolbox_2_noSubtitle))
# 
#         time.sleep(5)
# 
#         rc.sendKeys(["KEY_OK"])
#         self.assertTrue(self.page.findInList(Menu.toolboxNoSubtitle))
# 
#         rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
#         time.sleep(15)
#         rc.sendKeys(["KEY_OK"])
#         self.assertTrue(self.page.findInList(Menu.toolboxHearingImpairesSubtitles))
# 
#         time.sleep(5)
# 
#         rc.sendKeys(["KEY_BACK","KEY_MENU"])
#         if Env.STB == "NEWBOX":
#             rc.sendKeys(Menu.tab_myAccount)
#         else:
#             self.assertTrue(self.page.actionSelect(Menu.myAccount))
#         self.assertTrue(self.page.actionSelect(Menu.myPreferences))
#         self.assertTrue(self.page.actionSelect(Menu.subtitles))
#         self.assertTrue(self.page.actionSelect(Menu.noSubtitle))
# 
#         time.sleep(3)
# 
#         rc.sendKeys(["KEY_CHANNELUP"])
# 
#         self.test_passed = True

    def test_g_epg(self):
        '''Epg consistency '''
        self.logger.info(" ")
        self.logger.info("  ********************")
        self.logger.info("      EPG consistency")
        self.logger.info("  ********************")
        self.logger.info(" ")
 
        rc = RpiRemoteControl()
 
        rc.zap(LiveData.TV1.getLcn())
        rc.sendKeys(["KEY_INFO"])
        eit = self.page.getInfoFromLiveBanner()
        eit.display()
        rc.sendKeys(["KEY_BACK"])
 
        rc.sendKeys(["KEY_GUIDE"])  
        self.assertTrue(self.page.actionSelect(Menu.epgWeek))
        time.sleep(15)
        epg = self.page.getInfoFromEpgFocus()
        epg.display()
        rc.sendKeys(["KEY_CHANNELUP"])
        #self.assertEqual(eit.getProgram(),epg.getProgram(),"Eit != Epg (program)")
        #if epg.getNextProgram() != None :
        #    self.assertEqual(eit.getNextProgram(),epg.getNextProgram(),"Eit != Epg (next program)")
        if fuzz.ratio(eit.getProgram(),epg.getProgram()) < 50:
            time.sleep(60)
            #rc.zap(LiveData.TV1.getLcn())
            rc.sendKeys(["KEY_INFO"])
            eit = self.page.getInfoFromLiveBanner()
            eit.display()
            rc.sendKeys(["KEY_BACK"])
 
            rc.sendKeys(["KEY_GUIDE"])  
            self.assertTrue(self.page.actionSelect(Menu.epgWeek))
            time.sleep(15)
            epg = self.page.getInfoFromEpgFocus()
            epg.display()
            rc.sendKeys(["KEY_CHANNELUP"])
            if fuzz.ratio(eit.getProgram(),epg.getProgram()) < 50:
                return False
 
 
        if eit.getFavorite():
            rc.sendKeys(["KEY_GUIDE"])
            self.assertTrue(self.page.actionSelect(Menu.epgMyChannels))
            fav = self.page.getInfoFromEpgFocus()
            fav.display()
            self.assertEqual(eit.getChannelName(),fav.getChannelName(),"wrong favourite channel ")
            self.assertEqual(eit.getProgram(),fav.getProgram(),"Eit != Epg (favourite) ")
            rc.sendKeys(["KEY_UP"])
            fav = self.page.getInfoFromEpgFocus()
            rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            rc.sendKeys(["KEY_INFO"])
            eit = self.page.getInfoFromLiveBanner()
            eit.display()
            self.assertEqual(eit.getChannelName(),fav.getChannelName(),"wrong favourite channel (step 2)")
            self.assertTrue(eit.getFavorite())

            self.test_passed = True

    def test_h_liveRecord(self):
        '''Live Recording'''
        self.logger.info(" ")
        self.logger.info("  ********************")
        self.logger.info("      Live recording")
        self.logger.info("  ********************")
        self.logger.info(" ")

        rc = RpiRemoteControl()
        rc.zap(LiveData.TV6.getLcn())
        time.sleep(15)

        ''' program name  '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])

        ''' Instant Record '''
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(10)
        self.page.actionInstantRecord(PvrData.LENGTH_2)

        ''' waiting for recording - warning box checking'''
        time.sleep(60)
        rc.sendKeys(["KEY_CHANNELUP"])
        while self.page.findInDialogBox(DialogBox.RecordOnGoing):
            rc.sendKeys(["KEY_CHANNELUP"])
            time.sleep(60)
            rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(60)

        ''' checking name and video'''
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_pvr)
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrMyRecords)
        time.sleep(8)
        focusRecord = self.page.getInfoFromRecordFocus()

        self.logger.info("Record name / expected :"+str(focusRecord.getTitle())+" / "+str(currentProgram.getProgram())+" - "+str(currentProgram.getChannelName()))
        self.logger.info("Length / expected : "+str(focusRecord.getLenght())+" / "+str(PvrData.LENGTH_2))
        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV6")
        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(PvrData.LENGTH_2*60/2))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_i_scheduleRecord(self):

        '''Record scheduling'''
        self.logger.info(" ")
        self.logger.info("  **********************")
        self.logger.info("      Record scheduling ")
        self.logger.info("  **********************")
        self.logger.info(" ")

        rc = RpiRemoteControl()
        rc.zap(LiveData.TV1.getLcn())
        time.sleep(15)

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_pvr)
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrManualRecord)
        delta = 10

        currentDate = datetime.now()
        recordOneDate = currentDate + timedelta(minutes = delta)

        idOne = self.page.actionScheduleRecord(LiveData.PACKAGE_A, LiveData.TV5.getLcn(), recordOneDate, PvrData.LENGTH_3)
        self.assertTrue(idOne != False)

        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
        time.sleep(5)

        popUpDate = recordOneDate - timedelta(minutes = 3)
        wait = popUpDate - datetime.now()
        time.sleep(wait.seconds + 20)

        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordStartingSoon),"Starting soon pop-up expected")
        rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordOnGoing),"Record on going pop-up expected")
        rc.sendKeys(["KEY_CHANNELUP"])


        recordEndDate = recordOneDate + timedelta(minutes = PvrData.LENGTH_3)
        wait = recordEndDate - datetime.now()
        time.sleep(wait.seconds + 180)

        rc.sendKeys(["KEY_MENU"])

        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_pvr)
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()

        self.logger.info("Record name / expected : "+str(focusRecord.getTitle())+" / "+idOne)
        self.logger.info("Length / expected : "+str(focusRecord.getLenght())+" / "+str(PvrData.LENGTH_3))
        self.assertEqual(focusRecord.getTitle(),idOne,"Wrong record Name"+focusRecord.getTitle()+idOne)

        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(PvrData.LENGTH_3*60/2))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_j_epgRecord(self):

        '''Record from EPG  '''
        self.logger.info(" ")
        self.logger.info("  **********************")
        self.logger.info("      Record from EPG")
        self.logger.info("  **********************")
        self.logger.info(" ")

        rc = RpiRemoteControl()
        rc.zap(LiveData.TV6.getLcn())
        time.sleep(15)

        rc.sendKeys(["KEY_GUIDE"])
        self.assertTrue(self.page.actionSelect(Menu.epgWeek))
        time.sleep(15)
        rc.sendKeys(["KEY_RIGHT"])
        epg = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.epgRecord))
        rc.sendKeys(["KEY_DOWN"])
        rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        rc.zap(LiveData.TV1.getLcn())

        startRecordTime = epg.getStart()
        endRecordTime = epg.getLength() + startRecordTime
        wait = endRecordTime - datetime.now()

        time.sleep(wait.seconds + 180)

        rc.sendKeys(["KEY_CHANNELUP","KEY_MENU"])

        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_pvr)
        else:
            self.page.actionSelect(Menu.pvr)

        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()
        self.logger.info("Record name / expected : "+str(focusRecord.getTitle())+" / "+str(epg.getProgram()))
        self.logger("Length /expected : "+str(focusRecord.getLenght())+" / "+str(epg.getLength()))

        self.assertEqual(focusRecord.getTitle(),epg.getProgram(),"Wrong record Name")

        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(epg.getLength().seconds/3))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)

        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_k_dtt(self):
        '''DTT '''
        self.logger.info(" ")
        self.logger.info("  ********************")
        self.logger.info("      DTT")
        self.logger.info("  ********************")
        self.logger.info(" ")

        if Env.DTT:

            rc = RpiRemoteControl()
            rc.zap(LiveData.TV1.lcn)


            rc.sendKeys(["KEY_MENU"])
            if Env.STB == "NEWBOX":
                rc.sendKeys(Menu.tab_myAccount)
            else:
                self.assertTrue(self.page.actionSelect(Menu.myAccount))
            self.assertTrue(self.page.actionSelect(Menu.mySettings))
            self.assertTrue(self.page.actionSelect(Menu.dttChannels))
            self.assertTrue(self.page.actionSelect(Menu.dttSearch))

            end=False
            while not end:
                time.sleep(30)
                if not self.page.findInDialogBox(DialogBox.DttScanning):
                    end=True
            time.sleep(10)

            rc.sendKeys(["KEY_CHANNELUP"])

            ''' test selection source TV6 '''

            rc.zap(LiveData.TV6.lcn)
            time.sleep(15)

            rc.sendKeys(["KEY_INFO"])
            pg = self.page.getInfoFromLiveBanner()
            pg.display()
            self.assertTrue(pg.getChannelName() == LiveData.TV6.getFirstChannel_DttOn().getName(),"TV source incoherence")


            ''' test selection source TV2 '''

            rc.zap(LiveData.TV2.lcn)
            time.sleep(15)

            rc.sendKeys(["KEY_INFO"])
            pg = self.page.getInfoFromLiveBanner()
            pg.display()
            self.assertTrue(pg.getChannelName() == LiveData.TV2.getFirstChannel_DttOn().getName(),"TV source incoherence")
            rc.sendKeys(["KEY_BACK"])

        self.test_passed = True

