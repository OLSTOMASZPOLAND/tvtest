# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
import datetime
from NewTvTesting.Config import *

class TC_9718_T016940_schedule_an_instant_recording_EPG_is_avalaible_end_time_less_10_mins(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9718 - _T016940_schedule_an_instant_recording_EPG_is_avalaible_end_time_less_10_mins

    @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.page.cleanDeleteAllRecordings()
            '''SETTINGS'''
            afterShowDelay = 10

            ''' step '''
            self.logStepBeginning("STEP 3 - select an ongoing program whose will be finished in less than %s min and start recording" % afterShowDelay)

            self.page.zapToChannel(1)  # dont want any specific channel, just first one
            found = False
            for x in range (30):
                time.sleep(4)
                self.rc.sendKeys(["KEY_INFO"])
                time.sleep(3)

                info = self.page.getInfoFromLiveBanner()
                if not info:
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    continue
                if info.getStart() and info.getLength():
                    if((info.getStart() + info.getLength()) - datetime.datetime.now()).seconds < afterShowDelay * 60:
                        found = True
                        break                       
                self.rc.sendKeys(["KEY_CHANNELUP"])
            if not found:
                self.page.zapToChannel(1)  # dont want any specific channel, just first one
                self.page.sleep(300)
                for x in range (30):
                    time.sleep(4)
                    self.rc.sendKeys(["KEY_INFO"])
                    time.sleep(3)
    
                    info = self.page.getInfoFromLiveBanner()
                    if not info:
                        self.rc.sendKeys(["KEY_CHANNELUP"])
                        continue
                    if info.getStart() and info.getLength():
                        if((info.getStart() + info.getLength()) - datetime.datetime.now()).seconds < afterShowDelay * 60:
                            found = True
                            break              
                    self.rc.sendKeys(["KEY_CHANNELUP"])
            if not found:                
                self.assertTrue(False, "   ERR   cannot find proper channel")
                
            if self.page.findInDialogBox(Menu.channelNotInSubscription):
                self.page.actionSelect(u"tak".encode('utf-8'))

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            currTime = datetime.datetime.now()
            while not self.page.findInDialogBox(Menu.pvrRecord):
                if (datetime.datetime.now() - currTime).seconds > 180:
                    self.fail("   ERR   cannot find %s" % Menu.pvrRecord)
                time.sleep(3)

            self.rc.sendKeys(["KEY_OK"])

            self.logStepResults("STEP 3 - select an ongoing program whose will be finished in less than %s min and start recording" % afterShowDelay)

            self.logStepBeginning("check the record status in my records")

            self.page.goToPvrMyRecords(shouldBeEmpty=False)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            item = self.page.getInfoFromRecordPage()
            if not item:
                self.fail("   ERR   cannot get info from recording")

            self.assertTrue(info.getStart() + info.getLength() < item.getDate() + item.getLength() , "   ERR   incorrect end time")

            self.logStepResults("check the record status in my records")

            if not self.page.deletePvrRecord(True):
                self.page.deletePvrRecord(True)

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanDeleteAllRecordings()
