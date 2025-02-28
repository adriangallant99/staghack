"""
This module contains the AppointmentScheduler class which handles the logic for scheduling appointments for patients.
It ensures that patients are booked efficiently by finding the earliest available timeslots and booking appointments.

Classes:
    AppointmentScheduler: Handles appointment scheduling logic, ensuring patients are booked efficiently.

Functions:
    __init__(new_appointment_tracker: NewAppointmentTracker, analysis):
        Initializes the AppointmentScheduler with the necessary components.
    find_earliest_appointments(new_patient: pd.DataFrame, current_calendar_df: pd.DataFrame) -> pd.DataFrame:
        Finds the earliest available timeslots for a new patient.
    book_earliest_appointment(new_patient: pd.DataFrame, current_calendar_df: pd.DataFrame,
                                available_time_slots_df: pd.DataFrame) -> pd.DataFrame: 
        Books the earliest available appointment for a new patient.
    __update_new_appointment_tracker(new_appointment_id: int, current_calendar_df: pd.DataFrame):
        Updates the new appointment tracker with the new appointment.
    __add_to_analysis(new_patient: pd.DataFrame, available_time_slot: pd.DataFrame):
        Adds the new appointment information to the analysis.
"""

import pandas as pd

from preprocessing.preprocessor import Preprocessor

from scheduling.appointment_data_handler import AppointmentDataHandler
from scheduling.calendar_manager import CalendarManager
from scheduling.new_appointment_tracker import NewAppointmentTracker

from util.utility import read_json

class AppointmentScheduler:
    """
    Handles appointment scheduling logic, ensuring patients are booked efficiently.
    """

    def __init__(self, new_appointment_tracker:NewAppointmentTracker, analysis):
        self.appointment_data_handler = AppointmentDataHandler()
        self.calendar_manager = CalendarManager()
        self.preprocessor = Preprocessor("data/")
        self.analysis = analysis
        self.new_appointment_tracker = new_appointment_tracker


    def find_earliest_appointments(self, new_patient:pd.DataFrame, current_calendar_df:pd.DataFrame) -> pd.DataFrame:
            """
            Finds all providers in same state as new patient,
            finds all available timeslots, removes taken timeslots
            and timeslots earlier than registration.
            Lastly, sorts the list of avaiable timeslots from earliest to latest

            Args:
                new_patient (pd.DataFrame): information pertaining to the new patient
                current_calendar_df (pd.DataFrame): the calendar containing all timeslots

            Returns:
                pd.DataFrame: a collection of available timeslots
            """

            same_state_providers_df = current_calendar_df[current_calendar_df['STATE'] == new_patient['STATE']].sort_values(by = 'PROVIDERID')

            available_time_slots_df = self.calendar_manager.remove_taken_timeslots(same_state_providers_df)

            available_time_slots_df = self.calendar_manager.remove_timeslots_earlier_than_registration(new_patient, available_time_slots_df)

            return available_time_slots_df.sort_values(by=['DATE', 'START_DATETIME'])

    def book_earliest_appointment(self, new_patient:pd.DataFrame, current_calendar_df:pd.DataFrame,
                                    available_time_slots_df:pd.DataFrame) -> pd.DataFrame:
        """
        This private method populates the current_calendar_df calendar.
        It takes the new patient and assigns them to a slot in the calendar dataframe.
        It also writes their appointment info to the appointment data csv file.

        Args:
            new_patient (pd.DataFrame): future state, we have to tie patient to appointment somehow
            current_calendar_df (pd.DataFrame): the current state of the calendar
            available_time_slots_df (pd.DataFrame): the available timeslots for the new patient

        Returns:
            pd.DataFrame: the updated calendar
        """
        for _, available_time_slot in available_time_slots_df.iterrows():
            if self.new_appointment_tracker.check_if_provider_has_availibility(available_time_slot):
                # BETTER TO GO TO DATABASE INSTEAD?
                max_appointment_id = self.__get_max_appointment_id()
                new_appointment_id = int(max_appointment_id + 1)
                self.appointment_data_handler.update_appointment_data_table(new_appointment_id, available_time_slot)
                current_calendar_df = self.calendar_manager.update_calendar(new_appointment_id, available_time_slot, current_calendar_df)
                self.__update_new_appointment_tracker(new_appointment_id, current_calendar_df)
                self.__add_to_analysis(new_patient, available_time_slot)
                return current_calendar_df
            else:
                print(f"Provider: {available_time_slot['PROVIDERID']} does not have ability for {available_time_slot['DATE']}")
        return current_calendar_df

    def __update_new_appointment_tracker(self, new_appointment_id:int,current_calendar_df:pd.DataFrame):
        """
        Providers can only have 5 additional appointments booked per day. We have to keep track of that.

        Args:
            new_appointment_id (int): id of the new appointment that was just created
            current_calendar_df (pd.DataFrame): a calendar showing all appointments
        """
        provider_id, appointment_date = current_calendar_df.loc[
            current_calendar_df['APPOINTMENTID'] == new_appointment_id, ['PROVIDERID', 'DATE']].iloc[0]

        new_appointment_count = self.new_appointment_tracker.get_provider_by_date(provider_id, appointment_date)

        if  new_appointment_count != 'Not found':
            self.new_appointment_tracker.increment_provider_appointments(provider_id, appointment_date)
        else:
            self.new_appointment_tracker.add_provider(provider_id, appointment_date)
            self.new_appointment_tracker.increment_provider_appointments(provider_id, appointment_date)

    def __add_to_analysis(self, new_patient:pd.DataFrame, available_time_slot:pd.DataFrame):
        self.analysis.registration_info.append({
            'patient_id' : new_patient['PATIENTID'],
            'registration_date' : new_patient['REGISTRATIONDATE'],
            'program' : new_patient['PROGRAM'],
            'appointment_start_time' : available_time_slot['START_DATETIME']
        })

    def __get_max_appointment_id(self, ) -> int:
        """
        Retrieves the maximum appointment ID from the appointments DataFrame.

        This method fetches the appointments DataFrame and returns the highest value
        in the 'APPOINTMENTID' column.

        Returns:
            int: The maximum appointment ID.
        """
        appointment_df:pd.DataFrame = self.__get_appointments_df()
        return appointment_df['APPOINTMENTID'].max()

    def __get_appointments_df(self, ) -> pd.DataFrame:
        """
        Retrieves the appointments DataFrame.

        This method reads the necessary CSV files and returns the DataFrame
        containing appointment data.

        Returns:
            pd.DataFrame: The DataFrame containing appointment data.
        """
        # Maps CSV files to corresponding DataFrames
        pattern_mapping = read_json('data/pattern_map.json')

        # Create preprocessor and load data
        preprocessor = Preprocessor("data/")
        dfs = preprocessor.read_csvs(pattern_mapping)
        return dfs['appointment_df']
