import pandas as pd
from datetime import datetime, timedelta

class CalendarPopulator:

    def __init__(self, provider_availability_df=None, appointments_df=None):
        """
        Initializes the CalendarPopulator with provider availability and appointments dataframes.

        Args:
            provider_availability_df (pd.DataFrame, optional): DataFrame containing provider availability information.
            Defaults to None.
            appointments_df (pd.DataFrame, optional): DataFrame containing appointment information.
            Defaults to None.
        """
        if provider_availability_df is not None and appointments_df is not None:
            self.provider_availability = provider_availability_df.copy()
            self.appointments = appointments_df.copy()
            self._standardize_datetimes()

    def _standardize_datetimes(self):
        """
        Standardize the datetime columns in the provider availability and appointments dataframes.
        Converts the columns to datetime64[ns] format if they are not already in that format.
        """
        for col in ['START_DATETIME', 'END_DATETIME']:
            if self.provider_availability[col].dtype != 'datetime64[ns]':
                self.provider_availability[col] = pd.to_datetime(self.provider_availability[col])

        for col in ['appointment_start', 'appointment_end']:
            if self.appointments[col].dtype != 'datetime64[ns]':
                self.appointments[col] = pd.to_datetime(self.appointments[col])

    def populate_calendar(self):
        """
        Populate the calendar by marking availability slots as booked when they overlap with appointments.
        Uses a simplified overlap detection focused on start times falling within appointment ranges.
        """
        calendar = self.provider_availability.copy()
        calendar['APPOINTMENTID'] = None

        for _, appointment in self.appointments.iterrows():
            # Find slots where the start time falls within the appointment duration
            overlapping_slots = calendar[
                (calendar['PROVIDERID'] == appointment['PROVIDERID']) &
                (calendar['START_DATETIME'] >= appointment['appointment_start']) &
                (calendar['START_DATETIME'] < appointment['appointment_end'])
            ]

            if not overlapping_slots.empty:
                # Mark all states for this provider during these time slots
                time_slots = overlapping_slots['START_DATETIME'].unique()
                calendar.loc[
                    (calendar['PROVIDERID'] == appointment['PROVIDERID']) &
                    (calendar['START_DATETIME'].isin(time_slots)),
                    'APPOINTMENTID'
                ] = appointment['APPOINTMENTID']

        return calendar.sort_values(['PROVIDERID', 'START_DATETIME', 'STATE'])

    def get_available_slots(self, calendar, provider_id=None, state=None, start_date=None, end_date=None):
        """
        Retrieves available slots from the given calendar based on the specified filters.

        Args:
            calendar (pd.DataFrame): The calendar dataframe containing appointment information.
            provider_id (int, optional): The ID of the provider to filter by. Defaults to None.
            state (str, optional): The state to filter by. Defaults to None.
            start_date (str, optional): The start date to filter by in 'YYYY-MM-DD' format. Defaults to None.
            end_date (str, optional): The end date to filter by in 'YYYY-MM-DD' format. Defaults to None.

        Returns:
            pd.DataFrame: A dataframe containing the available slots sorted by start date, provider ID, and state.
        """
        # calendar = self.populate_calendar()
        available = calendar[calendar['APPOINTMENTID'].isna()].copy()

        if provider_id is not None:
            available = available[available['PROVIDERID'] == provider_id]

        if state is not None:
            available = available[available['STATE'] == state]

        if start_date is not None:
            start_date = pd.to_datetime(start_date)
            available = available[available['START_DATETIME'] >= start_date]

        if end_date is not None:
            end_date = pd.to_datetime(end_date)
            available = available[available['END_DATETIME'] <= end_date]

        return available.sort_values(['START_DATETIME', 'PROVIDERID', 'STATE'])

    def get_appointment_slots(self, appointment_id):
        """
        Retrieves the slots for a specific appointment based on the appointment ID.

        Args:
            appointment_id (int): The ID of the appointment to filter by.

        Returns:
            pd.DataFrame: A dataframe containing the slots for the specified appointment
                sorted by start date, provider ID, and state.
        """
        calendar = self.populate_calendar()
        appointment_slots = calendar[calendar['APPOINTMENTID'] == appointment_id].copy()
        return appointment_slots.sort_values(['START_DATETIME', 'PROVIDERID', 'STATE'])
