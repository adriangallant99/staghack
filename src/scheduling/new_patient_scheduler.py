"""
This module contains the NewPatientScheduler class, which is responsible for scheduling new patients into the calendar.
It utilizes various components such as Analysis, AppointmentDataHandler, AppointmentScheduler, and NewAppointmentTracker
to manage and schedule appointments for new patients.

Classes:
    NewPatientScheduler: A class to schedule new patients into the calendar.

Methods:
    __init__(self): Initializes the NewPatientScheduler class with the necessary components.
    schedule_new_patients(self, current_calendar_df: pd.DataFrame, new_patient_df: pd.DataFrame):
        Schedules the earliest possible appointments for all new patients.
    __sort_new_patients(self, new_patient_df: pd.DataFrame) -> pd.DataFrame:
        A private method to sort new patients in the order they registered.
"""

import pandas as pd

from analysis.analysis import Analysis
from scheduling.appointment_data_handler import AppointmentDataHandler
from scheduling.appointment_scheduler import AppointmentScheduler
from scheduling.new_appointment_tracker import NewAppointmentTracker
from util.debug import Debug

class NewPatientScheduler:
    """
    Class to schedule new patients into the calendar
    """

    def __init__(self,):
        """
        Initializes the NewPatientScheduler class with the necessary components
        """
        self.debug = Debug()
        self.new_appointment_tracker = NewAppointmentTracker()
        self.analysis = Analysis()
        self.appointment_scheduler = AppointmentScheduler(self.new_appointment_tracker, self.analysis)
        self.appointment_data_handler = AppointmentDataHandler()

    def schedule_new_patients(self, current_calendar_df:pd.DataFrame, new_patient_df:pd.DataFrame):
        """
        Schedules the earliest possible appointments for all new patients.
        If no available time slots exist for providers in the new patient area,
        those patients remain unscheduled.

        Args:
            current_calendar_df (pd.DataFrame): The current state of the calendar before new appointments.
            new_patient_df (pd.DataFrame): A collection of all new patient registration data.
        """
        print('Scheduling new patients now...')
        sorted_new_patient_df = self.__sort_new_patients(new_patient_df)
        booked_new_patient_ids = []
        for _, new_patient in sorted_new_patient_df.iterrows():
            available_time_slots_df = self.appointment_scheduler.find_earliest_appointments(new_patient, current_calendar_df)
            if available_time_slots_df.empty:
                print(f"No available timeslots for {new_patient['PATIENTID']}")
            else:
                current_calendar_df = self.appointment_scheduler.book_earliest_appointment(new_patient, current_calendar_df, available_time_slots_df)
                booked_new_patient_ids.append(new_patient.loc['PATIENTID'])
        if not self.debug.get_debug():
            self.appointment_data_handler.remove_scheduled_patients_from_new_patients_table(booked_new_patient_ids, new_patient_df)
        print(f"Summary:")
        print(f"New Patient Appointments Scheduled: {len(booked_new_patient_ids)} out of {len(sorted_new_patient_df)}")
        print(f"Patients left unscheduled: {len(new_patient_df)-len(booked_new_patient_ids)}")
        self.analysis.calculate_statistics()
        return current_calendar_df

    def __sort_new_patients(self, new_patient_df:pd.DataFrame) -> pd.DataFrame:
        """
        A private method to sort new patients in the order they registered. Turns the data into a queue (FIFO)

        Args:
            new_patient_df (pd.DataFrame): dataframe containing new patient registration info

        Returns:
            pd.DataFrame: the dataframe of patients, but sorted
        """
        sorted_new_patient_data_df = new_patient_df.sort_values(by=['REGISTRATIONDATE', 'PATIENTID', ], ascending=True)

        return sorted_new_patient_data_df
