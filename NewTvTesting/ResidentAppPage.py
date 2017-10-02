# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib2
import ssl
import time
from Config import *
from Containers import *
from RemoteControl import *
from NewTvTesting.Containers import *
from NewTvTesting.StbtIntegration import *
from datetime import datetime, timedelta
from random import randint
import logging
from __builtin__ import False
from cv2 import dilate

class WebKitPage(object):


    def __init__(self):
        self.rc = RpiRemoteControl()

        if Env.BROWSER == "firefox":
            self.driver = webdriver.Firefox()
        else:
            # self.driver = webdriver.Chrome('/My Program Files/Chromium/chromedriver.exe')
            # self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')

            # self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", service_args=["--verbose", "--log-path=/tmp/chromedriver.log"])
            # self.driver = webdriver.PhantomJS()
            self.driver = webdriver.PhantomJS(executable_path='/home/itoutline/phantomjs/bin/phantomjs')
            # self.driver.implicitly_wait(10)

        self.driver.set_window_size(1280, 800)
        self.logger = logging.getLogger('NewTvTesting.WebKitPage')



    def close(self):
        self.driver.quit()


    def actionSelect(self, t):
        self.logger.debug("  >>   selecting text >" + t + "<")
        if self.loadPageList():

            find = False
            index = 0

            while self.activeItems[index].text.encode('utf-8') != t and index < (len(self.activeItems) - 1):
                # self.logger.debug(self.activeItems[index].text)
                index = index + 1


            if self.activeItems[index].text.encode('utf-8') == t:
                find = True

            gap = index - self.activeHighlight

            if (gap >= 0 and find):
                for i in range (gap):
                    self.rc.sendKeys(["KEY_DOWN"])
                    time.sleep(0.8)
                time.sleep(0.8)
                self.rc.sendKeys(["KEY_OK"])
                return True
            elif (gap < 0 and find):
                for i in range (-gap):
                    self.rc.sendKeys(["KEY_UP"])
                    time.sleep(0.8)
                time.sleep(0.8)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(1)
                return True

            else:

                if len(self.driver.find_elements_by_css_selector(".ToolBoxLive")) > 0:
                    max = ConfAR.MAX_ITEMS_TOOLBOX
                else:
                    max = ConfAR.MAX_ITEMS

                if len(self.items) == max:

                    end = False
                    endText = self.activeItems[-1].text.encode('utf-8')

                    while not end:

                        for i in range(self.activeHighlight + 1):
                            self.rc.sendKeys(["KEY_UP"])
                            time.sleep(1)

                        self.loadPageList()
                        find = False
                        index = 0

                        while self.activeItems[index].text.encode('utf-8') != t and index < (len(self.activeItems) - 1):
                            index = index + 1
                            if self.activeItems[index].text.encode('utf-8') == endText:
                                end = True

                        if self.activeItems[index].text.encode('utf-8') == t:
                            find = True
                            end = True

                    if find:

                        gap = index - self.activeHighlight

                        if (gap >= 0):
                            for i in range (gap):
                                self.rc.sendKeys(["KEY_DOWN"])
                                time.sleep(0.8)
                            time.sleep(0.8)
                            self.rc.sendKeys(["KEY_OK"])
                            time.sleep(1)
                            return True
                        else:
                            for i in range (-gap):
                                self.rc.sendKeys(["KEY_UP"])
                                time.sleep(0.8)
                            time.sleep(0.8)
                            self.rc.sendKeys(["KEY_OK"])
                            time.sleep(1)
                            return True

                    else:
                        return False

                else:
                    return False
        else:
            # raise
            return False

    def actionSelectInLiveBanner(self, lcn, up=True, max=10):
        self.logger.debug("  >>   select channel " + str(lcn))

        self.loadLiveBanner()
        m = 0
        if (up):
            key = "KEY_UP"
        else:
            key = "KEY_DOWN"
        while (self.programInfo.lcn != lcn and m < max):
            self.rc.sendKeys([key])

            time.sleep(0.2)
            self.loadLiveBanner()
            m = m + 1
        if (self.programInfo.lcn == lcn):
            self.rc.sendKeys(["KEY_OK"])

            time.sleep(3)
            return True
        else:
            self.rc.sendKeys(["KEY_BACK"])
            return False

    def actionInstantRecord(self, length=5):
        self.logger.debug("  >>   actionInstantRecord - length >%d" % length + "< ")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if self.findInDialogBox(Menu.hardDrive):
                self.logger.error("   ERR   problem with the hard drive")
                return False
            element = self.driver.find_element_by_css_selector(".dialog.irDialog")

            currentDate = datetime.now()

            endDate = currentDate + timedelta(minutes=length)
            endHourTxt = str(endDate.hour)
            endMinTxt = str(endDate.minute)

            self.rc.sendKeys(["KEY_LEFT"])

            if len(endHourTxt) == 2:
                self.rc.sendKeys(["KEY_" + endHourTxt[0], "KEY_" + endHourTxt[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + endHourTxt[0]])


            if len(endMinTxt) == 2:
                self.rc.sendKeys(["KEY_" + endMinTxt[0], "KEY_" + endMinTxt[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + endMinTxt[0]])

            self.rc.sendKeys(["KEY_OK"])

            return True

        except Exception, e:
            self.logger.info("   ERR   " + str(e))
            return False

    def actionScheduleRecord(self, channelNumber, startDate, length, recurrence=0, name=None):
        self.logger.debug("  >>   actionScheduleRecord - channelNumber >" + str(channelNumber) + "< - startDate >" + str(startDate) + "< - length >" + str(length) + "< - recurrence >" + str(recurrence) + "< - name >" + str(name) + "<")
        channelNumber = int(channelNumber)
        time.sleep(3)

        # check is it in manual record scheduling
        if (not self.findInCssSelectorElement(Menu.pvrManualRecord, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in manual record scheduling")
            return False

        try:
            if name == None:
                name = str(randint(1000, 9999)).replace("0", "1")
            self.rc.sendWord(name)

            # find wanted channel on list
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(1)

            currTime = datetime.now()

            if channelNumber > 120:
                KEY = ["KEY_UP"]
            else:
                KEY = ["KEY_DOWN"]

            while((datetime.now() - currTime).seconds < 300):
                try:
                    self.driver.get(Rpi.DUMP)
                    time.sleep(1)
                    items = self.driver.find_elements_by_css_selector(".menuList.entered .list .container .listItem")
                    items = [int(item.text.encode('utf-8').split(u'. ')[0]) for item in items]
                    if channelNumber in items:
                        break
                    else:
                        self.rc.sendKeys(KEY * 9)
                    time.sleep(2)
                except:
                    pass
            else:
                raise Exception("   ERR   cannot find wanted lcn. Exiting...")

            self.driver.get(Rpi.DUMP)
            time.sleep(1)
            currItem = int(self.driver.find_element_by_css_selector(".menuList.entered .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')[0])

            if currItem < channelNumber:
                KEY = ["KEY_DOWN"]
            elif currItem > channelNumber:
                KEY = ["KEY_UP"]
            else:
                KEY = False

            if KEY:
                for i in range(10):
                    try:
                        self.rc.sendKeys(KEY)
                        self.driver.get(Rpi.DUMP)
                        time.sleep(1)
                        currItem = int(self.driver.find_element_by_css_selector(".menuList.entered .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')[0])
                        if currItem == channelNumber:
                            break
                    except:
                        pass

            self.rc.sendKeys(["KEY_OK", "KEY_DOWN"])

            self.driver.get(Rpi.DUMP)
            time.sleep(1)
            currItem = int(self.driver.find_element_by_css_selector("#channelsCB .textContainer .text").text.encode('utf-8').split(u'. ')[0])

            if currItem != channelNumber:
                self.logger.info("Error in actionScheduleRecord, cannot find given channel number")
                return False

            if len(str(startDate.day)) == 2:
                self.rc.sendKeys(["KEY_" + str(startDate.day)[0], "KEY_" + str(startDate.day)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(startDate.day)[0]])

            if len(str(startDate.month)) == 2:
                self.rc.sendKeys(["KEY_" + str(startDate.month)[0], "KEY_" + str(startDate.month)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(startDate.month)[0]])

            self.rc.sendKeys(["KEY_" + str(startDate.year)[2], "KEY_" + str(startDate.year)[3]])

            if len(str(startDate.hour)) == 2:
                self.rc.sendKeys(["KEY_" + str(startDate.hour)[0], "KEY_" + str(startDate.hour)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(startDate.hour)[0]])

            if len(str(startDate.minute)) == 2:
                self.rc.sendKeys(["KEY_" + str(startDate.minute)[0], "KEY_" + str(startDate.minute)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(startDate.minute)[0]])

            endDate = startDate + timedelta(minutes=length)

            if len(str(endDate.hour)) == 2:
                self.rc.sendKeys(["KEY_" + str(endDate.hour)[0], "KEY_" + str(endDate.hour)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(endDate.hour)[0]])

            if len(str(endDate.minute)) == 2:
                self.rc.sendKeys(["KEY_" + str(endDate.minute)[0], "KEY_" + str(endDate.minute)[1]])
            else:
                self.rc.sendKeys(["KEY_0", "KEY_" + str(endDate.minute)[0]])

            self.rc.sendKeys(["KEY_OK"])
            for index in range(0, recurrence):
                self.rc.sendKeys(["KEY_DOWN"])
            self.rc.sendKeys(["KEY_OK"])

            self.rc.sendKeys(["KEY_DOWN"])

            self.rc.sendKeys(["KEY_OK"])

            '''' Analyse pop-up'''

            time.sleep(10)
            self.driver.get(Rpi.DUMP)
            time.sleep(1)

            if self.findInDialogBox(Menu.pvrChangeConfirm):
                self.logger.debug("   >>>   changes confirmed")
                self.rc.sendKeys(["KEY_OK"])
                return True

            if self.findInDialogBox(DialogBox.PvrScheduleError):
                self.logger.debug("   ERR   Error popup in record scheduling")
                return False

            try:
                title = self.driver.find_element_by_css_selector(".dialog.message.pvrScheduling .box .title").text.encode('utf-8')
                nameInTheBox = self.driver.find_element_by_css_selector(".dialog.message.pvrScheduling .box .content .orange").text.encode('utf-8')
                if title == DialogBox.PvrScheduleOk and nameInTheBox == nameInTheBox:
                    self.rc.sendKeys(["KEY_OK"])
                    return name
                else:
                    self.logger.info("  >>   ERR: wrong popup title or record name")
                    return False

            except Exception, e:
                self.logger.info("  >>   ERR: error occured durign popup analyse: " + str(e))
                return False

        except Exception, e:
            self.logger.info("  >>   ERR: error occured: " + str(e))
            return False


    def getList(self):
        if self.loadPageList():
            return self.items
        else:
            return None

    def getInfoFromLiveBanner(self):
        if self.loadLiveBanner():
            return self.programInfo
        else:
            return None

    def getInfoFromTrickBar(self):
        if self.loadTrickBar():
            return self.trickBarStatus
        else:
            return None

    def getInfoFromEpgFocus(self):
        if self.loadEpg():
            return self.programInfo
        else:
            return None

    def getInfoFromMosaicFocus(self):
        if self.loadMosaic():
            return self.programInfo
        else:
            return None

    def getInfoFromRecordFocus(self):
        self.logger.debug("  >>   getInfoFromRecordFocus")
        if self.loadRecord():
            return self.recordItem
        else:
            return None

    def getInfoFromRecordPage(self):
        self.logger.debug("  >>   getInfoFromRecordPage")
        if self.loadRecordDetailed():
            return self.recordDetailedItem
        else:
            return None

    def getInfoFromVodPage(self):
        self.logger.debug("  >>   getInfoFromVodPage")
        if self.loadVodPage():
            return self.vod
        else:
            return None

    def getStatus(self):
        html = self.rc.getStbStatus()

        noRightPanel = None
        scene = None
        dialog = None

        if html == "READY":
            self.driver.get(Rpi.DUMP)
            time.sleep(1)

            try:
                if len(self.driver.find_elements_by_css_selector(".ToolBoxLive")) > 0:
                    scene = "TOOLBOX"
                elif len(self.driver.find_elements_by_css_selector(".virtualZappingBanner")) > 0:
                    scene = "ZAPPING_BANNER"
                elif len(self.driver.find_elements_by_css_selector(".live.scene")) > 0:
                    scene = "LIVE"
                elif len(self.driver.find_elements_by_css_selector(".whiteBg")) > 0:
                    scene = "PORTAL"
                else:
                    scene = "UNKNOWN"
            except:
                scene = "UNKNOWN"

            try:
                element = self.driver.find_element_by_css_selector(".scene.noRightView")
                if element.get_attribute("aria-hidden").find("false") > -1:
                    noRightPanel = True
            except:
                noRightPanel = False

            try:
                element = self.driver.find_element_by_css_selector(".dialog")
                dialog = True
            except:
                dialog = False


        return Status(str(html), noRightPanel, scene, dialog)

    def getClock(self):
        self.logger.debug("  >>   getClock")

        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            dateTxt = self.driver.find_element_by_css_selector(".breadcrumb .clock").text.encode('utf-8')
            day = dateTxt.split(" ")[0]
            hour = dateTxt.split(" ")[1]

            return datetime(int(day.split("/")[2]), int(day.split("/")[1]), int(day.split("/")[0]), int(hour.split(":")[0]), int(hour.split(":")[1]))

        except Exception:
            # raise
            return None

    def getFavoriteChannelListItemOnList(self):
        self.logger.debug("  >>   getFavoriteChannelListItemOnList")

        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            activeChannelListElement = self.driver.find_element_by_css_selector(".menuList .list .container .listItem.picto.highlight")
            channelDescElements = activeChannelListElement.find_element_by_css_selector("span.labeltext").text.encode('ascii', 'ignore').split(u'. ')
            if len(activeChannelListElement.find_elements_by_css_selector("span.picto.checked")) > 0:
                channelIconIsFavourite = True
            elif len(self.driver.find_elements_by_css_selector("span.picto")) > 0:
                channelIconIsFavourite = False
            else:
                return False

            return FavoriteChannelListItem(lcn=channelDescElements[0], channelName=channelDescElements[1], favorite=channelIconIsFavourite, active=True)

        except Exception:
            # raise
            return None

    def findInDialogBox(self, txt):
        self.logger.debug("  >>   findInDialogBox - txt >" + txt + "< ")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_css_selector(".dialog")) > 0:
                element = self.driver.find_element_by_css_selector(".box")
                text = element.text.encode('utf-8')
                if text.find(txt) > -1:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def findInList(self, t, onlyActive=False):
        self.logger.debug("  >>   findInList - t >" + t + "< - onlyActive >%s" % onlyActive + "< ")

        if self.loadPageList():
            for item in self.items:
                if item.text.encode('utf-8') == t:
                    if onlyActive:
                        if item.active:
                            return True
                    else:
                        return True

            if len(self.driver.find_elements_by_css_selector(".ToolBoxLive")) > 0:
                max = ConfAR.MAX_ITEMS_TOOLBOX
            else:
                max = ConfAR.MAX_ITEMS



            if len(self.items) == max:
                activeItems = []
                index = 0
                activeHighlight = 0

                for firstIndex, el in enumerate(self.items):
                    if el.active:
                        activeItems.append(el)
                        if firstIndex == self.highlight:
                            activeHighlight = index
                        index = index + 1

                endText = activeItems[-1].text.encode('utf-8')

                for i in range(activeHighlight + 1):
                        self.driver.get(Rpi.KEY_UP)
                        time.sleep(0.2)

                end = False
                while end == False:
                    self.loadPageList()

                    for item in self.items:
                        if item.text.encode('utf-8') == t:
                            if onlyActive:
                                if item.active:
                                    return True
                            else:
                                return True
                        if item.text.encode('utf-8') == endText:
                            end = True
                    self.driver.get(Rpi.KEY_UP)
                    time.sleep(0.2)
                return False
            else:
                return False
        else:
            return False

    def findInPage(self, txt):
        self.logger.debug("  >>   findInPage - txt >" + txt + "< ")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_tag_name('body')) > 0:
                element = self.driver.find_element_by_tag_name('body')
                text = element.text.encode('utf-8')
                if text.find(txt) > -1:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def loadTrickBar (self):
        self.driver.get(Rpi.DUMP)
        time.sleep(1)
        messageFirstRow = None
        messageSecondRow = None
        trickVisible = False
        try:
            if len(self.driver.find_elements_by_css_selector(".trick.hidden")):
                return False
            if self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv"):
                trickVisible = True
                if self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.pause"):
                    trickIcon = "Pause"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.play"):
                    trickIcon = "Play"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.forbidden"):
                    trickIcon = "Forbidden"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.rew4"):
                    trickIcon = "Rewind4"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.rew16"):
                    trickIcon = "Rewind16"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.rew32"):
                    trickIcon = "Rewind32"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.rew64"):
                    trickIcon = "Rewind64"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.fwd4"):
                    trickIcon = "Forward4"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.fwd16"):
                    trickIcon = "Forward16"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.fwd32"):
                    trickIcon = "Forward32"
                elif self.driver.find_elements(By.CSS_SELECTOR, ".iconMessageDiv .icon.fwd64"):
                    trickIcon = "Forward64"
            else:
                return False
            try:
                trickMessage = self.driver.find_element(By.ID, "message").text.encode('utf-8')
                trickMessage = trickMessage.split("\n")
                messageFirstRow = trickMessage[0]
                messageSecondRow = trickMessage[1]
            except Exception, e:
                pass
                    # raise
            self.trickBarStatus = TrickBarStatus(trickVisible, trickIcon, messageFirstRow, messageSecondRow)
            return True
        except Exception, e:
            # raise
            return False

    def findInXPathElement(self, txt, xpath):
        self.logger.debug("  >>   findInXPathElement - txt >" + txt + "< - xpath >" + xpath + "<")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            # self.logger.info("  >>   xpath >" + xpath + "<")
            element = self.driver.find_element_by_xpath(xpath)
            text = element.text.encode('utf-8')
            # self.logger.info("  >>   xpath element text >" + text + "<")
            if text.find(txt) > -1:
                return True
            else:
                return False
        except:
            # raise
            return False

    def findInXPathElementStyle(self, txt, xpath):
        self.logger.debug("  >>   findInXPathElementStyle - txt >" + txt + "< - xpath >" + xpath + "<")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            # self.logger.info("  >>   xpath >" + xpath + "<")
            element = self.driver.find_element_by_xpath(xpath)
            style = element.get_attribute("style").encode('utf-8')
            # self.logger.info("  >>   xpath element style >" + style + "<")
            if style.find(txt) > -1:
                return True
            else:
                return False
        except:
            return False

    def findInXPathElementClass(self, txt, xpath):
        self.logger.debug("  >>   findInXPathElementClass - txt >" + txt + "< - xpath >" + xpath + "<")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            # self.logger.info("  >>   xpath >" + xpath + "<")
            element = self.driver.find_element_by_xpath(xpath)
            cssClass = element.get_attribute("class").encode('utf-8')
            # self.logger.info("  >>   xpath element cssClass >" + cssClass + "<")
            if cssClass.find(txt) > -1:
                return True
            else:
                return False
        except:
            return False

    def findInCssSelectorElement(self, txt, cssSelector):
        self.logger.debug("  >>   findInCssSelectorElement - txt >" + txt + "< - cssSelector >" + cssSelector + "<")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            # self.logger.info("  >>   xpath >" + xpath + "<")
            element = self.driver.find_element_by_css_selector(cssSelector)
            text = element.text.encode('utf-8')
            # self.logger.info("  >>   xpath element text >" + text + "<")
            if text.find(txt) > -1:
                return True
            else:
                return False
        except:
            # raise
            return False

    def loadVodPage(self):
        self.logger.debug("  >>   loadVodPage")

        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_css_selector(".scene .dockCenter")) > 0:
                element = self.driver.find_element_by_css_selector(".breadcrumb .first")
                title = element.text.encode('utf-8')


                element = self.driver.find_element_by_css_selector(".scene .dockCenter .genres")
                genre = element.text.encode('utf-8')

                try:
                    element = self.driver.find_element_by_css_selector(".scene .dockCenter .duration")
                    lengthTxt = element.text
                    if genre == "":
                        genre = None
                        lengthMinTxt = lengthTxt.split(" ")[0]
                    else:
                        lengthMinTxt = lengthTxt.split(" ")[2]
                    length = timedelta(minutes=int(lengthMinTxt))
                except:
                    length = None

                try:
                    element = self.driver.find_element_by_css_selector(".scene .dockCenter .labelDuree .label2")
                    dateTxt = element.text
                    day = dateTxt.split(" ")[0]
                    hour = dateTxt.split(" ")[3]

                    endDate = datetime(int(day.split("/")[2]), int(day.split("/")[1]), int(day.split("/")[0]), int(hour.split(":")[0]), int(hour.split(":")[1]))

                except:
                    endDate = None
                try:
                    priceTxt = self.driver.find_elements_by_css_selector(".priceAndDispoBox .price")[0].text.encode('utf-8').split(' zł')[0]
                    price = float(priceTxt)

                except:
                    price = None

                self.vod = VodItem(title, genre, length, endDate, price)
                return True
            else:
                return False
        except Exception:
            return False


    def loadPageList(self):
        # self.logger.debug("  >>   loadPageList")

        self.highlight = None
        self.items = []
        self.activeHighlight = None
        self.activeItems = []

        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_css_selector(".box")) > 0:
                elements = self.driver.find_elements_by_css_selector(".box .listItem")
            # if there is radioList in the DOM and it's not hidden!
            elif len(self.driver.find_elements_by_css_selector(".radiolist .listItem")) > 0 and self.driver.find_element_by_css_selector("div.radiolist").get_attribute("style").encode('utf-8').find(u"display: none;".encode('utf-8')) == -1:
                elements = self.driver.find_elements_by_css_selector(".radiolist .listItem")
            # if there is menuList in the DOM and it's not hidden!
            elif len(self.driver.find_elements_by_css_selector(".menuList .list .container .listItem")) > 0 and self.driver.find_element_by_css_selector("div.menuList").get_attribute("style").encode('utf-8').find(u"display: none;".encode('utf-8')) == -1:
                elements = self.driver.find_elements_by_css_selector(".menuList .list .container .listItem")
            else:
                return False

            indexActive = 0

            for index, element in enumerate(elements):
                elementText = element.text
                # if element has children
                if len(element.find_elements_by_css_selector("detail")) > 0:
                    elementText += element.find_element_by_css_selector("detail").text  # TODO - check is it possible to have more that one element 'detail'

                if element.get_attribute("class").find("highlight") > -1:
                    self.highlight = index
                    self.activeHighlight = indexActive

                # zmiana Marcin Gmurczyk
                # if element.get_attribute("class").find("selected")>-1 or element.get_attribute("class").find("checked")>-1:
                    # selected=True
                if element.get_attribute("class").find("highlight") > -1 or element.get_attribute("class").find("checked") > -1:
                    selected = True
                else:
                    selected = False
                if element.get_attribute("class").find("inactive") > -1:
                    active = False
                else:
                    active = True
                    self.activeItems.append(ListItem(elementText, selected, active))
                    indexActive = indexActive + 1

                self.items.append(ListItem(elementText, selected, active))
            return True
        except Exception, e:
            return False

    def loadLiveBanner(self):
        self.logger.debug("  >>   loadLiveBanner")
        self.driver.get(Rpi.DUMP)
        time.sleep(1)
        
        if Env.STB_MODEL == "DAKOTA":
            #return  True
            print "DAKOTA"
            try:                    
                if self.driver.find_elements_by_css_selector(" body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation"):
    
                    clock = None
                    csaClass = None
                    genre = None
                    nextProgram = None
                    favorite = True
                    start = None
                    length = None
                    currentProgram = None
                    num = None
                    txt = None   
                    
                    
                      
                    #LCN - num Done
                    try:
                        #print " LCN TRY"
                        numCss=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.nameOfChannel")
                        num=numCss[0].text.encode('utf-8').split(" - ")[0]
                        num=int(num)
                        #print "num"
                        #print num
                    except:
                        num = None
                    #channelName - txt Done
                    try:
                        #print "Channelname TRY"
                        txtCss=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.nameOfChannel")
                        txt=txtCss[0].text.encode('utf-8').split(" - ")[1]
                        #print "txt"
                        #print txt
                    except:
                        txt = None
                    #program - currentProgram Done
                    try:
                        #print "currentprogram TRY"
                        currentProgramCss=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.program")
                        currentProgram=currentProgramCss[0].text.encode('utf-8').split(" - ")[0]
                        #print "currentProgram"
                        #print currentProgram
                    except:
                        currentProgram = None 
                                                 
                    #start - start do poprawy
                    try:
                        startCss=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.start")
                        startCss=startCss[0].text.encode('utf-8').split(" - ")[0]
                        now = datetime.now()
                        hourStart = startCss.split(":")[0]
                        minStart = startCss.split(":")[1]
                        if len(startCss) == 5:
                            start = datetime(now.year, now.month, now.day, int(hourStart), int(minStart))
                    except:
                        start = None   
                    #length - length 
                    try:
                        endCss=self.driver.find_elements_by_css_selector("body >  div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.end")
                        endCss=endCss[0].text.encode('utf-8').split(" - ")[0]
                        end = datetime.now()
                        hourEnd = endCss.split(":")[0]
                        minEnd = endCss.split(":")[1]
                        if len(endCss) == 5:
                            end = datetime(now.year, now.month, now.day, int(hourEnd), int(minEnd))
                        if end < start :
                            end = end + timedelta(days=1)
                        length = end - start 
                    except:
                        length = None   
                       
                    #genre - genre Done
                    try:
                        genreCSS=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.kind")
                        genre=genreCSS[0].text.encode('utf-8').split(" - ")[0]
                        if genre=="":
                            genre=None
                    except:
                        genre = None 
                          
                    #favorite - favorite Done
                    try:
                        if len(self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.favorite.hidden")) > 0:
                            favorite = False
                        else:
                            favorite = True
                    except:
                        favorite = None 
                    
                    #nextProgram - nextProgram Done
                    try:
                        nextProgramCss=self.driver.find_elements_by_css_selector("body > div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.nextProgram div.next")
                        nextProgram=nextProgramCss[0].text.encode('utf-8').split(" - ")[0]
                    except:
                        nextProgram = None  
                        
                    #clock - clock 
                    try:
                        clockCss=self.driver.find_elements_by_css_selector(" body >  div.ToolBoxLive div.banner.zappingBanner.effect div.content div.contentData div.programInformation div.clock.time")
                        clockCss=clockCss[0].text.encode('utf-8').split(" - ")[0]
                        nowClock = datetime.now()
                        hourClock = clockCss.split(":")[0]
                        minClock = clockCss.split(":")[1]
                        if len(clockCss) == 5:
                            clock = datetime(nowClock.year, nowClock.month, nowClock.day, int(hourClock), int(minClock))                        
                    except:
                        clock = None
                        
                    
                    #csaClass - csaClass 
                    try:
                        element = self.driver.find_element_by_class_name("pictoCsa")
                        cssClasses = element.get_attribute("class").encode('utf-8').split(" ")
                        for index in range(0, len(cssClasses)):
                            if cssClasses[index] != u"pictoCsa".encode('utf-8'):
                                csaClass = cssClasses[index]
                                break
                    except:
                        csaClass = None
                    
                    self.programInfo = ProgramInfoItem(num, txt, currentProgram, start, length, genre, favorite, nextProgram, clock=clock, csaClass=csaClass)   
                    return True
                else:
                    return False
            except:
                return False
        else:
            try:
    
                # if len(self.driver.find_elements_by_css_selector(".virtualZappingBanner"))>0:
                elements = self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect")
    
                # print self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect > div.channel > div > div.desc")
                # print self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect")
                if self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect"):
                    elements = self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect > div.channel > div > div.desc")
    
                    alltxt_list = elements[0].text.split(u'. ')
                    num = int(alltxt_list[0])
    
                    txt = alltxt_list[1]
                    # print txt
    #                 txt=""
    #                 inter=""
    #                 for index in range(2,len(alltxt_list)):
    #                     txt=txt+inter+alltxt_list[index]
    #                     inter=" "
    
                    # clock
                    clock = None
                    try:
                        element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.channel > div > div.clock")
                        timeText = element.text.encode('utf-8')
                        hour = timeText.split(":")[0]
                        minutes = timeText.split(":")[1]
                        now = datetime.now()
                        clock = datetime(now.year, now.month, now.day, int(hour), int(minutes))
                    except:
                        clock = None
    
                    # csa level
                    csaClass = None
                    try:
                        element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.moviePictos > span.pictoCsa")
                        cssClasses = element.get_attribute("class").encode('utf-8').split(" ")
                        for index in range(0, len(cssClasses)):
                            if cssClasses[index] != u"pictoCsa".encode('utf-8'):
                                csaClass = cssClasses[index]
                                break
                    except:
                        csaClass = None
    
                    element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.program")
                    currentProgram = element.text.encode('utf-8')
                    # print ("current program: " + currentProgram)
                    try:
                        # element=self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.kind")
                        element = self.driver.find_element_by_css_selector("div.kind")
                        # element=self.driver.find_element_by_xpath("/html/body/div[7]/div[2]/div/div/div[7]")
                        genre = element.get_attribute("innerHTML")
                        genre = genre.encode('utf-8')
                        # print ("kind: " + genre)
                    except:
                        genre = None
    
                    element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.next")
                    nextProgram = element.text.encode('utf-8')
                    if len(nextProgram) == 0:
                        nextProgram = None
                    if len(self.driver.find_elements_by_css_selector("body > div.banner.infoBanner.effect > div.channel > div > div.favorite.hidden")) > 0:
                        favorite = False
                    else:
                        favorite = True
    
                    element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.start")
                    start = None
                    length = None
    
                    if len(element.text.encode('utf-8')) == 5:
                        hour = element.text.split(":")[0]
                        min = element.text.split(":")[1]
                        now = datetime.now()
                        start = datetime(now.year, now.month, now.day, int(hour), int(min))
                        element = self.driver.find_element_by_css_selector("body > div.banner.infoBanner.effect > div.content > div > div > div.end")
                        if len(element.text) == 5:
                            hour = element.text.split(":")[0]
                            min = element.text.split(":")[1]
                            now = datetime.now()
                            end = datetime(now.year, now.month, now.day, int(hour), int(min))
                            if end < start :
                                end = end + timedelta(days=1)
                            length = end - start
    
                    self.programInfo = ProgramInfoItem(num, txt, currentProgram, start, length, genre, favorite, nextProgram, clock=clock, csaClass=csaClass)
    
                    return True
                else:
                    return False
    
            except Exception:
                return False

    def checkIfEpgIsAvalaible(self):
        """Function checks if some information from EPG can be obtained
 
        @precondition: Menu -> TV Program > Now
        @return: True when function can some information from EPG, False when error occurs
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   checkIfEpgIsAvalaible")
        time.sleep(15)
        item = self.getInfoFromEpgFocus()
        if not item:
            self.rc.sendKeys(["KEY_LEFT"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(15)
            item = self.getInfoFromEpgFocus()
            if not item:
                    self.logger.info("  >>   ERR: cant get info from epg focus")
                    return False
        if(item.getStart() != None and item.getLength() != None):
            return True
        else:
            self.logger.info("  >>   ERR: cant get info from epg focus")
            return False

    def recordFromEpg(self, delay=0, channelNumber=1, returnItem=None):
        """Function sets record from EPG today screen
 
        @precondition: Menu -> TV Program > Now

        @param delay: which program in future from current program should be recorded, 0 to record current program, 1 to record next program and so on (type: int)
        @param channel number: recorded channel number (type: int)
        @param returnItem: when function returns True, there will be in this list a ProgramInfoItem object cantaining information about recorded program (type: empty list [])
        @return: True if records sets correctly, False if not
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   recordFromEpg - delay >%s< - channelNumber >%s< - returnItem >%s<" % (delay, channelNumber, returnItem))
        if not self.checkIfEpgIsAvalaible():
            self.logger.info("   ERR   >>>   EGP is not avalaible")
            return False

        self.rc.zap(channelNumber)
        time.sleep(10)

        for x in range(0, delay):
            self.rc.sendKeys(["KEY_RIGHT"])

        time.sleep(15)
        temp = self.getInfoFromEpgFocus()

        if(not temp or (temp.getStart() - datetime.now()).seconds < 300 or temp.getStart() < datetime.now()):
            self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(25)
            temp = self.getInfoFromEpgFocus()

        if not temp:
            self.logger.debug("   ERR   cannot get info from epg focus")
            return False

        time.sleep(5)

        self.rc.sendKeys(["KEY_RECORD"])

        time.sleep(5)

        currTime = datetime.now()

        if delay == 0:
            while not self.findInDialogBox(Menu.pvrRecord):
                time.sleep(3)
                if (datetime.now() - currTime).seconds > 300:
                    self.logger.info("   ERR   >>>   cannot set record")
                    return False
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
        else:
            while not self.findInDialogBox(Menu.pvrRecording):
                time.sleep(3)
                if (datetime.now() - currTime).seconds > 300:
                    self.logger.info("   ERR   >>>   cannot set record")
                    return False
            time.sleep(10)
            self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])


        time.sleep(10)

        if returnItem == None:
            return True

        item = self.getInfoFromEpgFocus()

        if type(item) != ProgramInfoItem:
            self.logger.info("   ERR   >>>   cannot get info about epg focus")
            return False
        else:
            returnItem.append(item)
            self.logger.info("Program selected to record:")
            item.display()
            return True

    def loadEpg(self):
        self.logger.debug("  >>   loadEpg")

        time.sleep(3)  # wait a while, let the EPG load
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_css_selector(".epg .grid .content")) > 0:
                # channel number and channel name
                element = self.driver.find_element_by_css_selector(".epg .grid .content .row.selected .channelText")
                alltxt_list = element.text.split(u' ')
                lcn = int(alltxt_list[0].replace(".", ""))
                channelName = ""
                inter = ""
                for index in range(1, len(alltxt_list)):
                    channelName = channelName + inter + alltxt_list[index]
                    inter = " "

                # channel favorite
                element = self.driver.find_element_by_css_selector(".epg .grid .content .row.selected .epgHeart")
                favorite = False
                if element.get_attribute("style").encode('utf-8').find(u"display: none;".encode('utf-8')) == -1:  # if icon is not hidden
                    favorite = True

                # program
                program = self.driver.find_element_by_css_selector(".epg .grid.programInfo .description .title").text.encode('utf-8')
                # genre
                genre = self.driver.find_element_by_css_selector(".epg .grid.programInfo .description .genre").text.encode('utf-8')
                if genre == "":
                    genre = None

                # nextProgram
                nextProgram = None
                elements = self.driver.find_elements_by_css_selector(".epg .grid .content .cellContainers .cellContainer.selected .cell")
                willBeNext = False
                if  len(self.driver.find_elements_by_css_selector(".row.selected .noprogram.cell.selected")) < 1:
                    for e in elements:
                        if willBeNext:
                            nextProgram = e.text.encode('utf-8')
                            break
                        if e.get_attribute("class").find("selected") > -1:
                            willBeNext = True

                # clock
                clock = None
                try:
                    dateTxt = self.driver.find_element_by_css_selector(".breadcrumb .clock").text.encode('utf-8')
                    day = dateTxt.split(" ")[0]
                    hour = dateTxt.split(" ")[1]
                    clock = datetime(int(day.split("/")[2]), int(day.split("/")[1]), int(day.split("/")[0]), int(hour.split(":")[0]), int(hour.split(":")[1]))
                except:
                    clock = None

                # csa level
                csaClass = None
                try:
                    element = self.driver.find_element_by_css_selector(".epg .grid.programInfo .description .pictoBox .pictoCsa")
                    cssClasses = element.get_attribute("class").encode('utf-8').split(" ")
                    for index in range(0, len(cssClasses)):
                        if cssClasses[index] != u"pictoCsa".encode('utf-8'):
                            csaClass = cssClasses[index]
                            break
                except:
                    csaClass = None

                # start date and length
                start = None
                length = None
                element = self.driver.find_element_by_css_selector(".epg .grid.programInfo .description .date")
                if len(element.text) > 10 :
                    startTxt = element.text.split(" ")[0]
                    now = datetime.now()
                    start = datetime(now.year, now.month, now.day, int(startTxt.split(":")[0]), int(startTxt.split(":")[1]))

                    endTxt = element.text.split(" ")[2]
                    now = datetime.now()
                    end = datetime(now.year, now.month, now.day, int(endTxt.split(":")[0]), int(endTxt.split(":")[1]))
                    if end < start :
                        end = end + timedelta(days=1)
                    length = end - start

                # REC icon verification
                recording = False
                if len(self.driver.find_elements_by_css_selector(".epg .grid .content .cellContainers .cellContainer.selected .cell.selected .recording")) > 0:
                    recording = True

                # reminder icon verification
                reminder = False
                if len(self.driver.find_elements_by_css_selector(".epg .grid .content .cellContainers .cellContainer.selected .cell.selected .favorite")) > 0:
                    reminder = True

                self.programInfo = ProgramInfoItem(lcn, channelName.encode('utf-8'), program, start, length, genre, favorite, nextProgram, clock=clock, csaClass=csaClass, recording=recording, reminder=reminder)
                return True

            else:
                return False
        except Exception, e:
            # raise
            self.logger.info("Error occured + " + str(e))
            return False

    def loadMosaic(self):
        self.logger.debug("  >>   loadMosaic")

        self.grid = []
        channelFocus = None
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            if len(self.driver.find_elements_by_css_selector(".scene.mosaicView")) > 0:
                    self.grid.append([])
                    elements = self.driver.find_elements_by_css_selector(".scene.mosaicView .mosaic .mosaicItem.row1")
                    for index, element in enumerate(elements):
                        self.grid[0].append(element.find_element_by_css_selector(".focusLabel").text)
                        if element.get_attribute("class").find("highlight") > -1:
                            channelFocus = self.grid[0][index]

                    self.grid.append([])
                    elements = self.driver.find_elements_by_css_selector(".scene.mosaicView .mosaic .mosaicItem.row2")
                    for index, element in enumerate(elements):
                        self.grid[1].append(element.find_element_by_css_selector(".focusLabel").text)
                        if element.get_attribute("class").find("highlight") > -1:
                            channelFocus = self.grid[1][index]

                    self.grid.append([])
                    elements = self.driver.find_elements_by_css_selector(".scene.mosaicView .mosaic .mosaicItem.row3")
                    for index, element in enumerate(elements):
                        self.grid[2].append(element.find_element_by_css_selector(".focusLabel").text)
                        if element.get_attribute("class").find("highlight") > -1:
                            channelFocus = self.grid[2][index]

                    self.grid.append([])
                    elements = self.driver.find_elements_by_css_selector(".scene.mosaicView .mosaic .mosaicItem.row4")
                    for index, element in enumerate(elements):
                        self.grid[3].append(element.find_element_by_css_selector(".focusLabel").text)
                        if element.get_attribute("class").find("highlight") > -1:
                            channelFocus = self.grid[3][index]

                    element = self.driver.find_element_by_css_selector(".scene.mosaicView .mosaicTooltip")

                    programFocus = element.find_element_by_css_selector(".program").text.encode('utf-8')
                    programGenreFocus = element.find_element_by_css_selector(".kind").text.encode('utf-8')

                    alltxt_list = channelFocus.split(u'. ')
                    channelNum = int(alltxt_list[0])
                    channelTxt = (alltxt_list[1]).encode('utf-8')
                    inter = " "

#                     channelTxt=""
#                     inter=""
#                     for index in range(2,len(alltxt_list)):
#                         channelTxt=channelTxt+inter+alltxt_list[index]
#                         inter=" "

                    self.programInfo = ProgramInfoItem(channelNum, channelTxt, programFocus, None, None, programGenreFocus, None, None)
                    return True

        except Exception:
            # raise
            return False

    def loadRecord(self):
        self.logger.debug("  >>   loadRecord")

        time.sleep(3)
        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            domElement = None

            if len(self.driver.find_elements_by_css_selector(".recordMosaic .itemsContainer .item")) > 0:
                domElement = self.driver.find_element_by_css_selector(".recordMosaic .itemsContainer .focused")
            elif len(self.driver.find_elements_by_css_selector(".schedulingMosaic .itemsContainer .item")) > 0:
                domElement = self.driver.find_element_by_css_selector(".schedulingMosaic .itemsContainer .focused")
            else:
                return False

            focusTitle = domElement.find_element_by_css_selector(".title").text.encode('utf-8')
            details = domElement.find_element_by_css_selector(".status").text  # beginnig date is in the element with class "status" - don't know why....
            if details.find("niekompletne") != -1:
                focusDate = None
            else:
                dateTxt = details.split(" ")[0]
                hourTxt = details.split(" ")[1]
                focusDate = datetime(int(dateTxt.split("/")[2]), int(dateTxt.split("/")[1]), int(dateTxt.split("/")[0]), int(hourTxt.split(":")[0]), int(hourTxt.split(":")[1]))

            # REC icon verification
            if len(domElement.find_elements_by_css_selector(".recordingPicto")) == 0:  # is icon on the page
                return False
            recElementStyle = domElement.find_element_by_css_selector(".recordingPicto").get_attribute("style").encode('utf-8')
            if recElementStyle.find(u"display: none;".encode('utf-8')) > -1:  # if icon is hidden
                focusRecording = False
            else:
                focusRecording = True

            self.recordItem = RecordItem(focusTitle, focusDate, recording=focusRecording)

            return True

        except Exception, e:
            # raise
            self.logger.info("  >>>   error occured: " + str(e))
            return False

    def loadRecordDetailed(self):
        self.logger.debug("  >>   loadRecordDetailed")

        self.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            domElement = self.driver.find_element_by_css_selector(".pvrRecordDetails .recordInfo")

            recordTitle = domElement.find_element_by_css_selector(".scrollarea .title").text.encode('utf-8')

            # date and lenght
            elements = domElement.find_elements_by_css_selector(".leftContainer div.date")
            for index in range(0, len(elements)):

                elementTxt = elements[index].text.encode('utf-8')
                if elementTxt.find(u" - ".encode('utf-8')) > -1:
                    startHourTxt = elementTxt.split(" - ")[0]
                    endHourTxt = elementTxt.split(" - ")[1]
                else:
                    dateTxt = elementTxt
            # date
            recordStartDate = datetime(int(dateTxt.split('/')[2]), int(dateTxt.split('/')[1]), int(dateTxt.split('/')[0]), \
                            int(startHourTxt.split(":")[0]), int(startHourTxt.split(":")[1]))
            # lenght
            recordEndDate = datetime(int(dateTxt.split('/')[2]), int(dateTxt.split('/')[1]), int(dateTxt.split('/')[0]), \
                            int(endHourTxt.split(":")[0]), int(endHourTxt.split(":")[1]))
            if recordEndDate < recordStartDate:
                recordEndDate = recordEndDate + timedelta(days=1)
            recordLength = recordEndDate - recordStartDate

            # csa level
            recordCsaClass = None
            try:
                element = domElement.find_element_by_css_selector(".leftContainer .pictoBox .pictoCsa")
                cssClasses = element.get_attribute("class").encode('utf-8').split(" ")
                for index in range(0, len(cssClasses)):
                    if cssClasses[index] != u"pictoCsa".encode('utf-8'):
                        recordCsaClass = cssClasses[index]
                        break
            except:
                recordCsaClass = None

            # REC icon verification
            if len(domElement.find_elements_by_css_selector(".recordingPicto.toSeeOrNot")) > 0:
                recordRecording = True
            else:
                recordRecording = False

            self.recordDetailedItem = RecordDetailedItem(recordTitle, recordStartDate, recordLength, recording=recordRecording, csaClass=recordCsaClass)
            return True

        except:
            # raise
            return False

    def capturePage(self):
        try:
            self.driver.save_screenshot('screen.png')
        except Exception:
            # raise
            return False

    '''
    ##############################################################################################################
    ################################# START OF THE HIGH LEVEL API FUNCTIONS PART #################################
    ##############################################################################################################
    '''

    def goToMenu(self):
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(5)

        return True

    def goToMySettings(self):
        self.logger.debug("  >>   goToMySettings")

        self.goToMenu()

        if (not self.actionSelect(Menu.myAccount)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.myAccount + "<")
            return False
        time.sleep(5)
        if (not self.actionSelect(Menu.mySettings)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.mySettings + "<")
            return False
        time.sleep(3)

        return True

    def goToTvSettings(self):
        self.logger.debug("  >>   goToTvSettings")

        self.goToMenu()

        if (not self.actionSelect(Menu.myAccount)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.myAccount + "<")
            return False
        time.sleep(8)
        if (not self.actionSelect(Menu.tvSettings)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.tvSettings + "<")
            return False
        time.sleep(3)

        return True

    def goToVodMenu(self):
        self.logger.debug("  >>   goToVodMenu")

        self.goToMenu()

        if (not self.actionSelect(Menu.videoOnDemand)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.videoOnDemand + "<")
            return False
        time.sleep(8)

        # check if it is in the VoD menu - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in the VoD menu")
            return False

        return True

    def goToPvrMenu(self):
        self.logger.debug("  >>   goToPvrMenu")

        self.goToMenu()

        if (not self.actionSelect(Menu.pvr)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvr + "<")
            return False

        time.sleep(8)

        if self.findInDialogBox(Menu.hardDrive):
            self.logger.error("   ERR   problem with the hard drive")
            return False

        # check if it is in the PVR menu - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.pvrTV, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in the PVR menu")
            return False

        return True

    def goToVodMyVideos(self, fromVodMenu=False, inAdults=False):
        self.logger.debug("  >>   goToVodMyVideos - fromVodMenu >" + str(fromVodMenu) + "< - inAdults >" + str(inAdults) + "<")

        if (not fromVodMenu):
            if (not self.goToVodMenu()):
                self.logger.info("  >>   ERR: problem in function >goToVodMenu<")
                return False

        if inAdults:
            if (not self.goToVodAdults(fromVodMenu=True)):
                self.logger.info("  >>   ERR: problem in function >goToVodAdults<")
                return False

        if (not self.actionSelect(Menu.vodMyVideos)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodMyVideos + "<")
            return False
        time.sleep(8)
        # check if it is in the my videos menu
        if (not self.findInCssSelectorElement(Menu.vodMyVideos, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in my videos menu")
            return False

        return True

    def goToVodFavorites(self, fromVodMenu=False, inAdults=False):
        self.logger.debug("  >>   goToVodFavorites - fromVodMenu >%s" % fromVodMenu + "< - inAdults >%s" % inAdults + "< ")

        if (not fromVodMenu):
            if (not self.goToVodMenu()):
                self.logger.info("  >>   ERR: problem in function >goToVodMenu<")
                return False

        if inAdults:
            if (not self.goToVodAdults(fromVodMenu=True)):
                self.logger.info("  >>   ERR: problem in function >goToVodAdults<")
                return False

        if (not self.actionSelect(Menu.vodMyFavorites)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodMyFavorites + "<")
            return False
        time.sleep(8)
        # check if it is in the my favorites menu
        if (not self.findInCssSelectorElement(Menu.vodMyFavorites, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in my favorites menu")
            return False

        return True

    def goToVodAdults(self, fromVodMenu=False):
        self.logger.debug("  >>   goToVodAdults - fromVodMenu >%s" % fromVodMenu + "< ")

        if (not fromVodMenu):
            if (not self.goToVodMenu()):
                self.logger.info("  >>   ERR: problem in function >goToVodMenu<")
                return False

        if (not self.actionSelect(Menu.vodAdults)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodAdults + "<")
            return False
        time.sleep(8)

        # for adults
        if (not self.findInDialogBox(Menu.parentalControl)):
            self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
            return False
        self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
        self.rc.sendKeys(["KEY_OK"])
        if self.findInDialogBox(DialogBox.WrongConfidentialCode):
            self.logger.info("  >>   ERR: wrong confidential code")
            return False
        # check if it is in the adult menu - #TODO better check because of the wrong PIN POPUP
        if (not self.findInCssSelectorElement(Menu.vodAdults, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in the adult menu")
            return False

        return True

    def goToVodCatalog(self, vodCat):
        self.logger.debug("  >>   goToVodCatalog >" + vodCat + "<")

        if (not self.goToVodMenu()):
            self.logger.info("  >>   ERR: problem in function >goToVodMenu<")
            return False

        if (not self.actionSelect(Menu.vodCatalog)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodCatalog + "<")
            return False
        time.sleep(8)
        if (not self.actionSelect(vodCat)):
            self.logger.info("  >>   ERR: problem selecting >" + vodCat + "<")
            return False

        time.sleep(10)

        if (not self.findInCssSelectorElement(vodCat, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in the >" + vodCat + "<")
            return False

        time.sleep(10)

        items = self.getList()
        if not items:
            self.logger.info("  >>   ERR: cannot find any movie list")
            return False

        return True

    def startVodIfNotPlayed(self, goBackToVodScreen=False):
        self.logger.debug("  >>   startVodIfNotPlayed - goBackToVodScreen >" + str(goBackToVodScreen) + "<")

        maxWaitingTime = 7200
        stepWaitingTime = 5

        # DTH VoD downloading popup recognition
        # if there is popup with proper command on the list
        startTimestamp = time.time()
        if self.findInList(Menu.vodStartWatching):
            # wait until the command will be available
            while not self.findInList(Menu.vodStartWatching, onlyActive=True):
                if (time.time() - startTimestamp > maxWaitingTime):
                    self.logger.info("  >>   ERR: startVodIfNotPlayed - max waiting time exceeded")
                    return False
                self.logger.debug("  >>   startVodIfNotPlayed - vod downloading - waiting...")
                time.sleep(stepWaitingTime)
            # start watching
            if (not self.actionSelect(Menu.vodStartWatching)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.vodStopWatching + "<")
                return False
            time.sleep(20)

            if self.findInDialogBox(DialogBox.VodError2):
                self.logger.info("  >>   ERR: general error >" + DialogBox.VodError2 + "<")
                return False

        # is currently played - simple motion detection - TODO better check
        if Env.VIDEO:
            self.logger.debug("  >>   motionDetection")
            if (not motionDetection()):
                self.logger.info("  >>   ERR: problem checking motionDetection")
                return False

        # go back to VPS
        if goBackToVodScreen:
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(3)

            # one time VoD popup recognition
            if self.findInDialogBox(Menu.vodInfo):
                if (not self.actionSelect(Menu.vodStopWatching)):
                    self.logger.info("  >>   ERR: problem selecting >" + Menu.vodStopWatching + "<")
                    return False
                time.sleep(3)

        return True

    def startVodIfNotPlayedAndGoBackToVodCatalog(self):
        self.logger.debug("  >>   startVodIfNotPlayedAndGoBackToVodCatalog")

        if (not self.startVodIfNotPlayed(goBackToVodScreen=True)):
            self.logger.info("  >>   ERR: problem in function >startVodIfNotPlayed<")
            return False

        self.rc.sendKeys(["KEY_BACK"])

        return True

    def goToVodToAddToFavoritesInCatalog(self, count_vod_max_search=30):
        self.logger.debug("  >>   goToVodToAddToFavoritesInCatalog")

        # check is it in some VoD catalog, to prevent browsing in a wrong place - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in Vod catalog")
            return False

        self.rc.sendKeys(["KEY_OK"])

        for x in range(0, count_vod_max_search):
            time.sleep(3)
            if self.findInList(Menu.vodAddToFavorites):
                return True
            else:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(3)

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToVodToRemoveFromFavoritesInCatalog(self, count_vod_max_search=30):
        self.logger.debug("  >>   goToVodToRemoveFromFavoritesInCatalog")

        # check is it in some VoD catalog, to prevent browsing in a wrong place - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in Vod catalog")
            return False

        self.rc.sendKeys(["KEY_OK"])

        for x in range(0, count_vod_max_search):
            time.sleep(3)
            if self.findInList(Menu.vodRemoveFromFavorites):
                return True
            else:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(3)

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToVodToRentInCatalog(self, trailerActive=False, count_vod_max_search=30):
        self.logger.debug("  >>   goToVodToRentInCatalog - trailerActive >" + str(trailerActive) + "<")

        # check is it in some VoD catalog, to prevent browsing in a wrong place - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in Vod catalog")
            return False

        self.rc.sendKeys(["KEY_OK"])

        for x in range(0, count_vod_max_search):
            time.sleep(5)
            try:
                self.driver.get(Rpi.DUMP)
                time.sleep(1)
                self.driver.find_element_by_xpath("//div[@id='pictoCsa']")
            except Exception:
                if not self.loadVodPage():
                    self.logger.info("  >>   ERR: not in Vod, error occured while vod traversal")
                    return False
                self.rc.sendKeys(["KEY_RIGHT"])
                continue

            if self.findInList(Menu.vodRent):
                if trailerActive:
                    if self.findInList(Menu.vodTrailer, onlyActive=True):
                        return True
                else:
                    return True
            else:
                self.rc.sendKeys(["KEY_RIGHT"])

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToVodToRentInCatalogByCsaCategory(self, csaCat, trailerActive=False, count_vod_max_search=30):
        self.logger.debug("  >>   goToVodToRentInCatalogByCsaCategory - csaCat >" + str(csaCat) + "< - trailerActive >" + str(trailerActive) + "<")

        # check is it in some VoD catalog, to prevent browsing in a wrong place - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in Vod catalog")
            return False

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)

        for x in range(0, count_vod_max_search):
            try:
                self.driver.get(Rpi.DUMP)
                time.sleep(1)
                csa = self.driver.find_element_by_xpath("//div[@id='pictoCsa']")
                csa = csa.get_attribute("class").split(' ')[1]
            except Exception:
                if not self.loadVodPage():
                    self.logger.info("  >>   ERR: not in Vod, error occured while vod traversal")
                    return False
                self.rc.sendKeys(["KEY_RIGHT"])
                continue
            if type(csaCat) == list:
                if csa in csaCat and self.findInList(Menu.vodRent):
                    if trailerActive:
                        if self.findInList(Menu.vodTrailer, onlyActive=True):
                            return True
                        else:
                            self.rc.sendKeys(["KEY_RIGHT"])
                    else:
                        return True
                else:
                    self.rc.sendKeys(["KEY_RIGHT"])
                    time.sleep(3)
            elif self.findInXPathElementClass(csaCat, "//div[@id='pictoCsa']") and self.findInList(Menu.vodRent):  # is correct csa picto
                if trailerActive:
                    if self.findInList(Menu.vodTrailer, onlyActive=True):
                        return True
                else:
                    return True
            else:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(3)

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToPvrMyRecords(self, inAdults=False, shouldBeEmpty=False):
        """It goes to the my records screen in PVR menu
        
        @precondition: none
        @param inAdults: in adults PVR menu, default is False (type: boolean)
        @param shouldBeEmpty: the my records list should be empty, default is False (type: boolean)
        @return: True if expected place has reached, False if not and None if an error has occured
        @author: Leszek Wawrzonkowski
        """
        self.logger.debug("  >>   goToPvrMyRecords - inAdults >" + str(inAdults) + "< - shouldBeEmpty >" + str(shouldBeEmpty) + "<")

        if (not self.goToPvrMenu()):
            self.logger.info("  >>   ERR: problem in function >goToPvrMenu<")
            return None

        # for adults
        if inAdults:
            if (not self.actionSelect(Menu.pvrAdults)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrAdults + "<")
                return None
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return None
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)

        if (not self.actionSelect(Menu.pvrMyRecords)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrMyRecords + "<")
            return None
        if self.findInDialogBox(DialogBox.PvrNoRecords):
            if not shouldBeEmpty:
                self.logger.info("  >>   ERR: the list is empty")
                return False
            else:
                self.rc.sendKeys(["KEY_OK"])
                return True
        elif shouldBeEmpty:
            self.logger.info("  >>   ERR: the list is not empty")
            return False

        time.sleep(8)
        # check if it is in the my videos menu
        if (not self.findInCssSelectorElement(Menu.pvrMyRecords, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in my videos menu")
            return None

        return True

    def goToPvrMyScheduled(self, inAdults=False, shouldBeEmpty=False):
        """It goes to the my scheduled screen in PVR menu
        
        @precondition: none
        @param inAdults: in adults PVR menu, default is False (type: boolean)
        @param shouldBeEmpty: the my scheduled list should be empty, default is False (type: boolean)
        @return: True if expected place has reached, False if not and None if an error has occured
        @author: Leszek Wawrzonkowski
        """
        self.logger.debug("  >>   goToPvrMyScheduled - inAdults >" + str(inAdults) + "< - shouldBeEmpty >" + str(shouldBeEmpty) + "<")

        if (not self.goToPvrMenu()):
            self.logger.info("  >>   ERR: problem in function >goToPvrMenu<")
            return None

        # for adults
        if inAdults:
            if (not self.actionSelect(Menu.pvrAdults)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrAdults + "<")
                return None
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return None
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)

        if (not self.actionSelect(Menu.pvrMyScheduled)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrMyScheduled + "<")
            return None
        time.sleep(5)
        if self.findInDialogBox(DialogBox.PvrNoScheduled):
            if not shouldBeEmpty:
                self.logger.info("  >>   ERR: the list is empty")
                return False
            else:
                self.rc.sendKeys(["KEY_OK"])
                return True
        elif shouldBeEmpty:
            self.logger.info("  >>   ERR: the list is not empty")
            return False

        time.sleep(10)
        # check if it is in the my scheduled menu
        if (not self.findInCssSelectorElement(Menu.pvrMyScheduled, ".breadcrumb .last")):
            self.logger.info("  >>   ERR: not in my scheduled menu")
            return None

        return True

    def goToPvrByCsaCategory(self, csaCat, inAdults=False, count_pvr_max_search=10):
        self.logger.debug("  >>   goToPvrByCsaCategory - csaCat >" + csaCat + "< - inAdults >%s" % inAdults + "<")

        if (not self.goToPvrMyRecords(inAdults=inAdults)):
            self.logger.info("  >>   ERR: problem in function >goToPvrMyRecords<")
            return False

        for x in range(0, count_pvr_max_search):
            for y in range(0, x):
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(1)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            if self.findInXPathElementClass(csaCat, "//div[@id='pictoCsa']") and self.findInList(Menu.pvrPlay):  # is correct csa picto
                return True
            else:
                self.rc.sendKeys(["KEY_BACK"])
                time.sleep(2)

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToEpgProgramPlayedNowByCsaCategory(self, csaCat, count_tv_max_search=100):
        self.logger.debug("  >>   goToEpgProgramPlayedNowByCsaCategory - csaCat >" + csaCat + "<")

        self.rc.sendKeys(["KEY_TV"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_1"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(3)
        if (not self.actionSelect(Menu.epg)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.epg + "<")
            return False
        time.sleep(3)
        if (not self.actionSelect(Menu.epgWeek)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.epgWeek + "<")
            return False

        for x in range(0, count_tv_max_search):
            if self.findInXPathElementClass(csaCat, "//div[@id='pictoCsa']"):  # is correct csa picto
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)
                if self.findInList(Menu.epgPlay, onlyActive=True):
                    return True
                else:
                    self.rc.sendKeys(["KEY_BACK"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_DOWN"])
                    time.sleep(2)
            else:
                self.rc.sendKeys(["KEY_DOWN"])
                time.sleep(2)

        self.logger.info("  >>   ERR: element not found")
        return False

    def goToLiveByCsaCategory(self, csaCat=None, count_tv_max_search=100):
        self.logger.debug("  >>   goToLiveByCsaCategory - csaCat >" + str(csaCat) + "<")

        self.rc.sendKeys(["KEY_TV"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_0"])
        time.sleep(3)

        for x in range(0, count_tv_max_search):
            try:
                self.rc.sendKeys(["KEY_CHANNELUP"])
                self.rc.sendKeys(["KEY_INFO"])
                currentProgramInfo = self.getInfoFromLiveBanner()
                if (type(currentProgramInfo) is ProgramInfoItem):
                    if ((csaCat is None) or (currentProgramInfo.getCsaClass() == csaCat)):
                        # is currently played - simple motion detection - TODO better check
                        if Env.VIDEO:
                            if (not motionDetection()):
                                continue
                            self.rc.sendKeys(["KEY_INFO"])
                            return True
                        else:
                            self.rc.sendKeys(["KEY_INFO"])
                            return True
            except Exception:
                continue

        self.logger.info("  >>   ERR: element not found")
        return False

    def setParentalControl(self, level):
        self.logger.debug("  >>   setParentalControl - level >" + level + "<")

        # go to parental control settings screen
        if (not self.goToMySettings()):
            self.logger.info("  >>   ERR: problem in function >goToMySettings<")
            return False
        time.sleep(2)
        if (not self.actionSelect(Menu.parentalControl)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.parentalControl + "<")
            return False
        time.sleep(2)
        # verify the POPUP and send code
        if (not self.findInDialogBox(Menu.parentalControl)):
            self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
            return False
        self.rc.sendNumberSequence(Env.PARENTAL_CODE)
        self.rc.sendKeys(["KEY_OK"])

        # verify the POPUP
        if (not self.findInDialogBox(Menu.parentalControl)):
            self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
            return False

        # set proper level and verify the result
        if level == ParentalControl.SetDeactive:
            if (not self.actionSelect(ParentalControl.deactivate)):
                self.logger.info("  >>   ERR: problem selecting >" + ParentalControl.deactivate + "<")
                return False
            time.sleep(4)

            # verification
            if (not self.findInXPathElement(ParentalControl.IsDeactivatedDesc, "//span[@class='value']")):  # is deactive description presented
                self.logger.info("  >>   ERR: deactive description not presented")
                return False
            if (not self.findInXPathElement("", "//span[@class='parentalCtrlIcon']")):  # is icon on the page
                self.logger.info("  >>   ERR: parentalCtrlIcon not on the page source")
                return False
            if (not self.findInXPathElementStyle(u"display: none;".encode('utf-8'), "//span[@class='parentalCtrlIcon']")):  # is icon hidden
                self.logger.info("  >>   ERR: parentalCtrlIcon not hidden")
                return False
        else:
            if (not self.actionSelect(ParentalControl.Activate)):
                self.logger.info("  >>   ERR: problem selecting >" + ParentalControl.Activate + "<")
                return False
            time.sleep(2)
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False

            csaChoice = ""
            csaDesc = ""

            if level == ParentalControl.SetActiveCsa2:
                csaChoice = ParentalControl.ActivateCsa2
                csaDesc = ParentalControl.IsActivatedCsa2Desc
            elif level == ParentalControl.SetActiveCsa3:
                csaChoice = ParentalControl.ActivateCsa3
                csaDesc = ParentalControl.IsActivatedCsa3Desc
            elif level == ParentalControl.SetActiveCsa4:
                csaChoice = ParentalControl.ActivateCsa4
                csaDesc = ParentalControl.IsActivatedCsa4Desc
            else:
                # level unsupported
                self.logger.info("  >>   ERR: setParentalControl - level unsupported")
                return False

            if (not self.actionSelect(csaChoice)):
                self.logger.info("  >>   ERR: problem selecting >" + csaChoice + "<")
                return False
            time.sleep(4)

            # verification
            if (not self.findInXPathElement(ParentalControl.IsActivatedDesc, "//span[@class='value']")):  # is active description presented
                self.logger.info("  >>   ERR: active description not presented")
                return False
            if (not self.findInXPathElement(csaDesc, "//span[@class='orange']")):  # is level description presented
                self.logger.info("  >>   ERR: level description not presented")
                return False
            if (not self.findInXPathElement("", "//span[@class='parentalCtrlIcon']")):  # is icon on the page
                self.logger.info("  >>   ERR: parentalCtrlIcon not on the page source")
                return False
            if (self.findInXPathElementStyle(u"display: none;".encode('utf-8'), "//span[@class='parentalCtrlIcon']")):  # is icon not hidden
                self.logger.info("  >>   ERR: parentalCtrlIcon hidden")
                return False

        return True

    def rentVodThenPlay(self, checkParentalControl=False, goBackToVodScreen=False):
        self.logger.debug("  >>   rentVodThenPlay - checkParentalControl >" + str(checkParentalControl) + "< - goBackToVodScreen >" + str(goBackToVodScreen) + "<")
        vod_title = self.getInfoFromVodPage().title
        # vod_title = unicode(self.getInfoFromVodPage().title, 'utf-8')
        self.logger.info(" - VOD to rent >" + vod_title + "<")

        if (not self.actionSelect(Menu.vodRent)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodRent + "<")
            return False
        time.sleep(3)
        adultCodeTypedIn = False
        # purchase check (when no cash on the PREPAID account) - TODO to be sure if it should be check or not
        if self.findInDialogBox(Menu.vodAdultPopup):
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            if self.findInDialogBox(DialogBox.WrongConfidentialCode):
                self.logger.info("  >>   ERR: wrong confidential code")
                return False
            adultCodeTypedIn = True

        # parental control check
        if checkParentalControl and not adultCodeTypedIn:
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            if self.findInDialogBox(DialogBox.WrongParentalCode):
                self.logger.info("  >>   ERR: wrong parental code")
                return False
        elif checkParentalControl and adultCodeTypedIn:
            pass
        else:
            if self.findInDialogBox(Menu.parentalControl):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False

        time.sleep(10)

        # NPK
        if not self.findInDialogBox(Menu.vodNPK):
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodNPK + "<")
            return False
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        if self.findInDialogBox(Menu.vodNPKInfo):
            self.rc.sendKeys(["KEY_OK"])

        time.sleep(1)

        if self.findInDialogBox(DialogBox.VodError):  # TODO correct error description
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            return False
        if self.findInDialogBox(DialogBox.VodError2):
            self.logger.info("  >>   ERR: general error >" + DialogBox.VodError2 + "<")
            return False
        if self.findInDialogBox(DialogBox.VodError3):
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError3 + "<")
            return False
        if self.findInCssSelectorElement("menu", ".breadCrumb .path .first"):
            self.logger.info("  >>   ERR: problem with video playback, im back in main menu")
            return False

        time.sleep(10)

        if (self.startVodIfNotPlayed(goBackToVodScreen=goBackToVodScreen)):
            return True
        else:
            self.logger.info("  >>   ERR: problem in function >startVodIfNotPlayed<")
            return False

        return True

    def rentVodThenPlayAndBackToVodScreen(self, checkParentalControl=False):
        self.logger.debug("  >>   rentVodThenPlayAndBackToVodScreen - checkParentalControl >%s" % checkParentalControl + "<")

        if (not self.rentVodThenPlay(checkParentalControl=checkParentalControl, goBackToVodScreen=True)):
            self.logger.info("  >>   ERR: problem in function >rentVodThenPlay<")
            return False

        return True

    def watchVodTrailerThenBackToVodScreen(self, checkParentalControl=False):
        self.logger.debug("  >>   watchVodTrailerThenBackToVodScreen - checkParentalControl >%s" % checkParentalControl + "<")
        vod_title = self.getInfoFromVodPage().title.encode('utf-8')
        self.logger.info(" - VOD to watch trailer >" + vod_title + "<")

        maxWaitingTime = 600
        stepWaitingTime = 5

        if (not self.actionSelect(Menu.vodTrailer)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.vodTrailer + "<")
            return False
        # parental control check
        if checkParentalControl:
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
        else:
            if self.findInDialogBox(Menu.parentalControl):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False

        time.sleep(2)
        # DTH trailer downloading popup recognition
        startTimestamp = time.time()
        while self.findInDialogBox(Menu.vodTrailerDownloading):
            if (time.time() - startTimestamp > maxWaitingTime):
                self.logger.info("  >>   ERR: max waiting time exceeded - break")
                return False
            self.logger.debug("  >>   watchVodTrailerThenBackToVodScreen - trailer downloading - waiting...")
            time.sleep(stepWaitingTime)

        time.sleep(10)

        # is currently played - simple motion detection - TODO better check
        if Env.VIDEO:
            self.logger.debug("  >>   motionDetection")
            if (not motionDetection()):
                self.logger.info("  >>   ERR: problem checking motionDetection")
                return False

        # TODO perhaps motion detection will be helpful to check if trailer is still playing
        startTimestamp = time.time()
        while True:
            if (time.time() - startTimestamp > maxWaitingTime):
                self.logger.info("  >>   ERR: max waiting time exceeded - break")
                return False
            try:
                if self.getInfoFromVodPage().title.encode('utf-8') == vod_title:
                    break
                self.logger.debug("  >>   watchVodTrailerThenBackToVodScreen - trailer playing - waiting...")
                time.sleep(stepWaitingTime)
            except:
                self.logger.debug("  >>   watchVodTrailerThenBackToVodScreen - trailer playing - waiting...")
                time.sleep(stepWaitingTime)

        return True

    def playRentedVod(self, checkParentalControl=False, goBackToVodScreen=False):
        self.logger.debug("  >>   playRentedVod - checkParentalControl >" + str(checkParentalControl) + "< - goBackToVodScreen >" + str(goBackToVodScreen) + "<")
        # vod_title = self.getInfoFromVodPage().title.encode('utf-8')
        vod_title = self.getInfoFromVodPage().title
        self.logger.info(" - VOD to play >" + vod_title + "<")

        if self.findInList(Menu.vodPlay):
            if (not self.actionSelect(Menu.vodPlay)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.vodPlay + "<")
                return False
        elif self.findInList(Menu.vodResume):
            if (not self.actionSelect(Menu.vodResume)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.vodResume + "<")
                return False
        else:
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodPlay + "< or >" + Menu.vodResume + "<")
            return False
        # parental control check
        if checkParentalControl:
            if (not self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
        else:
            if self.findInDialogBox(Menu.parentalControl):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False
        time.sleep(20)
        if self.findInDialogBox(DialogBox.VodError):  # TODO correct error description
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            return False
        if (not self.startVodIfNotPlayed(goBackToVodScreen=goBackToVodScreen)):
            self.logger.info("  >>   ERR: problem in function >startVodIfNotPlayed<")
            return False

        return True

    def playRentedVodThenBackToVodScreen(self, checkParentalControl=False):
        self.logger.debug("  >>   playRentedVodThenBackToVodScreen - checkParentalControl >%s" % checkParentalControl + "<")

        if (not self.playRentedVod(checkParentalControl=checkParentalControl, goBackToVodScreen=True)):
            self.logger.info("  >>   ERR: problem in function >playRentedVod<")
            return False

        return True

    def rentAndPlayOrPlayRentedVod(self, checkParentalControl=False, goBackToVodScreen=False):
        self.logger.debug("  >>   rentAndPlayOrPlayRentedVod - checkParentalControl >" + str(checkParentalControl) + "< - goBackToVodScreen >" + str(goBackToVodScreen) + "<")

        if self.findInList(Menu.vodRent):
            if (not self.rentVodThenPlay(checkParentalControl=checkParentalControl, goBackToVodScreen=goBackToVodScreen)):
                self.logger.info("  >>   ERR: problem in function >rentVodThenPlay<")
                return False
        elif self.findInList(Menu.vodPlay) or self.findInList(Menu.vodResume):
            if (not self.playRentedVod(checkParentalControl=checkParentalControl, goBackToVodScreen=goBackToVodScreen)):
                self.logger.info("  >>   ERR: problem in function >playRentedVod<")
                return False
        else:
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodRent + "< or >" + Menu.vodPlay + "< or >" + Menu.vodResume + "<")
            return False

        return True

    def playPvrThenBackToPvrScreen(self, checkParentalControl=False, playDuration=0):
        self.logger.debug("  >>   playPvrThenBackToPvrScreen - checkParentalControl >%s" % checkParentalControl + "< - playDuration >%s" % playDuration + "< ")

        if (not self.actionSelect(Menu.pvrPlay)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrPlay + "<")
            return False
        # parental control check
        if checkParentalControl:
            if (not self.findInDialogBox(DialogBox.PvrParentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + DialogBox.PvrParentalControl + "<")
                return False
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
        else:
            if self.findInDialogBox(DialogBox.PvrParentalControl):
                self.logger.info("  >>   ERR: problem finding >" + DialogBox.PvrParentalControl + "<")
                return False
        time.sleep(10)
        if self.findInDialogBox(DialogBox.VodError):  # TODO correct error description
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            return False
        time.sleep(playDuration)
        # is currently played - simple motion detection - TODO better check
        if Env.VIDEO:
            self.logger.debug("  >>   motionDetection")
            if (not motionDetection()):
                self.logger.info("  >>   ERR: problem checking motionDetection")
                return False


        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)

        return True

    def deletePvrRecord(self, running=False):
        self.logger.debug("  >>   deletePvrRecord - running >%s<" % running)

        if running:
            if not self.actionSelect(Menu.pvrStop2):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrStop2 + "<")
                return False
            time.sleep(2)
            if not self.findInDialogBox(Menu.pvrStop):
                self.logger.info("  >>   ERR: problem finding >" + Menu.pvrStop + "<")
                return False
            time.sleep(2)
            if not self.actionSelect(Menu.pvrYes):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrYes + "<")
                return False
            if not self.findInDialogBox(Menu.pvrStopRecordConfirm):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrStopRecordConfirm + "<")
                return False
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
        if not self.actionSelect(Menu.pvrDelete):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrDelete + "<")
            return False
        if not self.findInDialogBox(DialogBox.PvrDeleteRecord):
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.PvrDeleteRecord + "<")
            return False
        if not self.actionSelect(Menu.pvrYes):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrYes + "<")
            return False
        time.sleep(1)
        if self.findInDialogBox(DialogBox.PvrDeleteRecordError):
            self.logger.info("  >>   ERR: cannot delete record: '{}' message".format(DialogBox.PvrDeleteRecordError))
            return False

        return True

    def playEpgProgram(self, checkNotParentalControl=True):
        self.logger.debug("  >>   playEpgProgram - checkNotParentalControl >%s" % checkNotParentalControl + "<")

        # check is it in some epg catalog - TODO maybe better check
        if (not self.findInCssSelectorElement(Menu.epg, ".breadcrumb .first")):
            self.logger.info("  >>   ERR: not in some epg catalog")
            return False

        if (not self.actionSelect(Menu.epgPlay)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.epgPlay + "<")
            return False
        # parental control check
        if checkNotParentalControl:
            if (self.findInDialogBox(Menu.parentalControl)):
                self.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False

        time.sleep(10)

        # is currently played - simple motion detection - TODO better check
        if Env.VIDEO:
            self.logger.debug("  >>   motionDetection")
            if (not motionDetection()):
                self.logger.info("  >>   ERR: problem checking motionDetection")
                return False

        return True

    def verifyVodVpsScreen(self, csaCat=None, trailerNotActive=False):
        self.logger.debug("  >>   verifyVodVpsScreen - csaCat >" + str(csaCat) + "< - trailerNotActive >" + str(trailerNotActive) + "<")
        vodItem = self.getInfoFromVodPage()
        if not (type(vodItem) is VodItem):
            self.logger.info("  >>   ERR: wrong VoD data")
            return False

        self.logger.info(" - VOD to verify VPS >" + vodItem.getTitle() + "<")

        if not (self.findInList(Menu.vodRent) or self.findInList(Menu.vodPlay) or self.findInList(Menu.vodResume)):
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodRent + "< or >" + Menu.vodPlay + "< or >" + Menu.vodResume + "<")
            return False

        if not self.findInList(Menu.vodTrailer, onlyActive=True):
            # error only when trailer should be active
            if not trailerNotActive:
                self.logger.info("  >>   ERR: problem finding >" + Menu.vodTrailer + "<")
                return False

        if not self.findInList(Menu.vodSummary, onlyActive=True):
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodSummary + "<")
            return False

        if not (self.findInList(Menu.vodAddToFavorites) or self.findInList(Menu.vodRemoveFromFavorites)):
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodAddToFavorites + "< or >" + Menu.vodRemoveFromFavorites + "<")
            return False

        if (csaCat is not None) and (not self.findInXPathElementClass(csaCat, "//div[@id='pictoCsa']")):
            self.logger.info("  >>   ERR: wrong CSA")
            return False

        # TODO verify the rest VPS screen elements in the 'vodItem' object

        return True

    def verifyPvrOnMyRecordsMosaic(self, title, altTitle, isRecording, startDate, maxMinutesDiff=1):
        self.logger.debug("  >>   verifyPvrOnMyRecordsMosaic - title >" + str(title) + "< - altTitle >" + str(altTitle) + "< - isRecording >" + str(isRecording) + "< - startDate >" + str(startDate) + "< - maxMinutesDiff >" + str(maxMinutesDiff) + "<")
        focusRecord = self.getInfoFromRecordFocus()
        if not (type(focusRecord) is RecordItem):
            self.logger.info("  >>   ERR: wrong record data")
            return False
        # focusRecord.display()

        # title check
        if not (focusRecord.getTitle() == title or focusRecord.getTitle() == altTitle):
            self.logger.info("  >>   ERR: wrong record name")
            return False
        # REC icon check
        if not focusRecord.getRecording() == isRecording:
            self.logger.info("  >>   ERR: REC icon doesn't found")
            return False
        # starting date check
        # print "START DELTA: " + str(focusRecord.getDate()-startDate)
        if not focusRecord.getDate() - startDate <= timedelta(minutes=maxMinutesDiff):
            self.logger.info("  >>   ERR: wrong start date")
            return False

        return True

    def verifyPvrOnSchedulingMosaic(self, title, altTitle, startDate, maxMinutesDiff=1):
        """Verification of the selected record item on the scheduling mosaic.
        
        Function checks if the record's title and the start date are like expected.
        
        @precondition: Go to My Scheduled in PVR Menu (adult or not), e.x. by function goToPvrMyScheduled
        @param title: expected title (type: str)
        @param altTitle: alternative version of the expected title (type: str)
        @param startDate: expected start date (type: datetime)
        @param maxMinutesDiff: maximum allowed difference between the expected start date and the record start date in minutes, default is 1 (type: int)
        @return: True if verificaton passed, False if not or error occured
        @author: Leszek Wawrzonkowski
        """
        self.logger.debug("  >>   verifyPvrOnSchedulingMosaic - title >" + str(title) + "< - altTitle >" + str(altTitle) + "< - startDate >" + str(startDate) + "< - maxMinutesDiff >" + str(maxMinutesDiff) + "<")
        focusRecord = self.getInfoFromRecordFocus()
        if not (type(focusRecord) is RecordItem):
            self.logger.info("  >>   ERR: wrong record data")
            return False
        # focusRecord.display()

        # title check
        if not (focusRecord.getTitle() == title or focusRecord.getTitle() == altTitle):
            self.logger.info("  >>   ERR: wrong record name")
            return False
        # starting date check
        # print "START DELTA: " + str(focusRecord.getDate()-startDate)
        if not focusRecord.getDate() - startDate <= timedelta(minutes=maxMinutesDiff):
            self.logger.info("  >>   ERR: wrong start date")
            return False

        return True

    def verifyPvrOnRecordScreen(self, title, altTitle, isRecording, startDate, lenght, csaClass=None, maxMinutesDiff=1):
        self.logger.debug("  >>   verifyPvrOnRecordScreen - title >" + str(title) + "< - altTitle >" + str(altTitle) + "< - isRecording >" + str(isRecording) + "< - startDate >" + str(startDate) + "< - lenght >" + str(lenght) + "< - csaClass >" + str(csaClass) + "< - maxMinutesDiff >" + str(maxMinutesDiff) + "<")
        pvrRecord = self.getInfoFromRecordPage()
        if not (type(pvrRecord) is RecordDetailedItem):
            self.logger.info("  >>   ERR: wrong record data")
            return False
        # pvrRecord.display()

        # title check
        if not (pvrRecord.getTitle() == title or pvrRecord.getTitle() == altTitle):
            self.logger.info("  >>   ERR: wrong record name")
            return False
        # REC icon check
        if not pvrRecord.getRecording() == isRecording:
            self.logger.info("  >>   ERR: REC icon doesn't found")
            return False
        # CSA check
        if not (csaClass is None):
            if not pvrRecord.getCsaClass() == csaClass:
                self.logger.info("  >>   ERR: wrong CSA")
                return False
        # starting date check
        # print "START DELTA: " + str(pvrRecord.getDate()-startDate)
        if not pvrRecord.getDate() - startDate <= timedelta(minutes=maxMinutesDiff):
            self.logger.info("  >>   ERR: wrong start date")
            return False
        # length check
        # print "LENGTH DELTA: " + str(pvrRecord.getLength()-timedelta(minutes = lenght))
        if not pvrRecord.getLength() - timedelta(minutes=lenght) <= timedelta(minutes=maxMinutesDiff):
            self.logger.info("  >>   ERR: wrong length")
            return False

        return True

    def waitForPvrNoCurrentAndScheduledRecords(self, maxWaitingTimeMin=100):
        self.logger.debug("  >>   waitForPvrNoCurrentAndScheduledRecords - maxWaitingTimeMin >" + str(maxWaitingTimeMin) + "<")

        maxWaitingTime = maxWaitingTimeMin * 60
        stepWaitingTime = 60

        startTimestamp = time.time()
        while True:
            if (time.time() - startTimestamp > maxWaitingTime):
                self.logger.info("  >>   ERR: max waiting time exceeded - break")
                return False

            # scheduled
            gotoResult = self.goToPvrMyScheduled(shouldBeEmpty=True)
            # error has occured
            if gotoResult is None:
                self.logger.info("  >>   ERR: problem in function >goToPvrMyScheduled<")
                return False
            # the list is not empty
            elif not gotoResult:
                time.sleep(stepWaitingTime)
                continue
            # my records #TODO probably last record check will be faster
            if (not self.actionSelect(Menu.pvrMyRecords)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrMyRecords + "<")
                return False
            if not self.findInDialogBox(DialogBox.PvrNoRecords):
                focusRecord = self.getInfoFromRecordFocus()
                if not (type(focusRecord) is RecordItem):
                    self.logger.info("  >>   ERR: wrong record data")
                    return False
                if focusRecord.getRecording():
                    time.sleep(stepWaitingTime)
                    continue
            else:
                self.rc.sendKeys(["KEY_OK"])

            # scheduled in adults
            gotoResult = self.goToPvrMyScheduled(inAdults=True, shouldBeEmpty=True)
            # error has occured
            if gotoResult is None:
                self.logger.info("  >>   ERR: problem in function >goToPvrMyScheduled<")
                return False
            # the list is not empty
            elif not gotoResult:
                time.sleep(stepWaitingTime)
                continue
            # my records in adults #TODO probably last record check will be faster
            if (not self.actionSelect(Menu.pvrMyRecords)):
                self.logger.info("  >>   ERR: problem selecting >" + Menu.pvrMyRecords + "<")
                return False
            if not self.findInDialogBox(DialogBox.PvrNoRecords):
                focusRecord = self.getInfoFromRecordFocus()
                if not (type(focusRecord) is RecordItem):
                    self.logger.info("  >>   ERR: wrong record data")
                    return False
                if focusRecord.getRecording():
                    time.sleep(stepWaitingTime)
                    continue
            else:
                self.rc.sendKeys(["KEY_OK"])

            break

        return True

    def setDTTChannels(self, activate):
        """Function turns on and search for or turns off DTT channels
 
        @precondition: Live channel displays
        @param activate:
                        >True      set DTT channels on and search for them
                        >False     set DTT channels off
        @return: True when function activate or deactivate DTT channels, False when error occurs
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   setDTTChannels - activate >" + str(activate) + "<")
        if not self.goToMenu():
            self.logger.info("  >>   ERR: not in Menu")
            return False
        if not self.actionSelect(Menu.myAccount):
            self.logger.info("  >>   ERR: not in MyAccount")
            return False
        if not self.actionSelect(Menu.tvSettings):
            self.logger.info("  >>   ERR: not in TV Settings")
            return False
        if not self.actionSelect(Menu.dttChannels):
            if not self.actionSelect(Menu.dttChannelsRFTV):
                self.logger.info("  >>   ERR: not in DTT channels")
                return False
        if activate:
            if not self.actionSelect(Menu.dttSearch):
                self.logger.info("  >>   ERR: cant find DTT search")
                return False
        else:
            if not self.actionSelect(Menu.dttDesactivation):
                self.logger.info("  >>   ERR: cant find deactivation button")
                return False
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return True

        currTime = datetime.now()
        while self.findInDialogBox(u"Trwa wyszukiwanie".encode("utf-8")):
            if(datetime.now() - currTime).seconds > 300:
                self.logger.info("  >>   ERR: time's up")
                return False
            time.sleep(10)

        time.sleep(20)

        if self.findInList(Menu.dttChannelsRFTV, True):
            return True

        if(self.findInDialogBox(u"Nie znaleziono".encode("utf-8"))):
            self.actionSelect(Menu.dttSearchLater)
            if self.findInList(Menu.dttChannelsRFTV, True):
                return True
            try:
                if(int(self.driver.find_element_by_xpath("//span[@class='value']").text) == 0):
                    self.logger.info("  >>   ERR: channels not found")
                    return False
            except:
                self.logger.info("  >>   ERR: channels not found")
                return False
        try:
            if(int(self.driver.find_element_by_xpath("//span[@class='value']").text) == 0):
                self.logger.info("  >>   ERR: channels not found")
                return False
        except:
            self.logger.info("  >>   ERR: channels not found")
            return False

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        return True

    def zapToChannel(self, channelNumber):
        """Function changes displaying channel and checks if channel is in fact changed
 
        @precondition: Fullscreen, live channel displays
        @param channelNumber: channel number (type: int)
        @return: True if channel changed correctly, False if not
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   zapToChannel - channelNumber >" + str(channelNumber) + "<")
        self.rc.zap(channelNumber)
        self.rc.sendKeys(["KEY_EXIT", "KEY_INFO"])
        time.sleep(2)
        info = self.getInfoFromLiveBanner()
        if type(info) == ProgramInfoItem:
            if info.getLcn() == int(channelNumber):
                self.rc.sendKeys(["KEY_EXIT"])
                return True
            else:
                self.logger.info("  >>   ERR: incorrect channel, should be {} in fact is {}".format(channelNumber, info.getLcn()))
                self.rc.sendKeys(["KEY_EXIT"])
                return False
        else:
            if self.driver.find_elements_by_css_selector('.wrDialog'):
                self.logger.info("  >>   ERR: another channel is now recording. No W&R rights.")
            else:
                self.logger.info("  >>   ERR: cannot get channel number from a live banner")
            self.rc.sendKeys(["KEY_EXIT"])
            return False


    def turnOffFavouriteChannels(self, p=250, byNumber=True):
        """Function add k program to favorite channels
 
        @precondition: Go to MENU->MYAccount->Mysettings->channels
        @param p: number of unchecking favorite channels 
        @param byNumber: variable determining if uncheck number of p channels or uncheck number of channels acoours in Description
                            >True        uncheck number of channels acoours in Description
                            >False     uncheck number of p channels
        @return: True when uncheck channels properly, False when error in uncheck channels
        @author: Tomasz Stasiuk
        """

        self.logger.debug("  >>   turnOffFavouriteChannels - p >" + str(p) + "< - byNumber >" + str(byNumber) + "<")

        if not (byNumber == False):
            time.sleep(2)
            self.driver.get(Rpi.DUMP)
            time.sleep(1)
            try:
                tekst = (self.driver.find_element_by_class_name("value").text).encode('utf-8')
            except:
                return True
            numberfavoritechannels = int(tekst.rsplit(' ', 5)[4])
            time.sleep(5)
        else:
            numberfavoritechannels = 1000

        i = 0
        ii = 0
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(1)
        self.rc.sendKeys(["KEY_UP"])

        while (i < p and ii < numberfavoritechannels):
            heart = self.getFavoriteChannelListItemOnList().favorite
            if heart:
                self.rc.sendKeys(["KEY_OK"])
                self.rc.sendKeys(["KEY_DOWN"])
                ii = ii + 1
            else:
                self.rc.sendKeys(["KEY_DOWN"])
            i = i + 1
            time.sleep(1)
        return True


    def turnOnFavouriteChannels(self, k):
        """Function add k program to favorite channels
 
        @precondition: Go to MENU->MYAccount->Mysettings->channels
        @param k:  the number of channels added 
        @return: True when add channels properly, False when error in add channels
        @author: Tomasz Stasiuk
        """
        i = 0
        self.logger.debug("  >>   turnOnFavouriteChannels - p >" + str(k) + "< ")
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(1)
        self.rc.sendKeys(["KEY_UP"])
        while (i < k):
            i = i + 1
            heart = self.getFavoriteChannelListItemOnList().favorite
            if not heart:
                self.rc.sendKeys(["KEY_OK"])
                self.rc.sendKeys(["KEY_DOWN"])
            else:
                self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(1)
        return True

    def setFavoriteChannels(self, channels):
        """Function add specified program/programs to favorite channels
 
        @precondition: None
        @param channels:  if only one channel is needed a string or int will be enough, if more channels are needed a list of channels should be provided
        @return: True when add channels properly, False when error in add channels
        @author: Marcin Gmurczyk
        """
        self.logger.debug("setFavorite >" + str(channels) + "<")
        if not isinstance(channels, list):
            channels = [int(channels)]
        length = len(channels)
        currElement = 0
        if not self.goToMySettings():
            self.logger.info("   ERR   problem in function goToMySettings")
            return False
        if not self.actionSelect(Menu.favoriteChannels):
            self.logger.info("   ERR   problem finding" + Menu.favoriteChannels)
            return False
        time.sleep(3)
        if not self.turnOffFavouriteChannels(byNumber=True):
            self.logger.info("   ERR   problem in function turnOffFavouriteChannels")
            return False
        self.rc.sendKeys(["KEY_BACK"])
        if not self.actionSelect(Menu.favoriteChannels):
            self.logger.info("   ERR   problem finding" + Menu.favoriteChannels)
            return False

        time.sleep(10)

        while(currElement < length):

            item = self.getFavoriteChannelListItemOnList()

            if not item:
                self.logger.info("   ERR   cannot get info about favorites channel")
                return False

            if int(item.getLcn()) < channels[currElement]:
                self.rc.sendKeys(["KEY_DOWN"] * (channels[currElement] - int(item.getLcn())))
            elif int(item.getLcn()) > channels[currElement]:
                self.rc.sendKeys(["KEY_UP"] * (int(item.getLcn()) - channels[currElement]))

            time.sleep(3)

            if int(item.getLcn()) == channels[currElement]:
                self.rc.sendKeys(["KEY_OK"])
            elif int(item.getLcn()) > channels[currElement]:
                while(int(self.getFavoriteChannelListItemOnList().getLcn()) != channels[currElement]):
                    self.rc.sendKeys(["KEY_DOWN"])
                    time.sleep(1)
                self.rc.sendKeys(["KEY_OK"])
            elif int(item.getLcn()) < channels[currElement]:
                while(int(self.getFavoriteChannelListItemOnList().getLcn()) != channels[currElement]):
                    self.rc.sendKeys(["KEY_UP"])
                    time.sleep(1)
                self.rc.sendKeys(["KEY_OK"])
            currElement += 1

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        return True

    def checkWorkingEpgKey(self, KEY, element):
        """Function Checking if moving buttons on the remote in EPG working properly
 
        @precondition: Go to EPG
        @param KEY: KEY choices (type: str):
                    "KEY_LEFT", "KEY_RIGHT", "KEY_DOWN", "KEY_UP", "KEY_FORWARD", "KEY_REWIND"
        @param KEY: element choices (type: str):
                    lcn, channelName, program, start, length, genre, favorite, nextProgram, clock, csaClass, recording
        @return: True if work properly , False if accours error when moving in EPG
        @author: Tomasz Stasiuk
        """
        self.logger.debug("  >>   checkWorkingEpgKey - KEY >" + str(KEY) + "< - element >" + str(element) + "<")
        time.sleep(5)
        self.logger.info("STEP -" + KEY)
        EPG1 = self.getInfoFromEpgFocus()
        if not (type(EPG1) is ProgramInfoItem):
            self.logger.info("  >>   ERR: false Loaded EPG1")
            return False
        epg1element = getattr(EPG1, element)
        KEYUSE = str('"' + KEY + '"')
        self.rc.sendKeys([KEYUSE])
        time.sleep(2)
        if not (KEY == "KEY_FORWARD" or KEY == "KEY_REWIND"):
            self.rc.sendKeys([KEYUSE])
        time.sleep(10)
        EPG2 = self.getInfoFromEpgFocus()
        epg2element = getattr(EPG2, element)
        if not (type(EPG2) is ProgramInfoItem):
            self.logger.info("  >>   ERR: false Loaded EPG2")
            return False
        if not (epg1element == epg2element):
            time.sleep(1)
        else:
            time.sleep(1)
            return False
        return True

    def checkIfInToolboxIsHeartIcon(self):
        """Function check if in toolbox occours heart(favorite) picture 
 
        @precondition: go to toolbox in live
        @return: True if found heart , False if not found heart
        @author: Tomasz Stasiuk
        """

        self.logger.debug("  >>   checkIfInToolboxIsHeartIcon")
        time.sleep(4)
        self.driver.refresh()
        self.driver.get(Rpi.DUMP)
        time.sleep(5)
        try:
            self.driver.find_element_by_css_selector(".pictoHeart")
            self.logger.info("  >>  Heart is found in toolbox")
            return True
        except:
            self.logger.info("  >>  Heart isn't found in toolbox")
            return False
        time.sleep(5)

    def setSubtitlesSettings(self, subtitlesSelect):
        """Function set subtitles settings
 
        @precondition: None
        @param subtitles: menu choices (type: str)
                > Menu.subtitleSelectNone
                > Menu.subtitleSelectPolish
                > Menu.subtitleSelectImpairedHearing
        @return: True if set correctly , False if error in set subtitles
        @author: Tomasz Stasiuk
        """

        self.logger.debug("  >>   setSubtitlesSettings subtitlesSelect>" + str(subtitlesSelect) + "<")
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(2)

        if (not self.goToMySettings()):
            self.logger.info("  >>   ERR: problem in function >goToMySettings<")
            return False
        time.sleep(2)
        if (not self.actionSelect(Menu.subtitles)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.subtitles + "<")
            return False
        time.sleep(2)

        if (subtitlesSelect == Menu.subtitleSelectNone):
            self.actionSelect(Menu.subtitleSelectNone)
            self.logger.info("  >>   Set subtitlest to None")
        elif (subtitlesSelect == Menu.subtitleSelectPolish):
            self.actionSelect(Menu.subtitleSelectPolish)
            self.logger.info("  >>   Set subtitlest to Polish")
        elif (subtitlesSelect == Menu.subtitleSelectImpairedHearing):
            self.actionSelect(Menu.subtitleSelectImpairedHearing)
            self.logger.info("  >>   Set subtitlest to ImpairedHearing")
        else:
            self.logger.info("  >>   ERR: problem selecting " + subtitlesSelect + "<")
            return False
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        return True


    def setLanguageSettings(self, languageSelect):
        """Function set subtitles settings
 
        @precondition: None
        @param subtitles: menu choices (type: str)
                > Menu.subtitleSelectNone
                > Menu.subtitleSelectPolish
                > Menu.subtitleSelectImpairedHearing
        @return: True if set correctly , False if error in set subtitles
        @author: Tomasz Stasiuk
        """

        self.logger.debug("  >>   setSubtitlesSettings subtitlesSelect>" + str(languageSelect) + "<")
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(2)

        if (not self.goToMySettings()):
            self.logger.info("  >>   ERR: problem in function >goToMySettings<")
            return False
        time.sleep(2)
        if (not self.actionSelect(Menu.language)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.language + "<")
            return False
        time.sleep(2)

        if (languageSelect == Menu.nativeSoundtrack):
            self.actionSelect(Menu.nativeSoundtrack)
            self.logger.info("  >>   Set subtitlest to None")
        elif (languageSelect == Menu.orginalSoundtrack):
            self.actionSelect(Menu.orginalSoundtrack)
            self.logger.info("  >>   Set subtitlest to Polish")
        else:
            self.logger.info("  >>   ERR: problem selecting " + languageSelect + "<")
            return False
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        return True


    def setSatVectors(self, number):
        """Function sets two sat vectors
         
        @param number: sets number of fesat cable connection (type: int)
                        0 - sets sat to zero
                        1 - sets sat to one with cable connected to fesat01
                        2 - sets sat to one with cable connected to fesat02
                        3 - sets sat to two with cables connected both to fesat01 and fesat02
        @precondition: None
        @return: True if set correctly , False otherwise
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   setSatVectors >number: %s<" % str(number))
        try:
            self.goToTvSettings()
            if not self.actionSelect(Menu.satSettings):
                self.logger.info("   ERR   cannot select " + Menu.satSettings)
                return False
            time.sleep(2)
            if not (number == 1 or number == 2):
                time.sleep(2)
                self.rc.sendKeys(["KEY_BACK"])
                try:
                    self.driver.get(Rpi.DUMP)
                    time.sleep(1)
                    curr_setting = self.driver.find_element_by_xpath("//div[@class='content']/span[3]").text
                    if number == 0:
                        _num = 'zero'
                    elif number == 3:
                        _num = 'dwa'
                    if curr_setting == _num:
                        self.rc.sendKeys(["KEY_TV"])
                        return True
                    else:
                        self.rc.sendKeys(["KEY_OK"])
                except Exception, e:
                    print e
            start_time = datetime.now() + timedelta(minutes=3)
            while not self.findInXPathElementClass("highlight", "//div[@id='internal']"):
                if datetime.now() > start_time:
                    self.logger.info("function is probably lost... quitting!")
                    return False
                self.rc.sendKeys(["KEY_UP"])
                time.sleep(1)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            while not self.findInXPathElementClass("highlight", "//div[@id='no_diseqc_id']"):
                if datetime.now() > start_time:
                    self.logger.info("function is probably lost... quitting!")
                    return False
                self.rc.sendKeys(["KEY_UP"])
                time.sleep(1)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(20)
            self.driver.get(Rpi.DUMP)
            time.sleep(1)
            item = self.driver.find_elements_by_xpath("//div[@class='tunnerContainer']/div[@class='disableDiv']")

            if number == 0:
                if item[0].get_attribute("style") == "display: block;" and item[1].get_attribute("style") == "display: block;":
                    self.rc.sendKeys(["KEY_OK"])
                else:
                    self.logger.info("  ERR   fesat cables detected")
                    return False
            elif number == 1:
                if item[0].get_attribute("style") == "display: none;" and item[1].get_attribute("style") == "display: block;":
                    self.rc.sendKeys(["KEY_OK"])
                else:
                    self.logger.info("  ERR   fesat cables connected incorrectly")
                    return False
            elif number == 2:
                if item[0].get_attribute("style") == "display: block;" and item[1].get_attribute("style") == "display: none;":
                    self.rc.sendKeys(["KEY_OK"])
                else:
                    self.logger.info("  ERR   fesat cables connected incorrectly")
                    return False
            elif number == 3:
                if item[0].get_attribute("style") == "display: none;" and item[1].get_attribute("style") == "display: none;":
                    self.rc.sendKeys(["KEY_OK"])
                else:
                    self.logger.info("  ERR   fesat cables connected incorrectly, one of cables is not connected")
                    return False
            else:
                self.logger.info("  ERR   unknown number variable: " + str(number))
                return False

            time.sleep(10)

            #===================================================================
            # self.goToTvSettings()
            # if not self.actionSelect(Menu.satSettings):
            #     self.logger.info("   ERR   cannot select " + Menu.satSettings)
            #     return False
            # self.rc.sendKeys(["KEY_BACK"])
            # time.sleep(5)
            # if number == 0:
            #     if not self.findInXPathElement(Menu.satZero, "//div[@class='content']/span[3]"):
            #         self.logger.info("   ERR   cannot set zero sat vectors")
            #         self.rc.sendKeys(["KEY_TV"])
            #         return False
            # elif number == 1:
            #     if not self.findInXPathElement(Menu.satOne, "//div[@class='content']/span[3]"):
            #         self.logger.info("   ERR   cannot set one sat vector")
            #         self.rc.sendKeys(["KEY_TV"])
            #         return False
            # elif number == 2:
            #     if not self.findInXPathElement(Menu.satOne, "//div[@class='content']/span[3]"):
            #         self.logger.info("   ERR   cannot set one sat vector")
            #         self.rc.sendKeys(["KEY_TV"])
            #         return False
            # elif number == 3:
            #     if not self.findInXPathElement(Menu.satTwo, "//div[@class='content']/span[3]"):
            #         self.logger.info("   ERR   cannot set two sat vectors")
            #         self.rc.sendKeys(["KEY_TV"])
            #         return False
            #===================================================================
        except Exception, e:
            self.logger.info("error occured: " + str(e))
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return False

        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        return True


    def checkStbStatusIfKoReboot(self):
        """Check STB status if ko reboot
        @precondition: none
        @return: True 
        @author: Tomasz Stasiuk
        """

        stbStatus = self.rc.getStbStatus()
        if stbStatus == "KO":
            self.logger.warning("Hard Reset")
            self.rc.hardReset()
            time.sleep(2)
            try:
                currTime = datetime.now()
                status = False
                moje = None
                time.sleep(15)
                while (status == False):
                    datanow = datetime.now()
                    calc = datanow - currTime
                    calc = calc.seconds
                    if (calc > 240):
                        status = True
                    self.rc.sendKeys(["KEY_INFO"])
                    time.sleep(2)
                    moje = self.getInfoFromLiveBanner()
                    time.sleep(3)
                    if moje != None:
                        status = True
                time.sleep(3)
                self.rc.sendKeys(["KEY_BACK"])
            except:
                time.sleep(250)
                pass

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return True

    def checkLive(self, pvrAndVod=False):
        """Check, live and full screen in live 
        @precondition: Go to live channel
        @return: True if set correctly , False if none live or fullscreen 
        @author: Tomasz Stasiuk
        """
        self.logger.debug("  >>   checkLive >pvrAndVod: {}<".format(pvrAndVod))
        display = motionDetection()
        if not (display == True):
            time.sleep(10)
            display = motionDetection()
            if not (display == True):
                self.logger.info("  >>  Motion not detected")
                return False
        self.logger.info("  >>  Motion detected")
        time.sleep(5)
        self.driver.get(Rpi.DUMP)
        time.sleep(1)
        if pvrAndVod == False:
            try:
                self.driver.find_element_by_css_selector(".live.scene")
            except:
                self.logger.info("  >>  ERR   live fullscreen scene not found")
                return False
        return True

    def cleanTurnOffAllFavoriteChannels(self):
        """Function Turn off all favorite channels
        @precondition: None
        @return: True  
        @author: Tomasz Stasiuk
        """
        self.rc.sendKeys(['KEY_BACK'])
        time.sleep(2)
        self.rc.sendKeys(['KEY_BACK'])
        time.sleep(2)
        self.rc.sendKeys(['KEY_TV'])
        time.sleep(2)
        self.rc.sendKeys(["KEY_MENU"])
        self.actionSelect(Menu.myAccount)
        self.actionSelect(Menu.mySettings)
        self.actionSelect(Menu.myChannels)
        time.sleep(1)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(5)
        if not (self.findInPage(Description.favoriteZeroChannels)):
            self.rc.sendKeys(["KEY_OK"])
            self.turnOffFavouriteChannels(byNumber=True)
            self.logger.info("  >>  Turn off all favorite channels")
        else:
            self.logger.info("  >>  All favorite channels are turn off")
        self.rc.sendKeys(['KEY_BACK'])
        time.sleep(2)
        self.rc.sendKeys(['KEY_BACK'])
        time.sleep(2)
        self.rc.sendKeys(['KEY_TV'])
        time.sleep(2)
        return True

    def cleanCodeAdultToDefault(self):
        """Function sets adult code to default 1111
        
        @precondition: None
        @return: True if function ends correctly, False otherwise
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   cleanCodeAdultToDefault()")
        try:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK"])
            time.sleep(2)
            self.goToMenu()
            self.actionSelect(Menu.myAccount)
            self.actionSelect(Menu.myCodes)
            self.actionSelect(Menu.adultCode)
            self.rc.sendNumberSequence("1234")
            time.sleep(2)
            if self.findInDialogBox(DialogBox.WrongConfidentialCode):
                self.rc.sendNumberSequence("2222")
                if self.findInDialogBox(DialogBox.WrongConfidentialCode):
                    self.rc.sendNumberSequence("4321")
                    if self.findInDialogBox(DialogBox.WrongConfidentialCode):
                        Env.CONFIDENTIAL_CODE = "1111"
                        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                        return True

            self.rc.sendNumberSequence("1111")
            time.sleep(1)
            self.rc.sendNumberSequence("1111")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            if self.findInDialogBox(DialogBox.NewAdultCodeConfirmation):
                Env.CONFIDENTIAL_CODE = "1111"
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                return True
            else:
                self.logger.debug("   ERR:   cannot find " + DialogBox.NewAdultCodeConfirmation)
                return False
        except Exception, e:
            self.logger.debug("Error occured during cleaning: " + str(e))
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return False

    def cleanCodeParentalToDefault(self):
        """Function sets parental code to default 2222
        
        @precondition: None
        @return: True if function ends correctly, False otherwise
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   cleanCodeParentalToDefault()")
        try:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK"])
            time.sleep(2)
            self.goToMenu()
            self.actionSelect(Menu.myAccount)
            self.actionSelect(Menu.myCodes)
            self.actionSelect(Menu.parentalCode)
            self.rc.sendNumberSequence("4321")
            time.sleep(2)
            if self.findInDialogBox(DialogBox.WrongParentalCode):
                self.rc.sendNumberSequence("1111")
                if self.findInDialogBox(DialogBox.WrongParentalCode):
                    self.rc.sendNumberSequence("1234")
                    if self.findInDialogBox(DialogBox.WrongParentalCode):
                        Env.PARENTAL_CODE = "2222"
                        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                        return True

            self.rc.sendNumberSequence("2222")
            time.sleep(1)
            self.rc.sendNumberSequence("2222")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            if self.findInDialogBox(DialogBox.NewParentalCodeConfirmation):
                Env.PARENTAL_CODE = "2222"
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                return True
            else:
                self.logger.debug("   ERR:   cannot find " + DialogBox.NewParentalCodeConfirmation)
                return False
        except Exception, e:
            self.logger.debug("Error occured during cleaning: " + str(e))
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return False

    def cleanDeleteAllRecordings(self):
        """Function delete all future and ongoing record in My Records
        
        @precondition: None
        @return: True if function ends correctly, False otherwise
        @author: Marcin Gmurczyk
        """
        self.logger.debug("  >>   cleanDeleteAllRecordings()")
        try:
            if self.goToPvrMyScheduled():
                time.sleep(3)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)
                try:
                    while self.deletePvrRecord():
                        self.rc.sendKeys(["KEY_OK"])
                except:
                    self.rc.sendKeys(["KEY_OK"])
                    pass
            else:
                self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            if self.actionSelect(Menu.pvrMyRecords):
                time.sleep(5)
                item = self.getInfoFromRecordFocus()
                if item and item.getRecording():
                    self.rc.sendKeys(["KEY_OK"])
                    if not self.deletePvrRecord(True):
                        return False
            else:
                self.rc.sendKeys(["KEY_OK"])
            self.rc.sendKeys(['KEY_BACK'])
            time.sleep(2)
            self.rc.sendKeys(['KEY_BACK'])
            time.sleep(2)
            self.rc.sendKeys(['KEY_TV'])
            time.sleep(2)
            return True
        except Exception, e:
            self.logger.info("   >>>   cleanDeleteAllRecordings error occured: " + str(e))
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            return False

    def checkPvrRecord(self):
        """Check if PVR Record work fine, (vido,play,pausa...)
        @precondition: Start PVR
        @return: True  
        @author: Tomasz Stasiuk
        """

        time.sleep(5)
        display = motionDetection()
        if display == True:
            self.logger.info("  >>  Find video stream")
        else:
            self.logger.info("  >>  No video stream")
            return False
        time.sleep(2)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)
        display = self.checkLive(pvrAndVod=True)
        if display == False:
            self.logger.info("  >>  Find video stream")
        else:
            self.logger.info("  >>  No video stream")
            return False
        time.sleep(60)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(10)
        display = self.checkLive(pvrAndVod=True)
        if display == True:
            self.logger.info("  >>  Find video stream")
        else:
            self.logger.info("  >>  No video stream")
            return False
        self.rc.sendKeys(["KEY_OK"])
        self.rc.sendKeys(["KEY_BACK"])
        return True

    def setRecommendation(self, select):
        """Function set Recommendation settings
 
        @precondition: None
        @param selec: menu choices (type: str)
                > Menu.activate
                > Menu.deactivate
        @return: True if set correctly , False if error in funkction
        @author: Tomasz Stasiuk
        """
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_MENU"])
        time.sleep(2)

        if (not self.goToMySettings()):
            self.logger.info("  >>   ERR: problem in function >goToMySettings<")
            return False
        time.sleep(2)
        if (not self.actionSelect(Menu.personalizedSuggestion)):
            self.logger.info("  >>   ERR: problem selecting >" + Menu.personalizedSuggestion + "<")
            return False
        time.sleep(2)
        if select == 'activate':
            try:
                select1 = self.actionSelect(Menu.activate)
            except:
                time.sleep(1)
            if select1 == True:
                time.sleep(2)
                self.rc.sendKeys(["KEY_OK"])
            else:
                time.sleep(2)
        elif select == 'deactivate':
            try:
                self.actionSelect(Menu.deactivate)
            except:
                time.sleep(2)
        else:
            self.logger.info("  >>  ERR in setRecommendation")
            return False
        time.sleep(10)
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        return True

    def findAccessibilityIcon(self):
        """Function finding accessibilityIcon
 
        @precondition: be in Menu
        @return: find = True if found accessibilityIcon , None if not found accessibilityIcon, False in error
        @author: Tomasz Stasiuk
        """

        txt = 'none'
        self.driver.get(Rpi.DUMP)
        time.sleep(1)
        moje = 'error'
        try:
            moje = self.driver.find_element_by_css_selector("div.breadCrumb.breadcrumb.breadcrumb div.icons span.accessibilityIcon")
            style = moje.get_attribute("style").encode('utf-8')
        except:
            time.sleep(2)
        style = style.find(txt)
        if style == -1:
            self.logger.info("  >>  find icon")
            return True
        else:
            self.logger.info("  >>  not find icon")
            return None
        if moje == 'error':
            self.logger.info("  >>  not find icon")
            return False

    def findOptinIcon(self):
        """Function finding accessibilityIcon
 
        @precondition: be in Menu
        @return: find = True if found accessibilityIcon , None if not found OptinIcon, False in error
        @author: Tomasz Stasiuk
        """

        txt = 'none'
        self.driver.get(Rpi.DUMP)
        time.sleep(1)
        moje = 'error'
        try:
            moje = self.driver.find_element_by_css_selector("div.breadCrumb.breadcrumb.breadcrumb div.icons span.optinIcon")
            style = moje.get_attribute("style").encode('utf-8')
        except:
            time.sleep(2)
        style = style.find(txt)
        if style == -1:
            self.logger.info("  >>  find icon")
            return True
        else:
            self.logger.info("  >>  not find icon")
            return None
        if moje == 'error':
            self.logger.info("  >>  not find icon")
            return False

    def getVolumeLevel(self):
        self.logger.debug("  >>   getVolumeLevel()")
        try:
            self.driver.get(Rpi.DUMP)
            time.sleep(1)
            item = self.driver.find_element_by_css_selector(".volume")
            itemClass = item.get_attribute("class")
            if itemClass.find("muted") > -1:
                return -1
            if itemClass.find("hidden") > -1:
                return False
            else:
                item = item.find_element_by_css_selector(".levelBar .levelOn")
                vol = item.get_attribute("style")
                vol = vol.split(": ")[1].split("%")[0]
                return float(vol)
        except:
            return False

    class findInLogs(object):
        def __init__(self, pattern, timeout=30, working=True, repeats=1):
            self.logger = logging.getLogger('NewTvTesting.WebKitPage')
            self.found = False
            self.text = None
            self.repeats = repeats
            self.pattern = pattern.encode('utf-8')
            self._thread = None
            self.timeout = timeout
            self.working = False
            self.rc = RpiRemoteControl()
            self._link = "/StbGetLogs.php?lineCount=500&clean=true&logLevel=all&pretty=false&logMode=all&searchErrors=false"

            if working:
                self.start()

        def start(self):
            try:
                self.rc.startLogs()
                import threading
                self.working = True
                self.rc.sendUrl(Rpi.URL_RPI + "/StbResetLogs.php?resetFile=true&resetScrollBack=true")
                self._thread = threading.Thread(target=self.backgroundFunction)
                self._thread.setDaemon(True)
                self._thread.start()
            except:
                self.working = False
                pass

        def backgroundFunction(self):
            start = datetime.now()
            while (datetime.now() - start).total_seconds() < self.timeout:
                try:
                    response = self.rc.sendUrl(Rpi.URL_RPI + self._link)
                    if response.getcode() == 200:
                        self.text = response.read()
                        if self.text.count(self.pattern) == self.repeats:
                            self.found = True
                            break
                    else:
                        time.sleep(0.1)
                except:
                    time.sleep(0.1)
            if not self.found:
                self.logger.info("   error in findInLogs > given pattern not found")
            self.working = False
            self._thread = None
            self.rc.startLogs()

        def debug(self):
            self.logger.info("-------------------------------")
            self.logger.info("")
            self.logger.info("current findInLogs variables:")
            self.logger.info("self.found: " + str(self.found))
            self.logger.info("self.text: " + str(self.text))
            self.logger.info("self.pattern: " + str(self.pattern))
            self.logger.info("self.timeout: " + str(self.timeout / 10))
            self.logger.info("self.working: " + str(self.working))
            self.logger.info("self.repeats: " + str(self.repeats))
            self.logger.info("")
            self.logger.info("-------------------------------")

    def deleteAllPvr(self):
        """Function delate all pvr(without sample) 
 
        @precondition: none
        @return: True if delate all , False if something go wrong 
        @author: Tomasz Stasiuk
        """
        a = 0
        i = 0
        n = 0
        b = 0
        c = 0

        check = self.goToPvrMyRecords()
        if check == False:
            return False
        self.rc.sendKeys(["KEY_BACK"])

        b = self.checkNumberOfPvr()
        if b == False:
            return False
        b = b + 1
        if b < 10:
            c = 30
        elif (b > 10 and b < 30):
            c = 60
        else:
            c = 90
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(c)
        info = self.getInfoFromRecordFocus()
        if info == None:
            return True
        time.sleep(8)
        while info != None:
            if not a == 0:
                n = 0
                while not n == a:
                    n = n + 1
                    self.rc.sendKeys(["KEY_RIGHT"])
                    time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            information = self.getInfoFromRecordPage()
            if information == None:
                return False
            title = information.title
            if information == None:
                return False
            if "sample" in title:
                a = a + 1;
                time.sleep(2)
                self.rc.sendKeys(["KEY_BACK"])
            else:
                self.actionSelect(Menu.pvrDelete)
                time.sleep(4)
                self.actionSelect(Menu.pvrYes)
            time.sleep(c)
            info = self.getInfoFromRecordFocus()
            if info == None:
                return False
            i = i + 1
            print i
            if i == b:
                return True
            if i == 120:
                return False
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

    def checkNumberOfPvr(self):

        """Function show number of pvr
 
        @precondition: go to nagrywarka TV screen
        @return: False if wrong, return number if all ok
        @author: Tomasz Stasiuk
        """
        self.logger.debug("  >>   checkNumberOfPvr - txt >")
        self.driver.get(Rpi.DUMP)
        time.sleep(2)
        try:
            info = self.driver.find_elements_by_css_selector ("html body div#pvrMenu.scene.whiteBg.pvrMenu div.dockCenter div.help.shadow div.text")
            info = info[0].text.encode('utf-8')
            info = info.split('\n')
            info = info[0]
            info = info.split(' ')
            info = info[3]
            info = int(info)
            return info
        except:
            # raise
            return False

    def sleep(self, sleep_time):
        """Function for logging sleep phases for better readability of test logs
        @param sleep_time: Time to sleep in seconds
        @author: Marcin Gmurczyk
        """
        seconds = timedelta(seconds=sleep_time)
        if sleep_time > 30:
            self.logger.debug(">>>   going to sleep for: {}, continuing on {}   <<<".format(seconds, str(datetime.now() + seconds).rsplit(".", 1)[0]))
        time.sleep(sleep_time)

    def simplifyProgramTitle(self, title):
        """Function simplifies given program title for purpose of checking if program record is made in PVR.
            For example: We are getting program title from live banner 'foo - odc. 123'. After instant record title in PVR may change to
            'Foo (123)'. But it also may not change. I belive it depends on EIT. So function will simplify (stupidify) given parameter. It will remove everything
            after first space so both, title from live banner and title from PVR will be 'FOO'.
        @param title: Program title to simplify
        @author: Marcin Gmurczyk
        """
        if  title.find(" ") != -1:
            return title.split(" ")[0].upper()
        else:
            return title.upper()
