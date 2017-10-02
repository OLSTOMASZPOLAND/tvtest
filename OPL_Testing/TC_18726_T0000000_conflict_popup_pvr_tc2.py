# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi, DialogBox
import time
import datetime

class TC_18726_T0000000_conflict_popup_pvr_tc2(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18726 - conflict_popup_pvr_tc2
    
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

            '''step - find suitable program'''

            self.assertTrue(self.page.goToMenu(), "   ERR   not in main menu")
            self.assertTrue(self.page.actionSelect(Menu.epg), "   ERR   not in epg")
            self.assertTrue(self.page.actionSelect(Menu.epgWeek), "   ERR   not in epg now")
            time.sleep(20)
            found = False
            self.rc.zap(self.rc.getChannelBBCHD)
            time.sleep(15)
            self.assertTrue(self.page.checkIfEpgIsAvalaible(), "   ERR   epg is not avalaible")
            self.rc.zap(self.rc.getChannelBBCHD)
            currTime = datetime.datetime.now()
            while not found and (datetime.datetime.now() - currTime).seconds < 120:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(5)
                newItem = self.page.getInfoFromEpgFocus()
                if not newItem or not newItem.getStart():
                    continue
                if (newItem.getStart() - datetime.datetime.now()).total_seconds() > 1200 and \
                    newItem.getLength() > datetime.timedelta(minutes=44):
                    found = True
                    newItem.display()
                    break

            if not found:
                self.fail("   ERR   cannot find suitable epg program")

            ''' step '''
            self.logStepBeginning("set instant record")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(2)
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to channel " + self.rc.getChannelTVPPolonia)
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            firstStartTime = datetime.datetime.now()
            firstEndTime = (newItem.getStart() + newItem.getLength() - datetime.timedelta(minutes=20))
            self.assertTrue(self.page.actionInstantRecord((firstEndTime - firstStartTime).total_seconds() / 60), "   ERR   cannot set instant record")
            self.logger.info("instant record set from {} till {}".format(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(seconds=(firstEndTime - firstStartTime).total_seconds())))

            self.logStepResults("set instant record")

            self.logStepBeginning("set conflict record from epg")

            self.assertTrue(self.page.goToMenu(), "   ERR   not in main menu")
            self.assertTrue(self.page.actionSelect(Menu.epg), "   ERR   not in epg")
            self.assertTrue(self.page.actionSelect(Menu.epgWeek), "   ERR   not in epg now")
            time.sleep(20)
            self.rc.zap(self.rc.getChannelBBCHD)
            time.sleep(15)
            self.assertTrue(self.page.checkIfEpgIsAvalaible(), "   ERR   epg is not avalaible")
            currTime = datetime.datetime.now()
            found = False
            while (datetime.datetime.now() - currTime).seconds < 180:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(5)
                currItem = self.page.getInfoFromEpgFocus()
                if not currItem:
                    continue
                if newItem.getProgram() == currItem.getProgram():
                    found = True
                    break

            if not found:
                self.fail("   ERR   cannot find previosuly searched program")

            currItem.display()
            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(3)

            currTime = datetime.datetime.now()

            while not self.page.findInDialogBox(Menu.pvrRecording):
                if (datetime.datetime.now() - currTime).seconds > 180:
                    self.fail("   ERR   cannot get record popup")
                time.sleep(10)

            self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])

            secondStartTime = newItem.getStart()
            secondEndTime = newItem.getStart() + newItem.getLength()

            self.logStepResults("set conflict record from epg")

            self.logStepBeginning("manage conficting records")

            time.sleep(15)

            self.assertTrue(self.page.findInDialogBox(DialogBox.ConflictRecordTitle) or self.page.findInDialogBox(DialogBox.ConflictRecordsLongMessage), "   ERR   problem finding conflict records popup")
            self.assertTrue(self.page.actionSelect(Menu.pvrManageRecordConflicts), "   ERR   cannot select " + Menu.pvrManageRecordConflicts)
            time.sleep(5)
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

            self.assertTrue(len(self.page.driver.find_elements_by_css_selector(".itemsContainer > .item")) == 2, "   ERR   two planned records should be present")

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

            self.rc.sendKeys(["KEY_RIGHT"])

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
