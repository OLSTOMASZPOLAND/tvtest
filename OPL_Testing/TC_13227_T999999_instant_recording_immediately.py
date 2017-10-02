# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_13227_T999999_instant_recording_immediately(TC_OPL_template):
    '''Implementation of the HP QC test ID - 13227_instant_recording_immediately
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            #self.page.cleanDeleteAllRecordings()
            
            ''' step '''
            self.logStepBeginning("zap to channel 8 and start instant record")
            
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia))
            
            self.rc.sendKeys(["KEY_RECORD"])
            
            time.sleep(20)
            
            self.assertTrue(self.page.findInDialogBox(Menu.pvrRecord), '   ERR   cannot find "%s" popup' % Menu.pvrRecord)
                        
            self.rc.sendKeys(["KEY_OK"])
            
            self.logStepResults("zap to channel 8 and start instant record")
            
            self.logStepBeginning("check if record is in progress")
            
            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records page")
            
            item = self.page.getInfoFromRecordFocus()
            if not item:
                self.fail("   ERR   cannot get focus from record focus")
                
            self.assertTrue(item.getRecording(), "   ERR   program is not recording")
            
            self.logStepResults("check if record is in progress")
            self.rc.sendKeys(["KEY_OK"])
            self.page.deletePvrRecord(True)

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanDeleteAllRecordings()