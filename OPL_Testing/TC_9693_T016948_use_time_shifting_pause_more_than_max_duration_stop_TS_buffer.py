# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from __builtin__ import int

class TC_9693_T016948_use_time_shifting_pause_more_than_max_duration_stop_TS_buffer(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9693 - T016948_UTC_9693_T016948_use_time_shifting_pause_more_than_max_duration_stop_TS_buffer
    
    Purpose: The user pauses the live for more than a maximum duration, he will be able only to replay within the 60 min time interval
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

        self.logStepResults("step 5 - wait 1 hour until buffer fills completely")

        ''' step '''
        self.logStepBeginning("step 6 - wait 1 hour and replay")

        self.page.sleep(3600)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 120 and (recordTime + maxDifference) > 120, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.logStepResults("step 6 - wait 1 hour and replay")

        ''' step '''
        self.logStepBeginning("step 7 - watch and after 1 hour stop TS session by pressing STOP key and check if live signal is displaying")

        self.page.sleep(900)  # check in middle

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue((recordTime - maxDifference) < 120 and (recordTime + maxDifference) > 120, "   ERR: incorrect recording time")

        self.rc.sendKeys(["KEY_PLAY"])

        self.page.sleep(900)  # check at the end

        if Env.VIDEO:
            if not motionDetection():
                time.sleep(15)
                if not motionDetection():
                    self.fail("   ERR   motion detection failed")

        self.rc.sendKeys(["KEY_STOP"])
        time.sleep(20)


        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(10)

        recordTime = self.getRecordTime()

        self.assertTrue(recordTime < 2, " >> ERR: live signal is not displaying")

        self.logStepResults("step 7 - watch and after 1 hour stop TS session by pressing STOP key and check if live signal is displaying")

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
