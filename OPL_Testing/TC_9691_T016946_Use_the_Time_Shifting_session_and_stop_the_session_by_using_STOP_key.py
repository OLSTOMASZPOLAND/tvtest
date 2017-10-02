# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from __builtin__ import int

class TC_9691_T016946_Use_the_Time_Shifting_session_and_stop_the_session_by_using_STOP_key(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9691 - T016946_Use time shifting_pause less than max duration_stop the TS session-V1_update
    
        Purpose:    The user pauses the live for less than the max duration,
                Use the Time Shifting session and stop the session by using STOP key.
                The user should be redirected to the Live program and the TS buffer is flushed
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

        self.logStepBeginning("step 7 - after 30 mins stop TS session by pressing STOP key and check if live signal is displaying")

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

        self.rc.sendKeys(["KEY_STOP"])

        time.sleep(10)

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue(recordTime < 2, " >> ERR: live signal is not displaying")

        self.rc.sendKeys(["KEY_STOP", "KEY_CHANNELUP", "KEY_CHANNELDOWN"])

        time.sleep(10)

        self.logStepResults("step 7 - after 30 mins stop TS session by pressing STOP key and check if live signal is displaying")

        self.logStepBeginning("step 8,9 - pause the Live and wait for the TS buffer fills and then press P+ on remote, live should be played")

        self.rc.sendKeys(["KEY_PLAY"])

        recordTime = 0

        while (recordTime <= 2):
            time.sleep(60)
            recordTime = self.getRecordTime()

        self.rc.sendKeys(["KEY_CHANNELUP", "KEY_CHANNELDOWN"])

        time.sleep(20)

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue(recordTime < 2, " >> ERR: live signal is NOT displaying")

        self.logStepResults("step 8,9 - pause the Live and wait for the TS buffer fills and then press P+ on remote, live should be played")

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
