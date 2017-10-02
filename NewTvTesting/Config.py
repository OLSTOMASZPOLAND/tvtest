# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser
import os

def readConfig(param):
    parser = SafeConfigParser()
    parser.readfp('config.ini')
    return parser.get('general', param)


class Env(object):

    parser = SafeConfigParser()
    parser.read('config.ini')

    REPORT_DIR = parser.get('general', 'report_dir')
    XML_DIR = parser.get('general', 'xml_dir')
    TEXT_DIR = parser.get('general', 'text_dir')
    TS_SUMMARY = parser.get('general', 'ts_summaryReport')
    TC_STBLOGS_DIR = parser.get('general', 'tc_stblogs_dir')
    TC_SCREENSHOTS_DIR = parser.get('general', 'tc_screenshots_dir')
    TC_RUNLOGS_FILE = parser.get('general', 'tc_runlogs_file')
    STB = parser.get('stb_config', 'stb')
    VIDEO = parser.getboolean('general', 'video')
    DTT = parser.getboolean('stb_config', 'dtt_capability')
    URL_RPI = parser.get('general', 'url_rpi')
    DEFINITION = parser.get('stb_config', 'definition')
    ESP_FILE = parser.get('stb_environment', 'esp_file')
    CONFIDENTIAL_CODE = parser.get('stb_config', 'confidential_code')
    PARENTAL_CODE = parser.get('stb_config', 'parental_code')
    BROWSER = parser.get('general', 'browser')
    INFRARED = parser.get('general', 'infrared')
    STB_LOGS_MAX_LINE_COUNT = parser.get('general', 'stb_logs_max_line_count')
    STB_GRABBER_RESET = parser.get('general', 'stbt_grabber_reset_script')
    ZONE = parser.get('stb_environment', 'zone')
    STB_MODEL = parser.get('stb_environment', 'stb_model')

class Rpi(object):

    URL_RPI = Env.URL_RPI

    URL_RPI_KEY = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName="
    URL_RPI_ZAP = URL_RPI + "sendChannelNumber.php?forceIR=" + \
        Env.INFRARED + "&channelNumber="
    URL_RPI_STATUS = URL_RPI + "StbGetStatus.php?forceIR=" + \
        Env.INFRARED
    URL_RPI_RESET = URL_RPI + "StbHardReboot.php"
    URL_RPI_START_LOGS = URL_RPI + "StbStartLogs.php?lineCount=" + Env.STB_LOGS_MAX_LINE_COUNT
    URL_RPI_STOP_LOGS = URL_RPI + "StbStopLogs.php"
    URL_RPI_GET_LOGS = URL_RPI + "StbGetLogs.php"
    # URL_RPI_RUN_COMMAND = URL_RPI + "StbRunCommand.php?command=%20more%20%2Fproc%2Fhnsa%2Ffrontpanel%20&timeout=true&forceNoShell=true&fireAndForget=false&retrieveStdout=true"
    URL_RPI_GET_FRONT_PANEL = URL_RPI + "StbRunCommand.php?command=%20more%20%2Fproc%2Fhnsa%2Ffrontpanel%20&timeout=true&forceNoShell=true&fireAndForget=false&retrieveStdout=true"  # Tomasz stasiuk

    DUMP = URL_RPI + \
        "sendKey.php?dumpDom=true&remoteName=newtv&forceIR=" + Env.INFRARED

    KEY_MENU = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_MENU"
    KEY_DOWN = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_DOWN"
    KEY_OK = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_OK"
    KEY_CHANNELUP = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_CHANNELUP"
    KEY_INFO = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_INFO"
    KEY_UP = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_UP"
    KEY_RIGHT = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_RIGHT"
    KEY_BACK = URL_RPI + "sendKey.php?dumpDom=false&remoteName=newtv&forceIR=" + \
        Env.INFRARED + "&keyName=KEY_BACK"


class ConfAR (object):
    MAX_ITEMS = 10
    MAX_ITEMS_TOOLBOX = 8


