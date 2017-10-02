# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from __builtin__ import int

class TC_9694_T016949_pause_live_for_more_60MIN_replay_within_the_60_min_time_range(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9694 - T016949_Use time shifting_pause more than max duration_go back review in TS session-V1_update
    
    Purpose: As the user pauses the live for more than the maximum duration (60min here) he will be able to replay only within the 60 min time range
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
        self.logStepBeginning("step 5 - wait 1 hour until buffer fills completely")

        self.page.sleep(3600)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 60 and (recordTime + maxDifference) > 60, "   ERR: incorrect recording time")

        self.logStepResults("step 5 - wait 1 hour until buffer fills completely")

        ''' step '''
        self.logStepBeginning("step 6 - wait 30 min and replay")

        self.page.sleep(1800)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 90 and (recordTime + maxDifference) > 90, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.logStepResults(("step 6 - wait 30 min and replay"))

        ''' step '''
        self.logStepBeginning("step 7 - after 1 hour go backward and watch again the replayed program")

        self.page.sleep(1800)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 90 and (recordTime + maxDifference) > 90, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(1800)  # check at the end

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 90 and (recordTime + maxDifference) > 90, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])


        self.rc.sendKeys(["KEY_REWIND", "KEY_REWIND", "KEY_REWIND", "KEY_REWIND"])

        time.sleep(120)

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 152 and (recordTime + maxDifference) > 152, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(1800)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 182 and (recordTime + maxDifference) > 182, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(1800)  # check at the end

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 182 and (recordTime + maxDifference) > 182, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("step 7 - after 1 hour go backward and watch again the replayed program")

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
