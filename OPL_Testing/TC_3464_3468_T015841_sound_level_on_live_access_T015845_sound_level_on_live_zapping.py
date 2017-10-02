# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time

class TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3464 and 3468 - sound_level_on_live_access & sound_level_on_live_zapping
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        self.logStepBeginning("go to main menu and play with sound")

        self.assertTrue(self.page.goToMenu(), "   ERR   cannot go to main menu")

        logVolUp = self.page.findInLogs("stb event [SOUND_UP] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEUP"])

        item = self.page.getVolumeLevel()

        while logVolUp.working:
            time.sleep(0.5)

        if not logVolUp.found:
            logVolUp.debug()
            self.fail("   ERR   vol up pattern cannot be found in logs")

        logVolDown = self.page.findInLogs("stb event [SOUND_DOWN] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEDOWN"])

        item2 = self.page.getVolumeLevel()

        self.assertTrue(item > item2, "    volume did not went down")

        while logVolDown.working:
            time.sleep(0.5)

        if not logVolDown.found:
            logVolDown.debug()
            self.fail("   ERR   vol down pattern cannot be found in logs")

        logMute = self.page.findInLogs("ROOT> BaseAppController > mute > newState ? true", 15)
        time.sleep(2)
        self.rc.sendKeys(["KEY_MUTE"])

        while logMute.working:
            time.sleep(0.5)

        if not logMute.found:
            logMute.debug()
            self.fail("   ERR   mute pattern not found in logs")
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            self.assertTrue(self.rc.getFrontPanel() == 'MutE', "   ERR   front panel not updated")

        self.logStepResults("go to main menu and play with sound")

        '''step'''

        self.logStepBeginning("go to vod menu and play with sound")

        self.assertTrue(self.page.goToVodMenu(), "   ERR   cannot go to vod menu")

        logVolUp = self.page.findInLogs("stb event [SOUND_UP] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEUP"])

        item = self.page.getVolumeLevel()

        while logVolUp.working:
            time.sleep(0.5)

        if not logVolUp.found:
            logVolUp.debug()
            self.fail("   ERR   vol up pattern cannot be found in logs")

        logVolDown = self.page.findInLogs("stb event [SOUND_DOWN] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEDOWN"])

        item2 = self.page.getVolumeLevel()

        self.assertTrue(item > item2, "    volume did not went down")

        while logVolDown.working:
            time.sleep(0.5)

        if not logVolDown.found:
            logVolDown.debug()
            self.fail("   ERR   vol down pattern cannot be found in logs")

        logMute = self.page.findInLogs("ROOT> BaseAppController > mute > newState ? true", 15)
        time.sleep(2)
        self.rc.sendKeys(["KEY_MUTE"])

        while logMute.working:
            time.sleep(0.5)

        if not logMute.found:
            logMute.debug()
            self.fail("   ERR   mute pattern not found in logs")

        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            self.assertTrue(self.rc.getFrontPanel() == 'MutE', "   ERR   front panel not updated")
            
        logMute = self.page.findInLogs("ROOT> BaseAppController > mute > newState ? false")
        time.sleep(2)
        self.rc.sendKeys(["KEY_MUTE"])
        item3 = self.page.getVolumeLevel()
        self.logger.info(item2)
        self.logger.info(item3)
        self.assertTrue(item2 == item3, "    ERR    different volume level after muting and unmuting sound")

        while logMute.working:
            time.sleep(0.5)

        if not logMute.found:
            logMute.debug()
            self.fail("   ERR   mute pattern not found in logs")

        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            self.assertTrue(self.rc.getFrontPanel() == 'MutE', "   ERR   front panel not updated")
            
        self.logStepResults("go to vod menu and play with sound")

        '''step'''

        self.logStepBeginning("go to live channel and play with sound")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(2)
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to channel " + self.rc.getChannelTVPPolonia)

        logVolUp = self.page.findInLogs("stb event [SOUND_UP] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEUP"])

        item = self.page.getVolumeLevel()

        while logVolUp.working:
            time.sleep(0.5)

        if not logVolUp.found:
            logVolUp.debug()
            self.fail("   ERR   vol up pattern cannot be found in logs")

        logVolDown = self.page.findInLogs("stb event [SOUND_DOWN] treated by default behavior", 15)

        time.sleep(2)

        self.rc.sendKeys(["KEY_VOLUMEDOWN"])

        item2 = self.page.getVolumeLevel()

        self.assertTrue(item > item2, "    volume did not went down")

        while logVolDown.working:
            time.sleep(0.5)

        if not logVolDown.found:
            logVolDown.debug()
            self.fail("   ERR   vol down pattern cannot be found in logs")

        logMute = self.page.findInLogs("ROOT> BaseAppController > mute > newState ? true", 15)
        time.sleep(2)
        self.rc.sendKeys(["KEY_MUTE"])

        while logMute.working:
            time.sleep(0.5)

        if not logMute.found:
            logMute.debug()
            self.fail("   ERR   mute pattern not found in logs")

        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            self.assertTrue(self.rc.getFrontPanel() == 'MutE', "   ERR   front panel not updated")
            
        logMute = self.page.findInLogs("ROOT> BaseAppController > mute > newState ? false")
        time.sleep(2)
        self.rc.sendKeys(["KEY_MUTE"])
        time.sleep(0.2)
        item3 = self.page.getVolumeLevel()
        self.assertTrue(item2 == item3, "    ERR    different volume level after muting and unmuting sound")

        while logMute.working:
            time.sleep(0.5)

        if not logMute.found:
            logMute.debug()
            self.fail("   ERR   mute pattern not be found in logs")

        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            self.assertTrue(self.rc.getFrontPanel() == 'MutE', "   ERR   front panel not updated")
            
        self.logStepResults("go to live channel and play with sound")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")