class Menu(object):

    # tab_myAccount = ["KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_RIGHT","KEY_RIGHT","KEY_RIGHT","KEY_OK"]
    # tab_myAccount = ["KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_OK","KEY_DOWN","KEY_DOWN","KEY_DOWN","KEY_OK"]
    tab_myAccount = [
        "KEY_DOWN", "KEY_DOWN", "KEY_DOWN", "KEY_DOWN", "KEY_DOWN", "KEY_OK"]
    tab_pvr = ["KEY_RIGHT", "KEY_RIGHT", "KEY_DOWN", "KEY_OK"]
    tab_epg = ["KEY_RIGHT", "KEY_OK"]
    tab_videoOnDemand = []

    ''' main menu'''

    greenMode = u"zarządzanie energią".encode('utf-8')
    greenModeTurnedOff = u"wyłączone.".encode('utf-8')
    greenModeTurnedOn = u"włączone.".encode('utf-8')
    
    prepaidAccount = u"konto prepaid".encode('utf-8')
    prepaidRecharge1 = u"50zł + bonus 10zł".encode('utf-8')
    prepaidRecharge2 = u"100zł".encode('utf-8')
    prepaidRecharge3 = u"25zł + bonus 5zł".encode('utf-8')
    prepaidRecharge4 = u"19,99zł + bonus 4zł".encode('utf-8')
    alsoSee = u"zobacz również".encode('utf-8')
    alsoSeeWithColon = u"zobacz również :".encode('utf-8')
    satSettings = u"ustawienia sat".encode('utf-8')
    satOne = u"jedno".encode('utf-8')
    satTwo = u"dwa".encode('utf-8')
    satZero = u"zero".encode('utf-8')
    satDecoder = u"dekoder".encode('utf-8')
    satDiseqcDisabled = u"wyłączony".encode('utf-8')
    

#   tvChannels = u"chaînes TV"
    tvChannels = u"Orange TV".encode('utf-8')

#   myAccount = u"mon compte"
    myAccount = u"moje konto".encode('utf-8')

#   myPurchases = u"mes achats"
    myPurchases = u"płatności".encode('utf-8')
    zoom = u"zoom".encode('utf-8')
    zoomNo = u"zoom (nie)".encode('utf-8')
    zoomYes = u"zoom (tak)".encode('utf-8')
    
    confirm = u"potwierdź".encode('utf-8')
#   myCodes = u"mes codes"
    myCodes = u"zmiana kodów".encode('utf-8')
    
    adultCode = u"kod dorosłych".encode('utf-8')
    parentalCode = u"kod dostępu".encode('utf-8')

#   mySettings = u"mes réglages"
    # WARRNING !!! There is space at the end.
    mySettings = u"moje ustawienia ".encode('utf-8')
    # mySettings = u"ustawienia tv"

    tvSettings = u"ustawienia tv".encode('utf-8')

    multimedia = u"multimedia".encode('utf-8')
#   myPreferences = u"mes préférences"
    myPreferences = u"kanały"  # to jest chyba to samo co mySettings

#   epg = u"programme TV"
    epg = u"program tv".encode('utf-8')
    
    pvrManageRecordConflicts = u"zarządzaj dwoma nagraniami".encode('utf-8')
    pvrRecordConflict = u"konflikt!".encode('utf-8')

#   videoOnDemand = u"vidéo a la demande"
    videoOnDemand = u"wideo na życzenie".encode('utf-8')
    
    channelNotInSubscription = u"Wybrany kanał nie należy do Twojej subskrypcji".encode('utf-8')

#   screenSize = u"format écran TV"
    screenSize = u"format obrazu".encode('utf-8')

#   size_4_3 = u"4/3"
    size_4_3 = u"4:3"

#   size_16_9 = u"16/9"
    size_16_9 = u"16:9"

#   parentalControl = u"contrôle parental"
    parentalControl = u"kontrola rodzicielska".encode('utf-8')

#   language = u"langue"
    language = u"wersja językowa".encode('utf-8')
    
#   nativeSoundtrack = u"version française"
    nativeSoundtrack = u"z lektorem".encode('utf-8')

#   orginalSoundtrack = u"version originale"
    orginalSoundtrack = u"oryginalna".encode('utf-8')

#   subtitles = u"sous-titres"
    subtitles = u"napisy".encode('utf-8')

#   noSubtitle = u"aucun"
    noSubtitle = u"brak".encode('utf-8')
    
    subtitleSelectNone = u"brak".encode('utf-8') 
    
    subtitleSelectPolish = u"polskie".encode('utf-8') 
        
    subtitleSelectImpairedHearing = u"dla niesłyszących".encode('utf-8') 

#   nativeSubtitles = u"français"
    nativeSubtitles = u"polskie".encode('utf-8')

