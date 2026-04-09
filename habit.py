# In this file i defines what a habit is and what it can do
from datetime import datetime
from typing import List

class Habit:
    """A class representing a single habit"""
    
    def __init__(self, name: str, description: str, periodicity: str):
        
        self.name = name
        self.description = description
        self.periodicity = periodicity  
        self.creation_date = datetime.now()  
        self.completions = []  
    
    def complete_task(self, timestamp=None):
        """
        we mark this habit as completed
        """
        if timestamp is None:
            timestamp = datetime.now()
        if isinstance(timestamp, datetime):
            self.completions.append(timestamp)
        else:
            # If it is a date object, we convert to datetime
            self.completions.append(datetime(timestamp.year, timestamp.month, timestamp.day))
        print(f" Completed: {self.name} on {timestamp}")
        return True
    
    def is_completed_in_period(self, start_date, end_date):
        """
        Checkking if this habit was completed between two dates
        Returns True if yes, and False if no
        """
        for completion in self.completions:
            # Only compare the date part, not the time
            if start_date <= completion.date() <= end_date:
                return True
        return False
    
    def __repr__(self):
        """What to show when we print a habit"""
        return f"{self.name} ({self.periodicity}) - {self.description}"