# calendar , new patient

#if provider time block gets scheduled for one state, every provider block for all states need to be built
    # provider 1 has meeting block at 2pm, it needs to get blocked across states

# returns a populated calendar with all new patient data

#columns - provider id, date, start datetime, end datetime, duration, state, appointment id, patient id, program, registration

import pandas as pd
from preprocessing.populator import CalendarPopulator

class NewPatientScheduler:

    def __init__(self,):
        pass

    def schedule_new_patients(self, current_calendar_df:pd.DataFrame, new_patient_df:pd.DataFrame):

        sorted_new_patient_df = self.__sort_new_patients(new_patient_df)

        for index, new_patient in sorted_new_patient_df.iterrows():
            current_calendar_df = self.__find_earliest_appointment(new_patient, current_calendar_df)

    def __sort_new_patients(self, new_patient_df:pd.DataFrame):
        """
        A private method to sort new patients in the order they registered. Turns the data into a queue (FIFO)

        Args:
            new_patient_df (pd.DataFrame): dataframe containing new patient registration info

        Returns:
            pd.DataFrame: the dataframe of patients, but sorted
        """
        sorted_new_patient_data_df = new_patient_df.sort_values(by=['REGISTRATIONDATE', 'PATIENTID', ], ascending=True)

        return sorted_new_patient_data_df

    def __find_earliest_appointment(self, new_patient, current_calendar_df):

        same_state_providers_df = current_calendar_df[current_calendar_df['STATE'] == new_patient['STATE']].sort_values(by = 'PROVIDERID')

        available_time_slots_df = self.__remove_taken_timeslots(same_state_providers_df)

        self.__book_earliest_appointment(new_patient, available_time_slots_df)

        pass

    def __remove_taken_timeslots(self, calendar_df:pd.DataFrame):
        """
        A private method for removing occupied timeslots from the calendar. New patients
        can't be scheduled during these windows.

        Args:
            calendar_df (pd.DataFrame): A calendar containing any appointments and open timeslots
                for each provider

        Returns:
            _type_: A calendar with all of the taken timeslots removed
        """
        populator = CalendarPopulator()
        available_time_slots_df = populator.get_available_slots(calendar_df)
        return available_time_slots_df
