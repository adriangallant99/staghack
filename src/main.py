"""
This module handles the preprocessing of appointment data, populating a calendar with provider availability and scheduled appointments, 
and scheduling new patients into the calendar.

Classes:
    Preprocessor: Handles reading and processing of CSV files containing appointment data.
    CalendarPopulator: Populates a calendar with provider availability and scheduled appointments.
    NewPatientScheduler: Schedules new patients into the populated calendar.
    Debug: Manages debug settings.

Functions:
    main: The main function that orchestrates the preprocessing, calendar population, and new patient scheduling.

Usage:
    Run this module to preprocess appointment data, populate the calendar, and schedule new patients.
"""
import pandas as pd

from preprocessing.preprocessor import Preprocessor
from preprocessing.populator import CalendarPopulator
from scheduling.new_patient_scheduler import NewPatientScheduler
from util.debug import Debug
from util.utility import read_json


def main():
    # Maps CSV files to corresponding DataFrames
    pattern_mapping = read_json('data/pattern_map.json')

    # Create preprocessor and load data
    preprocessor = Preprocessor("data/")
    dfs = preprocessor.read_csvs(pattern_mapping)

    processed_appointments = preprocessor.process_appointment_times()

    provider_availability = preprocessor.setup_provider_schedule(month=1, year=2025)

    # Initialize and use the calendar populator
    calendar = CalendarPopulator(provider_availability, processed_appointments)
    populated_calendar = calendar.populate_calendar()
    print(populated_calendar[populated_calendar['APPOINTMENTID'].notna()])

    new_patient_df = preprocessor.get_dataframe('new_patient_df')

    new_patient_scheduler = NewPatientScheduler()

    debug = Debug()
    debug.set_debug(False)
    if debug.get_debug():
        # When debugging, only schedule two test patients
        # new_patient_df = new_patient_df[new_patient_df['PATIENTID'].isin([22905, 22922])]
        populated_calendar = populated_calendar[populated_calendar['PROVIDERID'].isin([202])]
        new_patient_df = pd.DataFrame({
            'PATIENTID': [99990, 99991,99992,99993,99994,99995],
            'STATE': ['CT', 'CT','CT','CT','CT','CT'],
            'REGISTRATIONDATE': ['2025-01-10', '2025-01-10','2025-01-10','2025-01-10','2025-01-10','2025-01-10'],
            'PROGRAM': ['SUD', 'SUD','SUD','SUD','SUD','SUD']})

    updated_calendar = new_patient_scheduler.schedule_new_patients(populated_calendar, new_patient_df)

    print('Finished scheduling new patients')
    print('Program complete')

if __name__ == '__main__':
    main()

# TODO: Test to see what happens when provider has 5 appointments scheduled in a single day
# TODO: If max appointments is 5 per provider per day, what happens if a provider has 5 appointments already scheduled?
#       Should we increment to their next day on the calendar?
# TODO: Turn the appointment tracker into a file so the data can be saved and loaded?
# TODO: Should appointments be booked on same day as registration?
#       We'd need a timestamp of registration to know
# TODO: There should be a connection to the new patient and the appointment data.
#       How do we know which patient is which for each appointment?
