# -*- coding: utf-8 -*-

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3587_T014539_consult_the_video_presentation_screen_nominal_case(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3587 _consult_the_video_presentation_screen-nominal_case
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("go to VPS")
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod menu")
        self.assertTrue(self.page.goToVodToRentInCatalog(), "   ERR   cannot find vod to rent")
        self.logStepResults("go to VPS")
        
        self.logStepBeginning("check if important informations about VOD are displayed")
        
        info = self.page.getInfoFromVodPage()
        
        if not info:
            self.fail("   ERR   cannot get vod info")
        
        self.assertTrue(info.getTitle(), "   ERR   cannot get title")
        self.assertTrue(info.getLength(), "   ERR   cannot get length")
        self.assertTrue(info.getGenre(), "   ERR   cannot get genre")
        self.assertTrue(info.getPrice(), "   ERR   cannot get price")
        
        try:
            element = "#pictoCsa"
            self.page.driver.find_element_by_css_selector(element)
            element = ".country"
            self.page.driver.find_element_by_css_selector(element)
            element = ".directed"
            self.page.driver.find_element_by_css_selector(element)
            element = ".date"
            self.page.driver.find_element_by_css_selector(element)
            element = ".summary"
            self.page.driver.find_element_by_css_selector(element)
        except:
            self.fail("   ERR   cannot get " + element[1:])
            
        listA = self.page.getList()
        if not listA:
            self.fail("   ERR   cannot get list of buttons")
        self.assertTrue(listA[0].text.encode('utf-8') == Menu.vodRent, "   ERR   cannot get " + Menu.vodRent)
        self.assertTrue(listA[1].text.encode('utf-8') == Menu.vodTrailer, "   ERR   cannot get " + Menu.vodTrailer)
        self.assertTrue(listA[2].text.encode('utf-8') == Menu.vodSummary, "   ERR   cannot get " + Menu.vodSummary)
        self.assertTrue(listA[3].text.encode('utf-8') == Menu.vodAddToFavorites or listA[3].text.encode('utf-8') == Menu.vodRemoveFromFavorites, "   ERR   cannot get " + Menu.vodAddToFavorites + " or " + Menu.vodRemoveFromFavorites)
      
        self.logStepResults("check if important informations about VOD are displayed")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

