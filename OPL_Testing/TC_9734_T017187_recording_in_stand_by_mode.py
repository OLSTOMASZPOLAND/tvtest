# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from datetime import datetime, timedelta
import time
from NewTvTesting.Config import *

class TC_9734_T017187_recording_in_stand_by_mode(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9734 - _T017187_recording_in_stand_by_mode

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

            startTimeDelay = 28
            recordLength = 10

            ''' step '''
            self.logStepBeginning("set record")

            self.page.zapToChannel(self.rc.getChannelTVPPolonia)

            start = datetime.now() + timedelta(minutes=startTimeDelay)

            self.rc.sendKeys(["KEY_GREEN"])

            time.sleep(2)

            self.page.actionSelect(Menu.pvrManualRecord)
            time.sleep(2)
            recordName = self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, start, recordLength)
            self.assertTrue(recordName, "   ERR   cannot set a record")

            self.logStepResults("set record")

            self.rc.sendKeys(["KEY_POWER"])

            self.page.sleep((startTimeDelay + recordLength + 1) * 60)

            '''step'''
            self.logStepBeginning("check if record is made")

            self.rc.sendKeys(["KEY_POWER"])

            try:
                currTime = datetime.now()
                status = False
                moje = None        
                time.sleep(15)
                while (status == False):
                    datanow = datetime.now()
                    calc = datanow - currTime
                    calc = calc.seconds
                    if (calc > 240):
                        status = True
                    self.rc.sendKeys(["KEY_INFO"])
                    time.sleep(2)
                    moje = self.page.getInfoFromLiveBanner()
                    time.sleep(3)
                    if moje != None:
                        status = True
                time.sleep(3)
                self.rc.sendKeys(["KEY_BACK"])
            except:
                time.sleep(240)
                pass

            self.assertTrue(self.page.goToPvrMyRecords(shouldBeEmpty=False), "   ERR   not in my records")
            time.sleep(3)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)

            item = self.page.getInfoFromRecordPage()
            self.assertTrue(item.getTitle(), "   ERR   title incorrect")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(start).rsplit(':', 1)[0], "   ERR   incorrect start date")
            self.assertTrue(item.getLength().seconds == timedelta(minutes=recordLength).seconds, "   ERR   incorrect length")
            self.assertFalse(item.getRecording(), "   ERR   channel is still recording")
            
            self.rc.sendKeys(["KEY_OK"])
            self.page.actionSelect(Menu.pvrPlay)
            time.sleep(20)
            self.assertTrue(self.page.checkLive(True), "   ERR   pvr is not playing")

            self.logStepResults("check if record is made")

            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)
            self.page.deletePvrRecord()

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
