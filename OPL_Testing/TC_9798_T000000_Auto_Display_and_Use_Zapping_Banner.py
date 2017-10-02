# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9798 - _TC_T000000 auto display and use zapping banner
    
        @author: Tomasz Stasiuk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            channel1Name="1. TVP 1 HD"
            favoriteNo=[]
            BannerNo = []
            self.assertTrue(self.page.goToMySettings(), "ERR in goToMySettings")
            self.assertTrue(self.page.actionSelect(Menu.myChannels), "ERR go to kanaly")
            self.assertTrue(self.page.turnOffFavouriteChannels(), "ERR in turnOffFavouriteChannels")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(1)
    
            ''' step 1'''
            self.logStepBeginning("zap to channel and confirm banner information appears")
            
            self.rc.sendKeys(["KEY_2"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_1"])
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            favorite = self.page.driver.find_elements_by_xpath('//*[@class="favorite hidden"]') #if 
            #print "favorite"
            #print favorite
            if favorite==favoriteNo:
                #print "tutaj ja ja ja 1"
                self.fail("  >>  ERR channel is add to favorites")
            item = self.page.driver.find_element_by_css_selector("html body div.live.scene div.banner.zappingBanner.effect div.channel div.channelData div.desc")
            item = item.text.encode('utf-8')
            #print "item"
            #print item
            if not item==channel1Name:
                #print "tutaj ja ja ja 2"
                self.fail("  >>  ERR channelName is not current ")
            time.sleep(15)
            self.page.driver.get(Rpi.DUMP)
            zappingBanner=self.page.driver.find_elements_by_xpath('//*[@class="banner zappingBanner effect"]')
            #print "zappingBanner"
            #print zappingBanner
            if not zappingBanner==BannerNo:
                #print "tutaj ja ja ja 3"
                self.assertTrue(False, "  >>  ERR channel 3 isn't in EPG(favorite)")
                #self.fail("  >>  ERR zapping banner after 15 sec is still visible ")
                
            self.logStepResults("zap to channel and confirm banner information appears")
    
    
            ''' step 2'''
            self.logStepBeginning("Add chhanel to favorite")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.page.actionSelect(Menu.toolboxFavouriteChannelsNo)
            time.sleep(2)
            self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes)
            time.sleep(2)
            self.logStepResults("Add chhanel to favorite")
            
            ''' step 3'''
            self.logStepBeginning("zap to channel with favorite and confirm banner information appears")
            self.rc.sendKeys(["KEY_2"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_1"])
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            favorite = self.page.driver.find_elements_by_xpath('//*[@class="favorite hidden"]') #if 
            #print "favorite"
            #print favorite
            if not favorite==favoriteNo:
                #print "tutaj ja ja ja 4"
                self.fail("  >>  ERR channel is not add to favorites")
            item = self.page.driver.find_element_by_css_selector("html body div.live.scene div.banner.zappingBanner.effect div.channel div.channelData div.desc")
            item = item.text.encode('utf-8')
            #print "item"
            #print item
            if not item==channel1Name:
                #print "tutaj ja ja ja 5"
                self.fail("  >>  ERR channelName is not current ")
            zappingBanner=self.page.driver.find_elements_by_xpath('//*[@class="banner zappingBanner effect"]')
            #print "zappingBanner"
            #print zappingBanner
            if  zappingBanner==BannerNo:
                #print "tutaj ja ja ja 6"
                self.fail("  >>  ERR zapping banner is not  visible ")
                
            self.logStepResults("zap to channel and confirm banner information appears")
            self.assertTrue(self.page.goToMySettings(), "ERR in goToMySettings")
            self.assertTrue(self.page.actionSelect(Menu.myChannels), "ERR go to kanaly")
            self.assertTrue(self.page.turnOffFavouriteChannels(), "ERR in turnOffFavouriteChannels")
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
        except Exception, e:
            if not self.test_passed:
                self.page.goToMySettings()
                self.page.actionSelect(Menu.myChannels)
                self.page.turnOffFavouriteChannels()
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise
                
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
    
