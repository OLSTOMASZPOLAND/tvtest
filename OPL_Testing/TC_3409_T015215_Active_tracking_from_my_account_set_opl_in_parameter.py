# -*- coding: utf-8 -*-

 

import time
from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.DataSet import LiveData
from wheel.signatures import assertTrue

 

 
class TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter(TC_OPL_template):
    """
    Implementation of the HP QC test ID TC 3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter.
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   
    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
    
    
            ''' prestep '''
    
            self.logStepResults("AT_THE_BEGINNING")
            time.sleep(3)
                    
    
            ''' step '''
            self.logStepBeginning("STEP 1- Set deactivate Recommendation ")
            self.assertTrue(self.page.setRecommendation('activate'),'ERR in set activate Recommendation')
            self.logStepResults("STEP 1- Set deactivate Recommendation ")
        
            ''' step '''
            self.logStepBeginning("STEP 2- check icon in Menu")
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 2- check icon in Menu")
            
            
            
            ''' step '''
            self.logStepBeginning("STEP 3- check icon in Menu -> Orange TV")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.tvChannels), 'ERR: don`t go to Orange TV')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 3- check icon in Menu -> Orange TV")
    
    
            ''' step '''
            self.logStepBeginning("STEP 4- check icon in Menu -> VOD")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand), 'ERR: don`t go to VOD')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 4- check icon in Menu -> VOD")
    
    
            ''' step '''
            self.logStepBeginning("STEP 5- check icon in Menu -> TV on demand")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.tvOnDemand), 'ERR: don`t go to TV on demand')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 5- check icon in Menu -> TV on demand")
            
            
            ''' step '''
            self.logStepBeginning("STEP 6- check icon in Menu -> personalized suggestion")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), 'ERR: don`t go to personalized suggestion')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 6- check icon in Menu -> personalized suggestion")
    
    
            ''' step '''
            self.logStepBeginning("STEP 7- check icon in Menu -> epg")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.epg), 'ERR: don`t go to epg')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 7- check icon in Menu -> epg")
            
            
            
            ''' step '''
            self.logStepBeginning("STEP 8- check icon in Menu -> my account")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.myAccount), 'ERR: don`t go to my account')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 8- check icon in Menu -> my account")    
            
            
            ''' step '''
            self.logStepBeginning("STEP 9- check icon in Menu -> vod search")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.vodSearch), 'ERR: don`t go to vod search')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 9- check icon in Menu -> vod search")   
            
            
            
            ''' step '''
            self.logStepBeginning("STEP 10- check icon in Menu -> pvr")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.pvr), 'ERR: don`t go to pvr')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 10- check icon in Menu -> pvr")    
            
            
            
            ''' step '''
            self.logStepBeginning("STEP 11- check icon in Menu -> multimedia")
            time.sleep(5)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu ')
            self.assertTrue(self.page.actionSelect(Menu.multimedia), 'ERR: don`t go to multimedia')
            
            find = self.page.findOptinIcon()
            if find==None:
                time.sleep(1)
                self.assertTrue(False, "  >>   ERR: not find icon")
            elif find==True: 
                time.sleep(1)
                print 'find icon'
            else:
                self.assertTrue(False, "  >>   ERR: in findOptinIcon")
                time.sleep(1)
            self.logStepResults("STEP 11- check icon in Menu -> multimedia")                    
                
       
    
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            time.sleep(5)
            self.page.checkStbStatusIfKoReboot()
            self.page.setRecommendation('deactivate')
        