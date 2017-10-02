# -*- coding: utf-8 -*-

import logging
import time
import unittest

from NewTvTesting.ResidentAppPage import *
from NewTvTesting.RemoteControl import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Utils import *
from NewTvTesting.DataSet import *
from NewTvTesting.Config import *
from datetime import datetime, timedelta

class TC_OPL_template(unittest.TestCase):

    def setUp(self):
        self.reportsPath = self.__class__.__name__ + "/" + time.strftime("%Y_%m_%d_%H_%M_%S")
        createDirectoriesForReports(self.reportsPath)

        self.logger = logging.getLogger('NewTvTesting')
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')

        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setFormatter(formatter)
        self.logger.addHandler(self.streamHandler)

        self.fileHandler = logging.FileHandler(getTcReportFilePath(self.reportsPath))
        self.fileHandler.setFormatter(formatter)
        self.logger.addHandler(self.fileHandler)

        self.logStepsResults = True

        self.rc = RpiRemoteControl()
        self.page = WebKitPage()
        # stbStatus = self.rc.getStbStatus()
        stbStatus = "KO"
        
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
                        
                    self.rc.sendKeys(["KEY_BACK"])
                    time.sleep(1)
                    self.rc.sendKeys(["KEY_INFO"])
                    time.sleep(2)
                    moje = self.page.getInfoFromLiveBanner()
                    time.sleep(3)
                    if moje != None:
                        status = True
                print calc
                time.sleep(3)
                self.rc.sendKeys(["KEY_BACK"])
            except:
                time.sleep(240)
                pass

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        elif stbStatus == "Up\n":
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(5)
        elif stbStatus == "X_ORANGE-COM_Standby\n":
            self.rc.sendKeys(["KEY_POWER"])
            time.sleep(30)
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        
        self.test_passed = False

    def logStepBeginning(self, stepName):
        try:
            self.logger.info(stepName)
            # deep logging
            if self.logStepsResults:
                self.rc.startLogs()
        except Exception as e:
            self.logger.info(stepName + ": logStepBeginning ERROR: " + str(e))
            return False

    def logStepResults(self, stepName):
        try:
            # deep logging
            if self.logStepsResults:
                # stb logs
                self.logger.info(stepName + ": control stb logs")
                self.rc.stopLogs()
                writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, stepName))
        except Exception as e:
            self.logger.info(stepName + ": logStepResults ERROR: " + str(e))
            return False
        finally:
            # screen
            if Env.VIDEO:
                self.logger.info(stepName + ": control screen")
                screenshot(generateScreenFilePath(self.reportsPath, stepName))

    def tearDown(self):
        self.logger.info("----- tearDown -----")
        # time.sleep(10)
        # self.logger.info(self.shortDescription())
        try:
            if not self.test_passed:
                # print("Error " + self.__class__.__name__)
                self.logger.error("----- ERROR OCCURED -----")
                try:
                    msgStr = self.defaultTestResult()._exc_info_to_string(sys.exc_info(), self)
                    msgrStrLines = msgStr.splitlines()
                    self.logger.error(msgrStrLines[len(msgrStrLines) - 1])
                    self.logger.debug(msgStr)
                except Exception as e:
                    self.logger.error("ERROR parsing TC failure msg: " + str(e))
                writeLastPageSourceToFile(self.page.driver.page_source, self.reportsPath)
                self.logger.error("last page source saved")
                # screen
                if Env.VIDEO:
                    self.logger.error("screen after error")
                    screenshot(generateScreenFilePath(self.reportsPath, "tearDown"))
                # stb logs
                self.rc.stopLogs()
                writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, "tearDown"))
        except Exception as e:
            self.logger.error("Exception in tear down: {}".format(e))
        finally:
            self.logger.removeHandler(self.streamHandler)
            self.streamHandler.close()
            self.logger.removeHandler(self.fileHandler)
            self.fileHandler.close()
            try:
                self.page.close()
            except Exception as e:
                self.logger.error("Exception in tear down: {}".format(e))

    def test(self):
        pass