#   hearingImpairedSubtitles = u"sourds et malentendants"
    hearingImpairedSubtitles = u"dla niesłyszących".encode('utf-8')

    tvOnDemand = u"TV na życzenie".encode('utf-8')

#   myChannels = u"mes chaînes"
    myChannels = u"kanały".encode('utf-8')

#   personalizedSuggestion = u"suggestions personalisées"
    personalizedSuggestion = u"polecane".encode('utf-8')


#   accessibiliy = u"accessibilité"
    accessibiliy = u"udogodnienia".encode('utf-8')

#   legalInformation = u"infos juridiques"
    legalInformation = u"warunki prawne".encode('utf-8')

    activate = u"aktywuj".encode('utf-8')
    deactivate = u"deaktywuj".encode('utf-8')
    myViewershipRecommendation = u"moja oglądalność TV".encode('utf-8')
    
    audioDescription = u"audiodeskrypcja".encode('utf-8')
    audioDescriptionNo = u"audiodeskrypcja (nie)".encode('utf-8')
    audioDescriptionYes = u"audiodeskrypcja (tak)".encode('utf-8')

#   dttChannels = u"chaînes TNT"
    dttChannels = u"kanały tv naziemnej".encode('utf-8')
    dttChannelsRFTV = u"kanały telewizyjne".encode('utf-8')

#   dttSearch = u"lancer la recherche"
    dttSearch = u"rozpocznij wyszukiwanie".encode('utf-8')
    dttSearchLater = u"rozpocznij później".encode('utf-8')

#   dttDesactivation = u"désactiver les chaînes TNT"
    dttDesactivation = u"wyłącz kanały tv naziemnej".encode('utf-8')

    ''' vod '''

#   vodTrailer = u"bande-annonce"
    csa1_1h = u"csa1licencja1h".encode('utf-8')
    csa2_1h = u"csa2licencja1h".encode('utf-8')
    csa3_1h = u"csa3licencja1h".encode('utf-8')
    csa4_1h = u"csa4licencja1h".encode('utf-8')
    csa4_2h = u"csa4licencja2h".encode('utf-8')
    vodPackage = u"Fast and Furious".encode('utf-8')
    vodTrailer = u"zwiastun".encode('utf-8')
    vodTrailerDownloading = u"Trwa pobieranie zwiastuna".encode('utf-8')
    
    vodDownloading = u"pobieranie".encode('utf-8')
    
    vodSummary = u"streszczenie".encode('utf-8')
    VodBeginning = u"od początku".encode('utf-8')
    
    vodCatalog = u"katalog filmów".encode('utf-8')
    vodCatalogHorror = u"horror".encode('utf-8')
    vodCatalogWithTestContent = u"komedia".encode('utf-8')  # TODO correct place to store that config
    vodAdultCatalogWithTestContent = u"hetero".encode('utf-8')  # TODO correct place to store that config
    
    vodMyVideos = u"moje zamówienia".encode('utf-8')
    vodOrderPackage = u"zamów paczkę".encode('utf-8')
    
    vodAdults = u"dla dorosłych".encode('utf-8')
    vodSearch = u"wyszukiwarka".encode("utf-8")   
    vodNPK = u"Podsumowanie".encode('utf-8')  
    vodNPKlower = u"podsumowanie".encode('utf-8')
    vodNPKInfo = u"Informacja".encode('utf-8')
    vodAutomation  = u"automatyzacja".encode('utf-8')
    vodPolishMovies = u"kino polskie".encode('utf-8')
    vodDownloadComplete = u"pobieranie zakończone".encode('utf-8')
    vodDownloadInProgress = u"trwa pobieranie".encode('utf-8')
    vodDownloadSuspended = u"pobieranie wstrzymane".encode('utf-8')
    

    # vodAddToFavorites = u"ajouter aux favoris"
    vodAddToFavorites = u"dodaj do wybranych".encode('utf-8')
    
    favoriteChannels = u"kanały".encode('utf-8')
    
    # vodRemoveFromFavorites = u"retirer des favoris"
    vodRemoveFromFavorites = u"usuń z wybranych".encode('utf-8')
    # vodMyFavorites = u"Mes favoris"
    vodMyFavorites = u"moje wybrane".encode('utf-8')
    vodPurchaseConfirm = u"kontrola zakupów".encode('utf-8')
    # vodPayment = u"confirmer votre paiement"
    vodPayment = u"potwierdzenie zamówienia".encode('utf-8')
    # vodConfirm = u"confirmer votre location"
    # vodRent = u"louer"
    vodRent = u"wypożycz".encode('utf-8')
    vodPlay = u"oglądaj".encode('utf-8')
    vodPay = u"zamawiam i płacę".encode('utf-8')
    # vodResume = u"reprendre"
    vodAdultPopup = u"niepełnoletnich".encode('utf-8')
    vodResume = u"wznów oglądanie".encode('utf-8')
    vodStartWatching = u"rozpocznij oglądanie".encode('utf-8')
    vodStopWatching = u"zatrzymaj".encode('utf-8')
    vodInfo = u"informacja".encode('utf-8')
    vodMyVod = u"Mes vidéos"
    vodPackageOffer = u"zawartość oferty".encode('utf-8')
    VodError = u"błąd".encode('utf-8')  # TODO
    purchaseHistory = u"historia zakupów".encode("utf-8")

    ''' epg '''
