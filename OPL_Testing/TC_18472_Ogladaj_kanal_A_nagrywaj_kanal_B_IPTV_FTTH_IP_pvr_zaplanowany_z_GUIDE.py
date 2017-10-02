# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import Rpi, Menu, Env
import datetime

class TC_18472_Ogladaj_kanal_A_nagrywaj_kanal_B_IPTV_FTTH_IP_pvr_zaplanowany_z_GUIDE(TC_OPL_template):
    '''
    
        @author: Grzegorz Królikowski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            
            if Env.ZONE != "FTTH": 
                self.fail("   ERR   test can only run on FTTH")
            
            ''' prestep '''
            
            self.logStepResults("AT_THE_BEGINNING")
            
            if(not self.page.cleanDeleteAllRecordings()):
                self.page.cleanDeleteAllRecordings()
            self.assertTrue(self.page.setDTTChannels(False), "   ERR   Can't disable DTT channels")
            
            ''' step1 '''
            
            self.logger.info("----- step1 -----")
            self.logStepBeginning("step 1")
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 8")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row")
                
            self.assertTrue(self.page.goToMenu(), "   ERR   Can't go to 'menu'")
            self.assertTrue(self.page.actionSelect(Menu.epg), "   ERR   Can't go to 'program tv'")
            self.assertTrue(self.page.actionSelect(Menu.epgWeek), "   ERR   Can't go to 'teraz'")
            time.sleep(3)
            
            epgItem = self.page.getInfoFromEpgFocus()
            self.assertTrue(epgItem, "   ERR   Epg item is None type")
            self.assertTrue(epgItem.getLength(), "   ERR   Epg is not available")
            timeGap = (epgItem.getStart() + epgItem.getLength()) - datetime.datetime.now()
            for x in range(2):
                if(timeGap.total_seconds() < 300):
                    self.rc.sendKeys(["KEY_RIGHT"])
                    time.sleep(3)
                    epgItem = self.page.getInfoFromEpgFocus()
                    self.assertTrue(epgItem, "   ERR   Epg item is None type")
                    self.assertTrue(epgItem.getLength(), "   ERR   Epg is not available")
                    timeGap = (epgItem.getStart() + epgItem.getLength()) - datetime.datetime.now()
                else:
                    break
                    
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(20)
            
            isRecording = self.page.getInfoFromEpgFocus()
            if(isRecording != None):
                self.assertTrue(isRecording.getRecording(), "ERR   There is no red dot on planned recording")
                isRecording.display()
            
            endOfRecording = isRecording.getStart() + isRecording.getLength() + datetime.timedelta(minutes = 11)

            wait = isRecording.getStart() - datetime.datetime.now()
            if(wait.total_seconds() > 0):
                self.logger.info("I'll be sleeping for " + str(wait.total_seconds() / 60))
                time.sleep(wait.total_seconds())
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 8")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row OR user can't watch channel while recording")
            
            self.logStepResults("step 1")

            ''' step2 '''
            
            self.logger.info("----- step2 -----")
            self.logStepBeginning("step 2")
            
            self.assertTrue(self.page.zapToChannel(34), "   ERR   Can't zap to channel 34")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 34")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 34 in five checks in a row OR user can't watch channel while recording")
                
            waitForEnd = endOfRecording - datetime.datetime.now()
            self.logger.info("I'll be sleeping for " + str(waitForEnd.total_seconds()/60))
            time.sleep(waitForEnd.total_seconds())
            
            self.logStepResults("step 2")
            
            ''' step3 '''
            
            self.logger.info("----- step3 -----")
            self.logStepBeginning("step 3")
            
            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   Can't go to 'moje nagrania'")
            time.sleep(10)
            if(self.page.getInfoFromRecordFocus() != None):
                self.rc.sendKeys(["KEY_OK"])
                checkIfRecording = self.page.getInfoFromRecordPage()
                if(checkIfRecording != None):
                    if(checkIfRecording.getRecording() == False):
                        self.logger.info("Comparison of two items: ")
                        isRecording.display()
                        checkIfRecording.display()
                        dateFromItem = isRecording.getStart()
                        dateFromItem = str(dateFromItem).split()
                        dateFromItem = dateFromItem[0]
                        dateFromfRecording = checkIfRecording.getDate()
                        dateFromfRecording = str(dateFromfRecording).split()
                        dateFromfRecording = dateFromfRecording[0]
                        if((isRecording.getProgram() == checkIfRecording.getTitle()) and (dateFromItem == dateFromfRecording)):
                            self.logger.info("Recording channel match with channel watched before")
                    else:
                        self.fail("   ERR   Recording channel doesn't match with channel watched before")
                else:
                    self.fail("   ERR   Selected item is not available")
            else:
                self.fail("   ERR   There is no item available in 'moje nagrania'")
            
            self.logStepResults("step 3")
            
            ''' step4 '''
            
            self.logger.info("----- step4 -----")
            self.logStepBeginning("step 4")
            
            self.assertTrue(self.page.actionSelect(Menu.vodPlay), "   ERR   Can't go to 'ogladaj'")
            for i in range(5):
                if(self.page.checkLive(True)):
                    print "Motion detected on channel recorded video"
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in recorded video in five checks in a row")

            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(2)
            trickBar = self.page.getInfoFromTrickBar()
            self.assertTrue((trickBar), "   ERR   No trickBar obcject")
            if(trickBar.getTrickIcon() == "Forward4"):
                print "Video is in fast forward x4 mode"
                time.sleep(10)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(2)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(2)
                trickBar = self.page.getInfoFromTrickBar()
                self.assertTrue((trickBar), "   ERR   No trickBar obcject")
                if(trickBar.getTrickIcon() == "Pause"):
                    print "Video is paused"
                    self.rc.sendKeys(["KEY_PLAY"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_REWIND"])
                    time.sleep(2)
                    trickBar = self.page.getInfoFromTrickBar()
                    self.assertTrue((trickBar), "   ERR   No trickBar obcject")
                    if(trickBar.getTrickIcon() == "Rewind4"):
                        print "Video is in rewind x4 mode"
                        self.rc.sendKeys(["KEY_STOP"])
                        time.sleep(2)
                        self.page.driver.get(Rpi.DUMP)
                        time.sleep(2)
                        opis = self.page.driver.find_element_by_css_selector(".synopsis")
                        opis = opis.text.encode("utf-8")
                        print opis
                        self.assertTrue(self.page.actionSelect(Menu.vodSummary), "    ERR   Can't go to 'streszczenie")
                        time.sleep(2)
                        self.page.driver.get(Rpi.DUMP)
                        time.sleep(2)
                        streszczenie = self.page.driver.find_element_by_css_selector(".synopsis")
                        streszczenie = streszczenie.text.encode("utf-8")
                        print streszczenie
                        if(opis == streszczenie):
                            self.fail("    ERR   Nothing changes after pressing 'streszczenie'")
                        self.assertTrue(self.page.actionSelect(Menu.vodResume), "    ERR   Can't go to 'wznów oglądanie'")
                        time.sleep(2)
                        for i in range(5):
                            if(self.page.checkLive(True)):
                                print "Motion detected on channel recorded video"
                                break
                            else:
                                time.sleep(10)
                        else:
                            self.fail("   ERR   No motion detected in recorded video in five checks in a row")
                    else:
                        self.fail("   ERR   Video is not in rewind x4 mode")
                else:
                    self.fail("   ERR   Video is not paused")
            else:
                self.fail("   ERR   Video isn't in fast forward x4 mode")
            
            self.logStepResults("step 4")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                if(not self.page.cleanDeleteAllRecordings()):
                    self.page.cleanDeleteAllRecordings()