# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection, screenshot
import time
import datetime
from NewTvTesting.Utils import writeStbLogsToFile, generateStbLogFilePath, \
    generateScreenFilePath, getReportsDirPath

class TC_0000_Unitary_zapping_test(TC_OPL_template):
    '''    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        self.delay = 0  # w godzinach
        self.interval = 5.0  # jako float
        self.firstChannel = 1
        self.lastChannel = 9999
        self.iterations = 5000

        ''' step '''
        self.timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/times.txt", "a")
        self.i = self.lastChannel - self.firstChannel

        self.rc.zap(self.firstChannel)
        time.sleep(5)

        ''' step '''
        self.logStepBeginning("start zapping - interval >%i< - firstChannel >%i< - lastChannel >%i<" % (self.interval, self.firstChannel, self.lastChannel))

        if self.delay != 0:
            self.logger.info("sleeping for: " + str(self.delay * 3600 - 180) + " seconds")
            time.sleep(self.delay * 3600 - 180)
            self.resetSTB()

        self.foo = 60 / self.interval
        if self.foo % 2 == 0:
            self.foo += 1

        self.start = datetime.datetime.now()

        self.logger.info("Start time: " + str(self.start))

        while self.startZapping():
            pass

        self.timeReportFile.close()
        self.logStepBeginning("start zapping - interval >%i< - firstChannel >%i< - lastChannel >%i<" % (self.interval, self.firstChannel, self.lastChannel))

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def startZapping(self):
        self.logSave = 0
        try:
            while(self.iterations > 0):
                log = self.page.findInLogs('stb.event> StbEvent> HANDLER: MEDIA - REASON: AREA_CHANGED - ATTRIBUTES: {"session_id":"LIVE"}', 4, False, repeats=3)
                log.start()
                self.rc.sendUrl(Rpi.URL_RPI_KEY + "KEY_CHANNELUP")
                signal = datetime.datetime.now()

                while log.working:
                    time.sleep(0.1)

                if not log.found:
                    self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";0\n")
                    self.timeReportFile.flush()
                else:
                    self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";" + str((datetime.datetime.now() - signal).total_seconds()) + "\n")
                    self.timeReportFile.flush()

                dream = self.interval - (datetime.datetime.now() - signal).total_seconds()

                if dream > 0:
                    time.sleep(dream)

                self.logSave += 1

                self.iterations -= 1

                # if self.iterations % self.i == 0:
                    # self.rc.zap(self.firstChannel)

                #===============================================================
                # if self.logSave >= self.foo:
                #     writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, str(self.start)))
                #     if Env.VIDEO:
                #         screenshot(generateScreenFilePath(self.reportsPath, "screenshot"))
                #     self.logSave = 0
                # else:
                #     time.sleep(1)
                #===============================================================
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