#   epgTonight = u"ce soir"
    epgTonight = u"dzisiaj wieczorem".encode('utf-8')

    epgAlertOn = u"powiadom mnie".encode('utf-8')
    epgAlertOff = u"nie powiadamiaj mnie".encode('utf-8')
    
#   epgWeek = u"en ce moment"
    epgWeek = u"teraz".encode('utf-8')

#   epgDay = u"choisir un jour"
    epgDay = u"wybierz dzień".encode('utf-8')
    epgDayTomorrow = u"jutro".encode('utf-8') 
#   epgMyChannels = u"mes chaînes"
    epgMyChannels = u"kanały".encode('utf-8')

#   epgSearch = u"recherche"
    epgSearch = u"wyszukaj".encode('utf-8')

    # epgRecord = u"enregistrer".encode('utf-8')
    epgRecord = u"nagraj".encode('utf-8')
    epgPlay = u"oglądaj".encode('utf-8')

    ''' pvr '''
    hardDrive = u"dysk twardy".encode('utf-8')
#   pvr = u"enregistreur TV"
    pvr = u"nagrywarka".encode('utf-8')
    pvrTV = u"nagrywarka TV".encode('utf-8')
    pvrRecording = u"nagrywanie".encode('utf-8')
    
    pvrRecord = u"nagranie".encode('utf-8')
    
#   pvrMyRecords = u"mes enregistrements"
    pvrMyRecords = u"moje nagrania".encode('utf-8')
    
    pvrAdults = u"dla dorosłych".encode('utf-8')

#   pvrPlay = u"regarder"
    pvrPlay = u"oglądaj".encode('utf-8')

#   pvrResume = u"reprendre"
    pvrResume = u"wznów oglądanie".encode('utf-8')

#   pvrDelete = u"effacer"
    pvrDelete = u"usuń".encode('utf-8')
    
    pvrCancelRecord = u"zrezygnuj z nagrywania".encode('utf-8')

#   pvrYes = u"oui"
    pvrYes = u"tak".encode('utf-8')

#   pvrNo = u"non"
    pvrNo = u"nie".encode('utf-8')
    
    pvrChange = u"zmień".encode('utf-8')
    pvrChangeConfirm = u"Zmiany zostały wprowadzone".encode('utf-8')    
    
    pvrStopRecord = u"zatrzymanie bieżącego nagrania".encode("utf-8")
    pvrStopRecordConfirm = u"Nagranie zostało zatrzymane".encode("utf-8")
    pvrStop = u"zatrzymać trwające nagranie".encode("utf-8")
    pvrStop2 = u"zatrzymaj".encode('utf-8')
#   pvrManualRecord = u"enregistrer manuellement"
    pvrManualRecord = u"planowanie nagrań".encode('utf-8')

#    pvrScheduleOk = u"C’est fait !"

#   pvrMySchedulings = u"mes programmations"
    pvrMyScheduled = u"zaplanowane nagrania".encode('utf-8')

    ''' toolbox'''
    toolboxShare = u"partager"
    toolboxOndemand = u"a la demande".encode('utf-8')
    toolboxScreenSizeNative = u"format obrazu (oryginalny)".encode('utf-8')

#   toolboxSummary = u"résumé"
    toolboxSummary = u"streszczenie".encode('utf-8')

