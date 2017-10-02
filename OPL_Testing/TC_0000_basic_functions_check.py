# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
import datetime
from random import randint

class TC_0000_basic_functions_check(TC_OPL_template):
    '''TC_0000_basic_functions_check
    
        @author: Marcin Gmurczyk
    '''
    
    class Recording(object):
        def __init__(self, channel, start, end):            
            self.channel_number = channel
            self.start_time = start
            self.end_time = end
        def get_record_time_in_seconds(self):
            return (self.end_time - self.start_time).seconds
        
        def get_properties(self):
            text = []
            text.append(">Recording info<")
            text.append("\nChannel: {}".format(self.channel_number))
            text.append("\nStart_time: {}, ".format(self.start_time))
            if self.start_time < datetime.datetime.now():                
                text.append("already started")
            else:
                text.append("not started yet")
            text.append("\nEnd_time: {}, ".format(self.end_time))
            text.append("\nLength in minutes: {}, ".format((self.end_time - self.start_time).seconds / 60))
            return "".join(text)        

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        error = False
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        while True:
            try:     
                if error:
                    error = False
                    if not self.checkIfBoxIsDead():
                        self.logStepResults("ON DEAD BOX")
                        self.resetSTB()
                        self.rc.startLogs()
                        self.logger.error("resuming test after reboot")                        
                    self.page.cleanDeleteAllRecordings()
                rand = randint(1, 9)
                if rand == 1:
                    rand = randint(5, 10)
                    if not self.goToActiveStandby(rand):
                        error = True
                elif rand == 2:                    
                    item = self.recordPVRfromEPG_current_program(17, 0)
                    if not item:
                        error = True
                        self.page.cleanDeleteAllRecordings()
                    else:
                        self.logger.info("Starting record:\n{}".format(item.get_properties()))
                        self.page.sleep(item.get_record_time_in_seconds() + 60)
                        if not self.watchLastRecordedPVR(item):
                            error = True
                elif rand == 3:
                    rand = randint(10, 20)
                    item = self.recordPVR_instant_record(17, rand)
                    if not item:
                        error = True
                        self.page.cleanDeleteAllRecordings()
                    else:
                        self.logger.info("Starting record:\n{}".format(item.get_properties()))
                        self.page.sleep(item.get_record_time_in_seconds() + 60)
                        if not self.watchLastRecordedPVR(item):
                            error = True
                elif rand == 4:                    
                    rand = randint(10, 20)
                    rand2 = randint(10, 20)
                    item = self.recordPVR_actionScheduleRecord(17, datetime.datetime.now() + datetime.timedelta(minutes=rand), rand2)
                    if not item:
                        error = True
                        self.page.cleanDeleteAllRecordings()
                    else:
                        self.logger.info("Starting record:\n{}".format(item.get_properties()))
                        self.page.sleep(item.get_record_time_in_seconds() + 60)
                        if not self.watchLastRecordedPVR(item):
                            error = True
                elif rand == 5:         
                    rand = randint(1, 4)
                    if not self.browseEPG(rand):
                        error = True
                elif rand == 6:  
                    rand = randint(5, 15)
                    if not self.rentAndWatchVOD_then_go_back(rand):
                        error = True
                elif rand == 7:
                    if not self.goToVODCatalogAndBackToLive():
                        error = True
                elif rand == 8:
                    if not self.playWithTimeShifting(17):
                        error = True
                else:
                    self.logger.info("just sleep")              
                    self.page.sleep(randint(15, 30) * 60)                
                        
                self.logStepResults("after every step")
                self.rc.startLogs()
                        
            except Exception as e:
                self.logger.error("exception: {}".format(e))
                self.logStepResults("on exception")
                self.rc.startLogs()

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
    def checkIfBoxIsDead(self):
        self.logger.info(">>> checkIfBoxIsDead")        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(10)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(10)        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(10)
        if not self.page.findInCssSelectorElement(u"menu".encode('utf-8'), ".breadcrumb .first"):
            return False
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(5)
        return True    
    
    def goToActiveStandby(self, time_in_minutes):
        self.logger.info(">>> goToActiveStandby") 
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(10)
        if not self.page.zapToChannel(17):
            return False
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(5)
        if self.page.checkLive():
            return False        
        self.page.sleep(time_in_minutes * 60)
        self.rc.sendKeys(["KEY_POWER"])
        self.page.sleep(300)
        if not self.page.checkLive():
            return False
        return True           
        
    def recordPVRfromEPG_current_program(self, channel, delay_times):
        self.logger.info(">>> recordPVRfromEPG_current_program")                 
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.goToMenu():
            return False
        if not self.page.actionSelect(Menu.epg):
            return False
        if not self.page.actionSelect(Menu.epgWeek):
            return False
        self.rc.zap(channel)
        time.sleep(10)
        if delay_times:
            self.rc.sendKeys(["KEY_RIGHT"] * delay_times)
        time.sleep(10)
        item = self.page.getInfoFromEpgFocus()
        if not item:
            return False
        self.rc.sendKeys(["KEY_RECORD"])
        rand = randint(5, 15)
        time.sleep(10)
        if not self.page.actionInstantRecord(rand):
            return False        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        return self.Recording(channel, item.start, item.start + datetime.timedelta(minutes=rand))
        
    def recordPVR_instant_record(self, channel, length_in_minutes):  
        self.logger.info(">>> recordPVR_instant_record")      
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.zapToChannel(channel):
            return False
        self.rc.sendKeys(["KEY_RECORD"])
        if not self.page.actionInstantRecord(length_in_minutes):
            return False
        return self.Recording(channel, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(minutes=length_in_minutes))
    
    def recordPVR_actionScheduleRecord(self, channel, start, length_in_minutes): 
        self.logger.info(">>> recordPVR_actionScheduleRecord")             
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.goToPvrMenu():
            return False
        if not self.page.actionSelect(Menu.pvrManualRecord):
            return False
        time.sleep(5)
        if not self.page.actionScheduleRecord(channel, start, length_in_minutes):
            return False
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        return self.Recording(channel, start, start + datetime.timedelta(length_in_minutes))
    
    def browseEPG(self, channel):
        self.logger.info(">>> browseEPG")   
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.goToMenu():
            return False
        if not self.page.actionSelect(Menu.epg):
            return False
        time.sleep(3)
        if not self.page.actionSelect(Menu.epgWeek):
            return False
        time.sleep(10)
        self.rc.zap(channel)
        for i in range(30):
            time.sleep(4)
            rand = randint(1, 4)
            rand2 = randint(1, 4)
            if rand == 1:
                self.rc.sendKeys(["KEY_RIGHT"] * rand2)
            if rand == 2:
                self.rc.sendKeys(["KEY_LEFT"] * rand2)
            if rand == 3:
                self.rc.zap(rand2)      
            if rand == 4:
                self.rc.sendKeys(["KEY_FORWARD"] * rand2)
        
        if not self.page.findInCssSelectorElement(u"teraz".encode('utf-8'), ".breadcrumb .last"):
            return False

        self.rc.sendKeys(["KEY_TV"])
        time.sleep(15) 
        if not self.page.checkLive():
            return False
        return True

    def rentAndWatchVOD_then_go_back(self, time_after_will_go_back_in_minutes): 
        self.logger.info(">>> rentAndWatchVOD_then_go_back")          
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.zapToChannel(17):
            return False
        if not self.page.goToVodCatalog(Menu.vodCatalogWithTestContent):
            return False
        if not self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]):
            return False
        if not self.page.rentVodThenPlay():
            return False
        self.page.sleep(time_after_will_go_back_in_minutes * 30)
        if not self.page.checkLive(True):
            return False
        self.page.sleep(time_after_will_go_back_in_minutes * 30)        
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(15)
        if not self.page.checkLive():
            return False
        return True
    
    def goToVODCatalogAndBackToLive(self): 
        self.logger.info(">>> goToVODCatalogAndBackToLive")                    
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.zapToChannel(17):
            return False
        if not self.page.goToVodCatalog(Menu.vodCatalogWithTestContent):
            return False
        if not self.page.goToVodToRentInCatalog():
            return False
        time.sleep(10)
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(10)
        if not self.page.checkLive():
            return False
        return True
    
    def watchLastRecordedPVR(self, recorded_item):
        self.logger.info(">>> watchLastRecordedPVR")
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.goToPvrMyRecords():
            return False

        time.sleep(10)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        if not self.page.getInfoFromRecordPage():
            return False

        self.rc.sendKeys(["KEY_OK"])        
        time.sleep(60)
        if not self.page.checkLive(True):
            return False
        
        self.page.sleep(recorded_item.get_record_time_in_seconds())
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(10)
        if not self.page.checkLive():
            return False
        return True
        
    def playWithTimeShifting(self, channel):    
        def getRecordTime():
            a = self.page.getInfoFromTrickBar()
            if not a:
                time.sleep(2)
                a = self.page.getInfoFromTrickBar()
            if a != None:
                a = a.getMinutesInSecondRow()
                if type(a) == int:
                    return a
            else:
                return False
        self.logger.info(">>> playWithTimeShifting")                 
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        if not self.page.zapToChannel(channel):
            return False
        self.rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(10)        
        self.rc.sendKeys(["KEY_CHANNELDOWN"])
        time.sleep(30)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(90)
        if not getRecordTime():
            return False
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)
        if not self.page.checkLive():
            return False
        time.sleep(120)
        self.rc.sendKeys(["KEY_REWIND"] * 2)
        time.sleep(30)        
        if not self.page.checkLive():
            return False
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)        
        if not getRecordTime():
            return False        
        self.rc.sendKeys(["KEY_FORWARD"] * 2)
        time.sleep(120)        
        if not self.page.checkLive():
            return False
        
        return True        

    def resetSTB(self):
        self.logger.warning("Hard Reset")
        self.rc.hardReset()
        time.sleep(2)
        try:
            currTime = datetime.datetime.now()
            status = False
            moje = None
            time.sleep(15)
            while (status == False):
                datanow = datetime.datetime.now()
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
