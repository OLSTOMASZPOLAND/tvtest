# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi, DialogBox
import time
import datetime
from datetime import timedelta

class TC_18727_T0000000_conflict_popup_pvr_tc3(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18727 -conflict_popup_pvr_tc3
    
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

            ''' step '''
            self.logStepBeginning("set record in future")

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   not in pvr menu")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   problem selecting " + Menu.pvrManualRecord)
            time.sleep(5)
            firstStartTime = datetime.datetime.now() + timedelta(minutes=30)
            firstEndTime = firstStartTime + timedelta(minutes=60)
            record = self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, firstStartTime, 60)
            self.assertTrue(record, "   ERR   cannot schedule record")

            self.logStepResults("set record in future")

            self.logStepBeginning("set conflict instant record")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelBBCHD), "   ERR   cannot zap to channel " + self.rc.getChannelBBCHD)

            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(30)

            secondStartTime = datetime.datetime.now()

            self.assertTrue(self.page.actionInstantRecord(60), "   ERR   cannot set instant record")

            self.logStepResults("set conflict instant record")
            
            time.sleep(20)

            self.logStepBeginning("manage conficting records")

            self.assertTrue(self.page.findInDialogBox(DialogBox.ConflictRecordTitle) or self.page.findInDialogBox(DialogBox.ConflictRecordsLongMessage), "   ERR   problem finding conflict records popup")
            self.assertTrue(self.page.actionSelect(Menu.pvrManageRecordConflicts), "   ERR   cannot select " + Menu.pvrManageRecordConflicts)
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            self.assertTrue(self.page.driver.find_element_by_css_selector(".conflict").text == Menu.pvrRecordConflict, "   ERR   cannot find %s text" % Menu.pvrRecordConflict)
            self.assertTrue(len(self.page.driver.find_elements_by_css_selector(".conflict")) == 2, "   ERR   cannot find two 'konflikt!' texts")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".input.simplebutton.validate.disabled"), "   ERR   validate button is not disabled")

            firstEndTime = (firstEndTime + datetime.timedelta(minutes=1))
            self.sendHour(firstEndTime.hour)
            self.sendHour(firstEndTime.minute)
            firstEndTime = (firstEndTime - datetime.timedelta(minutes=1))

            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordOne > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordTwo > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".input.simplebutton.validate.disabled"), "   ERR   validate button is not disabled")

            secondStartTime = (secondStartTime - datetime.timedelta(minutes=1))
            self.sendHour(secondStartTime.hour)
            self.sendHour(secondStartTime.minute)
            secondStartTime = (secondStartTime + datetime.timedelta(minutes=1))

            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordOne > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordTwo > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".input.simplebutton.validate.disabled"), "   ERR   validate button is not disabled")

            self.rc.sendKeys(["KEY_DOWN"])

            time.sleep(2)

            difference = ((firstEndTime - secondStartTime) / 2) + datetime.timedelta(minutes=3)
            firstEndTime -= difference
            self.sendHour(firstEndTime.hour)
            self.sendHour(firstEndTime.minute)

            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordOne > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertFalse(self.page.driver.find_elements_by_css_selector(".recordTwo > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".input.simplebutton.validate.disabled"), "   ERR   validate button is not disabled")

            secondStartTime += difference
            self.sendHour((secondStartTime).hour)
            self.sendHour((secondStartTime).minute)

            try:
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                self.page.driver.find_element_by_css_selector(".conflict")
                self.fail("   ERR   'konflikt!' texts still visible")
            except:
                pass

            self.assertTrue(self.page.driver.find_elements_by_css_selector(".recordOne > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".recordTwo > .conflict.hidden"), "   ERR   conflict text is not visible")
            self.assertTrue(self.page.driver.find_elements_by_css_selector(".input.simplebutton.validate.focused"), "   ERR   validate button is not focused")

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(2)
            
            self.logStepResults("manage conficting records")
            
            self.logStepBeginning("check planned recordings")

            self.assertTrue(self.page.goToPvrMyScheduled(), "   ERR   cannot go to my scheduled")
            
            self.assertTrue(len(self.page.driver.find_elements_by_css_selector(".itemsContainer > .item")) == 1, "   ERR   one planned record should be present")

            firstStartTime = str(firstStartTime).rsplit(':', 1)[0]
            secondStartTime = str(secondStartTime).rsplit(':', 1)[0]

            item = self.page.getInfoFromRecordFocus()
            if not item:
                self.fail("   ERR   cannot get info from scheduled record")

            date = str(item.getDate()).rsplit(':', 1)[0]

            if not date == firstStartTime:
                if not date == secondStartTime:
                    self.logger.info("Looking for date " + date)
                    self.logger.info("First start date " + firstStartTime)
                    self.logger.info("Second start date " + secondStartTime)
                    self.fail("   ERR   incorrect date")
                    
            self.rc.sendKeys(["KEY_BACK"])
            self.page.actionSelect(Menu.pvrMyRecords)
            time.sleep(8)
            item = self.page.getInfoFromRecordFocus()
            self.assertIsNotNone(item, "   ERR   cannot get info from record focus")
            self.assertTrue(item.getRecording(), "   ERR   instant record is not in progress")

            self.logStepResults("check planned recordings")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            self.logger.info("----------- cleaning -----------")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()

    def sendHour(self, hour):
        hour = str(hour)
        if len(hour) == 1:
            self.rc.sendNumberSequence("0" + hour)
        else:
            self.rc.sendNumberSequence(hour)
