"""
Module for calculating statistics on the time to first appointment (TTFA) for patients.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from collections import defaultdict
from datetime import datetime

from util.debug import Debug

class Analysis:
    """
    Class to calculate statistics on the time to first appointment (TTFA) for patients
    """

    def __init__(self,):
        """
        registration_info = [{
            patient_id : int,
            registration_date : timestamp,
            appointment_date : timestamp,
            service: str
        },
        {
            ...
        }]
        """
        self.registration_info = []
        self.debug = Debug()

    def calculate_statistics(self,):
        """
        Capture and present Mean & Median time to first appointment (TTFA)
        Break the Mean & Median values for TTFA using a graphical format
        (make sure that the exact values are labeled for the final output) into
        different groups based on the PROGRAM that the patient is in:
        i. Combined
        ii. Mental Health
        iii. SUD
        """
        print('Displaying analysis...')
        mean_tffa, median_tffa = self.__calculate_tffa_stats()
        mean_tffas_by_group, median_tffas_by_group = self.__calculate_tffa_by_group()
        self.__plot_tffa_statistics(mean_tffa, median_tffa, mean_tffas_by_group, median_tffas_by_group)
        print('Analysis complete!')


    def __calculate_tffa_stats(self,):
        """
        Calculate the mean and median time to first appointment (TTFA) for all patients

        Returns:
            tuple: A tuple containing the mean and median TTFA in hours
        """
        try:
            print('Calculating TTFA statistics...')
            tffas = []
            for registration in self.registration_info:
                tffa = (registration['appointment_start_time'] - registration['registration_date'])
                tffas.append(tffa)
            df = pd.DataFrame(tffas)[0].dt.total_seconds()/3600
            mean_tffa = df.mean()
            median_tffa = df.median()

            print(f"Mean TTFA: {mean_tffa:.2f} hours")
            print(f"Median TTFA: {median_tffa:.2f} hours")
            return mean_tffa, median_tffa
        except Exception as e:
            print(f"Error calculating TTFA statistics: {e}")
            return None, None

    def __calculate_tffa_by_group(self,):
        """
        Calculate the mean and median time to first appointment (TTFA) for each health program

        Returns:
            tuple: A tuple containing the mean and median TTFA for each health
            program in hours
        """
        try:
            print('Calculating TTFA by program...')
            tffas_by_group = defaultdict(list)  # Automatically creates lists for new keys

            for registration in self.registration_info:
                program = registration['program']
                tffa = (registration['appointment_start_time'] - registration['registration_date'])
                tffas_by_group[program].append(tffa)
            tffas_by_group =  dict(tffas_by_group)

            # Ensure DataFrame columns can have different lengths by using pd.Series
            df = pd.DataFrame({key: pd.Series(value) for key, value in tffas_by_group.items()})
            df = df.apply(lambda col: col.dt.total_seconds() / 3600)

            mean_tffas = df.mean()
            median_tffas = df.median()

            print(f'Mean TFFAS By Program: \n {mean_tffas.T}')
            print(f'Median TFFAS By Program: \n {median_tffas.T}')

            return mean_tffas, median_tffas
        except Exception as e:
            print(f"Error calculating TTFA by program: {e}")
            return None, None

    def __plot_tffa_statistics(self, mean_tffa, median_tffa, mean_tffas_by_group, median_tffas_by_group):
        """
        Plot the mean and median TTFA statistics.

        Args:
            mean_tffa (float): Mean TTFA for all patients.
            median_tffa (float): Median TTFA for all patients.
            mean_tffas_by_group (pd.Series): Mean TTFA by program.
            median_tffas_by_group (pd.Series): Median TTFA by program.
        """
        try:
            print('Plotting TTFA statistics...')
            programs = ['Combined', 'Mental Health', 'SUD']
            mean_values = [mean_tffa] + [mean_tffas_by_group.get(p, float('nan')) for p in programs[1:]]
            median_values = [median_tffa] + [median_tffas_by_group.get(p, float('nan')) for p in programs[1:]]

            x = np.arange(len(programs))
            bar_width = 0.4

            plt.figure(figsize=(10, 5))
            bars1 = plt.bar(x - bar_width / 2, mean_values, width=bar_width, label='Mean TTFA')
            bars2 = plt.bar(x + bar_width / 2, median_values, width=bar_width, label='Median TTFA')

            # Adjust text position above the bars
            y_max = max(max(mean_values), max(median_values))
            plt.ylim(0, y_max + 2)  # Add extra space at the top

            for bars, values in [(bars1, mean_values), (bars2, median_values)]:
                for bar, value in zip(bars, values):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                            f'{value:.2f}', ha='center', fontsize=10)

            plt.xlabel('Program')
            plt.ylabel('TTFA (hours)')
            plt.title('Mean & Median TTFA by Program', pad=15)
            plt.xticks(x, programs)
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

            plt.tight_layout()

            # Add timestamp to the filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'data/output/ttfa_statistics_{timestamp}.png'
            plt.savefig(filename)
            plt.show()
            print('Plotting complete!')
        except Exception as e:
            print(f"Error plotting TTFA statistics: {e}")
