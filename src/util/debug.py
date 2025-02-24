import threading

class Debug:
    """
    Singleton class to manage debug mode
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
            self.debug = False
            self._initialized = True

    def set_debug(self,flag):
        """Retrieve appointment details."""
        print(f'Setting debug flag to {flag}')
        self.debug = flag
        return self.debug

    def get_debug(self,):
        """Retrieve appointment details."""
        return self.debug