#   toolboxFavouriteChannelsNo = u"chaînes (non)"
    toolboxFavouriteChannelsNo = u"kanały (nie)".encode('utf-8')

#   toolboxFavouriteChannelsYes = u"chaînes (oui)"
    toolboxFavouriteChannelsYes = u"kanały (tak)".encode('utf-8')

#   toolbox_2_favouriteChannelYes = u"oui"
    toolbox_2_favouriteChannelYes = u"tak".encode('utf-8')

#   toolbox_2_favouriteChannelNo = u"non"
    toolbox_2_favouriteChannelNo = u"nie".encode('utf-8')

#   toolboxNativeSoundtrack = u"langue (français)"
#   toolboxNativeSoundtrack = u"z lektorem"
    toolboxNativeSoundtrack = u"język (polski)".encode('utf-8')

#   toolboxOriginalSoundtrack = u"langue (anglais)"
#   toolboxOriginalSoundtrack = u"oryginalna"
    toolboxOriginalSoundtrack = u"język (angielski)".encode('utf-8')

#   toolboxAdSoundtrack = u"langue (audio description)"
    toolboxAdSoundtrack = u"audio deskrypcja".encode('utf-8')


#   toolbox_2_nativeSoundtrack = u"français"
#   toolbox_2_nativeSoundtrack = u"z lektorem"
    toolbox_2_nativeSoundtrack = u"polski".encode('utf-8')
    
    toolbox_2_englishSoundtrack = u"angielski".encode('utf-8')

#   toolbox_2_originalSoundtrack = u"anglais"
    toolbox_2_originalSoundtrack = u"oryginalna".encode('utf-8')

#   toolbox_2_adSoundtrack = u"audio description"
    toolbox_2_adSoundtrack = u"audio deskrypcja".encode('utf-8')

#   toolboxNoSubtitle = u"sous-titres (aucun)"
    toolboxNoSubtitle = u"brak".encode('utf-8')

#   toolboxNativeSubtitle = u"sous-titres (français)"
    toolboxNativeSubtitle = u"napisy (polski)".encode('utf-8')
    toolboxNoSubtitleLong = u"napisy (brak)".encode('utf-8')
    toolboxOriginalSubtitle = u"napisy (angielski)".encode('utf-8')
#   toolboxHearingImpairesSubtitles = u"sous-titres (malentendant)"
    toolboxHearingImpairesSubtitles = u"dla niesłyszących".encode('utf-8')


#   toolbox_2_noSubtitle = u"aucun"
    toolbox_2_noSubtitle = u"brak".encode('utf-8')

#   toolbox_2_nativeSubtitle = u"français"
    toolbox_2_nativeSubtitle = u"polski".encode('utf-8')

#   toolbox_2_hearingImpairesSubtitles = u"malentendant"
    toolbox_2_hearingImpairesSubtitles = u"dla niesłyszących".encode('utf-8')

#   toolboxImageSizeOriginal = u"format image (original)"
    toolboxImageSizeOriginal = u"format (oryginalny)".encode('utf-8')

    toolboxImageSizeZoom = u"format (zoom)".encode('utf-8')

#   toolboxImageSizeWide = u"format image (large)"
    toolboxImageSizeWide = u"format (szeroki)".encode('utf-8')

#   toolbox_2_imageSizeOriginal = u"original"
    toolbox_2_imageSizeOriginal = u"oryginalny".encode('utf-8')

    toolbox_2_imageSizeZoom = u"zoom".encode('utf-8')

