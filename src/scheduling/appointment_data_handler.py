"""
This module provides functionality for handling appointment data, including
removing scheduled patients from the new patients table and updating the
appointment data table with new appointments.

Classes:
    AppointmentDataHandler: Handles storage and modification of appointment-related data.

Methods:
    remove_scheduled_patients_from_new_patients_table(booked_new_patient_ids, new_patient_df):
        Removes scheduled patients from the new patients table.

    update_appointment_data_table(new_appointment_id, new_appointment):
        Inserts a new record for the latest appointment into the appointment data table.

    __format_appointment_for_csv(new_appointment):
        Formats the new appointment information to align with the CSV file requirements.
"""

import pandas as pd

class AppointmentDataHandler:
    """
    Handles storage and modification of appointment-related data.
    """

    def remove_scheduled_patients_from_new_patients_table(self, booked_new_patient_ids:list[int], new_patient_df:pd.DataFrame):
        """
        Remove scheduled patients from new patients table because they
        are no longer new. They have been scheduled.

        Args:
            booked_new_patient_ids (list[int]): ids of new patients who were booked
        """
        remaining_new_patients_df = \
            new_patient_df[~new_patient_df["PATIENTID"].isin(booked_new_patient_ids)]
        try:
            remaining_new_patients_df.to_csv("data/New Patient Data.csv", mode='w', index=False)
            print(f'{len(booked_new_patient_ids)} scheduled patients have been removed from New Patient Data')
        except FileNotFoundError:
            print("Error: The file 'data.csv' was not found.")
        except KeyError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def update_appointment_data_table(self, new_appointment_id:int, new_appointment:pd.DataFrame):
        """
        Opens the Appointment Data Source and inserts a new record for the latest appointment

        Args:
            new_appointment_id (int): id of the appointment about to be created
            new_appointment (pd.DataFrame): information pertaining to the new appointment
        """
        new_appointment = new_appointment.copy()
        new_appointment['APPOINTMENTID'] = new_appointment_id

        new_appointment_data_entry = self.__format_appointment_for_csv(new_appointment)
        try:
            new_appointment_data_entry.to_csv('data/Appointment Data.csv', mode='a', header=False, index=False)
            print('New Appointment added to table successfully!')
        except FileNotFoundError:
            print("Error: The specified file was not found.")
        except PermissionError:
            print("Error: You do not have permission to write to this file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __format_appointment_for_csv(self, new_appointment:pd.DataFrame) -> pd.DataFrame:
        """
        This method modifies the column names to align with the csv as well as
        converts the values to their proper string formats

        APPOINTMENTID,APPOINTMENTDATE,APPOINTMENTSTARTTIME,APPOINTMENTDURATION,PROVIDERID
        291760,        2025-01-29,      12:30 PM,           60,                 118

        Args:
            new_appointment (pd.DataFrame): new appointment information

        Returns:
            pd.DataFrame: new appointment information formatted for the csv file
        """
        appointment_id = str(new_appointment['APPOINTMENTID'])
        date = new_appointment['DATE'].strftime('%Y-%m-%d')
        start_time = new_appointment['START_DATETIME'].strftime('%I:%M %p')
        duration = int(new_appointment['TIME_RANGE'].seconds/60)
        provider_id = str(new_appointment['PROVIDERID'])

        new_appointment_data_entry = pd.DataFrame([{
            'APPOINTMENTID' : appointment_id,
            'APPOINTMENTDATE' : date,
            'APPOINTMENTSTARTTIME' : start_time,
            'APPOINTMENTDURATION' : duration,
            'PROVIDERID': provider_id
        }])

        return new_appointment_data_entry
