# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return


 

 

class TC_3003_T014446_NavigateIntiTheZappingList(TC_OPL_template):

    """Implementation of the HP QC test ID - 3003_T014446_NavigateIntiTheZappingList
 
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
        self.logStepBeginning('STEP 1 -Open zapping list')
        self.rc.sendKeys(["KEY_3"])
        time.sleep(4)    
        self.rc.sendKeys(["KEY_LIST"])
        time.sleep(4)
        self.logStepResults('STEP 1 -Open zapping list')
        
        ''' step '''
        self.logStepBeginning('STEP 2 -find favorite channels')
        lista = self.page.findInPage(Description.favoriteInList)
        l=1
        if not (lista==True):
            while (l<20):
                l=l+1
                self.rc.sendKeys(["KEY_LEFT"])
                time.sleep(4)
                lista = self.page.findInPage(Description.favoriteInList)
                if (lista==True):
                    l=20
        time.sleep(5)
        if (lista!=True):
            self.assertTrue(False, "  >>  ERR not found favorite channels  ")
        self.logStepResults('STEP 2 -find favorite channels')

        ''' step '''
        self.logStepBeginning('STEP 3 -find Orange TV channels')
        lista = self.page.findInPage(Description.orangeTvInList)
        l=1
        if not (lista==True):
            while (l<20):
                l=l+1
                self.rc.sendKeys(["KEY_LEFT"])
                time.sleep(4)
                lista = self.page.findInPage(Description.orangeTvInList)
                if (lista==True):
                    l=20
        time.sleep(5)
        if (lista!=True):
            self.assertTrue(False, "  >>  ERR not found Orange TV channels  ")
        self.logStepResults('STEP 3 -find Orange TV channels')

        ''' step '''
        self.logStepBeginning('STEP 4 -find information channels')
        lista = self.page.findInPage(Description.informationInList)
        l=1
        if not (lista==True):
            while (l<20):
                l=l+1
                self.rc.sendKeys(["KEY_LEFT"])
                time.sleep(4)
                lista = self.page.findInPage(Description.informationInList)
                if (lista==True):
                    l=20
        time.sleep(5)
        if (lista!=True):
            self.assertTrue(False, "  >>  ERR not found information channels  ")
        self.logStepResults('STEP 4 -find information channels')

        ''' step '''
        self.logStepBeginning('STEP 5 -find sport channels')
        lista = self.page.findInPage(Description.sportInList)
        l=1
        if not (lista==True):
            while (l<20):
                l=l+1
                self.rc.sendKeys(["KEY_LEFT"])
                time.sleep(4)
                lista = self.page.findInPage(Description.sportInList)
                if (lista==True):
                    l=20
        time.sleep(5)
        if (lista!=True):
            self.assertTrue(False, "  >>  ERR not found sport channels  ")
        self.logStepResults('STEP 5 -find sport channels')

        self.rc.sendKeys(["KEY_TV"])


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        