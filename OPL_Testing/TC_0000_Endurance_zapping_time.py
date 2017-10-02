# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection
import time
import datetime
from NewTvTesting.Utils import  getReportsDirPath

class TC_0000_Endurance_zapping_time(TC_OPL_template):
    '''Implementation of the Endurance_TC100-01_Fast_zapping_test_HD-HD_5sec
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        self.delay = 0  # w godzinach
        self.interval = 10.0  # jako float
        self.firstChannel = 1
        self.secondChannel = 2
        self.firstRunIterations = 10  # tylko parzyste
        self.secondRunIterations = 0  # tylko parzyste

        ''' step '''
        self.logStepBeginning("step set favorite channels")

        #self.page.setFavoriteChannels([self.firstChannel, self.secondChannel])
        time.sleep(5)

        self.logStepResults("step set favorite channels")

        ''' step '''
        self.logStepBeginning("start zapping - interval >%i< - firstChannel >%i< - secondChannel >%i<" % (self.interval, self.firstChannel, self.secondChannel))

        self.assertTrue(self.page.zapToChannel(self.secondChannel), "   ERR   cannot zap to channel " + str(self.secondChannel))
        time.sleep(10)

        if Env.VIDEO:
            self.assertTrue(motionDetection(), "   ERR    motion detection is not working")

        self.assertTrue(self.page.zapToChannel(self.firstChannel), "   ERR   cannot zap to channel " + str(self.firstChannel))
        time.sleep(10)

        if Env.VIDEO:
            self.assertTrue(motionDetection(), "   ERR    motion detection is not working")
        
        self.rc.sendKeys(["KEY_LIST"])
        time.sleep(2)
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent")
            item = item.text.encode('utf-8')
            while item != Description.favoriteInList:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(2)
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent")
                item = item.text.encode('utf-8')
        except Exception, e:
            self.fail("   ERR   cannot load favorite list: " + str(e))

        self.rc.sendKeys(["KEY_BACK"])

        if self.delay != 0:
            self.logger.info("sleeping for: " + str(self.delay * 3600 - 180) + " seconds")
            time.sleep(self.delay * 3600 - 180)
            self.resetSTB()
        
        time.sleep(10)

        self.rc.sendKeys(["KEY_LIST"])
        time.sleep(2)
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent").text.encode('utf-8')
        self.assertTrue(Description.favoriteInList == item, "   ERR   cannot display list")

        while self.startZapping(self.firstRunIterations):
            pass

        if self.secondRunIterations != 0:
            self.resetSTB()

            time.sleep(10)

            self.rc.sendKeys(["KEY_LIST"])
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)

            item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent").text.encode('utf-8')
            self.assertTrue(Description.favoriteInList == item, "   ERR   cannot display list")

            while self.startZapping(self.secondRunIterations):
                pass

        self.logStepResults("start zapping - interval >%i< - firstChannel >%i< - secondChannel >%i<" % (self.interval, self.firstChannel, self.secondChannel))

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def startZapping(self, iterations):
        firstToSecond = type('firstToSecond', (object,), {'min' : 99.0, 'max' : 0.0, 'sum' : 0.0})
        firstToSecond.timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/times1-2.txt", "a")
        secondToFirst = type('secondToFirst', (object,), {'min' : 99.0, 'max' : 0.0, 'sum' : 0.0})
        secondToFirst.timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/times2-1.txt", "a")
        try:
            for i in range(iterations):

                if i % 2 == 0:
                    obj = firstToSecond
                else:
                    obj = secondToFirst

                log = self.page.findInLogs('stb.event> StbEvent> HANDLER: MEDIA - REASON: AREA_CHANGED - ATTRIBUTES: {"session_id":"LIVE"}', self.interval, False, repeats=3)
                log.start()
                signal = datetime.datetime.now()
                self.rc.sendUrl(Rpi.URL_RPI_KEY + "KEY_CHANNELUP")

                while log.working:
                    time.sleep(0.1)

                if not log.found:
                    obj.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";0\n")
                    obj.timeReportFile.flush()
                else:
                    t = float((datetime.datetime.now() - signal).total_seconds())
                    obj.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";" + str(t) + "\n")
                    obj.timeReportFile.flush()
                    if(t < obj.min):
                        obj.min = t
                    if(t > obj.max):
                        obj.max = t

                    obj.sum += t

                dream = self.interval - (datetime.datetime.now() - signal).total_seconds()

                if dream > 0:
                    time.sleep(dream)
            firstToSecond.mean = firstToSecond.sum / (iterations / 2)
            secondToFirst.mean = secondToFirst.sum / (iterations / 2)

            timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/timeReport.txt", "a")

            timeReportFile.write("Zapping time_%i: Kanał numer %i -> kanał numer %i:min %f:śred %f:max %f" % (iterations, self.firstChannel, self.secondChannel, \
                                                    firstToSecond.min, firstToSecond.mean, firstToSecond.max))
            timeReportFile.write("\n\n")
            timeReportFile.write("Zapping time_%i: Kanał numer %i -> kanał numer %i:min %f:śred %f:max %f" % (iterations, self.secondChannel, self.firstChannel, \
                                                    secondToFirst.min, secondToFirst.mean, secondToFirst.max))

            timeReportFile.write("\n\n")

            timeReportFile.write("Zapping time_%i: min %f:śred %f:max %f" % (self.interval, min(firstToSecond.min, secondToFirst.min), (firstToSecond.mean + secondToFirst.mean) / 2, \
                                                                            max(firstToSecond.max, secondToFirst.max)))

            timeReportFile.write("\n\n")
            timeReportFile.close()
            firstToSecond.timeReportFile.write("\n\n")
            secondToFirst.timeReportFile.write("\n\n")
            firstToSecond.timeReportFile.close()
            secondToFirst.timeReportFile.close()

            return False
        except Exception, e:
            self.logger.info("   ERR   " + str(e))
            return True

    def resetSTB(self):
        self.logger.warning("Hard Reset")
        self.rc.hardReset()
        time.sleep(2)
        try:
            currTime = datetime.datetime.now()
            status = False
            moje = None
            time.sleep(15)
            while (status == False):
                datanow = datetime.datetime.now()
                calc = datanow - currTime
                calc = calc.seconds
                if (calc > 240):
                    status = True
                self.rc.sendKeys(["KEY_INFO"])
                time.sleep(2)
                moje = self.page.getInfoFromLiveBanner()
                time.sleep(3)
                if moje != None:
                    status = True
            time.sleep(3)
            self.rc.sendKeys(["KEY_BACK"])
        except:
            time.sleep(240)
            pass
