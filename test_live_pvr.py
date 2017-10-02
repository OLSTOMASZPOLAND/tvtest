# -*- coding: utf-8 -*-


import unittest
import time

from NewTvTesting.ResidentAppPage import *
from NewTvTesting.RemoteControl import *
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.DataSet import *



class TestLivePvr(unittest.TestCase):


    def setUp(self):
        self.logger = logging.getLogger('NewTvTesting')
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)
        formatter = logging.Formatter('%(levelname)s :: %(message)s')
        handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)

        self.page = WebKitPage()
        rc = RpiRemoteControl()

        rc.sendKeys(["KEY_CHANNELUP"])
        if self.page.findInDialogBox(DialogBox.RecordOnGoing):
            rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
            if Env.STB == "NEWBOX":
                rc.sendKeys(["KEY_OK"])
        else:
            rc.sendKeys(["KEY_CHANNELUP"])
            if self.page.findInDialogBox(DialogBox.RecordOnGoing):
                rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
                if Env.STB == "NEWBOX":
                    rc.sendKeys(["KEY_OK"])

        status = self.page.getStatus()
        scene = status.getScene()

        if scene == "TOOLBOX" or scene == "ZAPPING_BANNER":
            rc.sendKeys(["KEY_BACK"])
        elif scene == "PORTAL" or scene == "UNKNOWN":
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])

        if status.findDialogBox():
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])


        self.test_passed = False

    def tearDown(self):

        print(self.shortDescription())


        if not self.test_passed:
            print("Error " + self.id())
            output = self.id() + time.strftime("%c")
            if Env.VIDEO:
                screenshot(Env.SCREENSHOTS_DIR + output + ".png")

        self.page.close()


    def test_a_Init(self):

        ''' delete all previous records '''
        print " "
        print "hard Reset and delete all previous records"

        rc = RpiRemoteControl()

        rc.hardReset()
        time.sleep(180)

        rc.sendKeys(["KEY_MENU"])
        
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)

        
        self.page.actionSelect(Menu.pvrMyRecords)
        time.sleep(4)
        while self.page.getInfoFromRecordFocus() != None:
            rc.sendKeys(["KEY_OK"])
            self.page.actionSelect(Menu.pvrDelete)
            self.page.actionSelect(Menu.pvrYes)
            time.sleep(6)
        rc.sendKeys(["KEY_CHANNELUP"])

        ''' no DTT '''

        time.sleep(10)
        rc.sendKeys(["KEY_MENU"])



        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_RIGHT","KEY_RIGHT","KEY_RIGHT","KEY_OK"])
        else:
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
        self.assertTrue(self.page.actionSelect(Menu.mySettings))
        self.assertTrue(self.page.actionSelect(Menu.dttChannels))
        self.assertTrue(self.page.actionSelect(Menu.dttDesactivation))

        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_b_InstantRecording(self):

        ''' Instant record Content displayed in My records'''
        print " "
        print " Instant record Content displayed in My records"


        ''' TV1 '''

        rc = RpiRemoteControl()

        rc.zap(LiveData.TV1.getLcn())
        time.sleep(15)

        ''' program name retrival '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])


        ''' Instant Record launch '''
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(15)
        self.page.actionInstantRecord(PvrData.LENGTH_1)

        ''' waiting for recording '''
        time.sleep(PvrData.LENGTH_1*60+10)

        ''' checking name and video'''
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected :",focusRecord.getTitle()," / ",currentProgram.getProgram()," - ",currentProgram.getChannelName()
        print "Length / expected : ",focusRecord.getLenght()," / ",PvrData.LENGTH_1

        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV1")
        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(PvrData.LENGTH_1*60/2))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])
        time.sleep(10)

        rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(5)



        ''' TV6 '''

        ''' Instant Record launch '''
        rc.zap(LiveData.TV6.getLcn())
        time.sleep(15)

        ''' program name retrival '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])

        ''' Instant Record '''
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(15)
        self.page.actionInstantRecord(PvrData.LENGTH_2)

        ''' waiting for recording - warning box checking'''
        time.sleep(60)
        rc.sendKeys(["KEY_CHANNELUP"])
        while self.page.findInDialogBox(DialogBox.RecordOnGoing):
            rc.sendKeys(["KEY_CHANNELUP"])
            time.sleep(60)
            rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(60)

        ''' checking name and video'''
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected :",focusRecord.getTitle()," / ",currentProgram.getProgram()," - ",currentProgram.getChannelName()
        print "Length / expected : ",focusRecord.getLenght()," / ",PvrData.LENGTH_2
        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV6")
        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(PvrData.LENGTH_2*60/2))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_c_ManualRecordScheduling(self):

        '''Manual Record Scheduling and Content Playing'''
        print " "
        print "Manual Record Scheduling and Content Playing "

        rc = RpiRemoteControl()

        rc.zap(LiveData.TV1.getLcn())
        time.sleep(15)


        rc.sendKeys(["KEY_MENU"])

        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)

        self.page.actionSelect(Menu.pvrManualRecord)
        delta = 10

        currentDate = datetime.now()
        recordOneDate = currentDate + timedelta(minutes = delta)

        idOne = self.page.actionScheduleRecord(LiveData.PACKAGE_A, LiveData.TV1.getLcn(), recordOneDate, PvrData.LENGTH_1)
        self.assertTrue(idOne != False)

        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
        time.sleep(5)

        rc.zap(LiveData.TV2.getLcn())

        ''' Record Starting Pop Up Expected '''

        popUpDate = recordOneDate - timedelta(minutes = 3)
        wait = popUpDate - datetime.now()
        time.sleep(wait.seconds + 10)

        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordStartingSoon),"Record Starting Pop-Up Expected")
        rc.sendKeys(["KEY_OK"])

        time.sleep(10)

        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordOnGoing),"Record OnGoing Pop-Up Expected")

        rc.sendKeys(["KEY_CHANNELUP"])


        recordEndDate = recordOneDate + timedelta(minutes = PvrData.LENGTH_1)
        wait = recordEndDate - datetime.now()
        time.sleep(wait.seconds + 180)

        rc.sendKeys(["KEY_MENU"])

        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)

        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()

        self.assertEqual(focusRecord.getTitle(),idOne,"Wrong record Name"+focusRecord.getTitle()+idOne)
        print "Record name / expected : ",focusRecord.getTitle()," / ",idOne
        print "Length / expected : ",focusRecord.getLenght()," / ", PvrData.LENGTH_1
        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(PvrData.LENGTH_1*60/2))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)

        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_c_RecordFromEpg(self):

        ''' Record from EPG  '''
        print " "
        print "Record from EPG "

        rc = RpiRemoteControl()
        rc.zap(LiveData.TV6.getLcn())
        time.sleep(15)

        rc.sendKeys(["KEY_GUIDE"])
        self.assertTrue(self.page.actionSelect(Menu.epgWeek))
        time.sleep(15)
        rc.sendKeys(["KEY_RIGHT"])
        epg = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.epgRecord))
        rc.sendKeys(["KEY_DOWN"])
        rc.sendKeys(["KEY_OK"])
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        rc.zap(LiveData.TV1.getLcn())

        startRecordTime = epg.getStart()
        endRecordTime = epg.getLength() + startRecordTime
        wait = endRecordTime - datetime.now()

        time.sleep(wait.seconds + 180)

        rc.sendKeys(["KEY_CHANNELUP","KEY_MENU"])

        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_pvr)
        else:
            self.page.actionSelect(Menu.pvr)

        self.page.actionSelect(Menu.pvrMyRecords)
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected : ",focusRecord.getTitle()," / ", epg.getProgram()
        print "Length / expected : ",focusRecord.getLenght()," / ", epg.getLength()

        self.assertEqual(focusRecord.getTitle(),epg.getProgram(),"Wrong record Name")

        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(int(epg.getLength().seconds/3))
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])

        time.sleep(10)

        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_e_InstantRecording_EndingTimeConflict_1(self):

        '''Instant Recording ending date conflict - choice 1 - suggested choice'''
        print " "
        print "Instant Recording ending date conflict - choice 1 - suggested choice"

        rc = RpiRemoteControl()

        rc.zap(LiveData.TV1.getLcn())
        time.sleep(15)

        ''' Record 'One' manual scheduling -> delta min'''
        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        self.page.actionSelect(Menu.pvrManualRecord)


        delta = 10
        currentDate = datetime.now()
        recordOneDate = currentDate + timedelta(minutes = delta)
        idOne = self.page.actionScheduleRecord(LiveData.PACKAGE_A, LiveData.TV6.getLcn(), recordOneDate, PvrData.LENGTH_2)
        self.assertTrue(idOne != False)
        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
        time.sleep(5)


        ''' Instant Record : modifying end date -> conflict -> first choice selection'''


        ''' program name retrival '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])


        ''' Instant Record '''
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(15)
        self.page.actionInstantRecord(delta + PvrData.LENGTH_1)
        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordConflict),"Conflict Pop-Up Expected")
        time.sleep(10)
        rc.sendKeys(["KEY_OK"])

        ''' waiting for the end of the 2  records '''
        recordEndDate = recordOneDate + timedelta(minutes = PvrData.LENGTH_2)
        wait = recordEndDate - datetime.now()
        time.sleep(wait.seconds + 180)

        ''' checking '''
        error = False
        rc.sendKeys(["KEY_CHANNELUP"])
        if self.page.findInDialogBox(DialogBox.RecordOnGoing):
            error = True
            rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
            if Env.STB == "NEWBOX":
                rc.sendKeys(["KEY_OK"])
        else:
            rc.sendKeys(["KEY_CHANNELUP"])
            if self.page.findInDialogBox(DialogBox.RecordOnGoing):
                error = True
                rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
                if Env.STB == "NEWBOX":
                    rc.sendKeys(["KEY_OK"])

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords))

        time.sleep(5)
        rc.sendKeys(["KEY_RIGHT"])
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected :",focusRecord.getTitle()," / ",currentProgram.getProgram()," - ",currentProgram.getChannelName()
        print "Length / expected : ",focusRecord.getLenght()," / ",delta
        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV1")
        rc.sendKeys(["KEY_LEFT"])

        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected : ",focusRecord.getTitle()," / ",idOne
        print "Length / expected : ",focusRecord.getLenght()," / ",PvrData.LENGTH_2
        self.assertEqual(focusRecord.getTitle(),idOne,"Wrong record name idOne"+focusRecord.getTitle()+idOne)
        time.sleep(5)

        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(30)
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        self.assertFalse(error,"Record still on going")


        self.test_passed = True

    def test_f_InstantRecording_EndingTimeConflict_2(self):

        '''Instant Recording ending date conflict - choice 2 - scheduled record cancel'''
        print " "
        print "Instant Recording ending date conflict - choice 2 - scheduled record cancel"

        rc = RpiRemoteControl()

        rc.zap(LiveData.TV5.getLcn())
        time.sleep(15)

        ''' Record 'One' manual scheduling -> 10 min'''
        rc.sendKeys(["KEY_MENU"])
        
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        
        self.page.actionSelect(Menu.pvrManualRecord)
        delta = 10
        currentDate = datetime.now()
        recordOneDate = currentDate + timedelta(minutes = delta)



        idOne = self.page.actionScheduleRecord(LiveData.PACKAGE_A,LiveData.TV3.getLcn(),recordOneDate,PvrData.LENGTH_1)
        self.assertTrue(idOne != False)
        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
        time.sleep(5)

        ''' Instant Record : modifying end date -> conflict -> second choice delete scheduled record'''
        ''' program name retrival '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])


        ''' Instant Record '''
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(15)
        self.page.actionInstantRecord(delta + PvrData.LENGTH_1)
        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordConflict),"Conflict Pop-Up Expected")
        time.sleep(10)
        rc.sendKeys(["KEY_DOWN","KEY_OK"])


        ''' waiting for the end of the instant  record '''
        wait = timedelta(minutes = PvrData.LENGTH_1 + delta)
        time.sleep(wait.seconds + 180)


        ''' checking '''
        error = False
        rc.sendKeys(["KEY_CHANNELUP"])
        if self.page.findInDialogBox(DialogBox.RecordOnGoing):
            error = True
            rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
            if Env.STB == "NEWBOX":
                rc.sendKeys(["KEY_OK"])
        else:
            rc.sendKeys(["KEY_CHANNELUP"])
            if self.page.findInDialogBox(DialogBox.RecordOnGoing):
                error = True
                rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
                if Env.STB == "NEWBOX":
                    rc.sendKeys(["KEY_OK"])

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        
        self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords))
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected :",focusRecord.getTitle()," / ",currentProgram.getProgram()," - ",currentProgram.getChannelName()
        print "Length / expected : ",focusRecord.getLenght()," / ", PvrData.LENGTH_1 + delta
        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV5")
        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(30)
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])
        self.assertFalse(error,"Record still on going")

        self.test_passed = True

    def test_g_InstantRecording_DefaultEndingTimeConflict_3(self):

        '''Instant Recording ending date conflict - choice 3 - advanced management'''
        print " "
        print "Instant Recording ending date conflict - choice 3 - advanced management "

        rc = RpiRemoteControl()

        rc.zap(LiveData.TV12.getLcn())
        time.sleep(15)

        ''' Record 'One' manual scheduling -> 15 min'''
        rc.sendKeys(["KEY_MENU"])
        
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        
        self.page.actionSelect(Menu.pvrManualRecord)
        delta = 15
        currentDate = datetime.now()
        recordOneDate = currentDate + timedelta(minutes = delta)
        idOne = self.page.actionScheduleRecord(LiveData.PACKAGE_A,LiveData.TV1.getLcn(),recordOneDate,PvrData.LENGTH_2)
        self.assertTrue(idOne != False)
        rc.sendKeys(["KEY_BACK","KEY_CHANNELUP"])
        time.sleep(5)

        ''' Instant Record : modifying end date -> conflict -> third choice conflict management'''

        ''' program name retrival '''
        rc.sendKeys(["KEY_GUIDE","KEY_DOWN","KEY_OK"])
        time.sleep(20)
        currentProgram = self.page.getInfoFromEpgFocus()
        rc.sendKeys(["KEY_CHANNELUP"])


        ''' Instant Record '''
        currentDate = datetime.now()
        rc.sendKeys(["KEY_RECORD"])
        time.sleep(15)
        self.page.actionInstantRecord(delta + PvrData.LENGTH_1)
        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordConflict),"Conflict Pop-Up Expected")
        time.sleep(10)
        rc.sendKeys(["KEY_DOWN","KEY_DOWN","KEY_OK"])

        ''' conflict management pop up '''
        self.assertTrue(self.page.findInDialogBox(DialogBox.RecordConflictManagement),"Management Conflict Pop-Up Expected")
        newInstantRecordEndDate = recordOneDate + timedelta(minutes = int(PvrData.LENGTH_1/2 -1) )
        length1 = newInstantRecordEndDate - currentDate
        newScheduledRecordBeginDate =  recordOneDate + timedelta(minutes = int(PvrData.LENGTH_1/2 +1) )
        recordEndDate = recordOneDate + timedelta(minutes = PvrData.LENGTH_2)
        length2 = recordEndDate - newScheduledRecordBeginDate

        rc.sendDateHourMin(newInstantRecordEndDate)
        rc.sendDateHourMin(newScheduledRecordBeginDate)
        rc.sendKeys(["KEY_OK"])

        ''' waiting for the end of the 2 records '''
        self.assertFalse(self.page.getStatus().findDialogBox(),"Unexpected Dialog Box")

        wait = recordEndDate - datetime.now()
        time.sleep(wait.seconds + 180)

        ''' checking '''
        error = False
        rc.sendKeys(["KEY_CHANNELUP"])
        if self.page.findInDialogBox(DialogBox.RecordOnGoing):
            error = True
            rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
            if Env.STB == "NEWBOX":
                rc.sendKeys(["KEY_OK"])
        else:
            rc.sendKeys(["KEY_CHANNELUP"])
            if self.page.findInDialogBox(DialogBox.RecordOnGoing):
                error = True
                rc.sendKeys(["KEY_STOP","KEY_DOWN","KEY_OK"])
                if Env.STB == "NEWBOX":
                    rc.sendKeys(["KEY_OK"])

        rc.sendKeys(["KEY_MENU"])
        
        if Env.STB == "NEWBOX":
            rc.sendKeys(["KEY_RIGHT","KEY_RIGHT","KEY_DOWN","KEY_OK"])
        else:
            self.page.actionSelect(Menu.pvr)
        
        self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords))

        rc.sendKeys(["KEY_RIGHT"])


        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected :",focusRecord.getTitle()," / ",currentProgram.getProgram()," - ",currentProgram.getChannelName()
        print "Length / expected : ",focusRecord.getLenght()," / ", int(length1.seconds/60)
        rc.sendKeys(["KEY_LEFT"])
        self.assertTrue(focusRecord.getTitle() == currentProgram.getProgram() or focusRecord.getTitle() == currentProgram.getChannelName(),"Wrong record name TV12")
        focusRecord = self.page.getInfoFromRecordFocus()
        print "Record name / expected : ",focusRecord.getTitle()," / ", idOne
        print "Length / expected : ",focusRecord.getLenght()," / ", int(length2.seconds/60)
        self.assertEqual(focusRecord.getTitle(),idOne,"Wrong name idOne"+focusRecord.getTitle()+idOne)
        time.sleep(5)

        rc.sendKeys(["KEY_OK"])
        self.page.actionSelect(Menu.pvrPlay)
        time.sleep(30)
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        rc.sendKeys(["KEY_STOP"])
        time.sleep(10)
        rc.sendKeys(["KEY_CHANNELUP"])

        self.assertFalse(error,"Record still on going")

        time.sleep(60)

        self.test_passed = True








    def test_z_(self):

        ''' xxxx '''


        self.test_passed = True

