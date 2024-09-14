import threading


class SingletonBase:
    _instances = {}
    _locks = {}

    def __new__(cls, *args, **kwargs):
        # Create a key based on the class and the provided arguments
        key = (cls, args, frozenset(kwargs.items()))

        if key not in cls._instances:
            # Initialize a lock for each unique instance key
            if key not in cls._locks:
                cls._locks[key] = threading.Lock()

            with cls._locks[key]:  # Ensure only one thread can create the instance
                if key not in cls._instances:  # Double-checked locking
                    instance = super(SingletonBase, cls).__new__(cls)
                    instance._initialize(*args, **kwargs)  # Call initialization method
                    cls._instances[key] = instance
        return cls._instances[key]

    def _initialize(self, *args, **kwargs):
        """Method to initialize the instance. Should be overridden by subclasses."""
        pass

    @classmethod
    def clear_instance(cls, *args, **kwargs):
        """Clear the instance for the given parameters (useful for testing or resetting)."""
        key = (cls, args, frozenset(kwargs.items()))
        if key in cls._instances:
            del cls._instances[key]
