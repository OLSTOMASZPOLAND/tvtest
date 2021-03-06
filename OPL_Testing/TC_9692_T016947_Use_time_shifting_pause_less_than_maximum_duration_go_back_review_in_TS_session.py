# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from __builtin__ import int

class TC_9692_T016947_Use_time_shifting_pause_less_than_maximum_duration_go_back_review_in_TS_session(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9692 - T016947_Use time shifting_pause less than max duration_go back review in TS session-V1_update
    
    Purpose: Use_time_shifting_pause_less_than_maximum_duration_go_back_review_in_TS_session
    @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        '''SETTINGS'''
        maxDifference = 5
        '''SETTINGS'''

        ''' step '''
        self.logStepBeginning("step 3,4 - pause channel and check if it is actually paused")

        self.page.zapToChannel(self.rc.getChannelTVPPolonia)

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        item = self.page.getInfoFromTrickBar()
        
        self.assertTrue(item != None, "   >>   ERR: can't find trick symbol")
        
        item = item.getTrickIcon()

        self.assertTrue(item == "Pause", "   >>   ERR: can't find pause symbol")

        if Env.VIDEO:
            if motionDetection():
                    self.fail("   ERR   motion detected but channel should be paused")

        self.logStepResults("step 3,4 - pause channel and check if it is actually paused")

        ''' step '''
        self.logStepBeginning("step 5 - after 30 mins replay the program by using the PLAY remote control key")

        recordTime = 0

        while (recordTime <= 30):
            time.sleep(60)
            recordTime = self.getRecordTime()

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.logStepResults("step 5 - after 30 mins replay the program by using the PLAY remote control key")

        ''' step '''
        self.logStepBeginning("step 6 - continue watching when TS maximum buffer is reached")

        self.page.sleep(900)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 30 and (recordTime + maxDifference) > 30, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(900)  # check when max buffer is reached

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 30 and (recordTime + maxDifference) > 30, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("step 6 - continue watching when TS maximum buffer is reached")

        ''' step '''
        self.logStepBeginning("step 7 - after another 30 mins rewind to beginning and watch")

        self.page.sleep(900)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 30 and (recordTime + maxDifference) > 30, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(960)  # check at the end

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 30 and (recordTime + maxDifference) > 30, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_REWIND", "KEY_REWIND", "KEY_REWIND", "KEY_REWIND"])

        time.sleep(120)

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 62 and (recordTime + maxDifference) > 62, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("step 7 - after another 30 mins rewind to beginning and watch")

        ''' step '''
        self.logStepBeginning("step 8 - go forward the record on TS buffer")

        self.page.sleep(1800)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 60 and (recordTime + maxDifference) > 60, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(1800)  # check at the end

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 60 and (recordTime + maxDifference) > 60, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("step 8 - go forward the record on TS buffer")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def getRecordTime(self):
        a = self.page.getInfoFromTrickBar()
        if not a:
            time.sleep(2)
            a = self.page.getInfoFromTrickBar()
        if a != None:
            a = a.getMinutesInSecondRow()
            if type(a) == int:
                return a
        else:
            self.fail("   ERR   cannot get time")
