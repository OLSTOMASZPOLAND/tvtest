# -*- coding: utf-8 -*-

from ResidentAppPage import TvItem, ChannelDetail
from Config import Env
import json


def EspDataChannel(package, lcn):

    with open(Env.ESP_FILE) as json_file:
        json_data = json.load(json_file)
        try:
            find = False
            lcnTab = json_data['UNIVERS_LIST'][
                package]['Bqt_List'][0]['Chnl_List']
            for index, l in enumerate(lcnTab):
                if l['LCN'] == lcn:
                    find = True
                    break
            if find:
                channels = []
                # for c in json_data['UNIVERS_LIST'][package]['Bqt_List'][0]['Chnl_List'][index]['Srv_List']:
                #   channels.append(ChannelDetail(c['Lng_nme'],c['ResT'],c['Src'],c['Slg']))
                for c in json_data['UNIVERS_LIST'][package]['Bqt_List'][0]['Chnl_List'][index]['Srv_List']:
                    channels.append(
                        ChannelDetail(c['Lng_nme'], c['ResT'], c['Src']))
                return TvItem(lcn, channels)
            else:
                return -1
        except (KeyError):
            return -1


def EspDataPackage(package):
    with open(Env.ESP_FILE) as json_file:
        json_data = json.load(json_file)
        try:
            packageName = json_data['UNIVERS_LIST'][
                package]['Bqt_List'][0]['Lng_nme']
            return packageName
        except (KeyError):
            pass


class LiveData(object):

    ''' Package A -> bouquet cible pour tests
        PFQ : Orange = 1 ; CANAL = 0'''


#     PACKAGE_A = 1
#     PACKAGE_B = 0
#
#     PACKAGE_A_NAME = EspDataPackage(1)
#     PACKAGE_B_NAME = EspDataPackage(0)
#
#     TV1 = EspDataChannel(PACKAGE_A,1)
#     TV2 = EspDataChannel(PACKAGE_A,2)
#     TV3 = EspDataChannel(PACKAGE_A,3)
#     TV4 = EspDataChannel(PACKAGE_A,4)
#     TV5 = EspDataChannel(PACKAGE_A,5)
#     TV6 = EspDataChannel(PACKAGE_A,6)
#     TV8 = EspDataChannel(PACKAGE_A,8)
#     TV12 = EspDataChannel(PACKAGE_A,12)
#     TVnoright = TvItem(980,[ChannelDetail("no right","HD","IP")])
#
#     TVCSA5 = TvItem(204,[ChannelDetail("CSA5","HD","IP")])

    ''' Package A -> bouquet Orange TV'''

    PACKAGE_A = 0

    PACKAGE_A_NAME = EspDataPackage(0)

    TV1 = EspDataChannel(PACKAGE_A, 1)
    TV2 = EspDataChannel(PACKAGE_A, 2)
    TV3 = EspDataChannel(PACKAGE_A, 3)
    TV4 = EspDataChannel(PACKAGE_A, 4)
    TV5 = EspDataChannel(PACKAGE_A, 5)
    TV6 = EspDataChannel(PACKAGE_A, 6)
    TV8 = EspDataChannel(PACKAGE_A, 8)
    TV15 = EspDataChannel(PACKAGE_A, 15)  # Polsat News
    TV45 = EspDataChannel(PACKAGE_A, 45)  # FOX HD
    TVnoright = TvItem(980, [ChannelDetail("no right", "HD", "IP")])

    TVCSA5 = TvItem(204, [ChannelDetail("CSA5", "HD", "IP")])


class PvrData(object):

    ''' record length min '''
    LENGTH_1 = 8
    LENGTH_2 = 16
    LENGTH_3 = 32


class TimeShifting(object):

    ''' TS record length min '''

    LENGTH_1 = 2
    LENGTH_2 = 10


class VodData(object):

    TRAILER_1 = [u"tous les films récents", u"20 plus récentes",
                 u"REFMA03_2ndExploit Camille redouble G4R1C3P2", ]
    FAVORITE_1 = [u"recherche par genre", u"famille", u"Air Bud Superstar"]
    VOD_2 = [u"recherche par genre", u"aventure", u"Fire & ice JFB0"]
    VOD_3 = [u"recherche par genre", u"aventure", u"Fire & ice JFB21"]
    VOD_1 = [u"recherche par genre", u"aventure", u"Abel - HD"]
