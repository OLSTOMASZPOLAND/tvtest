# -*- coding: utf-8 -*-
from NewTvTesting.RemoteControl import RpiRemoteControl
from NewTvTesting.DataSet import *
import logging
import time
from NewTvTesting.ResidentAppPage import WebKitPage

if __name__ == '__main__':
    
    logger = logging.getLogger('NewTvTesting')
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    formatter = logging.Formatter('%(levelname)s :: %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    
    
    rc = RpiRemoteControl()
    page = WebKitPage()
    
    status = page.getStatus()
    print status.getStbStatus()
    stbStatus = status.getStbStatus()
    if stbStatus == "KO":
        print("Hard Reset")
        #rc.hardReset()
        #time.sleep(180)
        #status = page.getStatus()
    elif stbStatus == "Up":
        rc.sendKeys(["KEY_TV"])
    elif stbStatus == "X_ORANGE-COM_Standby":
        rc.sendKeys(["KEY_POWER"])
        time.sleep(5)
        #rc.sendKeys(["KEY_TV"])
    
    #rc.sendKeys(["KEY_MENU"])
    time.sleep(1)
    #page.actionSelect(u"płatności")
    
    page.close()
    
    
