# -*- coding: utf-8 -*-

import logging
import re
from Config import *


class ListItem(object):

    def __init__(self, text, selected=False, active=True):
        self.text = text
        self.selected = selected
        self.active = active

class FavoriteChannelListItem(object):

    def __init__(self, lcn, channelName, favorite=False, active=True):
        self.lcn = lcn
        self.channelName = channelName
        self.favorite = favorite
        self.active = active
        self.logger = logging.getLogger('NewTvTesting.FavoriteChannelListItem')
    
    def getLcn(self):
        return self.lcn

    def getChannelName(self):
        return self.channelName

    def getFavorite(self):
        return self.favorite
    
    def getActive(self):
        return self.active

    def display(self):
        self.logger.info("-------- favorite channel list item details ------")
        self.logger.info("lcn : " + str(self.lcn))
        self.logger.info("channel name : " + str(self.channelName))
        self.logger.info("favorite : " + str(self.favorite))
        self.logger.info("active: " + str(self.active))
        self.logger.info("-------------------------------")

class ProgramInfoItem(object):

    def __init__(self, lcn, channelName, program, start, length, genre, favorite, nextProgram, clock=None, csaClass=None, recording=None, reminder=None):
        self.lcn = lcn
        self.channelName = channelName
        self.favorite = favorite
        self.program = program
        self.start = start
        self.length = length
        self.genre = genre
        self.nextProgram = nextProgram
        self.clock = clock
        self.csaClass = csaClass
        self.recording = recording
        self.reminder = reminder
        self.logger = logging.getLogger('NewTvTesting.ProgramInfoItem')

    def getLcn(self):
        return self.lcn

    def getChannelName(self):
        return self.channelName

    def getProgram(self):
        return self.program

    def getStart(self):
        return self.start

    def getGenre(self):
        return self.genre

    def getLength(self):
        return self.length

    def getNextProgram(self):
        return self.nextProgram

    def getFavorite(self):
        return self.favorite
    
    def getClock(self):
        return self.clock
    
    def getCsaClass(self):
        return self.csaClass
    
    def getRecording(self):
        return self.recording
    
    def getReminder(self):
        return self.reminder

    def display(self):
        self.logger.info("-------- program details ------")
        self.logger.info("lcn : " + str(self.lcn))
        self.logger.info("channel name : " + str(self.channelName))
        self.logger.info("program : " + str(self.program))
        self.logger.info("start : " + str(self.start))
        self.logger.info("length : " + str(self.length))
        self.logger.info("genre : " + str(self.genre))
        self.logger.info("next program : " + str(self.nextProgram))
        self.logger.info("favorite : " + str(self.favorite))
        self.logger.info("clock : " + str(self.clock))
        self.logger.info("csaClass : " + str(self.csaClass))
        self.logger.info("recording: " + str(self.recording))
        self.logger.info("reminder: " + str(self.reminder))
        self.logger.info("-------------------------------")


class RecordItem(object):

    def __init__(self, title, date, recording=False):
        self.title = title
        self.date = date
        self.recording = recording
        self.logger = logging.getLogger("NewTvTesting.RecordItem")

    def getTitle(self):
        return self.title

    def getDate(self):
        return self.date
    
    def getRecording(self):
        return self.recording

    def display(self):
        self.logger.info("-------- record details ------")
        self.logger.info(str(self.title))
        self.logger.info(str(self.date))
        self.logger.info("recording: " + str(self.recording))
        self.logger.info("------------------------------")

class RecordDetailedItem(object):

    def __init__(self, title, date, length, recording=False, csaClass=None):
        self.title = title
        self.date = date
        self.length = length
        self.recording = recording
        self.csaClass = csaClass
        self.logger = logging.getLogger("NewTvTesting.RecordDetailedItem")

    def getTitle(self):
        return self.title
    
    def getDate(self):
        return self.date
    
    def getLength(self):
        return self.length
    
    def getRecording(self):
        return self.recording
    
    def getCsaClass(self):
        return self.csaClass

    def display(self):
        self.logger.info("-------- record detailed details ------")
        self.logger.info("title : " + str(self.title))
        self.logger.info("date : " + str(self.date))
        self.logger.info("length : " + str(self.length))
        self.logger.info("recording: " + str(self.recording))
        self.logger.info("csaClass: " + str(self.csaClass))
        self.logger.info("------------------------------")