#   toolbox_2_imageSizeWide = u"large"
    toolbox_2_imageSizeWide = u"szeroki".encode('utf-8')

    noFavoriteChannelsInChannelsList = u"Żaden kanał nie został wybrany.".encode('utf-8')
    pvrConfirmation = u"potwierdzenie zapisu".encode('utf-8')

    toolboxSource = u"source"
    
    conflictAttention = u"uwaga".encode('utf-8')
    
    oneShotMovie = u"5 PLN".encode('utf-8')
    film = u"5 PLN".encode('utf-8')
    filmNO = u"SD_vod_test_5_csa3".encode('utf-8')
    film_csa1 =  u"VOD_csa1".encode('utf-8')
    VOD_ang_subtitles = u"SD_vod_test_5_csa3".encode('utf-8')
    VOD_subtitles = u"SD_vod_test_5_csa3".encode('utf-8')
    VOD_subtitlesV2 = u"VOD_subtitles".encode('utf-8')
    VOD_ang_language  = u"5 PLN".encode('utf-8')
    VOD_language = u"5 PLN".encode('utf-8')
    VOD_language_subtitles = u"5 PLN".encode('utf-8')
    VOD_csa1 = u"5 PLN".encode('utf-8')
    VOD_csa2 = u"5 PLN".encode('utf-8')
    VOD_csa3 = u"5 PLN".encode('utf-8')
    VOD_csa4 = u"5 PLN".encode('utf-8')
    VOD_csa5 = u"5 PLN".encode('utf-8')
    VOD_oneshot_csa1 = u"5 PLN".encode('utf-8')
    VOD_oneshot_csa1v2 = u"VOD_oneshot_csa1".encode('utf-8')
    VOD_oneshot_csa5 = u"5 PLN".encode('utf-8')
    VOD_long_view = u"5 PLN".encode('utf-8')
    VOD_long_time = u"5 PLN".encode('utf-8')
    VOD_HD = u"5 PLN".encode('utf-8')
    VOD_SD = u"5 PLN".encode('utf-8')
    VOD_csa5_adult = u"5 PLN".encode('utf-8')
    VOD_oneshot_csa1_adult = u"5 PLN".encode('utf-8')
    VOD_oneshot_csa5_adult = u"5 PLN".encode('utf-8')
    VOD_long_time_adult = u"5 PLN".encode('utf-8')
    
    
class DialogBox(object):

    WrongNewParentalCode0000 = u"Kod dostępu musi być inny niż 0000".encode('utf-8')
    WrongNewAdultCode0000 = u"Kod dorosłych musi być inny niż 0000".encode('utf-8')
    NewAdultCodeConfirmation = u"Kod dorosłych został zmieniony".encode('utf-8')
    RecordOnGoing = u"en cours d'enregistrement"
    RecordStartingSoon = u"va démarrer dans 3 mn"
    RecordConflict = u"Conflit d'enregistrement"
    RecordConflictManagement = u"gestion avancée du conflit"
    DttScanning = u"recherche de chaînes TNT"
    VodError = u"Błąd".encode('utf-8')
    VodError2 = u"połączenie z usługą".encode('utf-8') 
    VodError3 = u"błąd pobierania".encode('utf-8')
    WrongParentalCode = u"błędny kod dostępu".encode('utf-8')
    WrongConfidentialCode = u"Błędny kod dorosłych".encode('utf-8')
    NewParentalCodeConfirmation = u"Kod dostępu został zmieniony".encode('utf-8')
    PvrParentalControl = u"dostęp do programu".encode('utf-8')
    PvrDeleteRecord = u"usuwanie nagrania".encode('utf-8')
    PvrDeleteRecordError = u"Błąd podczas usuwania".encode('utf-8')
    PvrNoRecords = u"brak nagrań".encode('utf-8')
    PvrScheduleError = u"Wystąpił błąd w planowaniu nagrań!".encode('utf-8')
    PvrNoScheduled = u"Nie masz zaplanowanych żadnych nagrań.".encode('utf-8')
    PvrScheduleOk = u"powiadomienie".encode('utf-8')
    Close = u"zamknij".encode('utf-8')
    AdultCodeMismatch = u"Kod dorosłych i potwierdzenie\npowinny być identyczne".encode('utf-8')
    ConfidentialCodeMismatch = u"Kod dostępu i potwierdzenie powinny być identyczne".encode('utf-8')
    AnotherPvrRunning = u"Nie można uruchomić szybkiego nagrywania".encode('utf-8')
    PvrConfirm = u"potwierdź".encode('utf-8')
    GreenEnergyOn = u"włącz".encode('utf-8')
    GreenEnergyOff = u"wyłącz".encode('utf-8')
    ConflictRecordsLongMessage = u"Twój program nie może zostać zatwierdzony".encode('utf-8')
    ConflictRecordTitle = u"informacja".encode('utf-8')

