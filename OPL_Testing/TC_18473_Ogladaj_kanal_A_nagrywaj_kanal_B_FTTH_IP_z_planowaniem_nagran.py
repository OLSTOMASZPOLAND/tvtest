# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import Rpi, Menu, Env
import datetime

class TC_18473_Ogladaj_kanal_A_nagrywaj_kanal_B_FTTH_IP_z_planowaniem_nagran(TC_OPL_template):
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
            
            ''' step '''
            
            self.logStepBeginning("step 1")
            
            dateStartRecording = datetime.datetime.now() + datetime.timedelta(minutes = 8)
            dateEndRecording = dateStartRecording + datetime.timedelta(minutes = 5)
            self.assertTrue(self.page.goToPvrMenu(), "   ERR   Can't go to 'nagrywarka TV'")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   Can't go to 'planowanie nagran'")
            self.assertTrue(self.page.actionScheduleRecord(8, dateStartRecording, 5), "   ERR   Can't schedule record")
            self.assertTrue(self.page.actionSelect(Menu.pvrMyScheduled), "   ERR   Can't go to 'zaplanowane nagrania'")
            if(self.page.findInDialogBox(Menu.pvrMyScheduled)):
                self.fail("   ERR   No scheduled records")
            else:
                record = self.page.getInfoFromRecordFocus()
                if(record != None):
                    recordTitle = record.getTitle()
                    recordDate = record.getDate()
                    record.display()
                else:
                    self.fail("   ERR   record is None type")
                
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            
            self.logStepResults("step 1")
            
            ''' step '''
            
            self.logStepBeginning("step 2")
            
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 8")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row")
                
            self.assertTrue(self.page.zapToChannel(34), "   ERR   Can't zap to channel 34")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 34")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 34 in five checks in a row")
            
            self.logStepResults("step 2")
            
            ''' step '''
            
            self.logStepBeginning("step 3")
            
            waitGap  = dateStartRecording - datetime.datetime.now()
            if(waitGap.total_seconds() > 0):
                self.logger.info("I'll be sleeping for " + str(waitGap.total_seconds()/60))
                time.sleep(waitGap.total_seconds())
            
            self.assertTrue(self.page.goToPvrMenu(), "   ERR   Can't go to 'nagrywarka TV'")
            self.assertTrue(self.page.actionSelect(Menu.pvrMyScheduled), "   ERR   Can't go to 'zaplanowane nagrania'")
            if(self.page.findInDialogBox(Menu.pvrMyScheduled)):
                self.rc.sendKeys(["KEY_OK"])
            else:
                self.fail("   ERR   There are still scheduled recordings")
            
            self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords), "   ERR   Can't go to 'moje nagrania'")
            self.rc.sendKeys(["KEY_OK"])
            objectInMyRecordings = self.page.getInfoFromRecordPage()
            self.assertTrue(objectInMyRecordings, "   ERR   None type object in 'my recordings'")
            self.assertTrue(objectInMyRecordings.getRecording(), "   ERR   Object is not in recording state")
            objectInMyRecordings.display()
            recordingDate = objectInMyRecordings.getDate()
            recordingTitle = objectInMyRecordings.getTitle()
            self.assertTrue((recordTitle == recordingTitle) and (recordDate == recordingDate), "   ERR   Objects don't match")
            
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 8")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 8 in five checks in a row")
                
            self.assertTrue(self.page.zapToChannel(34), "   ERR   Can't zap to channel 34")
            for i in range(5):
                if(self.page.checkLive(False)):
                    self.logger.info("Motion detected on channel 34")
                    break
                else:
                    time.sleep(10)
            else:
                self.fail("   ERR   No motion detected in channel 34 in five checks in a row")
            
            self.logStepResults("step 3")
            
            ''' step '''
            self.logger.info("----- step4 -----")
            self.logStepBeginning("step 4")
            
            waitGap  = dateEndRecording - datetime.datetime.now()
            if(waitGap.total_seconds() > 0):
                self.logger.info("I'll be sleeping for " + str(waitGap.total_seconds()/60))
                time.sleep(waitGap.total_seconds())
            
            self.assertTrue(self.page.goToPvrMenu(), "   ERR   Can't go to 'nagrywarka TV'")
            self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords), "   ERR   Can't go to 'moje nagrania'")
            time.sleep(3)
            recordedObject = self.page.getInfoFromRecordFocus()
            self.assertTrue(recordedObject, "   ERR   recordedObject is None type")
            recordingDate = recordedObject.getDate()
            recordingTitle = recordedObject.getTitle()
            self.assertTrue((recordTitle == recordingTitle) and (recordDate == recordingDate), "   ERR   Objects don't match")
            self.assertTrue(not recordedObject.getRecording(), "   ERR   Object is in recording state")
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.vodPlay), "   ERR   Can't go to 'ogladaj'")
            
            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(2)
            trickBar = self.page.getInfoFromTrickBar()
            self.assertTrue((trickBar), "   ERR   No trickBar obcject")
            if(trickBar.getTrickIcon() == "Forward4"):
                self.logger.info("Video is in fast forward x4 mode")
                time.sleep(10)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(2)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(2)
                trickBar = self.page.getInfoFromTrickBar()
                self.assertTrue((trickBar), "   ERR   No trickBar obcject")
                if(trickBar.getTrickIcon() == "Pause"):
                    self.logger.info("Video is paused")
                    self.rc.sendKeys(["KEY_PLAY"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_REWIND"])
                    time.sleep(2)
                    trickBar = self.page.getInfoFromTrickBar()
                    self.assertTrue((trickBar), "   ERR   No trickBar obcject")
                    if(trickBar.getTrickIcon() == "Rewind4"):
                        self.logger.info("Video is in rewind x4 mode")
                        self.rc.sendKeys(["KEY_STOP"])
                        time.sleep(2)
                        self.assertTrue(self.page.actionSelect(Menu.vodResume), "    ERR   Can't go to 'wznów oglądanie'")
                        time.sleep(2)
                        for i in range(5):
                            if(self.page.checkLive(True)):
                                self.logger.info("Motion detected on channel recorded video")
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