class ChannelDetail(object):

    def __init__(self, name, definition="HD", source="IP", slogan=None):
        self.name = name
        self.definition = definition
        self.source = source
        self.slogan = slogan

    def getName(self):
        return self.name

    def getDefinition(self):
        return self.definition

    def getSource(self):
        return self.source

    def getSlogan(self):
        return self.slogan


class TvItem(object):

    def __init__(self, lcn, channels):
        self.lcn = lcn
        self.channels = channels
        self.logger = logging.getLogger("NewTvTesting.TvItem")

    def getLcn(self):
        return self.lcn

    def getChannels(self):
        return self.channels

    def getChannel(self, n):
        return self.channels[n]

    def getFirstChannel_DttOff(self):
        for c in self.channels:
            if c.getSource() == "IP":
                if c.getDefinition() == "HD" and Env.DEFINITION == "HD":
                    return c
                if c.getDefinition() == "SD":
                    return c

    def getFirstChannel_DttOn(self):
        for c in self.channels:
            if c.getSource() == "DTT":
                return c
        return self.getFirstChannel_DttOff()

    def display(self):
        self.logger.info("-------- Tv details ------")
        self.logger.info(str(self.lcn))
        for c in self.channels:
            self.logger.info(str(c.name) + " / " + str(c.definition) + " / " + str(c.source))
        self.logger.info("--------------------------")


class VodItem(object):

    def __init__(self, title, genre, length, endDate, price):
        self.title = title
        self.genre = genre
        self.length = length
        self.endDate = endDate
        self.price = price
        self.logger = logging.getLogger('NewTvTesting.VodItem')

    def getTitle(self):
        return self.title

    def getGenre(self):
        return self.genre

    def getLength(self):
        return self.length

    def getEndDate(self):
        return self.endDate
    
    def getPrice(self):
        return self.price

    def display(self):
        self.logger.info("-------- Vod details ------")
        self.logger.info(str(self.title))
        self.logger.info("genre : " + str(self.genre))
        self.logger.info("length : " + str(self.length))
        self.logger.info("movie rental end date : " + str(self.endDate))
        self.logger.info("price : " + str(self.price))        
        self.logger.info("---------------------------")


class Status(object):

    def __init__(self, stbStatus, noRightPanel=None, scene=None, dialog=None):
        self.stbStatus = stbStatus
        self.noRightPanel = noRightPanel
        self.scene = scene
        self.dialog = dialog
        self.logger = logging.getLogger('NewTvTesting.Status')

    def getStbStatus(self):
        return self.stbStatus

    def findNoRightPanel(self):
        return self.noRightPanel

    def getScene(self):
        return self.scene

    def findDialogBox(self):
        return self.dialog

    def display(self):
        self.logger.info("-------- status ------")
        self.logger.info(" " + str(self.stbStatus))
        self.logger.info(" no right screen : " + str(self.noRightPanel))
        self.logger.info(" scene : " + str(self.scene))
        self.logger.info(" dialog box : " + str(self.dialog))
        self.logger.info("----------------------")


class TrickBarStatus(object):

    def __init__(self, trickVisible, trickIcon, messageFirstRow, messageSecondRow):
        self.trickVisible = trickVisible
        self.trickIcon = trickIcon
        self.messageFirstRow = messageFirstRow
        self.messageSecondRow = messageSecondRow
        self.logger = logging.getLogger('NewTvTesting.TrickBarStatus')
        
    def getTrickVisible(self):
        return self.trickVisible
    
    def getTrickIcon(self):
        return self.trickIcon
    
    def getMessageFirstRow(self):
        return self.messageFirstRow
    
    def getMessageSecondRow(self):
        return self.messageSecondRow
    
    def getMinutesInSecondRow(self):
        try:
            recordTime = re.findall('\d+', self.messageSecondRow)
            recordTime = int(recordTime[0])
            return recordTime
        except:
            return None

    def display(self):
        self.logger.info("-------- TrickBar ------")
        self.logger.info(" Trick visible : " + str(self.trickVisible))
        self.logger.info(" Trick Icon : " + str(self.trickIcon))
        self.logger.info(" Trick First Row : " + str(self.messageFirstRow))
        self.logger.info(" Trick Second Row : " + str(self.messageSecondRow))
        self.logger.info("------------------------")
