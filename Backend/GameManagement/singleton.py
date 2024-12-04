# myapp/singleton.py

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            # Initialize your singleton instance here
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        # Any initialization logic for your singleton
        self.some_property = "Initial Value"

    def some_method(self):
        # Example method for your singleton
        print(f"calling some_method: {self.some_property}")
        return self.some_property