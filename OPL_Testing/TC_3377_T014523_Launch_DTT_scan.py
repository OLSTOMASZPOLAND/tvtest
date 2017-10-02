# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
import datetime
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Config import *
from NewTvTesting.Containers import *

class TC_3377_T014523_Launch_DTT_scan(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3377_T014523_Launch_DTT_scan
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' step '''
            self.logStepBeginning("set DTT channels")

            self.assertTrue(self.page.goToMenu(), "  >>   ERR: not in Menu")
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "  >>   ERR: not in MyAccount")
            self.assertTrue(self.page.actionSelect(Menu.tvSettings), "  >>   ERR: not in TV Settings")
            self.assertTrue(self.page.actionSelect(Menu.dttChannels), "  >>   ERR: not in DTT channels")

            self.assertTrue(self.page.findInList(Menu.dttSearch, True), "  >>   ERR   cannot find " + Menu.dttSearch)
            self.assertTrue(self.page.findInList(Menu.dttDesactivation, True), "  >>   ERR   cannot find " + Menu.dttDesactivation)
            self.assertTrue(self.page.actionSelect(Menu.dttSearch), "  >>   ERR   cannot select " + Menu.dttSearch)

            time.sleep(5)

            currTime = datetime.datetime.now()
            while self.page.findInDialogBox(u"Trwa wyszukiwanie".encode("utf-8")):
                if(datetime.datetime.now() - currTime).seconds > 300:
                    self.fail("  >>   ERR: time's up")
                time.sleep(5)

            time.sleep(10)

            if self.page.findInDialogBox(u"Nie znaleziono".encode("utf-8")):
                self.page.actionSelect(Menu.dttSearchLater)
                self.fail("   ERR   no DTT channels found")

            try:
                numb = int(self.page.driver.find_element_by_xpath("//span[@class='value']").text)
                if not numb:
                    self.fail("  >>   ERR: channels not found")
            except:
                self.fail("  >>   ERR: channels not found")                

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("set DTT channels")

            '''step'''
            self.logStepBeginning("check if DTT channels displays correctly")

            channel = int(self.rc.getChannelTVP1HD_dtt)
            maxChannel = channel + numb
            error = 0
            self.assertTrue(self.page.zapToChannel(channel), "   ERR   cannot zap to channel " + self.rc.getChannelTVP1HD_dtt)
            while channel <= 262 and channel < maxChannel:
                time.sleep(4)
                self.rc.sendKeys(["KEY_INFO"])
                time.sleep(2)
                info = self.page.getInfoFromLiveBanner()
                if type(info) == ProgramInfoItem:
                    if info.getLcn() == channel:
                        if not self.page.checkLive():
                            
                            self.logStepResults("   ERR   channel %i is not displaying correctly" % channel)
                            error += 1
                    else:
                        self.logStepResults("   ERR   cannot zap to channel " + str(channel))
                        error += 1
                else:
                    self.logStepResults("   ERR   cannot zap to channel " + str(channel))
                    error += 1

                channel += 1
                self.rc.sendKeys(["KEY_CHANNELUP"])

            self.logStepResults("check if DTT channels displays correctly")


            if error:
                self.fail("   ERR    %i channels wasnt displaying correctly. Check screenshots." % error)

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            self.logger.info("----------- cleaning -----------")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
