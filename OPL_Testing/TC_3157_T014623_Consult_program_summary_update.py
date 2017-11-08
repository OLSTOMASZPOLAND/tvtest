# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_3157_T014623_Consult_program_summary_update(TC_OPL_template):

    """Implementation of the HP QC test ID - TC_3157_T014623_Consult_program_summary_update
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)  # wait a while, let the EPG load

        
        ''' step '''
        self.logStepBeginning("STEP 1 - Go To EPG all program channels")     

        self.rc.sendKeys(["KEY_BACK"]) 
        time.sleep(1)       
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(1)
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelHBOHD), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        self.rc.sendKeys(["KEY_GREEN"]) 
        time.sleep(1) 
        self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        time.sleep(1)
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), 'ERRPR IN GO TO EPG  Channels') 
        time.sleep(1)
        self.assertTrue(self.page.checkIfEpgIsAvalaible(), '>> ERROR  lack of EPG')
        self.logStepResults("STEP 1 - Go To EPG all program channels")
        
        ''' step '''
        self.logStepBeginning("STEP 2 -check epg list  ")
        self.rc.sendKeys(["KEY_ok"])
        time.sleep(5)
        self.assertTrue(self.page.findInList(Menu.epgPlay))
        time.sleep(1)
        self.assertTrue(self.page.findInList(Menu.epgRecord))
        time.sleep(1)
        self.assertTrue(self.page.findInList(Menu.toolboxSummary))
        time.sleep(1)
        self.logStepResults("STEP 2 - check epg list")
        ''' step '''
        self.logStepBeginning("STEP 3 -check details  ")
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            day = self.page.driver.find_element_by_xpath(".//*[@id='rpitest_pgm_start_date']")
            day = day.text.encode('utf-8')
            hourEnd = self.page.driver.find_element_by_xpath(".//*[@id='rpitest_pgm_end_time']")
            hourEnd = hourEnd.text.encode('utf-8')
            hourStart = self.page.driver.find_element_by_xpath(".//*[@id='rpitest_pgm_start_time']")
            hourStart = hourStart.text.encode('utf-8')
            title = self.page.driver.find_element_by_xpath("html/body/div[8]/div[4]/div[5]/div[1]")
            title = title.text.encode('utf-8') 
            type = self.page.driver.find_element_by_xpath("html/body/div[8]/div[4]/div[5]/div[2]/div/div[1]")
            type = type.text.encode('utf-8')  
            CountryYear = self.page.driver.find_element_by_xpath("html/body/div[8]/div[4]/div[5]/div[2]/div/div[2]")
            CountryYear = CountryYear.text.encode('utf-8')
            actors = self.page.driver.find_element_by_xpath("html/body/div[8]/div[4]/div[5]/div[2]/div/div[4]")
            actors = actors.text.encode('utf-8')   
            summary = self.page.driver.find_element_by_xpath("html/body/div[8]/div[4]/div[5]/div[2]/div/div[5]")
            summary = summary.text.encode('utf-8')          
            
        except:
            self.assertTrue(False, "ERR: No description on epg")

        if (len(day)==0):
            self.assertFalse(False, "ERR: No date of program")
        if (len(hourEnd)==0):
            self.assertFalse(False, "ERR: No end time of program")
        if (len(hourStart)==0):
            self.assertFalse(False, "ERR: No start time of program")            
        if (len(title)==0):
            self.assertFalse(False, "ERR: No title of program")            
        if (len(type)==0):
            self.assertFalse(False, "ERR: No type of program")
        if (len(CountryYear)==0):
            self.assertFalse(False, "ERR: No year and caountry of program")            
        if (len(actors)==0):
            self.assertFalse(False, "ERR: No actors of program")            
        if (len(summary)==0):
            self.assertFalse(False, "ERR: No summary of program")
        
        self.logger.info("----------- "+day +" -----------")
        self.logger.info("----------- "+hourEnd +" -----------")
        self.logger.info("----------- "+hourStart +" -----------")
        self.logger.info("----------- "+title +" -----------")
        self.logger.info("----------- "+type +" -----------")
        self.logger.info("----------- "+CountryYear +" -----------")
        self.logger.info("----------- "+actors +" -----------")
        self.logger.info("----------- "+summary +" -----------")

        
        self.logStepResults("STEP 3 - check details")
                

            
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        
