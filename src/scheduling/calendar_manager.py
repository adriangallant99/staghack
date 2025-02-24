"""
This module provides the CalendarManager class, which handles various calendar-related operations
such as finding and updating timeslots for scheduling appointments. It includes methods to remove
occupied timeslots, filter timeslots based on patient registration dates, and update the calendar
with new appointments to prevent double-booking.

Classes:
    CalendarManager: A class that manages calendar operations for scheduling appointments.

Methods:
    remove_taken_timeslots(calendar_df: pd.DataFrame) -> pd.DataFrame:
        Removes occupied timeslots from the calendar.

    remove_timeslots_earlier_than_registration(new_patient: pd.DataFrame, available_time_slots_df: pd.DataFrame) -> pd.DataFrame:
        Removes timeslots that are earlier than the registration date of a new patient.

    update_calendar(new_appointment_id: int, new_appointment: pd.DataFrame, current_calendar_df: pd.DataFrame) -> pd.DataFrame:
        Updates the calendar to include a new appointment, preventing double-booking.
"""

import pandas as pd

from preprocessing.populator import CalendarPopulator

class CalendarManager:
    """
    Handles calendar-related operations, such as finding and updating timeslots.
    """

    def remove_taken_timeslots(self, calendar_df:pd.DataFrame) -> pd.DataFrame:
        """
        A private method for removing occupied timeslots from the calendar. New patients
        can't be scheduled during these windows.

        Args:
            calendar_df (pd.DataFrame): A calendar containing any appointments and open timeslots
                for each provider

        Returns:
            pd.DataFrame: A calendar with all of the taken timeslots removed
        """
        populator = CalendarPopulator()
        available_time_slots_df = populator.get_available_slots(calendar_df)
        return available_time_slots_df

    def remove_timeslots_earlier_than_registration(self, new_patient:pd.DataFrame, available_time_slots_df:pd.DataFrame) -> pd.DataFrame:
        """
        Remove timeslots earlier than the registration date of the patient

        Args:
            new_patient (pd.DataFrame): new patient information
            available_time_slots_df (pd.DataFrame): a calendar of all available timeslots
        """
        new_patient['REGISTRATIONDATE'] = pd.to_datetime(new_patient['REGISTRATIONDATE'])
        available_time_slots_df['DATE'] = pd.to_datetime(available_time_slots_df['DATE'])
        available_time_slots_df = available_time_slots_df[available_time_slots_df['DATE'] > new_patient['REGISTRATIONDATE']]
        return available_time_slots_df

    def update_calendar(self, new_appointment_id:int, new_appointment:pd.DataFrame, current_calendar_df:pd.DataFrame) -> pd.DataFrame:
        """
        This method updates the in-program calendar to include the new appointment.
        This is important as it updates the calendar mid-execution, allowing us to
        avoid double-booking previously-open timeslots.

        Args:
            new_appointment_id (int): id of the new appointment
            new_appointment (pd.DataFrame): information about the new
                appointment that was booked
            current_calendar (pd.DataFrame): the calendar used for booking appointments

        Returns:
            pd.DataFrame: updated calendar
        """

        new_appointment = new_appointment.copy()

        # Ensure 'START_DATETIME' is in datetime format before comparison
        current_calendar_df['START_DATETIME'] = pd.to_datetime(current_calendar_df['START_DATETIME'])
        current_calendar_df['DATE'] = pd.to_datetime(current_calendar_df['DATE'])
        new_appointment['START_DATETIME'] = pd.to_datetime(new_appointment['START_DATETIME'])
        new_appointment['DATE'] = pd.to_datetime(new_appointment['DATE'])


        condition = (current_calendar_df['DATE'] == new_appointment['DATE']) & \
            (current_calendar_df['START_DATETIME'] == new_appointment['START_DATETIME']) & \
            (current_calendar_df['PROVIDERID'] == new_appointment['PROVIDERID'])

        # Count rows meeting the condition
        num_rows_updated = condition.sum()
        current_calendar_df.loc[condition,'APPOINTMENTID'] = new_appointment_id

        print('Provider timeslots booked as a result of this appointment: %i' % num_rows_updated)

        return current_calendar_df