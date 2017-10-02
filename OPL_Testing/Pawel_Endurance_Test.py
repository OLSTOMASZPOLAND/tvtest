# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import datetime
import time
from NewTvTesting.Utils import getReportsDirPath, generateScreenFilePath, \
    generateStbLogFilePath, writeStbLogsToFile, getTcReportFilePath
from NewTvTesting.StbtIntegration import screenshot
from NewTvTesting import ResidentAppPage
import NewTvTesting
from random import randint
from time import sleep
import subprocess
import shlex



class pawel_endurance_test(TC_OPL_template):

#============================================= SET BEGINING PARAMETERS FOR TEST =============================================================
    KANAL_STARTOWY = 266                # Set Start Channel 
    KANAL_KONCOWY = 282                 # Set Ending Channel
    howLong=2                          # TC length in minutes
    lenghtVideo=6                       # video length recording in minutes
    '''TestCaseList ={1: self.changeLanguage,2: self.swichChanel,3: self.timeSchifting,4: self.recordedVideo, 5: self.timeSchiftingPplus, 6: self.goToEpg, 7: self.recordAndCheckVideo} '''
#============================================================================================================================================
#======================================================= RANDOM TEST CASE ===================================================================
    def randomTC (self):     
        TestCaseList ={1: self.changeLanguage,2: self.swichChanel,3: self.timeSchifting,4: self.recordedVideo, 5: self.timeSchiftingPplus, 6: self.goToEpg, 7: self.recordAndCheckVideo}       
#         TestCaseList ={1: self.changeLanguage,2: self.swichChanel,3: self.timeSchifting,4: self.timeSchiftingPplus, 5: self.goToEpg}
#         TestCaseList ={1: self.swichChanel,2: self.goToEpg,3: self.recordAndCheckVideo,4: self.recordedVideo,5: self.changeLanguage,}

        return TestCaseList[randint(1,len(TestCaseList))]       
        
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self): 
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        ''' step '''
          
        countTest=0
        rebootTime=3*60*60  # Reboot time set on 3h
        startTime=time.time() 
        
        while True:

            try:              
                
                
                selectedTestCase=self.randomTC()                                                            # Random Test case            
                self.logger.info("=========== "+ str(selectedTestCase.__name__) +" ===========")            # write title of TC to log
                
                with open("/home/tvtest/testEnv/RANDOM_logs.txt", "a") as text_file:
                    text_file.write("RUN:  %s   timestamp %s  SCENARIO:  %s \n" % (countTest, time.asctime(), str(selectedTestCase.__name__)))
                    text_file.write
                #=================================== Control Screen ===================================
                ''' step '''
                self.logStepBeginning("CONTROL SCREEN")
                   
                self.logger.info("========= Control Screen =========" )
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                self.rc.sendKeys(["KEY_MENU"])
                time.sleep(2) 
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)  
                self.logStepResults("CONTROL SCREEN")
                time.sleep(2)  
                #======================================================================================

                
#                 self.changeLanguage(self.howLong)
#                 self.swichChanel(self.howLong)
#                 self.timeSchifting(self.howLong)
#                 self.timeSchiftingPplus(self.howLong)
#                 self.goToEpg(self.howLong)
#                 self.recordedVideo(self.howLong, self.lenghtVideo)
#                 self.recordAndCheckVideo(self.howLong)
                                  
                                         
                if str(selectedTestCase.__name__)=="recordedVideo":
                    selectedTestCase(self.howLong, self.lenghtVideo)
                else:
                    selectedTestCase(self.howLong)
                    
                if time.time() > (startTime + rebootTime):
                    self.logger.warning("Hard Reset")
                    self.rc.hardReset()
                    screenshot(generateScreenFilePath(self.reportsPath, "HARD RESET"))
                    time.sleep(120)  
                    startTime=time.time()
                else:
                    pass
                
            except Exception, e:
                self.logStepResults("Error occurred - %s" % e)
                self.logger.info("   ERR:   Error occurred - %s" % e)
                
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

