# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi, DialogBox
import time
import datetime

class TC_18725_T0000000_conflict_popup_pvr_tc1(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18725 -conflict_popup_pvr_tc1
    
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
            while not found and (datetime.datetime.now() - currTime).seconds < 180:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(5)
                newItem = self.page.getInfoFromEpgFocus()
                if not newItem or not newItem.getStart():
                    continue
                print newItem.getStart() - datetime.datetime.now()
                if (newItem.getStart() - datetime.datetime.now()).total_seconds() > 2640 and \
                    newItem.getLength() > datetime.timedelta(minutes=44):
                    found = True
                    break

            if not found:
                self.fail("   ERR   cannot find suitable epg program")

            newItem.display()

            ''' step '''
            self.logStepBeginning("set record in future")

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   not in pvr menu")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   problem selecting " + Menu.pvrManualRecord)
            time.sleep(5)
            firstStartTime = datetime.datetime.now() + (newItem.getStart() - datetime.datetime.now()) - datetime.timedelta(minutes=20)
            firstEndTime = firstStartTime + datetime.timedelta(minutes=40)
            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, firstStartTime, 40), "   ERR   cannot schedule record")

            self.logStepResults("set record in future")

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
            while (datetime.datetime.now() - currTime).seconds < 120:
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

            self.logStepBeginning("manage conflicting records")  
                      
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

            self.logStepResults("manage conflicting records")
            
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
