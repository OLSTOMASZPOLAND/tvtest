# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return


 

 

class TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream(TC_OPL_template):

    """Implementation of the HP QC test ID - 2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream
 
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
        self.logStepBeginning('STEP 1 -chcek settings language ')
        self.assertTrue(self.page.setLanguageSettings(Menu.nativeSoundtrack),"error in settings checking")
        time.sleep(4)
        self.logStepResults('STEP 1 -chcek settings language ')
        
        ''' step '''
        self.logStepBeginning('STEP 2 -Open HBO')
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelHBOHD), " >> ERR IN Zap To HBO HD")
        time.sleep(4)
        self.logStepResults('STEP 2 -Open HBO')
        
        ''' step '''
        self.logStepBeginning('STEP 3 -open toolbox and check multilanguage')
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxNativeSoundtrack), "  >>  ERR not found "+Menu.toolboxNativeSoundtrack)
        self.assertTrue(self.page.actionSelect(Menu.toolbox_2_nativeSoundtrack), "  >>  ERR not found favorite channels  "+Menu.toolbox_2_nativeSoundtrack)
        time.sleep(3)
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxNativeSoundtrack), "  >>  ERR not found "+Menu.toolboxNativeSoundtrack)
        self.assertTrue(self.page.actionSelect(Menu.toolbox_2_englishSoundtrack), "  >>  ERR not found favorite channels  "+Menu.toolbox_2_englishSoundtrack)
        time.sleep(3)
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.findInPage(Menu.toolboxOriginalSoundtrack), "  >>  ERR not found "+Menu.toolboxOriginalSoundtrack)
        
        self.logStepResults('STEP 3 -open toolbox and check multilanguage')



        self.rc.sendKeys(["KEY_TV"])


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        
