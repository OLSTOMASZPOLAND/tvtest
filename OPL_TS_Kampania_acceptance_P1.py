# -*- coding: utf-8 -*-
import unittest
from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles
from OPL_Testing.TC_2951_T014369_zap_to_mosaic import TC_2951_T014369_zap_to_mosaic
from OPL_Testing.TC_2980_T014405_open_the_toolbox import TC_2980_T014405_open_the_toolbox
from OPL_Testing.TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream import TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream
from OPL_Testing.TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox import TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox
from OPL_Testing.TC_2998_T014426_use_timeshift_on_allowed_program_update import TC_2998_T014426_use_timeshift_on_allowed_program_update
from OPL_Testing.TC_3003_T014446_NavigateIntiTheZappingList import TC_3003_T014446_NavigateIntiTheZappingList
from OPL_Testing.TC_3162_T014637_Navigate_into_EPG_all_program_grid import TC_3162_T014637_Navigate_into_EPG_all_program_grid
from OPL_Testing.TC_3167_T014645_Navigate_into_EPG_days_list_update import TC_3167_T014645_Navigate_into_EPG_days_list_update
from OPL_Testing.TC_3186_T016089_search_a_content_without_choose_a_search_type_update import TC_3186_T016089_search_a_content_without_choose_a_search_type_update
from OPL_Testing.TC_3356_T014489_consult_favorite_channels_from_my_account import TC_3356_T014489_consult_favorite_channels_from_my_account
from OPL_Testing.TC_3368_T014506_consult_prepaid_account import TC_3368_T014506_consult_prepaid_account
from OPL_Testing.TC_3420_T015654_Reload_prepaid_account_payment_control_activated import TC_3420_T015654_Reload_prepaid_account_payment_control_activated
from OPL_Testing.TC_3541_T014667_search_a_content_on_vod_catalog import TC_3541_T014667_search_a_content_on_vod_catalog
from OPL_Testing.TC_3587_T014539_consult_the_video_presentation_screen_nominal_case import TC_3587_T014539_consult_the_video_presentation_screen_nominal_case
from OPL_Testing.TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog import TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog
from OPL_Testing.TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog import TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog
from OPL_Testing.TC_9402_T09402_Navigate_into_EPG_homepage import TC_9402_T09402_Navigate_into_EPG_homepage
from OPL_Testing.TC_9470_T014339_Zap_to_basic_channel import TC_9470_T014339_Zap_to_basic_channel
from OPL_Testing.TC_9580_T015441_Awake_last_watched_channel import TC_9580_T015441_Awake_last_watched_channel
from OPL_Testing.TC_9581_T017245_Awake_from_active_standby_mode import TC_9581_T017245_Awake_from_active_standby_mode
from OPL_Testing.TC_9582_T017246_Awake_from_standby_mode import TC_9582_T017246_Awake_from_standby_mode
from OPL_Testing.TC_9583_T017247_Awake_from_deep_standby_mode import TC_9583_T017247_Awake_from_deep_standby_mode
from OPL_Testing.TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR import TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR
from OPL_Testing.TC_18483_18481_OgladajDttTvNagrywajIpZEpg import TC_18483_18481_OgladajDttTvNagrywajIpZEpg
from OPL_Testing.TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran import TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran
from OPL_Testing.TC_18489_OgladajIpTvNagrywajDttZInstantPVR import TC_18489_OgladajIpTvNagrywajDttZInstantPVR
from OPL_Testing.TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran import TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran
from OPL_Testing.TC_18493_OgladajDttTvNagrywajIpZInstantPvr import TC_18493_OgladajDttTvNagrywajIpZInstantPvr
from OPL_Testing.TC_18725_T0000000_conflict_popup_pvr_tc1 import TC_18725_T0000000_conflict_popup_pvr_tc1
from OPL_Testing.TC_18726_T0000000_conflict_popup_pvr_tc2 import TC_18726_T0000000_conflict_popup_pvr_tc2
from OPL_Testing.TC_18727_T0000000_conflict_popup_pvr_tc3 import TC_18727_T0000000_conflict_popup_pvr_tc3
from OPL_Testing.TC_13227_T999999_instant_recording_immediately import TC_13227_T999999_instant_recording_immediately
from OPL_Testing.TC_3004_T014447_Zapping_list_no_favorite_channel import TC_3004_T014447_Zapping_list_no_favorite_channel
from OPL_Testing.TC_9471_T014340_Zap_to_basic_channel import TC_9471_T014340_Zap_to_basic_channel
from OPL_Testing.TC_9472_T014341_Zap_to__basic_channel_infobanner import TC_9472_T014341_Zap_to__basic_channel_infobanner
from OPL_Testing.TC_9473_T014342_Zap_to__basic_channel_zapping_list import TC_9473_T014342_Zap_to__basic_channel_zapping_list
from OPL_Testing.TC_9474_T014343_Zap_to__basic_channel_mosaic import TC_9474_T014343_Zap_to__basic_channel_mosaic
from OPL_Testing.TC_9475_T014344_Zap_to__basic_channel_EPG import TC_9475_T014344_Zap_to__basic_channel_EPG
from OPL_Testing.TC_9476_T014345_Zap_to__basic_channel_wake_up_screen import TC_9476_T014345_Zap_to__basic_channel_wake_up_screen
from OPL_Testing.TC_18552_T014339_Za_to_basic_chanel_P import TC_18552_T014339_Za_to_basic_chanel_P
from OPL_Testing.TC_9805_Auto_using_P import TC_9805_Auto_using_P
from OPL_Testing.TC_3699_T014566_watch_rental_vod_from_the_play_key import TC_3699_T014566_watch_rental_vod_from_the_play_key
from OPL_Testing.TC_3703_T014776_watch_a_no_rented_vod import TC_3703_T014776_watch_a_no_rented_vod
from OPL_Testing.TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process import TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process
from OPL_Testing.TC_3543_T014669_search_content_by_using_the_keyboard import TC_3543_T014669_search_content_by_using_the_keyboard
from OPL_Testing.TC_3544_T014670_search_vod_by_tytle import TC_3544_T014670_search_vod_by_tytle
from OPL_Testing.TC_3539_VOD_video_presentation_favorites import TC_3539_VOD_video_presentation_favorites
from OPL_Testing.TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid import TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid
from OPL_Testing.TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict import TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict
from OPL_Testing.TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic import TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic
from OPL_Testing.TC_3214_T016689_Delete_an_in_progress_record import TC_3214_T016689_Delete_an_in_progress_record
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import TC_8912_T016328_display_information_of_recording_updated
from OPL_Testing.TC_3315_T014575_consult_wake_up_screen_last_watched_channel import TC_3315_T014575_consult_wake_up_screen_last_watched_channel
from OPL_Testing.TC_3316_T014576_consult_wake_up_screen_EPG_program_list import TC_3316_T014576_consult_wake_up_screen_EPG_program_list
from OPL_Testing.TC_3357_T014491_Consult_favorite_channels_from_list import TC_3357_T014491_Consult_favorite_channels_from_list
from OPL_Testing.TC_3358_T014492_Manage_the_favorite_channels_from_my_acount import TC_3358_T014492_Manage_the_favorite_channels_from_my_acount
from OPL_Testing.TC_3359_T014493_Manage_the_favorite_channels_from_toolbox import TC_3359_T014493_Manage_the_favorite_channels_from_toolbox
from OPL_Testing.TC_3429_T016026_Set_the_default_subtitle_none_IP_stream import TC_3429_T016026_Set_the_default_subtitle_none_IP_stream
from OPL_Testing.TC_18496_T999999_001 import TC_18496_T999999_001
from OPL_Testing.TC_18497_T999999_002_PVR import TC_18497_T999999_002_PVR
from OPL_Testing.TC_18497_T999999_002_TS import TC_18497_T999999_002_TS
from OPL_Testing.TC_23098_T999999_003 import TC_23098_T999999_003
from OPL_Testing.TC_18499_T999999_004 import TC_18499_T999999_004
from OPL_Testing.TC_18500_T999999_005 import TC_18500_T999999_005
from OPL_Testing.TC_18501_T999999_006_PVR import TC_18501_T999999_006_PVR
from OPL_Testing.TC_18502_T999999_007 import TC_18502_T999999_007
from OPL_Testing.TC_18503_T999999_008 import TC_18503_T999999_008
from OPL_Testing.TC_18514_T999999_019 import TC_18514_T999999_019
from OPL_Testing.TC_18515_T999999_020 import TC_18515_T999999_020
from OPL_Testing.TC_18526_T999999_031 import TC_18526_T999999_031
from OPL_Testing.TC_18527_T999999_032 import TC_18527_T999999_032
from OPL_Testing.TC_18529_T999999_034 import TC_18529_T999999_034
from OPL_Testing. TC_18530_T999999_035 import  TC_18530_T999999_035
from OPL_Testing.TC_18532_T999999_037 import TC_18532_T999999_037
from OPL_Testing.TC_18533_T999999_038 import TC_18533_T999999_038
from OPL_Testing.TC_18534_T999999_039 import TC_18534_T999999_039
from OPL_Testing.TC_9597_T000000_download_a_vod__immediately_playback_VPS import TC_9597_T000000_download_a_vod__immediately_playback_VPS

