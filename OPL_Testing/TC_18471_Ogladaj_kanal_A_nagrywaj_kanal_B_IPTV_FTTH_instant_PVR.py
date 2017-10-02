# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import Rpi, Menu, Env
import datetime

class TC_18471_Ogladaj_kanal_A_nagrywaj_kanal_B_IPTV_FTTH_instant_PVR(TC_OPL_template):
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

            print "----------step1----------"
            self.logStepBeginning("step 1")

            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    print "Motion detected on channel 8"
                    self.rc.sendKeys(["KEY_RECORD"])
                    time.sleep(20)
                    self.assertTrue(self.page.actionInstantRecord(5), "   ERR   Can't set recording")
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_INFO"])
                    infoFromLiveBanner = self.page.getInfoFromLiveBanner()
                    self.rc.sendKeys(["KEY_BACK"])
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row")

            self.logStepResults("step 1")

            print "----------step2----------"
            self.logStepBeginning("step 2")

            self.assertTrue(self.page.zapToChannel(34), "   ERR   Can't zap to channel 34")
            for i in range(5):
                if(self.page.checkLive(False)):
                    print "Motion detected on channel 34"
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 34 in five checks in a row")

            self.logStepResults("step 2")

            print "----------step3----------"
            self.logStepBeginning("step 3")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   Can't go to 'moje nagrania'")
            time.sleep(10)
            if(self.page.getInfoFromRecordFocus() != None):
                self.rc.sendKeys(["KEY_OK"])
                checkIfRecording = self.page.getInfoFromRecordPage()
                if(checkIfRecording != None):
                    if(checkIfRecording.getRecording() == True):
                        print "info------------------------"
                        infoFromLiveBanner.display()
                        checkIfRecording.display()
                        print "info------------------------"
                        dateFromLiveBanner = infoFromLiveBanner.getStart()
                        dateFromLiveBanner = str(dateFromLiveBanner).split()
                        dateFromLiveBanner = dateFromLiveBanner[0]
                        dateFromfRecording = checkIfRecording.getDate()
                        dateFromfRecording = str(dateFromfRecording).split()
                        dateFromfRecording = dateFromfRecording[0]
                        if((infoFromLiveBanner.getProgram() == checkIfRecording.getTitle()) and (dateFromLiveBanner == dateFromfRecording)):
                            print "Recording channel match with channel watched before"
                    else:
                        self.fail("   ERR   Recording channel doesn't match with channel watched before")
                else:
                    self.fail("   ERR   Selected item is not in recording state")
            else:
                self.fail("   ERR   There is no item available in 'moje nagrania'")


            self.logStepResults("step 3")

            print "----------step4----------"
            self.logStepBeginning("step 4")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    print "Motion detected on channel 8"
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row OR user is no able to watch channel that is recording")

            waitGap = ((checkIfRecording.getDate() + datetime.timedelta(minutes=6)) - datetime.datetime.now())
            print "I'll be sleeping for " + str((waitGap.total_seconds()) / 60) + " minutes"
            time.sleep(waitGap.total_seconds())
            self.logStepResults("step 4")

            print "----------step5----------"
            self.logStepBeginning("step 5")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   Can't go to 'moje nagrania'")
            time.sleep(10)
            if(self.page.getInfoFromRecordFocus() != None):
                self.rc.sendKeys(["KEY_OK"])
                checkLastItem = self.page.getInfoFromRecordPage()
                if(checkLastItem.getRecording() != True):
                    print "info------------------------"
                    infoFromLiveBanner.display()
                    checkLastItem.display()
                    print "info------------------------"
                    dateFromfLastItem = checkLastItem.getDate()
                    dateFromfLastItem = str(dateFromfLastItem).split()
                    dateFromfLastItem = dateFromfLastItem[0]
                    if ((infoFromLiveBanner.getProgram() in checkLastItem.getTitle()) or (checkLastItem.getTitle() in infoFromLiveBanner.getProgram())) and (dateFromLiveBanner == dateFromfLastItem):
                        print "Recorded item match with channel watched before"
                    else:
                        self.fail("   ERR   Recorded item doesn't match with channel watched before")
                else:
                    self.fail("   ERR   Selected item is in recording state")
            else:
                self.fail("   ERR   There is no item available in 'moje nagrania'")

            self.logStepResults("step 5")
            
            print "----------step6----------"
            self.logStepBeginning("step 6")

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
            self.logStepResults("step 6")

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