class ParentalControl(object):
    SetDeactive = "Deactive"
    SetActiveCsa2 = "ActiveCsa2"
    SetActiveCsa3 = "ActiveCsa3"
    SetActiveCsa4 = "ActiveCsa4"
    
    Activate = u"aktywuj".encode('utf-8')
    ActivateCsa2 = u"7, 12, 16 lat".encode('utf-8')
    ActivateCsa3 = u"12, 16 lat".encode('utf-8')
    ActivateCsa4 = u"16 lat".encode('utf-8')
    deactivate = u"deaktywuj".encode('utf-8')
    IsActivatedDesc = u"aktywna".encode('utf-8')
    IsDeactivatedDesc = u"nieaktywna".encode('utf-8')
    IsActivatedCsa2Desc = u"7, 12, 16 lat".encode('utf-8')
    IsActivatedCsa3Desc = u"12, 16 lat".encode('utf-8')
    IsActivatedCsa4Desc = u"16 lat".encode('utf-8')
    
    CssClassCsa1 = u"csa01".encode('utf-8')
    CssClassCsa2 = u"csa02".encode('utf-8')
    CssClassCsa3 = u"csa03".encode('utf-8')
    CssClassCsa4 = u"csa04".encode('utf-8')
    CssClassCsa5 = u"csa05".encode('utf-8')

class InfoMessages(object):
    VodErrorTech = u"VOD technical problem"
    VodErrorMenu = u"VOD menu problem"
    CsaContentNotFound = u"Content with expected CSA level not found"
    ContentNotFound = u"Content not found"

class Remote(object):
    LETTERS = {}
    LETTERS["a"] = [2, 1]
#    LETTERS["ą"] = [2, 2]
    LETTERS["b"] = [2, 3]
    LETTERS["c"] = [2, 4]
#    LETTERS["ć"] = [2, 5]
    LETTERS["d"] = [3, 1]
    LETTERS["e"] = [3, 2]
#    LETTERS["ę"] = [3, 3]
    LETTERS["f"] = [3, 4]
    LETTERS["g"] = [4, 1]
    LETTERS["h"] = [4, 2]
    LETTERS["i"] = [4, 3]
    LETTERS["j"] = [5, 1]
    LETTERS["k"] = [5, 2]
    LETTERS["l"] = [5, 3]
#    LETTERS["ł"] = [5, 4]
    LETTERS["m"] = [6, 1]
    LETTERS["n"] = [6, 2]
#    LETTERS["ń"] = [6, 3]
    LETTERS["o"] = [6, 4]
#    LETTERS["ó"] = [6, 5]
    LETTERS["p"] = [7, 1]
    LETTERS["q"] = [7, 2]
    LETTERS["r"] = [7, 3]
    LETTERS["s"] = [7, 4]
#    LETTERS["ś"] = [7, 5]
    LETTERS["t"] = [8, 1]
    LETTERS["u"] = [8, 2]
    LETTERS["v"] = [8, 3]
    LETTERS["w"] = [9, 1]
    LETTERS["x"] = [9, 2]
    LETTERS["y"] = [9, 3]
    LETTERS["z"] = [9, 4]
#    LETTERS["ź"] = [9, 5]
#    LETTERS["ż"] = [9, 6]

    LETTERS["0"] = [0, 2]
    LETTERS["1"] = [1, 8]
    LETTERS["2"] = [2, 6]
    LETTERS["3"] = [3, 5]
    LETTERS["4"] = [4, 4]
    LETTERS["5"] = [5, 5]
    LETTERS["6"] = [6, 6]
    LETTERS["7"] = [7, 6]
    LETTERS["8"] = [8, 4]
    LETTERS["9"] = [9, 7]

    LETTERS[" "] = [0, 1]
    LETTERS["@"] = [1, 1]
    LETTERS["."] = [1, 2]
    LETTERS[","] = [1, 3]
    LETTERS["-"] = [1, 4]
    LETTERS["?"] = [1, 5]
    LETTERS["!"] = [1, 6]
    LETTERS["&"] = [1, 7]
    
class Description(object):
    
    favoriteZeroChannels = u"Brak kanałów".encode('utf-8')
    favoriteInList = u"ulubione kanały".encode('utf-8')
    informationInList = u"Informacje".encode('utf-8')
    sportInList = u"Sport".encode('utf-8')
    orangeTvInList = u"Orange TV".encode('utf-8')
    IsActivatedRecommendation = u"aktywna".encode('utf-8')
    IsDeactivatedRecommendation = u"nieaktywna".encode('utf-8')
    vodSearchNone = u"Brak wyników".encode('utf-8')
    vodSearchNonePopup = u"Spróbuj wpisać do wyszukiwarki inne słowo lub zamknij klawiaturę.".encode('utf-8')
