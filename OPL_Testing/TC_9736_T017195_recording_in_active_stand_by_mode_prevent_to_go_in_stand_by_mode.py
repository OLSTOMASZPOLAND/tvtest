# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from datetime import datetime, timedelta
import time
from NewTvTesting.Config import *

class TC_9736_T017195_recording_in_active_stand_by_mode_prevent_to_go_in_stand_by_mode(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9736 - _T017195_recording_in_active_stand_by_mode_prevent_to_go_in_stand_by_mode

    @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():                
                self.page.cleanDeleteAllRecordings()

            startTimeDelay = 20
            recordLength = 20

            ''' step '''
            self.logStepBeginning("set record")
            self.page.zapToChannel(self.rc.getChannelTVPPolonia)

            self.page.goToPvrMenu()

            time.sleep(2)

            self.page.actionSelect(Menu.pvrManualRecord)
            time.sleep(2)
            start = datetime.now() + timedelta(minutes=startTimeDelay)
            recordName = self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, start, recordLength)
            self.assertTrue(recordName, "   ERR   cannot set a record")

            self.logStepResults("set record")

            self.rc.sendKeys(["KEY_POWER"])

            time.sleep((startTimeDelay + recordLength + 1) * 60)

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

            item = self.page.getInfoFromRecordPage()

            self.assertTrue(item.getTitle(), "   ERR   title incorrect")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(start).rsplit(':', 1)[0], "   ERR   incorrect start date")
            self.assertTrue(item.getLength().seconds == timedelta(minutes=recordLength).seconds, "   ERR   incorrect length")
            self.assertTrue(item.getRecording() == False, "   ERR   channel is still recording")

            self.logStepResults("check if record is made")

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
