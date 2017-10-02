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
from OPL_Testing.TC_3004_T014447_Zapping_list_no_favorite_channel import TC_3004_T014447_Zapping_list_no_favorite_channel
from OPL_Testing.TC_9471_T014340_Zap_to_basic_channel import TC_9471_T014340_Zap_to_basic_channel
from OPL_Testing.TC_9472_T014341_Zap_to__basic_channel_infobanner import TC_9472_T014341_Zap_to__basic_channel_infobanner
from OPL_Testing.TC_9473_T014342_Zap_to__basic_channel_zapping_list import TC_9473_T014342_Zap_to__basic_channel_zapping_list
from OPL_Testing.TC_9474_T014343_Zap_to__basic_channel_mosaic import TC_9474_T014343_Zap_to__basic_channel_mosaic
from OPL_Testing.TC_9475_T014344_Zap_to__basic_channel_EPG import TC_9475_T014344_Zap_to__basic_channel_EPG
from OPL_Testing.TC_9476_T014345_Zap_to__basic_channel_wake_up_screen import TC_9476_T014345_Zap_to__basic_channel_wake_up_screen
from OPL_Testing.TC_18552_T014339_Za_to_basic_chanel_P import TC_18552_T014339_Za_to_basic_chanel_P
from OPL_Testing.TC_9805_Auto_using_P import TC_9805_Auto_using_P
from OPL_Testing.TC_3898_T016299_Brownse_my_selection_list_when_list_is_empty import TC_3898_T016299_Brownse_my_selection_list_when_list_is_empty
from OPL_Testing.TC_3699_T014566_watch_rental_vod_from_the_play_key import TC_3699_T014566_watch_rental_vod_from_the_play_key
from OPL_Testing.TC_3703_T014776_watch_a_no_rented_vod import TC_3703_T014776_watch_a_no_rented_vod
from OPL_Testing.TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process import TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process
from OPL_Testing.TC_3621_T015968_stop_and_resume_vod_electrical_reboot import TC_3621_T015968_stop_and_resume_vod_electrical_reboot
from OPL_Testing.TC_10906_T016034_Consult_a_no_rented_paid_vod import TC_10906_T016034_Consult_a_no_rented_paid_vod
from OPL_Testing.TC_10924_T016044_Consult_a_no_bookmared_VOD import TC_10924_T016044_Consult_a_no_bookmared_VOD
from OPL_Testing.TC_3543_T014669_search_content_by_using_the_keyboard import TC_3543_T014669_search_content_by_using_the_keyboard
from OPL_Testing.TC_3544_T014670_search_vod_by_tytle import TC_3544_T014670_search_vod_by_tytle
from OPL_Testing.TC_3570_T015995_Search_result_is_empty import TC_3570_T015995_Search_result_is_empty
from OPL_Testing.TC_3539_VOD_video_presentation_favorites import TC_3539_VOD_video_presentation_favorites
from OPL_Testing.TC_3191_T016094_search_results_is_empty import TC_3191_T016094_search_results_is_empty
from OPL_Testing.TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid import TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid
from OPL_Testing.TC_9690_T016945_Use_the_Time_Shifting_session_and_go_on_watching_the_TS_buffer_up_to_4h import TC_9690_T016945_Use_the_Time_Shifting_session_and_go_on_watching_the_TS_buffer_up_to_4h
from OPL_Testing.TC_9691_T016946_Use_the_Time_Shifting_session_and_stop_the_session_by_using_STOP_key import TC_9691_T016946_Use_the_Time_Shifting_session_and_stop_the_session_by_using_STOP_key
from OPL_Testing.TC_9692_T016947_Use_time_shifting_pause_less_than_maximum_duration_go_back_review_in_TS_session import TC_9692_T016947_Use_time_shifting_pause_less_than_maximum_duration_go_back_review_in_TS_session
from OPL_Testing.TC_9693_T016948_use_time_shifting_pause_more_than_max_duration_stop_TS_buffer import TC_9693_T016948_use_time_shifting_pause_more_than_max_duration_stop_TS_buffer
from OPL_Testing.TC_9694_T016949_pause_live_for_more_60MIN_replay_within_the_60_min_time_range import TC_9694_T016949_pause_live_for_more_60MIN_replay_within_the_60_min_time_range
from OPL_Testing.TC_9718_T016940_schedule_an_instant_recording_EPG_is_avalaible_end_time_less_10_mins import TC_9718_T016940_schedule_an_instant_recording_EPG_is_avalaible_end_time_less_10_mins
from OPL_Testing.TC_9733_T017186_recording_in_active_stand_by import TC_9733_T017186_recording_in_active_stand_by
from OPL_Testing.TC_9734_T017187_recording_in_stand_by_mode import TC_9734_T017187_recording_in_stand_by_mode
from OPL_Testing.TC_9735_T017188_recording_in_deep_stand_by_mode import TC_9735_T017188_recording_in_deep_stand_by_mode
from OPL_Testing.TC_9736_T017195_recording_in_active_stand_by_mode_prevent_to_go_in_stand_by_mode import TC_9736_T017195_recording_in_active_stand_by_mode_prevent_to_go_in_stand_by_mode
from OPL_Testing.TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict import TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict
from OPL_Testing.TC_8979_T016692_Modify_a_no_start_record_in_my_scheduled_recordings_mosaic import TC_8979_T016692_Modify_a_no_start_record_in_my_scheduled_recordings_mosaic
from OPL_Testing.TC_8981_T017085_Modify_a_finished_record_in_my_records_mosaic import TC_8981_T017085_Modify_a_finished_record_in_my_records_mosaic
from OPL_Testing.TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic import TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic
from OPL_Testing.TC_3214_T016689_Delete_an_in_progress_record import TC_3214_T016689_Delete_an_in_progress_record
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import TC_8912_T016328_display_information_of_recording_updated
from OPL_Testing.TC_3315_T014575_consult_wake_up_screen_last_watched_channel import TC_3315_T014575_consult_wake_up_screen_last_watched_channel
from OPL_Testing.TC_3316_T014576_consult_wake_up_screen_EPG_program_list import TC_3316_T014576_consult_wake_up_screen_EPG_program_list
from OPL_Testing.TC_3324_T015085_Check_if_user_can_get_personalized_recommendations_from_Main_Menu import TC_3324_T015085_Check_if_user_can_get_personalized_recommendations_from_Main_Menu
from OPL_Testing.TC_3337_T014466_modify_adult_code_set_it_to_code_to_0000 import TC_3337_T014466_modify_adult_code_set_it_to_code_to_0000
from OPL_Testing.TC_3338_T014467_modify_adult_code_error_with_new_code_confirmation import TC_3338_T014467_modify_adult_code_error_with_new_code_confirmation
from OPL_Testing.TC_3340_T014471_modify_confidential_code_wrong_current_code import TC_3340_T014471_modify_confidential_code_wrong_current_code
from OPL_Testing.TC_3341_T014472_modify_confidential_code_set_it_to_code_to_0000 import TC_3341_T014472_modify_confidential_code_set_it_to_code_to_0000
from OPL_Testing.TC_3342_T014473_modify_confidential_code_error_with_new_code_confirmation import TC_3342_T014473_modify_confidential_code_error_with_new_code_confirmation
from OPL_Testing.TC_3357_T014491_Consult_favorite_channels_from_list import TC_3357_T014491_Consult_favorite_channels_from_list
from OPL_Testing.TC_3358_T014492_Manage_the_favorite_channels_from_my_acount import TC_3358_T014492_Manage_the_favorite_channels_from_my_acount
from OPL_Testing.TC_3359_T014493_Manage_the_favorite_channels_from_toolbox import TC_3359_T014493_Manage_the_favorite_channels_from_toolbox
from OPL_Testing.TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter import TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter
from OPL_Testing.TC_3410_T015216_Deactive_tracking_from_my_account_set_opl_out_parameter import TC_3410_T015216_Deactive_tracking_from_my_account_set_opl_out_parameter
from OPL_Testing.TC_3404_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_out import TC_3404_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_out
from OPL_Testing.TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in import TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in
from OPL_Testing.TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5 import TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5
from OPL_Testing.TC_3389_T014689_Configure_zoom_preferences import TC_3389_T014689_Configure_zoom_preferences
from OPL_Testing.TC_3429_T016026_Set_the_default_subtitle_none_IP_stream import TC_3429_T016026_Set_the_default_subtitle_none_IP_stream

