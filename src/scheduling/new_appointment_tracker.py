"""
This module defines the NewAppointmentTracker class, a singleton that tracks the number of new appointments
by date for each provider. The class ensures thread safety and prevents race conditions using a lock.

Classes:
    NewAppointmentTracker: A singleton class that maintains a record of new appointments for providers by date.

Methods:
    __new__(cls): Ensures only one instance of the class is created.
    __init__(self): Initializes the new_appointment_tracker dictionary.
    get_provider(self, provider_id): Retrieves appointment details for a given provider.
    get_provider_by_date(self, provider_id, date): Retrieves appointment details for a provider on a specific date.
    add_provider(self, provider_id, date): Adds or updates a provider in the tracker.
    increment_provider_appointments(self, provider_id, date):
        Increments the appointment count for a provider on a specific date.
    remove_appointment(self, appointment_id): Removes an appointment if it exists.
    get_all_appointments(self): Retrieves all appointments.
    check_if_provider_has_availibility(self, appointment_info):
        Checks if a provider has availability for a particular day.
"""

import threading

class NewAppointmentTracker:
    """
    A singleton class that tracks the amount of new appointments
    by date for each provider
    {
        provider_id: {
            date: new appointment count,
            date: new appointment count
        },
        provider_id: {
            ...
        }
    }
    """
    _instance = None
    _lock = threading.Lock()  # Ensures thread safety

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # Prevents race conditions
                if cls._instance is None:  # Double-check locking
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False  # Prevents reinitialization issues
        return cls._instance

    def __init__(self):
        if not self._initialized:  # Ensures __init__ runs only once
            self.new_appointment_tracker = {}
            self._initialized = True

    def get_provider(self, provider_id):
        """Retrieve appointment details."""
        return self.new_appointment_tracker.get(provider_id, "Not found")

    def get_provider_by_date(self, provider_id, date):
        """Retrieve provider appointment by a specified date"""
        provider_data = self.new_appointment_tracker.get(provider_id, "Not found")
        if provider_data == "Not found":
            return "Not found"
        return provider_data.get(date, "Not found")

    def add_provider(self, provider_id, date):
        """Add or update an provider in the tracker."""
        self.new_appointment_tracker[provider_id] = {}
        self.new_appointment_tracker[provider_id][date] = 0

    def increment_provider_appointments(self, provider_id, date):
        """Find a provider's date and increment by one"""
        self.new_appointment_tracker[provider_id][date] += 1

    def remove_appointment(self, appointment_id):
        """Remove an appointment if it exists."""
        if appointment_id in self.new_appointment_tracker:
            del self.new_appointment_tracker[appointment_id]

    def get_all_appointments(self):
        """Retrieve all appointments."""
        return self.new_appointment_tracker

    def check_if_provider_has_availibility(self, appointment_info):
        """Check if a provider has availability for a particular day"""
        provider_id = appointment_info['PROVIDERID']
        appointment_date = appointment_info['DATE']
        new_appointment_count = self.get_provider_by_date(provider_id, appointment_date)
        new_appointment_count = 0 if new_appointment_count == "Not found" else new_appointment_count
        if new_appointment_count >= 5:
            print(f'Provider: {provider_id} has booked the maximum amount of appointments for {appointment_date.strftime('%Y-%m-%d')}')
            return False
        return True
