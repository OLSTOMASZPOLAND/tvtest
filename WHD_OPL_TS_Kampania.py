# -*- coding: utf-8 -*-
import unittest
from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles
from OPL_Testing.TC_3370_T014508_Consult_purchase_history_from_purchase_history import TC_3370_T014508_Consult_purchase_history_from_purchase_history
from OPL_Testing.TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process import TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process
from OPL_Testing.TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane import TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane
from OPL_Testing.TC_3699_T014566_watch_rental_vod_from_the_play_key import TC_3699_T014566_watch_rental_vod_from_the_play_key
from OPL_Testing.TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process import TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process
from OPL_Testing.TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in import TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in
from OPL_Testing.TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter import TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter
from OPL_Testing.TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5 import TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5
from OPL_Testing.TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode import TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode
from OPL_Testing.TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update import TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update
from OPL_Testing.TC_3541_T014667_search_a_content_on_vod_catalog import TC_3541_T014667_search_a_content_on_vod_catalog
from OPL_Testing.TC_3377_T014523_Launch_DTT_scan import TC_3377_T014523_Launch_DTT_scan
from OPL_Testing.TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR import TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR
from OPL_Testing.TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran import TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran
from OPL_Testing.TC_18489_OgladajIpTvNagrywajDttZInstantPVR import TC_18489_OgladajIpTvNagrywajDttZInstantPVR
from OPL_Testing.TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran import TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran
from OPL_Testing.TC_18493_OgladajDttTvNagrywajIpZInstantPvr import TC_18493_OgladajDttTvNagrywajIpZInstantPvr
from OPL_Testing.TC_3221_T016765_When_record_is_in_progress_zap_to_another_program import TC_3221_T016765_When_record_is_in_progress_zap_to_another_program
from OPL_Testing.TC_3214_T016689_Delete_an_in_progress_record import TC_3214_T016689_Delete_an_in_progress_record
from OPL_Testing.TC_3430_T016027_Set_the_default_subtitle_none_DTT_stream import TC_3430_T016027_Set_the_default_subtitle_none_DTT_stream
from OPL_Testing.TC_3429_T016026_Set_the_default_subtitle_none_IP_stream import TC_3429_T016026_Set_the_default_subtitle_none_IP_stream
from OPL_Testing.TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping import TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping
from OPL_Testing.TC_3368_T014506_consult_prepaid_account import TC_3368_T014506_consult_prepaid_account
from OPL_Testing.TC_9802_T999999_Auto_select_summary_option import TC_9802_T999999_Auto_select_summary_option
from OPL_Testing.TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner import TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TC_3370_T014508_Consult_purchase_history_from_purchase_history("test"))
    suite.addTest(TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process("test"))
    suite.addTest(TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane("test"))
    suite.addTest(TC_3699_T014566_watch_rental_vod_from_the_play_key("test"))
    suite.addTest(TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process("test"))
    suite.addTest(TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in("test"))
    suite.addTest(TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter("test"))
    suite.addTest(TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5("test"))
    suite.addTest(TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode("test"))
    suite.addTest(TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update("test"))
    suite.addTest(TC_3541_T014667_search_a_content_on_vod_catalog("test"))
    suite.addTest(TC_3377_T014523_Launch_DTT_scan("test"))
    suite.addTest(TC_18480_18484_OgladajDttTvNagrywajIpZInstantPVR("test"))
    suite.addTest(TC_18485_18482_OgladajDttTvNagrywajIpZPlanowaniemNagran("test"))
    suite.addTest(TC_18489_OgladajIpTvNagrywajDttZInstantPVR("test"))
    suite.addTest(TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran("test"))
    suite.addTest(TC_18493_OgladajDttTvNagrywajIpZInstantPvr("test"))
    suite.addTest(TC_3221_T016765_When_record_is_in_progress_zap_to_another_program("test"))
    suite.addTest(TC_3214_T016689_Delete_an_in_progress_record("test"))
    suite.addTest(TC_3430_T016027_Set_the_default_subtitle_none_DTT_stream("test"))
    suite.addTest(TC_3429_T016026_Set_the_default_subtitle_none_IP_stream("test"))
    suite.addTest(TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping("test"))
    suite.addTest(TC_3368_T014506_consult_prepaid_account("test"))
    suite.addTest(TC_9802_T999999_Auto_select_summary_option("test"))
    suite.addTest(TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner("test"))

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()