# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return


 

 

class TC_10906_T016034_Consult_a_no_rented_paid_vod(TC_OPL_template):

    """Implementation of the HP QC test ID - 10906_T016034_Consult_a_no_rented_paid_vod
 
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
        
        self.logStepBeginning('STEP 1 -Go to VOD and no rented vod')
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "ERR: Entering VOD Catalog" +Menu.vodCatalogWithTestContent)

        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)

        status = True
        i=0
        while(status==True):
            i=i+1
            if i==20:
                self.assertTrue(False, "  >>   ERR: None found not rent vod")
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            rent=self.page.findInPage(Menu.vodRent)
            if rent==True:
                status=False
            else:
                self.rc.sendKeys(["KEY_BACK"])
                time.sleep(3)
                self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])
        
        self.logStepResults('STEP 1 -Go to VOD and no rented vod')
        
        ''' step '''
        self.logStepBeginning('STEP 2 -Check highlight')
        self.rc.sendKeys(["KEY_DOWN", "KEY_UP"]) 
        time.sleep(3)
        self.page.driver.get(Rpi.DUMP)
        moje=True;
        try:
            moje = self.page.driver.find_element_by_css_selector("div.scene.whiteBg.vpsMainWidget div.menuList.dockLeft div.list div.container div#vpsRent.listItem.highlight") #.html body div.scene.whiteBg.vpsMainWidget div.menuList.dockLeft div.list div.container div#vpsTrailer.listItem.inactive    
        except:
            time.sleep(1)
        if moje != True:
            self.assertTrue(True, "  >>   found highlight")  
        else:
            self.assertTrue(False, "  >>   ERR: Not highlight") 
             
        self.logStepResults('STEP 2 -check highlight')
        


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        