# -*- coding: utf-8 -*-
import unittest
from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles
from OPL_Testing.TC_2951_T014369_zap_to_mosaic import TC_2951_T014369_zap_to_mosaic
from OPL_Testing.TC_2980_T014405_open_the_toolbox import TC_2980_T014405_open_the_toolbox
from OPL_Testing.TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream import TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream
from OPL_Testing.TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox import TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox
from OPL_Testing.TC_2993_T01421_Change_channel_by_the_infobanner import TC_2993_T01421_Change_channel_by_the_infobanner
from OPL_Testing.TC_2998_T014426_use_timeshift_on_allowed_program_update import TC_2998_T014426_use_timeshift_on_allowed_program_update
from OPL_Testing.TC_3003_T014446_NavigateIntiTheZappingList import TC_3003_T014446_NavigateIntiTheZappingList
from OPL_Testing.TC_3150_TC_3151_T014616_T014617_Add_and_Remove_an_alarts import TC_3150_TC_3151_T014616_T014617_Add_and_Remove_an_alarts
from OPL_Testing.TC_3313_T014567_consult_main_menu_entry_points import TC_3313_T014567_consult_main_menu_entry_points
from OPL_Testing.TC_3162_T014637_Navigate_into_EPG_all_program_grid import TC_3162_T014637_Navigate_into_EPG_all_program_grid
from OPL_Testing.TC_3167_T014645_Navigate_into_EPG_days_list_update import TC_3167_T014645_Navigate_into_EPG_days_list_update
from OPL_Testing.TC_3186_T016089_search_a_content_without_choose_a_search_type_update import TC_3186_T016089_search_a_content_without_choose_a_search_type_update
from OPL_Testing.TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode import TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode
from OPL_Testing.TC_3330_T015091_consult_customized_recommendations_opt_out import TC_3330_T015091_consult_customized_recommendations_opt_out
from OPL_Testing.TC_3339_T014470_Modify_confidential_code import TC_3339_T014470_Modify_confidential_code
from OPL_Testing.TC_3356_T014489_consult_favorite_channels_from_my_account import TC_3356_T014489_consult_favorite_channels_from_my_account
from OPL_Testing.TC_3368_T014506_consult_prepaid_account import TC_3368_T014506_consult_prepaid_account
from OPL_Testing.TC_3370_T014508_Consult_purchase_history_from_purchase_history import TC_3370_T014508_Consult_purchase_history_from_purchase_history
from OPL_Testing.TC_3391_T014692_set_the_green_parameter_update import TC_3391_T014692_set_the_green_parameter_update
from OPL_Testing.TC_3420_T015654_Reload_prepaid_account_payment_control_activated import TC_3420_T015654_Reload_prepaid_account_payment_control_activated
from OPL_Testing.TC_3421_T015655_set_the_green_parameter_activate_End_to_End_test_update import TC_3421_T015655_set_the_green_parameter_activate_End_to_End_test_update
from OPL_Testing.TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update import TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update
from OPL_Testing.TC_3456_T015815_sound_level_on_vod_start import TC_3456_T015815_sound_level_on_vod_start
from OPL_Testing.TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping import TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping
from OPL_Testing.TC_3541_T014667_search_a_content_on_vod_catalog import TC_3541_T014667_search_a_content_on_vod_catalog
from OPL_Testing.TC_3558_T015975_search_in_adult import TC_3558_T015975_search_in_adult
from OPL_Testing.TC_3587_T014539_consult_the_video_presentation_screen_nominal_case import TC_3587_T014539_consult_the_video_presentation_screen_nominal_case
from OPL_Testing.TC_3642_T014706_video_consult_similar_reco_associated_to_a_regular_vod_user_in_opt_in import TC_3642_T014706_video_consult_similar_reco_associated_to_a_regular_vod_user_in_opt_in
from OPL_Testing.TC_3646_T015101_video_consult_similar_reco_associated_to_a_regular_vod_at_the_end_of_video import TC_3646_T015101_video_consult_similar_reco_associated_to_a_regular_vod_at_the_end_of_video
from OPL_Testing.TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog import TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog
from OPL_Testing.TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog import TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog
from OPL_Testing.TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process import TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process
from OPL_Testing.TC_9402_T09402_Navigate_into_EPG_homepage import TC_9402_T09402_Navigate_into_EPG_homepage
from OPL_Testing.TC_9470_T014339_Zap_to_basic_channel import TC_9470_T014339_Zap_to_basic_channel
from OPL_Testing.TC_9580_T015441_Awake_last_watched_channel import TC_9580_T015441_Awake_last_watched_channel
from OPL_Testing.TC_9581_T017245_Awake_from_active_standby_mode import TC_9581_T017245_Awake_from_active_standby_mode
from OPL_Testing.TC_9582_T017246_Awake_from_standby_mode import TC_9582_T017246_Awake_from_standby_mode
from OPL_Testing.TC_9583_T017247_Awake_from_deep_standby_mode import TC_9583_T017247_Awake_from_deep_standby_mode
from OPL_Testing.TC_9802_T999999_Auto_select_summary_option import TC_9802_T999999_Auto_select_summary_option
from OPL_Testing.TC_18684_RFC_2904_interactive_banners_fast_shifting_mosaic_pages import TC_18684_RFC_2904_interactive_banners_fast_shifting_mosaic_pages
from OPL_Testing.TC_18704_RFC_2904_interactive_banners_going_to_next_page_when_banner_is_selected import TC_18704_RFC_2904_interactive_banners_going_to_next_page_when_banner_is_selected
from OPL_Testing.TC_18713_RFC_2904_interactive_banners_selecting_the_right_baner_from_every_row import TC_18713_RFC_2904_interactive_banners_selecting_the_right_baner_from_every_row
from OPL_Testing.TC_18725_T0000000_conflict_popup_pvr_tc1 import TC_18725_T0000000_conflict_popup_pvr_tc1
from OPL_Testing.TC_18726_T0000000_conflict_popup_pvr_tc2 import TC_18726_T0000000_conflict_popup_pvr_tc2
from OPL_Testing.TC_18727_T0000000_conflict_popup_pvr_tc3 import TC_18727_T0000000_conflict_popup_pvr_tc3
from OPL_Testing.TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane import TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane
from OPL_Testing.TC_13227_T999999_instant_recording_immediately import TC_13227_T999999_instant_recording_immediately
from OPL_Testing.TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner import TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner("test"))
    suite.addTest(TC_2951_T014369_zap_to_mosaic("test"))
    suite.addTest(TC_2980_T014405_open_the_toolbox("test"))
    suite.addTest(TC_2982_T014407_change_the_audio_version_of_a_program_on_toolbox_ip_stream("test"))
    suite.addTest(TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox("test"))
    suite.addTest(TC_2993_T01421_Change_channel_by_the_infobanner("test"))
    suite.addTest(TC_2998_T014426_use_timeshift_on_allowed_program_update("test"))
    suite.addTest(TC_3003_T014446_NavigateIntiTheZappingList("test"))
    suite.addTest(TC_3150_TC_3151_T014616_T014617_Add_and_Remove_an_alarts("test"))
    suite.addTest(TC_3313_T014567_consult_main_menu_entry_points("test"))
    suite.addTest(TC_3162_T014637_Navigate_into_EPG_all_program_grid("test"))
    suite.addTest(TC_3167_T014645_Navigate_into_EPG_days_list_update("test"))
    suite.addTest(TC_3186_T016089_search_a_content_without_choose_a_search_type_update("test"))
    suite.addTest(TC_3321_T014582_Consult_Wake_up_creen_from_stand_by_mode("test"))
    suite.addTest(TC_3330_T015091_consult_customized_recommendations_opt_out("test"))
    suite.addTest(TC_3339_T014470_Modify_confidential_code("test"))
    suite.addTest(TC_3356_T014489_consult_favorite_channels_from_my_account("test"))
    suite.addTest(TC_3368_T014506_consult_prepaid_account("test"))
    suite.addTest(TC_3370_T014508_Consult_purchase_history_from_purchase_history("test"))
    suite.addTest(TC_3391_T014692_set_the_green_parameter_update("test"))
    suite.addTest(TC_3420_T015654_Reload_prepaid_account_payment_control_activated("test"))
    suite.addTest(TC_3421_T015655_set_the_green_parameter_activate_End_to_End_test_update("test"))
    suite.addTest(TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update("test"))
    suite.addTest(TC_3456_T015815_sound_level_on_vod_start("test"))
    suite.addTest(TC_3464_3468_T015841_sound_level_on_live_access_T015845_sound_level_on_live_zapping("test"))
    suite.addTest(TC_3541_T014667_search_a_content_on_vod_catalog("test"))
    suite.addTest(TC_3558_T015975_search_in_adult("test"))
    suite.addTest(TC_3587_T014539_consult_the_video_presentation_screen_nominal_case("test"))
    suite.addTest(TC_3642_T014706_video_consult_similar_reco_associated_to_a_regular_vod_user_in_opt_in("test"))
    suite.addTest(TC_3646_T015101_video_consult_similar_reco_associated_to_a_regular_vod_at_the_end_of_video("test"))
    suite.addTest(TC_3676_T015933_add_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
    suite.addTest(TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog("test"))
    suite.addTest(TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process("test"))
    suite.addTest(TC_9402_T09402_Navigate_into_EPG_homepage("test"))
    suite.addTest(TC_9470_T014339_Zap_to_basic_channel("test"))
    suite.addTest(TC_9580_T015441_Awake_last_watched_channel("test"))
    suite.addTest(TC_9581_T017245_Awake_from_active_standby_mode("test"))
    suite.addTest(TC_9582_T017246_Awake_from_standby_mode("test"))
    suite.addTest(TC_9583_T017247_Awake_from_deep_standby_mode("test"))
    suite.addTest(TC_9802_T999999_Auto_select_summary_option("test"))
    suite.addTest(TC_18684_RFC_2904_interactive_banners_fast_shifting_mosaic_pages("test"))
    suite.addTest(TC_18704_RFC_2904_interactive_banners_going_to_next_page_when_banner_is_selected("test"))
    suite.addTest(TC_18713_RFC_2904_interactive_banners_selecting_the_right_baner_from_every_row("test"))
    suite.addTest(TC_18725_T0000000_conflict_popup_pvr_tc1("test"))
    suite.addTest(TC_18726_T0000000_conflict_popup_pvr_tc2("test"))
    suite.addTest(TC_18727_T0000000_conflict_popup_pvr_tc3("test"))
    suite.addTest(TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane("test"))
    suite.addTest(TC_13227_T999999_instant_recording_immediately("test"))

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()
