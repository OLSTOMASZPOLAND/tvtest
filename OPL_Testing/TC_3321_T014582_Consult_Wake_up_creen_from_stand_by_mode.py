# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return
from datetime import datetime, timedelta


 

 

class TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode(TC_OPL_template):

    """Implementation of the HP QC test ID - 3321 T014582_Consult_Wake_up_creen_from_stand_by_mode
     Finito Done
    @author: Tomasz Stasiuk
    """


       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)
             
        ''' step '''
        self.logStepBeginning("STEP 1- Turn off stb")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(70)
        self.logStepResults("STEP 1- Turn off stb")
        
        ''' step '''
        self.logStepBeginning("STEP 2- Turn on stb and check wake-up screen")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(1)
        status=False
        currTime = datetime.now()
        i=0
        while(status==False):
            datanow = datetime.now()
            calc = datanow - currTime
            calc = calc.seconds
            if (calc>400):
                self.assertTrue(False, '  >>  ERR too long waiting for wake-up screen')
            if self.page.findInPage("swoje ulubione kanały"):
                status=True
            i = i+1
        self.logStepResults("STEP 2-  Turn on stb and check wake-up screen")
        
        ''' step '''
        self.logStepBeginning("STEP 3- Check live in fullscreen")
        time.sleep(15)
        self.assertTrue(self.page.checkLive(), '  >>  ERR None live or none fullscreen')
        self.logStepResults("STEP 3- Check live in fullscreen")
        
        
        
        ''' step '''
        self.logStepBeginning("STEP 4- Turn off stb")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(15)
        self.logStepResults("STEP 4- Turn off stb")
        
        
        
        ''' step '''
        self.logStepBeginning("STEP 5- Turn on stb and go to >"+"wybierz swoje ulubione kanały"+"<check wake-up screen")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(1)
        status=False
        currTime = datetime.now()
        i=0
        while(status==False):
            datanow = datetime.now()
            calc = datanow - currTime
            calc = calc.seconds
            if (calc>240):
                status = True
            if self.page.findInPage("swoje ulubione kanały"):
                status=True
            i = i+1
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
	time.sleep(3)
        if not self.page.findInPage("swoje ulubione kanały"):
            self.assertTrue(False, '  >>  ERR other message then "no favorite channels"')
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])
        self.logStepResults("STEP 5- Turn on stb and go to >"+"wybierz swoje ulubione kanały"+"<check wake-up screen")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        
