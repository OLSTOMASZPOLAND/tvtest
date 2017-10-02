# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi
import time

class TC_3539_VOD_video_presentation_favorites(TC_OPL_template):
    '''Implementation of the HP QC test ID - 0000 - T999999
    
    Purpose: Star icon displays after selecting 'dodaj do wybranych' in VOD item
    
        @author: Grzegorz Krolikowski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            
            self.logStepBeginning("step 1")
            
            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   Can't go to 'katalog filmow'")
            
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            try:
                element = self.page.driver.find_element_by_css_selector(".container .listItem")
            except:
                self.fail("   ERR   There is nothing on the list, at least one item required")
                
            element = element.text
            self.assertTrue(self.page.actionSelect(element), "   ERR   Can't go to " + element)
            
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            
            element = self.page.driver.find_elements_by_xpath("/html/body/div[7]/div[1]/div[3]/div/div[4]") 
            element = element[0].text        
               
            star = self.page.driver.find_elements_by_css_selector(".heart_w")
            
            if(element.encode('utf-8') == "dodaj do wybranych"):
                if(len(star) != 0):
                    self.fail("   ERR   Heart displays when it should not")
                else:
                    self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites) , "   ERR   Can't go to 'dodaj do wybranych'")
                    time.sleep(2)
                    self.page.driver.get(Rpi.DUMP)
                    time.sleep(2)
                    star = self.page.driver.find_elements_by_css_selector(".heart_w")
                    if(len(star) != 1):
                        self.fail("   ERR   Heart doesn't display")
            else:
                if(element.encode('utf-8') == "usuń z wybranych"):
                    if(len(star) != 1):
                        self.fail("   ERR   Heart doesn't display")
                    else:
                        self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites) , "   ERR   Can't go to 'dodaj do wybranych'")
                        time.sleep(2)
                        self.page.driver.get(Rpi.DUMP)
                        time.sleep(2)
                        star = self.page.driver.find_elements_by_css_selector(".heart_w")
                        print len(star)
                        if(len(star) == 1):
                            print len(star)
                            self.fail("   ERR   Heart displays when it should not")
                            
            self.logStepResults("step 1")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                