if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(TC_2951_T014369_zap_to_mosaic("test"))
#     suite.addTest(TC_2980_T014405_open_the_toolbox("test"))
#     suite.addTest(TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream("test"))
#     suite.addTest(TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox("test"))
#     suite.addTest(TC_2998_T014426_use_timeshift_on_allowed_program_update("test"))
#     suite.addTest(TC_3003_T014446_NavigateIntiTheZappingList("test"))
#     suite.addTest(TC_3162_T014637_Navigate_into_EPG_all_program_grid("test"))
#     suite.addTest(TC_3167_T014645_Navigate_into_EPG_days_list_update("test"))
#     suite.addTest(TC_3186_T016089_search_a_content_without_choose_a_search_type_update("test"))
#     suite.addTest(TC_3356_T014489_consult_favorite_channels_from_my_account("test"))
#     suite.addTest(TC_3368_T014506_consult_prepaid_account("test"))
#     suite.addTest(TC_3420_T015654_Reload_prepaid_account_payment_control_activated("test"))
#     suite.addTest(TC_3541_T014667_search_a_content_on_vod_catalog("test"))
#     suite.addTest(TC_3587_T014539_consult_the_video_presentation_screen_nominal_case("test"))
#     suite.addTest(TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
#     suite.addTest(TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
#     suite.addTest(TC_9402_T09402_Navigate_into_EPG_homepage("test"))
#     suite.addTest(TC_9470_T014339_Zap_to_basic_channel("test"))
#     suite.addTest(TC_9580_T015441_Awake_last_watched_channel("test"))
#     suite.addTest(TC_9581_T017245_Awake_from_active_standby_mode("test"))
#     suite.addTest(TC_9582_T017246_Awake_from_standby_mode("test"))
#     suite.addTest(TC_9583_T017247_Awake_from_deep_standby_mode("test"))
#     suite.addTest(TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR("test"))
#     suite.addTest(TC_18483_18481_OgladajDttTvNagrywajIpZEpg("test"))
#     suite.addTest(TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran("test"))
#     suite.addTest(TC_18489_OgladajIpTvNagrywajDttZInstantPVR("test"))
#     suite.addTest(TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran("test"))
#     suite.addTest(TC_18493_OgladajDttTvNagrywajIpZInstantPvr("test"))
#     suite.addTest(TC_18725_T0000000_conflict_popup_pvr_tc1("test"))
#     suite.addTest(TC_18726_T0000000_conflict_popup_pvr_tc2("test"))
#     suite.addTest(TC_18727_T0000000_conflict_popup_pvr_tc3("test"))
#     suite.addTest(TC_13227_T999999_instant_recording_immediately("test"))
#     suite.addTest(TC_3004_T014447_Zapping_list_no_favorite_channel("test"))
#     suite.addTest(TC_9471_T014340_Zap_to_basic_channel("test"))
#     suite.addTest(TC_9472_T014341_Zap_to__basic_channel_infobanner("test"))
#     suite.addTest(TC_9473_T014342_Zap_to__basic_channel_zapping_list("test"))
#     suite.addTest(TC_9474_T014343_Zap_to__basic_channel_mosaic("test"))
#     suite.addTest(TC_9475_T014344_Zap_to__basic_channel_EPG("test"))
#     suite.addTest(TC_9476_T014345_Zap_to__basic_channel_wake_up_screen("test"))
#     suite.addTest(TC_18552_T014339_Za_to_basic_chanel_P("test"))
#     suite.addTest(TC_9805_Auto_using_P("test"))
#     suite.addTest(TC_3699_T014566_watch_rental_vod_from_the_play_key("test"))
#     suite.addTest(TC_3703_T014776_watch_a_no_rented_vod("test"))
#     suite.addTest(TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process("test"))
#     suite.addTest(TC_3543_T014669_search_content_by_using_the_keyboard("test"))
#     suite.addTest(TC_3544_T014670_search_vod_by_tytle("test"))
#     suite.addTest(TC_3539_VOD_video_presentation_favorites("test"))
#     suite.addTest(TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid("test"))
#     suite.addTest(TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict("test"))
#     suite.addTest(TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic("test"))
#     suite.addTest(TC_3214_T016689_Delete_an_in_progress_record("test"))
#     suite.addTest(TC_8912_T016328_display_information_of_recording_updated("test"))
#     suite.addTest(TC_3315_T014575_consult_wake_up_screen_last_watched_channel("test"))
#     suite.addTest(TC_3316_T014576_consult_wake_up_screen_EPG_program_list("test"))
#     suite.addTest(TC_3357_T014491_Consult_favorite_channels_from_list("test"))
#     suite.addTest(TC_3358_T014492_Manage_the_favorite_channels_from_my_acount("test"))
#     suite.addTest(TC_3359_T014493_Manage_the_favorite_channels_from_toolbox("test"))
#     suite.addTest(TC_3429_T016026_Set_the_default_subtitle_none_IP_stream("test"))
#     suite.addTest(TC_18496_T999999_001("test"))
#     suite.addTest(TC_18497_T999999_002_PVR("test"))
#     suite.addTest(TC_18497_T999999_002_TS("test"))
#     suite.addTest(TC_23098_T999999_003("test"))
#     suite.addTest(TC_18499_T999999_004("test"))
#     suite.addTest(TC_18500_T999999_005("test"))
#     suite.addTest(TC_18501_T999999_006_PVR("test"))
#     suite.addTest(TC_18502_T999999_007("test"))
#     suite.addTest(TC_18503_T999999_008("test"))
#     suite.addTest(TC_18514_T999999_019("test"))
#     suite.addTest(TC_18515_T999999_020("test"))
#     suite.addTest(TC_18526_T999999_031("test"))
#     suite.addTest(TC_18527_T999999_032("test"))
#     suite.addTest(TC_18529_T999999_034("test"))
#     suite.addTest( TC_18530_T999999_035("test"))
#     suite.addTest(TC_18532_T999999_037("test"))
#     suite.addTest(TC_18533_T999999_038("test"))
#     suite.addTest(TC_18534_T999999_039("test"))
#     suite.addTest(TC_9597_T000000_download_a_vod__immediately_playback_VPS("test"))


    ''' UHD WHD bez DTT i 2nd tunner'''
    
    suite = unittest.TestSuite()
    suite.addTest(TC_2951_T014369_zap_to_mosaic("test"))
    suite.addTest(TC_2980_T014405_open_the_toolbox("test"))
    suite.addTest(TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream("test"))
    suite.addTest(TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox("test"))
    suite.addTest(TC_2998_T014426_use_timeshift_on_allowed_program_update("test"))
    suite.addTest(TC_3003_T014446_NavigateIntiTheZappingList("test"))
    suite.addTest(TC_3162_T014637_Navigate_into_EPG_all_program_grid("test"))
    suite.addTest(TC_3167_T014645_Navigate_into_EPG_days_list_update("test"))
    suite.addTest(TC_3186_T016089_search_a_content_without_choose_a_search_type_update("test"))
    suite.addTest(TC_3356_T014489_consult_favorite_channels_from_my_account("test"))
    suite.addTest(TC_3368_T014506_consult_prepaid_account("test"))
    suite.addTest(TC_3420_T015654_Reload_prepaid_account_payment_control_activated("test"))
    suite.addTest(TC_3541_T014667_search_a_content_on_vod_catalog("test"))
    suite.addTest(TC_3587_T014539_consult_the_video_presentation_screen_nominal_case("test"))
    suite.addTest(TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
    suite.addTest(TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
    suite.addTest(TC_18725_T0000000_conflict_popup_pvr_tc1("test"))
    suite.addTest(TC_18726_T0000000_conflict_popup_pvr_tc2("test"))
    suite.addTest(TC_18727_T0000000_conflict_popup_pvr_tc3("test"))
    suite.addTest(TC_13227_T999999_instant_recording_immediately("test"))
    '''
    suite.addTest(TC_3004_T014447_Zapping_list_no_favorite_channel("test"))
    suite.addTest(TC_9471_T014340_Zap_to_basic_channel("test"))
    suite.addTest(TC_9472_T014341_Zap_to__basic_channel_infobanner("test"))
    suite.addTest(TC_9473_T014342_Zap_to__basic_channel_zapping_list("test"))
    suite.addTest(TC_9474_T014343_Zap_to__basic_channel_mosaic("test"))
    suite.addTest(TC_9475_T014344_Zap_to__basic_channel_EPG("test"))
    suite.addTest(TC_9476_T014345_Zap_to__basic_channel_wake_up_screen("test"))
    suite.addTest(TC_18552_T014339_Za_to_basic_chanel_P("test"))
    suite.addTest(TC_9805_Auto_using_P("test"))
    suite.addTest(TC_3699_T014566_watch_rental_vod_from_the_play_key("test"))
    suite.addTest(TC_3703_T014776_watch_a_no_rented_vod("test"))
    suite.addTest(TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process("test"))
    suite.addTest(TC_3543_T014669_search_content_by_using_the_keyboard("test"))
    suite.addTest(TC_3544_T014670_search_vod_by_tytle("test"))
    suite.addTest(TC_3539_VOD_video_presentation_favorites("test"))
    suite.addTest(TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid("test"))
    suite.addTest(TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict("test"))
    suite.addTest(TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic("test"))
    suite.addTest(TC_3214_T016689_Delete_an_in_progress_record("test"))
    suite.addTest(TC_8912_T016328_display_information_of_recording_updated("test"))
    suite.addTest(TC_3315_T014575_consult_wake_up_screen_last_watched_channel("test"))
    suite.addTest(TC_3316_T014576_consult_wake_up_screen_EPG_program_list("test"))
    suite.addTest(TC_3357_T014491_Consult_favorite_channels_from_list("test"))
    suite.addTest(TC_3358_T014492_Manage_the_favorite_channels_from_my_acount("test"))
    suite.addTest(TC_3359_T014493_Manage_the_favorite_channels_from_toolbox("test"))
    suite.addTest(TC_3429_T016026_Set_the_default_subtitle_none_IP_stream("test"))
    '''

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()
