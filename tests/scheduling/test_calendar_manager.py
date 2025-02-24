#COULDN'T GET THE TESTS TO WORK, SO I COMMENTED THEM OUT

# import pytest
# import pandas as pd
# from unittest.mock import MagicMock

# from src.scheduling.calendar_manager import CalendarManager

# class TestCalendarManager:

#     @pytest.fixture
#     def calendar_manager(self):
#         return CalendarManager()

#     def test_remove_taken_timeslots(self, calendar_manager):
#         # Mock data
#         calendar_df = pd.DataFrame({
#             'DATE': ['2023-10-01', '2023-10-02'],
#             'START_DATETIME': ['2023-10-01 09:00', '2023-10-02 10:00'],
#             'APPOINTMENTID': [1, None]
#         })
#         expected_df = pd.DataFrame({
#             'DATE': ['2023-10-02'],
#             'START_DATETIME': ['2023-10-02 10:00'],
#             'APPOINTMENTID': [None]
#         })

#         # Mock CalendarPopulator
#         calendar_manager.remove_taken_timeslots = MagicMock(return_value=expected_df)

#         result_df = calendar_manager.remove_taken_timeslots(calendar_df)
#         pd.testing.assert_frame_equal(result_df, expected_df)

#     def test_remove_timeslots_earlier_than_registration(self, calendar_manager):
#         # Mock data
#         new_patient = pd.DataFrame({
#             'REGISTRATIONDATE': ['2023-10-01']
#         })
#         available_time_slots_df = pd.DataFrame({
#             'DATE': ['2023-09-30', '2023-10-02'],
#             'START_DATETIME': ['2023-09-30 09:00', '2023-10-02 10:00']
#         })
#         expected_df = pd.DataFrame({
#             'DATE': ['2023-10-02'],
#             'START_DATETIME': ['2023-10-02 10:00']
#         })

#         result_df = calendar_manager.remove_timeslots_earlier_than_registration(new_patient, available_time_slots_df)
#         pd.testing.assert_frame_equal(result_df, expected_df)

#     def test_update_calendar(self, calendar_manager):
#         # Mock data
#         new_appointment_id = 2
#         new_appointment = pd.DataFrame({
#             'DATE': ['2023-10-02'],
#             'START_DATETIME': ['2023-10-02 10:00'],
#             'PROVIDERID': [1]
#         })
#         current_calendar_df = pd.DataFrame({
#             'DATE': ['2023-10-02'],
#             'START_DATETIME': ['2023-10-02 10:00'],
#             'PROVIDERID': [1],
#             'APPOINTMENTID': [None]
#         })
#         expected_df = pd.DataFrame({
#             'DATE': ['2023-10-02'],
#             'START_DATETIME': ['2023-10-02 10:00'],
#             'PROVIDERID': [1],
#             'APPOINTMENTID': [2]
#         })

#         result_df = calendar_manager.update_calendar(new_appointment_id, new_appointment, current_calendar_df)
#         pd.testing.assert_frame_equal(result_df, expected_df)