if __name__ == '__main__':
    suite = unittest.TestSuite()
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
    suite.addTest(TC_3004_T014447_Zapping_list_no_favorite_channel("test"))
    suite.addTest(TC_9471_T014340_Zap_to_basic_channel("test"))
    suite.addTest(TC_9472_T014341_Zap_to__basic_channel_infobanner("test"))
    suite.addTest(TC_9473_T014342_Zap_to__basic_channel_zapping_list("test"))
    suite.addTest(TC_9474_T014343_Zap_to__basic_channel_mosaic("test"))
    suite.addTest(TC_9475_T014344_Zap_to__basic_channel_EPG("test"))
    suite.addTest(TC_9476_T014345_Zap_to__basic_channel_wake_up_screen("test"))
    suite.addTest(TC_18552_T014339_Za_to_basic_chanel_P("test"))
    suite.addTest(TC_9805_Auto_using_P("test"))
    suite.addTest(TC_3898_T016299_Brownse_my_selection_list_when_list_is_empty("test"))
    suite.addTest(TC_3699_T014566_watch_rental_vod_from_the_play_key("test"))
    suite.addTest(TC_3703_T014776_watch_a_no_rented_vod("test"))
    suite.addTest(TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process("test"))
    suite.addTest(TC_3621_T015968_stop_and_resume_vod_electrical_reboot("test"))
    suite.addTest(TC_10906_T016034_Consult_a_no_rented_paid_vod("test"))
    suite.addTest(TC_10924_T016044_Consult_a_no_bookmared_VOD("test"))
    suite.addTest(TC_3543_T014669_search_content_by_using_the_keyboard("test"))
    suite.addTest(TC_3544_T014670_search_vod_by_tytle("test"))
    suite.addTest(TC_3570_T015995_Search_result_is_empty("test"))
    suite.addTest(TC_3539_VOD_video_presentation_favorites("test"))
    suite.addTest(TC_3191_T016094_search_results_is_empty("test"))
    suite.addTest(TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid("test"))
    suite.addTest(TC_9690_T016945_Use_the_Time_Shifting_session_and_go_on_watching_the_TS_buffer_up_to_4h("test"))
    suite.addTest(TC_9691_T016946_Use_the_Time_Shifting_session_and_stop_the_session_by_using_STOP_key("test"))
    suite.addTest(TC_9692_T016947_Use_time_shifting_pause_less_than_maximum_duration_go_back_review_in_TS_session("test"))
    suite.addTest(TC_9693_T016948_use_time_shifting_pause_more_than_max_duration_stop_TS_buffer("test"))
    suite.addTest(TC_9694_T016949_pause_live_for_more_60MIN_replay_within_the_60_min_time_range("test"))
    suite.addTest(TC_9718_T016940_schedule_an_instant_recording_EPG_is_avalaible_end_time_less_10_mins("test"))
    suite.addTest(TC_9733_T017186_recording_in_active_stand_by("test"))
    suite.addTest(TC_9734_T017187_recording_in_stand_by_mode("test"))
    suite.addTest(TC_9735_T017188_recording_in_deep_stand_by_mode("test"))
    suite.addTest(TC_9736_T017195_recording_in_active_stand_by_mode_prevent_to_go_in_stand_by_mode("test"))
    suite.addTest(TC_11115_T016360_auto_schedule_a_record_EPG_programming_conflict("test"))
    suite.addTest(TC_8979_T016692_Modify_a_no_start_record_in_my_scheduled_recordings_mosaic("test"))
    suite.addTest(TC_8981_T017085_Modify_a_finished_record_in_my_records_mosaic("test"))
    suite.addTest(TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic("test"))
    suite.addTest(TC_3214_T016689_Delete_an_in_progress_record("test"))
    suite.addTest(TC_8912_T016328_display_information_of_recording_updated("test"))
    suite.addTest(TC_3315_T014575_consult_wake_up_screen_last_watched_channel("test"))
    suite.addTest(TC_3316_T014576_consult_wake_up_screen_EPG_program_list("test"))
    suite.addTest(TC_3324_T015085_Check_if_user_can_get_personalized_recommendations_from_Main_Menu("test"))
    suite.addTest(TC_3337_T014466_modify_adult_code_set_it_to_code_to_0000("test"))
    suite.addTest(TC_3338_T014467_modify_adult_code_error_with_new_code_confirmation("test"))
    suite.addTest(TC_3340_T014471_modify_confidential_code_wrong_current_code("test"))
    suite.addTest(TC_3341_T014472_modify_confidential_code_set_it_to_code_to_0000("test"))
    suite.addTest(TC_3342_T014473_modify_confidential_code_error_with_new_code_confirmation("test"))
    suite.addTest(TC_3357_T014491_Consult_favorite_channels_from_list("test"))
    suite.addTest(TC_3358_T014492_Manage_the_favorite_channels_from_my_acount("test"))
    suite.addTest(TC_3359_T014493_Manage_the_favorite_channels_from_toolbox("test"))
    suite.addTest(TC_3409_T015215_Active_tracking_from_my_account_set_opl_in_parameter("test"))
    suite.addTest(TC_3410_T015216_Deactive_tracking_from_my_account_set_opl_out_parameter("test"))
    suite.addTest(TC_3404_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_out("test"))
    suite.addTest(TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in("test"))
    suite.addTest(TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5("test"))
    suite.addTest(TC_3389_T014689_Configure_zoom_preferences("test"))
    suite.addTest(TC_3429_T016026_Set_the_default_subtitle_none_IP_stream("test"))

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()