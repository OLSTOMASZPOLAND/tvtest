# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from __builtin__ import int, str

class TC_9690_T016945_Use_the_Time_Shifting_session_and_go_on_watching_the_TS_buffer_up_to_4h(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9690 - T016945_Use time shifting_pause less than max duration_go on watch TS buffer-V1_update
    
    Purpose:     The user pauses the live for less than the max duration,
                 Use the Time Shifting session and go on watching the TS buffer (up to 4h)
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
            self.assertTrue(not motionDetection(), "  >>   ERR: motion detected and it shouldn't be there")

        self.logStepResults("step 3,4 - pause channel and check if it is actually paused")

        ''' step '''
        self.logStepBeginning("step 5 - after 30 mins replay the program by using the PLAY remote control key")

        recordTime = self.getRecordTime()

        while (recordTime <= 30):
            time.sleep(30)
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
        self.logStepBeginning("step 7 - after another 30 mins keep watching TS buffer")

        self.page.sleep(900)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.page.sleep(900)  # check at the end

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

        self.logStepResults("step 7 - after another 30 mins keep watching TS buffer")

        ''' step '''
        self.logStepBeginning("step 8,9 - continue watch the program stored on TS until 4h record is reached")

        self.page.sleep(5000)  # check in middle

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

        self.page.sleep(4000)  # check at the end

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

        self.page.sleep(2000)

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue(recordTime < 2, "   ERR: live is not displaying")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("step 8,9 - continue watch the program stored on TS until 4h record is reached")

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