#======================================================== TEST CASES FUNCTION ===============================================================
                  
    def changeLanguage(self, howLong):
        '''Implementation
        - Set test case length (default test will be repeated 20 minutes)
        
        - zap to channel HBO
        - Press OK button
        - Press Down button
        - Press Ok Button 
        - Change language to other ( Press down button and then press OK)
        - Wait 10 seconds
        - Press OK button
        - Press Down button
        - Press Down button ( now you are focused on subtitle)
        - Press OK button
        - Change subtitle to other ( Press down  and the press OK button)
        - Wait 10 seconds
        
        - Zap to other channel and repeat all steps
        '''
        timeout = time.time() + 60*howLong                      # set  minutes from now

        while True:
            
            if time.time()<timeout:              
                #=========================================== zap to HBO  HD ===========================================
                try:
                    ''' step 1 '''
                    self.zap("HBO", "changeLanguage",1)
                    #========================================change language===========================================   
                    ''' step 2 '''
                    self.changeNativeLanguage("changeLanguage",2)
                    #========================================change language of subtitle=================================
                    ''' step 3 '''
                    self.changeNativeSubtitle("changeLanguage",3)
                
                except Exception, e:  
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
                #=========================================== zap to HBO 2 HD and repeat step 1 ========================
                try:
                    ''' step 4'''
                    self.zap("HBO2", "changeLanguage",4)
                    #========================================change language===========================================
                    ''' step 5'''
                    self.changeNativeLanguage("changeLanguage",5) 
                    #========================================change language of subtitle=================================
                    ''' step 6'''
                    self.changeNativeSubtitle("changeLanguage",6)
                    
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
                    
            else:
                break
    #========================================================= P+ and P- ===============================================
    def swichChanel(self,howLong):
        '''Implementation
        - Set test case length (default test will be repeated 20 minutes)
        - TEST start from default Channel HBO- ZAP to HBO 
        
        Since now test will be repeated  according to set test case length (default test will be repeated 20 minutes)
        - Watch live
        - Press P+
        - Wait 10 seconds
        - Press P-
        - wait 10 seconds
        '''
        ''' step 1'''
        self.zap("HBO", "swichChanel",1)                                   #ZAP to HBO To start from default parameter
        timeout = time.time() + 60*howLong                                                                          # SET Test Case Length - minutes from now
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
        time.sleep(10)
        
        while True:
            try:
                if time.time()<timeout:
                    ''' step 2'''
                    self.logStepBeginning("step 2 -swichChanel-CHANNELUP")
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    time.sleep(3)
                    self.logStepResults("step 2 -swichChanel-CHANNELUP")
                    
                    
                    ''' step 3'''
                    self.logStepBeginning("step 3 -swichChanel-CHANNELDOWN")
                    self.rc.sendKeys(["KEY_CHANNELDOWN"])
                    time.sleep(3)
                    self.logStepResults("step 3 -swichChanel-CHANNELDOWN")
                else:
                    break
            except Exception, e:
                self.logStepResults("Error occurred - %s" % e)
                self.logger.info("   ERR:   Error occurred - %s" % e)
                         
    #========================================= TIME SHIFTING ==========================================================               
    def timeSchifting (self,howLong):
        '''Implementation
        - Set test case length (default test will be repeated 20 minutes)
        - Zap to channel HBO
        - Press Play button
        - Live is paused - Wait 70 seconds
        - Press Play button ( now paused video is played)
        - Wait 10 seconds
        - Press Menu
        - Press P+            (back to live)
        - Wait 10 seconds
        - Zap to other channel
        - Repeat all step for new channel
        '''
        timeout = time.time() + 60*howLong                       #  minutes from now
        
        while True:
            if time.time()<timeout:
                #===================================== ZAP to HBO 1 HD ===============      
                try:
                    ''' step 1 '''
                    self.zap("HBO", "timeSchifting",1) 
                    
                    ''' step 2 '''
                    self.pause70play("timeSchifting", 2)
                    
                    ''' step 4 '''
                    self.logStepBeginning("step 4 -timeSchifting- BACK TO LIVE TV ")
                    
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    time.sleep(4)
                    self.logStepResults("step 4 -timeSchifting- BACK TO LIVE TV ")
                    time.sleep(6)                   
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)

                #===================================== ZAP to HBO 2 HD ===============      
                try:
                    ''' step 5 '''
                    self.zap("HBO2", "timeSchifting",5)
                    
                    ''' step 6 '''
                    self.pause70play("timeSchifting", 6)
                    
                    ''' step 8 '''
                    self.logStepBeginning("step 8 -timeSchifting- BACK TO LIVE TV ")
                    
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    time.sleep(4)
                    self.logStepResults("step 8 -timeSchifting- BACK TO LIVE TV ")
                    time.sleep(6)                     
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
        
            else:
                break

    #=======================================================================================================================================
    #=============Record video-> during active recording video go to 'My Recors'-> start watching PVR-> change Language=====================
    #=============Change Subtitle-> go to Live-> Start Time schiftig-> PLAY time schift-> go to Live-> End recording->ZAP HBO2==============
    #=======================================================================================================================================
    def recordedVideo(self, howLong, lenghtVideo):
        '''Implementation
        - Set test case length (default test will be repeated 20 minutes)
        - Zap to channel
        - Press REC button
        - Wait until pop up occurs and  when the pop up occurs set recording time ( default recording time in test is set on 7 minutes )
        - Wait 40 seconds
        - Press Key MENU
        - Select PVR ("nagrywarka")
        - Press OK ( go to 'my record')
        - Press OK (chose current recording video)
        - Press OK ( PvrPLAY- watch current recording video)
        - Wait 30 seconds
        - Press OK
        - Press Down (chose Language )
        - Press OK (change language  to other - press key down and then OK)
        - Wait 10 second
        - Press OK button
        - Press Down button
        - Press Down button ( now you are focused on subtitle)
        - Press OK button
        - Change subtitle to other ( Press down  and the press OK button)
        - Wait 20 seconds
        - Press Back button
        - Press Back button
        - Press TV button
        - Press Play button
        - Live is paused - Wait 70 seconds - this case is depended from frimware. current firmware not allow to perform timeshifting during PVR
        - Press Play button ( now paused video is played)
        - Wait 30 seconds
        - Press menu button
        - Press P+
        - Wait until Recording video end
        - Zap to other channel
        - Repeat step for other channel
        '''
        
        timeout = time.time() + 60*howLong
        while True:
            if time.time()<timeout:
                try:
                    ''' step 1'''
                    self.zap("HBO", "recordedVideo",1)

                    ''' step 2'''
                    self.logStepBeginning("step 2 -recordedVideo- START RECORDING VIDEO")
                    
                    time.sleep(4)
                    self.logger.info(" Start Recording Video")
                    self.rc.sendKeys(["KEY_RECORD"])
                    #============================= count time since start video=======================
                    currentDate = time.time()                    
                    time.sleep(10)
                    checkProblems=self.page.actionInstantRecord(lenghtVideo)
                    if (checkProblems==False):
                        self.logger.info("Something go wrong Error Occurs")
                        self.logger.info("Probably problem with hard drive or POP UP was not displayed")
                        self.logger.info("FINISH SCENARIO")
                        break 
                    
                    else:
                        pass
                    
                    
                    time.sleep(2)
                    self.logStepResults("step 2 -recordedVideo- START RECORDING VIDEO")
                    
                    ''' step 3'''
                    self.logStepBeginning("step 3 -recordedVideo-SELECT MyPVR START WATCH CURRENT RECORDING VIDEO")
                    #NewTvTesting.ResidentAppPage.WebKitPage.actionInstantRecord(self.page,lenghtVideo)
                    time.sleep(30)
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(2)
                    self.page.actionSelect(Menu.pvr)                  
                    time.sleep(2)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 3-1 TC_RECORDED_VIDEO Open MENU PVR"))
                    self.page.actionSelect(Menu.pvrMyRecords)
                    time.sleep(70)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 3-2 TC_RECORDED_VIDEO Open MY PVR"))
                    self.rc.sendKeys(["KEY_OK"])
                    time.sleep(5)
                    self.logger.info("Open Menu->MyRecord->Current recording Video ")
                    screenshot(generateScreenFilePath(self.reportsPath, "step 3-3 TC_RECORDED_VIDEO Open Menu_MyRecord_Current_recording_Video"))
                    self.page.actionSelect(Menu.pvrPlay)
                    time.sleep(15)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 3-4 TC_RECORDED_VIDEO Open Menu_MyRecord_Current_recording_Video"))
                    time.sleep(15)
                    self.logStepResults("step 3 -recordedVideo-SELECT MyPVR START WATCH CURRENT RECORDING VIDEO")
                    #============================= Language change ===================================
                    ''' step 4'''
                    self.changeNativeLanguage("recordedVideo", 4)
                    #============================= Subtitle change ===================================
                    ''' step 5'''
                    self.changeNativeSubtitle("recordedVideo", 5)
                    #============================= Time shifting ==================================== 
                    ''' step 6'''
                    self.logStepBeginning("step 6 -recordedVideo- TIMESHIFT BACK BACK TV")
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                    time.sleep(5)
                    self.logStepResults("step 6 -recordedVideo- TIMESHIFT BACK BACK TV")
                    
                    self.pause70play("recordedVideo", 6)
                      
                    ''' step 8'''
                    self.logStepBeginning("step 8 -recordedVideo- TIMESHIFT BACK TO LIVE TV")
                    
                    time.sleep(15)
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(3)
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    self.logger.info("End Timeshifting")
                    self.logStepResults("step 8 -recordedVideo- TIMESHIFT BACK TO LIVE TV")

                    while True:
                        if (time.time()<currentDate+(60*lenghtVideo)+10):
                            time.sleep(30)
                        else:
                            break

                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
                    
                finally:  
                    try:
                        self.logger.info("----------- cleaning -----------")
                        self.logger.info("-----------Delete Planned and Current recording PVR -----------")
                        self.page.cleanDeleteAllRecordings() 
                        time.sleep(2)
                    except Exception, e:
                        self.logStepResults("Error occurred - %s" % e)
                        self.logger.info("   ERR:   Error occurred - %s" % e)

                #============================================ the same for HBO 2 ==========================================
                try:
                    ''' step 9'''
                    self.zap("HBO2", "recordedVideo",9)

                    ''' step 10'''
                    self.logStepBeginning("step 10 -recordedVideo- START RECORDING VIDEO")
                    
                    time.sleep(2)
                    self.logger.info(" Start Recording Video")
                    self.rc.sendKeys(["KEY_RECORD"])
                    #============================= count time since start video=======================
                    currentDate = time.time()                    
                    time.sleep(10)
                    
                    checkProblems=self.page.actionInstantRecord(lenghtVideo)
                    
                    if (checkProblems==False):
                        self.logger.info("Something go wrong Error Occurs")
                        self.logger.info("Probably problem with hard drive or POP UP was not displayed")
                        self.logger.info("FINISH SCENARIO")
                        break 
                    else:
                        pass

                    time.sleep(2)
                    self.logStepResults("step 10 -recordedVideo- START RECORDING VIDEO")
                    
                    ''' step 11'''
                    self.logStepBeginning("step 11 -recordedVideo-SELECT MyPVR START WATCH CURRENT RECORDING VIDEO")
                    #NewTvTesting.ResidentAppPage.WebKitPage.actionInstantRecord(self.page,lenghtVideo)
                    time.sleep(30)
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(2)
                    self.page.actionSelect(Menu.pvr)                  
                    time.sleep(2)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 11-1TC_RECORDED_VIDEO Open MENU PVR"))
                    self.page.actionSelect(Menu.pvrMyRecords)
                    time.sleep(70)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 11-2TC_RECORDED_VIDEO Open MY PVR"))
                    self.rc.sendKeys(["KEY_OK"])
                    time.sleep(5)
                    self.logger.info("Open Menu->MyRecord->Current recording Video ")
                    screenshot(generateScreenFilePath(self.reportsPath, "step 11-3 TC_RECORDED_VIDEO Open Menu_MyRecord_Current_recording_Video"))
                    self.page.actionSelect(Menu.pvrPlay)
                    time.sleep(15)
                    screenshot(generateScreenFilePath(self.reportsPath, "step 11-4 TC_RECORDED_VIDEO Open Menu_MyRecord_Current_recording_Video"))
                    time.sleep(15)
                    self.logStepResults("step 11 -recordedVideo-SELECT MyPVR START WATCH CURRENT RECORDING VIDEO")
                    #============================= Language change ===================================
                    ''' step 12'''
                    self.changeNativeLanguage("recordedVideo", 12)
                    #============================= Subtitle change ===================================
                    ''' step 13'''
                    self.changeNativeSubtitle("recordedVideo", 13)
                    #============================= Time shifting ====================================
                    ''' step 14'''
                    self.logStepBeginning("step 14 -recordedVideo- TIMESHIFT BACK BACK TV")
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                    time.sleep(5)
                    self.logStepResults("step 14 -recordedVideo- TIMESHIFT BACK BACK TV")
                    
                    self.pause70play("recordedVideo", 14)
                    
                    ''' step 16'''
                    self.logStepBeginning("step 16 -recordedVideo- TIMESHIFT BACK TO LIVE TV")
                    
                    time.sleep(15)
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(3)
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    self.logger.info("End Timeshifting")
                    self.logStepResults("step 16 -recordedVideo- TIMESHIFT BACK TO LIVE TV")

                    while True:
                        if (time.time()<currentDate+(60*lenghtVideo)+10):
                            time.sleep(30)
                        else:
                            break

                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
                    
                finally:  
                    try:
                        self.logger.info("----------- cleaning -----------")
                        self.logger.info("-----------Delete Planned and Current recording PVR -----------")
                        self.page.cleanDeleteAllRecordings() 
                        time.sleep(2)
                    except Exception, e:
                        self.logStepResults("Error occurred - %s" % e)
                        self.logger.info("   ERR:   Error occurred - %s" % e)
                    
            else:
                break
    
    def checkNumberOfPlannedPvr(self):
            # check planned recording
        try:    
            self.page.driver.get(Rpi.DUMP)
            info = self.page.driver.find_elements_by_css_selector('html body div#pvrMenu.scene.whiteBg.pvrMenu div.dockCenter div.help.shadow div.text')
            
            info = info[0].text.encode('utf-8')
            info = info.split('\n')
            info = info[0]
            info = info.split(' ')
            info = info[3]
            info = int(info)
            return info
        except Exception, e:
            self.logger.info("   ERR:   Error occurred - %s" % e)
            return False
            
    def recordAndCheckVideo(self,howLong):
        ''' Press Play button
        - Implementation
        - ZAP HBO
        - Press Menu 
        - Select option (recorder -PVR menu)
        - Focus on MY PVR check number of PVR
        - Select Planned PVR
        - Press Back ( now you are focused on Planned PVR)
        - Check number of Planned PVR
        - If any PVR is planned delete all Planned PVR
        - If number of PVR is less than 20 record 5  minutes video. Record 5 minutes video until summary number of PVR will be 20
        - Start live
        =======Since now test will be repeated during next 20 minutes=======
        - Press Menu 
        - Select option (recorder -PVR menu)
        - Select option My PVR
        - Count how long time the page is loading
        - Press key Back
        - Repeat steps
        '''
        try:
            
            ''' step 1'''           
            self.zap("HBO", "recordAndCheckVideo",1)
            
            ''' step 2'''
            self.logStepBeginning("step 2 -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PVR")
            
            checkProblems=self.page.goToPvrMenu()
            if (checkProblems==False):
                self.logger.info("step 2 -recordAndCheckVideo-GO TO PVR PROBLEM OCCURS END loop")
                return 
            
            
            time.sleep(2)        
            NumOfPvr=self.page.checkNumberOfPvr()
            self.logger.info("Number of PVR "+ str(NumOfPvr))
            self.logStepResults("step 2 -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PVR")
                     
            ''' step 3'''
            self.logStepBeginning("step 3 -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PLANNED PVR")  
                  
            self.page.actionSelect(Menu.pvrMyScheduled)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)
            NumOfPlannedPvr=self.checkNumberOfPlannedPvr()
            self.logger.info("Number of planned PVR "+ str(NumOfPlannedPvr))
            self.logStepResults("step 3 -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PLANNED PVR")
            

            if (NumOfPlannedPvr>0):
                
                ''' step '''
                self.logStepBeginning("step 4 -recordAndCheckVideo-DELETE ALL PLANNED PVR")  
                
                self.logger.info("-----------Delete Planned and Current recording PVR -----------")
                self.page.cleanDeleteAllRecordings() 
                self.logStepResults("step  4 -recordAndCheckVideo-DELETE ALL PLANNED PVR")

            else:
                time.sleep(1)         
            #============================================== NumOfPvr or NumOfPlannedPvr == FALSE Repeat step===========================
            if (str(NumOfPvr)==False):
                ''' step 2 REPEATED'''
                self.logStepBeginning("step 2 REPEATED -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PVR")
                
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                time.sleep(2) 
                checkProblems=self.page.goToPvrMenu()
                if (checkProblems==False):
                    self.logger.info("step 2 -recordAndCheckVideo-GO TO PVR PROBLEM OCCURS END loop")
                    return 
                
                time.sleep(2)        
                NumOfPvr=self.page.checkNumberOfPvr()
                self.logger.info("Number of PVR "+ str(NumOfPvr))
                self.logStepResults("step 2 REPEATED -recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PVR")
           
            elif (str(NumOfPlannedPvr)==False):
                ''' step 3 REPEATED'''
                self.logStepBeginning("step 3 REPEATED-recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PLANNED PVR")  
                
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                time.sleep(2)    
                checkProblems=self.page.goToPvrMenu()
                
                if (checkProblems==False):
                    self.logger.info("step 3 -recordAndCheckVideo-GO TO PVR PROBLEM OCCURS END loop")
                    return 
                time.sleep(2)                      
                self.page.actionSelect(Menu.pvrMyScheduled)
                self.rc.sendKeys(["KEY_BACK"])
                time.sleep(4)
                NumOfPlannedPvr=self.checkNumberOfPlannedPvr()
                self.logger.info("Number of planned PVR "+ str(NumOfPlannedPvr))
                self.logStepResults("step 3 REPEATED-recordAndCheckVideo-GO TO PVR MENU AND CHECK NUMBER OF PLANNED PVR")
            
            else:
                pass
            #======================================================================================================================
            if (str(NumOfPvr)==False) or (str(NumOfPlannedPvr)==False):
                self.logger.info("Number of PVR "+ str(NumOfPvr))
                self.logger.info("Number of PLANNED PVR "+ str(NumOfPlannedPvr))
                self.logger.info("ONE OF VALUE IS FALSE- Program wrong read these value or lost connection with box")
                return
            else:
                pass
            
            
            if (NumOfPvr<20):

                for i in range(20-NumOfPvr):
                    
                    ''' step '''
                    self.logStepBeginning("step  -recordAndCheckVideo-RECORD 5 MINUTE VIDEO TO FILL LIST PVR TO 20")
                    
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
                    time.sleep(3)
                    self.rc.sendKeys(["KEY_RECORD"])
                    time.sleep(10)
                    #NewTvTesting.ResidentAppPage.WebKitPage.actionInstantRecord(self.page,5)                    #RECORD 5 MINUTE pvr
                    self.page.actionInstantRecord(5)
                    screenshot(generateScreenFilePath(self.reportsPath, "TC_RECORD_AND_CHECK_VIDEO RECORD  5 MINUTE PVR"))
                    time.sleep(6*60)
                    i=i+1                    
                    self.logStepResults("step  -recordAndCheckVideo-RECORD 5 MINUTE VIDEO TO FILL LIST PVR TO 20")
            else:
                
                timeout = time.time() + 60*howLong                                                                   #  minutes from now

                ''' step 5'''
                self.logStepBeginning("step 5  -recordAndCheckVideo-GO TO PVR")
                    
                checkProblems=self.page.goToPvrMenu()
                if (checkProblems==False):
                    self.logger.info("step 5 -recordAndCheckVideo-GO TO PVR PROBLEM OCCURS END loop")
                    return 
                
                
                self.logStepResults("step 5  -recordAndCheckVideo-GO TO PVR")
                
                while True:
                    if time.time()<timeout:
                        checkTime=time.time()
                        
                        ''' step 6'''
                        self.logStepBeginning("step 6  -recordAndCheckVideo-GO TO PVR LIST MOSAIC COUNT TIME")
                        
                        
                        self.rc.sendKeys(["KEY_OK"])
                        
                        while True:                                        
                            self.page.driver.get(Rpi.DUMP)
                            info = self.page.driver.find_elements_by_css_selector('html body div.scene.whiteBg.recordMosaic div.pvrMosaic.recordMosaic div.itemsContainer div#item0.item.focused')
                            
                            if len(info) !=0:
                                checkTime=time.time()-checkTime
                                self.logger.info("Loaded Page with video in time [s] "+ str(checkTime)) #get dump average takes 2 seconds
                                screenshot(generateScreenFilePath(self.reportsPath, "step 6  -recordAndCheckVideo-GO TO PVR LIST MOSAIC COUNT TIME"))
                                break
                            else:
                                self.logger.info("Page with recorded video not loaded yet ")
       
                        print checkTime

                        self.rc.sendKeys(["KEY_BACK"])
                        self.logStepResults("step 6  -recordAndCheckVideo-GO TO PVR LIST MOSAIC COUNT TIME")
                    else:
                        break
                        
        except Exception, e:
                self.logStepResults("Error occurred - %s" % e)
                self.logger.info("   ERR:   Error occurred - %s" % e)
                
        finally:
            
            try:
                self.logger.info("----------- cleaning -----------")
                self.logger.info("-----------Delete Planned and Current recording PVR -----------")
                self.page.cleanDeleteAllRecordings() 
                time.sleep(2)  
            except Exception, e:
                self.logStepResults("Error occurred - %s" % e)
                self.logger.info("   ERR:   Error occurred - %s" % e)
            

    def goToEpg (self, howLong):
        
        ''' IMPLEMENTATION
         ZAP to HBO
        
        - Press Menu 
        - Select EPG
        - Select EPG Now
        - Wait 15 seconds
        - Press P+ to come back to live
        - Wait 30 seconds
        - Press P+ to change channel
        - Press Menu 
        - Select EPG
        - Select EPG Now
        - Wait 15 seconds
        - Press P+ to come back to live
        - Wait 30 seconds
        - Press P-
        - Repeat all step
        '''

        ''' step 1'''
        self.zap("HBO", "goToEpg",1)

        timeout = time.time() + 60*howLong
        while True:
            if time.time()<timeout:
                try:
                    ''' step 2'''
                    self.logStepBeginning("step 2 -goToEpg-CHOSE EPG MENU- CHOSE NOW")
                                          
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(6)
                    
                    self.page.actionSelect(Menu.epg)  #chose EPG menu
                    time.sleep(3)
                    screenshot(generateScreenFilePath(self.reportsPath, "goToEpg-CHOSE EPG MENU- CHOSE MENU"))
                    time.sleep(2)
                    self.page.actionSelect(Menu.epgWeek) #chose now 'teraz'
                    time.sleep(3)
                    self.logStepResults("step 2 -goToEpg-CHOSE EPG MENU- CHOSE NOW")
                    
                    ''' step 3'''
                    self.logStepBeginning("step 3 -goToEpg-COME BACK TO LIVE AND CHANNEL UP")
                    
                    time.sleep(10)
                    self.rc.sendKeys(["KEY_CHANNELUP"]) # come back to live
                    time.sleep(30) 
                    self.logger.info("PRESS P+")
                    self.rc.sendKeys(["KEY_CHANNELUP"]) #change channel up P+
                    time.sleep(3)
                    self.logStepResults("step 3 -goToEpg-COME BACK TO LIVE AND CHANNEL UP")
                    
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)

                try:
                    ''' step 4'''
                    self.logStepBeginning("step 4 -goToEpg-CHOSE EPG MENU- CHOSE NOW")
                    
                    self.rc.sendKeys(["KEY_MENU"])
                    time.sleep(6)
                    self.page.actionSelect(Menu.epg)  #chose EPG menu
                    time.sleep(3)
                    screenshot(generateScreenFilePath(self.reportsPath, "goToEpg-CHOSE EPG MENU- CHOSE MENU"))
                    
                    time.sleep(2)
                    self.page.actionSelect(Menu.epgWeek) #chose now 'teraz'
                    time.sleep(3)
                    self.logStepResults("step 4 -goToEpg-CHOSE EPG MENU- CHOSE NOW")
                    
                    ''' step 5'''
                    self.logStepBeginning("step 5 -goToEpg-COME BACK TO LIVE AND CHANNEL DOWN")
                    
                    time.sleep(10)
                    self.logger.info("Back to LIVE")
                    self.rc.sendKeys(["KEY_CHANNELUP"]) # come back to live
                    time.sleep(30) 
                    self.logger.info("PRESS P-")
                    self.rc.sendKeys(["KEY_CHANNELDOWN"]) #change channel up P-
                    time.sleep(6) 
                    self.logStepResults("step 5 -goToEpg-COME BACK TO LIVE AND CHANNEL DOWN")
                    
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)

            else:
                break 
            
    def timeSchiftingPplus (self,howLong):
        '''Implementation
        - Set test case length (default test will be repeated 20 minutes)
        - Zap to channel
        - Press Play button
        - Live is paused - Wait 70 seconds
        - Press Play button ( now paused video is played)
        - Press P+
        - Repeat all step for new channel
        '''
        
        timeout = time.time() + 60*howLong                       #  minutes from now
        
        ''' step 1'''
        self.zap("HBO", "timeSchiftingPplus",1)
        
        while True:
            if time.time()<timeout:
                #===================================== ZAP to CHANNEL ===============      

                try:
                    ''' step 2'''
                    time.sleep(10)
                    self.pause70play("timeSchiftingPplus", 2)
                    
                    
                    ''' step 4'''
                    self.logStepBeginning("step 4 -timeSchiftingPplus-Watch during 20seconds timeshifting")
                    time.sleep(20)
                    self.logStepResults("step 4 -timeSchiftingPplus-Watch during 20seconds timeshifting")
                  
                    
                    ''' step 5'''
                    self.logStepBeginning("step 5 -timeSchiftingPplus-CHANNEL UP")
                    
                    time.sleep(10)
                    self.logger.info("PRESS P+")
                    self.rc.sendKeys(["KEY_CHANNELUP"])
                    time.sleep(8)
                    self.logStepResults("step 4 -timeSchiftingPplus-CHANNEL UP")
                    time.sleep(2)
                   
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)

                #===================================== ZAP TO P+ CHANNEL ========================================      
                try:
                    ''' step 6'''
                    time.sleep(10)
                    self.pause70play("timeSchiftingPplus", 6)
  
                    ''' step 8'''
                    self.logStepBeginning("step 8 -timeSchiftingPplus-Watch during 20seconds timeshifting")
                    time.sleep(20)
                    self.logStepResults("step 8 -timeSchiftingPplus-Watch during 20seconds timeshifting")

                    ''' step 9'''
                    self.logStepBeginning("step 9 -timeSchiftingPplus-CHANNEL DOWN")
                    
                    time.sleep(10) 
                    self.logger.info("PRESS P-")
                    self.rc.sendKeys(["KEY_CHANNELDOWN"])
                    time.sleep(8)
                    self.logStepResults("step 9 -timeSchiftingPplus-CHANNEL DOWN")
                    time.sleep(2)
                              
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
           
            else:
                break
                      
    def pvrTimeshifting(self, howLong, lenghtVideo):
        
        timeout = time.time() + 60*howLong                       #  minutes from now
        ''' step 1'''
        self.logStepBeginning("step 1 -pvrTimeshifting-BEGIN- ZAP HBO")
        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])   
        checkZaping=self.page.zapToChannel(self.rc.getChannelHBOHD)             
        self.logStepResults("step 1 -pvrTimeshifting-BEGIN- ZAP HBO")
        
        while True:
            if time.time()<timeout:  

                try:
                    ''' step 2'''
                    self.logStepBeginning("step 2 -pvrTimeshifting-START RECORDING VIDEO")
                    time.sleep(2)
                    self.logger.info(" Start Recording Video")
                    self.rc.sendKeys(["KEY_RECORD"])
                    time.sleep(10)
                    checkProblems=self.page.actionInstantRecord(lenghtVideo)
                    if (checkProblems==False):
                        self.logger.info("Something go wrong Error Occurs")
                        self.logger.info("Probably problem with hard drive or POP UP was not displayed")
                        self.logger.info("FINISH SCENARIO")
                        break 
                    
                    else:
                        pass
                 
                    time.sleep(2)
                    currentDate = time.time()   
                    self.logStepResults("step 2 -pvrTimeshifting-START RECORDING VIDEO")
                    
                    ''' step 3'''
                    self.logStepBeginning("step 3 -pvrTimeshifting-WAIT AND START TIMESHIFTING")
                    
                    self.logger.info(" Wait 1 minute and Start Timeshift")
                    time.sleep(60)
                    self.logger.info(" Start Timeshifting - PAUSE LIVE TV")
                    self.rc.sendKeys(["KEY_PLAY"])
                    time.sleep(10)
                    screenshot(generateScreenFilePath(self.reportsPath, "TC_PVRTIMESHIFTING - PAUSE LIVE TV"))
                    
                    time.sleep(60)
                    
                    self.logStepResults("step 3 -pvrTimeshifting-WAIT AND START TIMESHIFTING")
                    
                    ''' step 4'''
                    self.logStepBeginning("step 4 -pvrTimeshifting-END TIMESHIFTING")
                    
                    self.logger.info(" END Timeshifting - PLAY PAUSE LIVE TV")
                    self.rc.sendKeys(["KEY_PLAY"])
                    time.sleep(10)
                    self.logStepResults("step 4 -pvrTimeshifting-END TIMESHIFTING")
                    
                    
                    ''' step 5'''
                    self.logStepBeginning("step 5 -pvrTimeshifting-END RECORDING")
                    while True:
                        if (time.time()<currentDate+(60*lenghtVideo)+10):
                            time.sleep(30)
                        else:
                            break
                    self.logStepResults("step 5 -pvrTimeshifting-END RECORDING")
                    
                except Exception, e:
                    self.logStepResults("Error occurred - %s" % e)
                    self.logger.info("   ERR:   Error occurred - %s" % e)
                    
                finally:  
                    try:
                        self.logger.info("----------- cleaning -----------")
                        self.logger.info("-----------Delete Planned and Current recording PVR -----------")
                        self.page.cleanDeleteAllRecordings()                                        #Function delete all future and ongoing record in My Records
                        time.sleep(2)
                    except Exception, e:
                        self.logStepResults("Error occurred - %s" % e)
                        self.logger.info("   ERR:   Error occurred - %s" % e)
            
            else:
                break           # End function when timeout occurs  
            

    def zap(self, channelName, scenarioName,step):
        
        if (channelName=="HBO"):
            ''' step 1'''
            self.logStepBeginning("step %s -%s-BEGIN - ZAP %s" % (step,scenarioName,channelName))
            
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
            time.sleep(4)
            checkZaping=self.page.zapToChannel(self.rc.getChannelHBOHD)                   
            time.sleep(2)      
            self.logStepResults("step %s -%s-BEGIN - ZAP %s" % (step,scenarioName,channelName))
        
        elif (channelName=="HBO2"):
            ''' step 1'''
            self.logStepBeginning("step %s -%s-BEGIN - ZAP %s" % (step,scenarioName,channelName))
            
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
            time.sleep(4)
            checkZaping=self.page.zapToChannel(self.rc.getChannelHBO2HD)                   
            time.sleep(2)      
            self.logStepResults("step %s -%s-BEGIN - ZAP %s" % (step,scenarioName,channelName))
        else:
            self.logger.info(" UNKNOWN ZAP CHANNEL NAME -ZAP TO HBO")
            
            ''' step 1'''
            self.logStepBeginning("step %s -%s-BEGIN - ZAP HBO" % (step,scenarioName))
            
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK","KEY_TV"])
            time.sleep(4)
            checkZaping=self.page.zapToChannel(self.rc.getChannelHBOHD)                   
            time.sleep(2)      
            self.logStepResults("step %s -%s-BEGIN - ZAP HBO" % (step,scenarioName))
            
    def changeNativeLanguage(self,scenarioName, step):
        
        ''' step 2 '''
        self.logStepBeginning("step %s -%s-CHANGE NATIVE SOUNDTRACK " % (step,scenarioName))

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)  
        checkLanguage=self.page.actionSelect(Menu.toolboxNativeSoundtrack)
        
        if checkLanguage==False:
            self.logger.info("Not find Native sound track change it manually")
            time.sleep(16) 
            self.rc.sendKeys(["KEY_OK"])    # one more time open wucik MENU 'OK'
            time.sleep(4) 
           
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            screenshot(generateScreenFilePath(self.reportsPath, "%s TC_CHANGE_LANGUAGE change sound track manually" % scenarioName))
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
        else:
            self.logger.info("Change native sound track to other")
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            screenshot(generateScreenFilePath(self.reportsPath, "%s TC_CHANGE_LANGUAGE change sound track automatically" % scenarioName))
            self.rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        self.logStepResults("step %s -%s-CHANGE NATIVE SOUNDTRACK "  % (step, scenarioName))

    def changeNativeSubtitle(self,scenarioName,step):
        ''' step 3 '''
        self.logStepBeginning("step %s -%s - CHANGE NATIVE SUBTITLE" % (step, scenarioName))

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)                    
        checkSubtitles=self.page.actionSelect(Menu.toolboxNoSubtitleLong)
        
        if checkSubtitles==False :
            
            time.sleep(16) 
            self.rc.sendKeys(["KEY_OK"])    # one more time open quick MENU 'OK'
            time.sleep(4) 
           
            self.logger.info("Not find Native subtitle change it manually")
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)

            self.rc.sendKeys(["KEY_OK"])
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            screenshot(generateScreenFilePath(self.reportsPath, "%s TC_CHANGE_LANGUAGE change subtitle manually" % scenarioName))
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])     
        else:
            self.logger.info("Change native subtitle to other")
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            screenshot(generateScreenFilePath(self.reportsPath, "%s TC_CHANGE_LANGUAGE change subtitle automatically" % scenarioName))
            self.rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        self.logStepResults("step %s -%s - CHANGE NATIVE SUBTITLE" % (step, scenarioName))
        
        
    def pause70play(self,scenarioName,step):
        
        ''' step 2 '''
        self.logStepBeginning("step %s -%s- PAUSE TV " % (step,scenarioName))
        
        time.sleep(2)
        self.rc.sendKeys(["KEY_PLAY"])                                  #pause
        self.logger.info("Pause the Live video")
        self.logger.info("====== Waiting 70sec... ======")
        time.sleep(30)
        self.logStepResults("step %s -%s- PAUSE TV " % (step,scenarioName))
        step=step+1
        ''' step 3 '''
        self.logStepBeginning("step %s -%s- PLAY PAUSED TV" % (step,scenarioName))
        
        time.sleep(40)  
        self.rc.sendKeys(["KEY_PLAY"])                                 #play
        self.logger.info("Start pasued video-->time shift")
        time.sleep(10)
        self.logStepResults("step %s -%s- PLAY PAUSED TV" % (step,scenarioName))
        
