import pandas as pd
import os
import re
import glob
import calendar
from datetime import datetime, timedelta

class Preprocessor:
    def __init__(self, folderpath=None):
        """
        Initialize the Preprocessor with a folder path.

        Args:
            folderpath (str, optional): Path to the folder containing CSV files
        """
        self.folderpath = folderpath
        self.dataframes = {}  # Dictionary to store multiple dataframes

    def read_csvs(self, pattern_df_mapping):
        """
        Read multiple CSV files matching regex patterns and assign to specified DataFrame names.
        """
        try:
            # Check if pattern_df_mapping is None or empty
            if not pattern_df_mapping:
                raise ValueError("pattern_df_mapping is None or empty")

            if not isinstance(pattern_df_mapping, dict):
                raise ValueError(f"pattern_df_mapping must be a dictionary, got {type(pattern_df_mapping)}")

            if not self.folderpath:
                raise ValueError("No folder path provided")

            if not os.path.exists(self.folderpath):
                raise FileNotFoundError(f"Folder not found: {self.folderpath}")

            # Get all CSV files in the folder
            all_csv_files = glob.glob(os.path.join(self.folderpath, "*.csv"))
            print(f"Found CSV files: {all_csv_files}")  # Debug print

            for pattern, df_name in pattern_df_mapping.items():
                matching_files = []
                for file in all_csv_files:
                    if re.search(pattern, os.path.basename(file)):
                        matching_files.append(file)

                print(f"Pattern '{pattern}' matched files: {matching_files}")  # Debug print

                if not matching_files:
                    print(f"Warning: No files found matching pattern '{pattern}'")
                    continue

                if len(matching_files) > 1:
                    print(f"Warning: Multiple files found for pattern '{pattern}'. Using the first match.")

                try:
                    self.dataframes[df_name] = pd.read_csv(matching_files[0])
                    print(f"Successfully loaded {matching_files[0]} as {df_name}")
                except Exception as e:
                    print(f"Error reading {matching_files[0]}: {str(e)}")

            return self.dataframes

        except Exception as e:
            print(f"Error in read_csvs: {str(e)}")
            return None

    def get_dataframe(self, df_name):
        """
        Retrieve a specific DataFrame by name.

        Args:
            df_name (str): Name of the DataFrame to retrieve

        Returns:
            pandas.DataFrame: The requested DataFrame
        """
        return self.dataframes.get(df_name)

    def join_provider_state_data(self, provider_key='PROVIDERID', how='left'):
        """
        Join provider state data with provider schedule data.

        Args:
            provider_key (str): The key to join on (default: 'provider_id')
            how (str): Type of join to perform (default: 'left')

        Returns:
            pandas.DataFrame: Joined DataFrame with provider schedule and state data
        """
        try:
            schedule_df = self.dataframes.get('provider_schedule_df')
            state_df = self.dataframes.get('provider_state_df')

            if schedule_df is None or state_df is None:
                raise ValueError("Provider schedule or state DataFrames not found. Please load the data first.")

            # Make copies to avoid modifying original dataframes
            schedule_copy = schedule_df.copy()
            state_copy = state_df.copy()

            # Perform the join
            joined_df = schedule_copy.merge(
                state_copy,
                on=provider_key,
                how=how,
                suffixes=('_schedule', '_state')
            )

            # Store the joined dataframe
            self.dataframes['provider_schedule_with_state'] = joined_df

            print(f"Successfully joined provider state data with schedule data.")
            print(f"Shape before join: {schedule_df.shape}")
            print(f"Shape after join: {joined_df.shape}")

            # Check for any providers that didn't get matched
            if how == 'left':
                unmatched = joined_df[joined_df.isna().any(axis=1)]
                if len(unmatched) > 0:
                    print(f"Warning: {len(unmatched)} providers in schedule data had no matching state data")

            #ADRIAN - I ADDED THIS SO WE CAN REMOVE TIMESLOTS BEFORE 8:30AM AND AFTER 9:00PM

            joined_df = joined_df.copy()

            # Define the time range (we'll only care about the time, not the date)
            start_time = pd.to_datetime('2025-02-20 08:30:00').time()  # Extracting only the time
            end_time = pd.to_datetime('2025-02-20 21:00:00').time()

            joined_df['SLOTSTARTTIME_TIMESTAMP'] = pd.to_datetime(joined_df['SLOTSTARTTIME']).dt.time

            # GET RID OF SLOTS THAT DON'T FIT WITHIN THE START AND END TIMES 8:30 AM - 9:00 PM
            joined_df = joined_df[(joined_df['SLOTSTARTTIME_TIMESTAMP'] >= start_time) & (joined_df['SLOTSTARTTIME_TIMESTAMP'] <= end_time)]

            joined_df = joined_df.drop('SLOTSTARTTIME_TIMESTAMP', axis=1)

            return joined_df

        except Exception as e:
            print(f"Error joining provider state data: {str(e)}")
            return None

    def process_appointment_times(self, ):
        """
        Process appointment dataframe to:
        1. Convert date and time to datetime objects
        2. Calculate end time based on duration
        3. Remove appointments outside business hours (8:30 AM - 9:00 PM)

        TO DO, SEND THE CANCELLED APPOINTMENTS BACK TO THE QUEUE

        Returns:
            pandas.DataFrame: Processed appointment DataFrame
        """
        try:
            # Get the appointment dataframe
            df = self.dataframes.get('appointment_df')
            if df is None:
                raise ValueError("Appointment DataFrame not found. Please load the data first.")

            # Make a copy to avoid modifying original
            df = df.copy()

            # Combine date and time into a single datetime column
            df['appointment_start'] = pd.to_datetime(
                df['APPOINTMENTDATE'] + ' ' + df['APPOINTMENTSTARTTIME'],
                format='%Y-%m-%d %I:%M %p'
            )

            # Convert duration to timedelta and calculate end time
            df['appointment_end'] = df['appointment_start'] + pd.to_timedelta(df['APPOINTMENTDURATION'], unit='minutes')

            # Create time range (useful for checking overlaps)
            df['time_range'] = df.apply(
                lambda x: pd.date_range(
                    start=x['appointment_start'],
                    end=x['appointment_end'],
                    freq='min'  # 'min' represents minutes
                ),
                axis=1
            )

            # Filter for business hours
            df['start_time'] = df['appointment_start'].dt.time
            df['end_time'] = df['appointment_end'].dt.time

            # Create business hour bounds
            business_start = pd.to_datetime('8:30 AM').time()
            business_end = pd.to_datetime('9:00 PM').time()

            # Filter appointments within business hours
            df_filtered = df[
                (df['start_time'] >= business_start) &
                (df['end_time'] <= business_end)
            ]

            # Remove temporary columns used for filtering
            df_filtered = df_filtered.drop(['start_time', 'end_time'], axis=1)

            # Store processed dataframe
            self.dataframes['appointment_df_processed'] = df_filtered

            print("Successfully processed appointment times.")
            print(f"Original appointments: {len(df)}")
            print(f"Appointments within business hours: {len(df_filtered)}")
            print(f"Removed appointments: {len(df) - len(df_filtered)}")

            return df_filtered

        except Exception as e:
            print(f"Error processing appointment times: {str(e)}")
            return None

    def setup_provider_schedule(self, year=None, month=None):
        """
        Set up a calendar of date-time slots for providers based on their weekly schedule.

        Args:
            year (int, optional): Year to generate schedule for. Defaults to current year.
            month (int, optional): Month to generate schedule for. Defaults to current month.

        Returns:
            pandas.DataFrame: Calendar of available slots with provider IDs
        """
        try:
            schedule_df = self.join_provider_state_data()
            if schedule_df is None:
                raise ValueError("Provider schedule DataFrame not found. Please load the data first.")

            # Use current year and month if not specified
            today = datetime.now()
            year = year or today.year
            month = month or today.month

            # Get number of days in the month
            num_days = calendar.monthrange(year, month)[1]

            # Create a list to store all schedule entries
            schedule_entries = []

            # For each provider's schedule
            for _, row in schedule_df.iterrows():
                provider_id = row['PROVIDERID']
                day_of_week = row['DAYOFWEEK']  # 1 = Monday, 7 = Sunday
                start_time = datetime.strptime(row['SLOTSTARTTIME'], '%H:%M').time()
                end_time = datetime.strptime(row['SLOTENDTIME'], '%H:%M').time()

                # For each day in the month
                for day in range(1, num_days + 1):
                    # Create datetime for this day
                    current_date = datetime(year, month, day)

                    # Check if this day matches the provider's schedule day
                    # Convert Python's weekday (0 = Monday) to match your data's format
                    if (current_date.weekday() + 1) == day_of_week:
                        # Create datetime for start and end times
                        slot_start = datetime.combine(current_date, start_time)
                        slot_end = datetime.combine(current_date, end_time)

                        # Calculate time range
                        time_range = slot_end - slot_start

                        # Add entry to schedule
                        schedule_entries.append({
                            'PROVIDERID': provider_id,
                            'DATE': current_date.date(),
                            'START_DATETIME': slot_start,
                            'END_DATETIME': slot_end,
                            'TIME_RANGE': time_range,  # New column
                            'STATE': row.get('STATE', None)  # Include state if available
                        })

            # Create DataFrame from entries
            provider_availability_df = pd.DataFrame(schedule_entries)

            # Sort by date and start time
            provider_availability_df = provider_availability_df.sort_values(['DATE', 'START_DATETIME', 'PROVIDERID'])

            # Store in dataframes dictionary
            self.dataframes['provider_calendar'] = provider_availability_df

            print(f"Successfully created schedule for {calendar.month_name[month]} {year}")
            print(f"Total slots generated: {len(provider_availability_df)}")

            return provider_availability_df

        except Exception as e:
            print(f"Error setting up schedule: {str(e)}")
            return None
