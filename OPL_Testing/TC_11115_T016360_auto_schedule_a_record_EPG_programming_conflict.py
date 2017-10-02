# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
import datetime

class TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict(TC_OPL_template):
    '''Implementation of the HP QC test ID - 11115 - _T016360_auto_schedule_a_record_EPG_programming_conflict
    
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

            ''' step '''
            self.logStepBeginning("STEP 3,4,5 - find and start recording of a future programme in EPG")

            self.page.zapToChannel(self.rc.getChannelTVPPolonia)
            self.assertTrue(self.page.goToMenu(), "   ERR   cannot go to menu")
            time.sleep(5)
            self.page.actionSelect(Menu.epg)
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.epgWeek), "   ERR   not in EPG")
            item = []
            
            self.rc.zap(self.rc.getChannelTVPPolonia)
            
            if self.page.checkIfEpgIsAvalaible():                
                self.assertTrue(self.page.recordFromEpg(1, self.rc.getChannelTVPPolonia, item), "   ERR   cannot set record")
            else:
                self.rc.zap(self.page.rc.getChannelBBCHD)
                self.assertTrue(self.page.recordFromEpg(1, self.rc.getChannelBBCHD, item), "   ERR   cannot set record")


            self.logStepResults("STEP 3,4,5 - find and start recording of a future programme in EPG")

            self.logStepBeginning("STEP 6,7 check my planned recordings and my records")

            if not self.page.goToPvrMyRecords():
                self.rc.sendKeys(["KEY_OK"])
                if not self.page.goToPvrMyRecords(shouldBeEmpty=True):
                    self.assertTrue(False, "   ERR   cannot go to my records")
            else:
                time.sleep(10)
                currItem = self.page.getInfoFromRecordFocus()
                if not currItem:
                    self.fail("   ERR   cannot get info from record page")
                self.assertTrue(currItem.getTitle() != item[0].getProgram() and currItem.getDate() != item[0].getStart(), "   ERR   record displays in my records")

            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=False), "   ERR   not in my scheduled")

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)

            currItem = self.page.getInfoFromRecordPage()

            self.assertTrue(item[0].getStart() == currItem.getDate(), "   ERR   incorrect start time")
            self.assertTrue(item[0].getStart() + item[0].getLength() == currItem.getDate() + currItem.getLength(), "   ERR   incorrect end time")
            self.assertTrue(item[0].getProgram() == currItem.getTitle(), "   ERR   incorrect title")
            self.rc.sendKeys(["KEY_TV"])

            self.logStepResults("STEP 6,7 check my planned recordings and my records")

            self.page.sleep((item[0].getStart() - datetime.datetime.now()).seconds + 120)

            self.logStepBeginning("STEP 8,9 - check my planned recordings and my records on start")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            
            time.sleep(5)

            currItem = self.page.getInfoFromRecordFocus()

            self.assertTrue(currItem.getTitle() == item[0].getProgram() and currItem.getDate() == item[0].getStart() \
                            and currItem.getRecording() == True, "   ERR   incorrect title or start date")

            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True), "   ERR   my scheduled is not empty")

            self.rc.sendKeys(["KEY_TV"])

            self.logStepResults("STEP 8,9 -  check my planned recordings and my records on start")

            self.page.sleep((item[0].getStart() + item[0].getLength() - datetime.datetime.now()).seconds + 120)

            self.logStepBeginning("STEP 10,11 -  check my planned recordings and my records on end")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            
            time.sleep(5)

            currItem = self.page.getInfoFromRecordFocus()

            self.assertTrue(currItem.getTitle() == item[0].getProgram() and currItem.getDate() == item[0].getStart() \
                        and currItem.getRecording() == False, "   ERR   incorrect title or start date")

            self.rc.sendKeys(["KEY_OK"])

            self.page.deletePvrRecord()

            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True), "   ERR   my scheduled is not empty")

            self.logStepResults("STEP 10,11 -  check my planned recordings and my records on end")

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