# this file manages all habits and handles saving and loading

import json
from datetime import datetime
from typing import List, Optional
from habit import Habit

class HabitTracker:
    
    def __init__(self, storage_file="habits.json"):
        """
        creating a new habit tracker
        :param storage_file: The file where we save data
        """
        # here is the list to store all Habit objects
        self.habits = []  
        self.storage_file = storage_file
    
    def add_habit(self, name, description, periodicity):
        """
        create a new habit and add it to the list
        Returns the new habit
        """
        # Here we check if habit with same name already exists or not
        if self.get_habit_by_name(name):
            print(f"Habit '{name}' already exists!")
            return None
        
        # Now we create the new habit
        new_habit = Habit(name, description, periodicity)
        self.habits.append(new_habit)
        print(f" Added new habit: {name}")
        return new_habit
    
    def remove_habit(self, name):
        """
        Remove a habit by its name
        Returns True if found and removed, False if not found
        """
        for i, habit in enumerate(self.habits):
            if habit.name.lower() == name.lower():
                del self.habits[i]
                print(f"Removed habit: {name}")
                return True
        print(f"Habit '{name}' not found!")
        return False
    
    def get_habit_by_name(self, name):
        """
        Find a habit by its name 
        Returns the habit or None if not found
        """
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return habit
        return None
    
    def get_habits_by_periodicity(self, periodicity):
        """
        Return all habits with a given periodicity
        periodicity should be "daily" or "weekly"
        """
        result = []
        for habit in self.habits:
            if habit.periodicity == periodicity:
                result.append(habit)
        return result
    
    def get_all_habits(self):
        """Return all habits"""
        return self.habits
    
    def save(self):
        """
        Here it Save all habits to the JSON file
        """
        data = []
        for habit in self.habits:
            # Converting each habit to a dictionary here
            habit_dict = {
                "name": habit.name,
                "description": habit.description,
                "periodicity": habit.periodicity,
                "creation_date": habit.creation_date.isoformat(),
                "completions": [dt.isoformat() for dt in habit.completions]
            }
            data.append(habit_dict)
        
        # Now we write to file
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(" Habits saved to file")
    
    def load(self):
        """
        Load habits from the JSON file
        If file doesn't exist, we then create predefined habits
        """
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # No saved file found, the we create predefined habits
            print("No saved habits found. Creating predefined habits...")
            self._create_predefined_habits()
            return
        
        # We clear current habits if needed
        self.habits = []
        
        # We can recreate each habit from the data here
        for item in data:
            habit = Habit(
                name=item["name"],
                description=item["description"],
                periodicity=item["periodicity"]
            )
            # Restoring the creation date
            habit.creation_date = datetime.fromisoformat(item["creation_date"])
            # And restoring all completion dates
            habit.completions = [datetime.fromisoformat(dt) for dt in item["completions"]]
            self.habits.append(habit)
        
        print(f"Loaded {len(self.habits)} habits from file")
    
    def _create_predefined_habits(self):
        """
        i am to create 5 example habits with 4 weeks of fake data
        This runs only when no saved file exists
        """
        from datetime import timedelta, date
        
        # Create 5 habits
        self.add_habit("Workout", "30 minute workout", "daily")
        self.add_habit("Reading", "Read 20 pages of a book", "daily")
        self.add_habit("Meditate", "10 minutes of meditation", "daily")
        self.add_habit("Watering plants", "Water indoor plants", "weekly")
        self.add_habit("Programming skills", "Practice Programming", "weekly")
        
        # Lets generate fake completions for the last 4 weeks
        today = date.today()
        
        for habit in self.habits:
            # Clearing any auto-generated completions
            habit.completions = []
            
            # For daily habits also
            if habit.periodicity == "daily":
                # Go back 28 days that is 4 weeks
                # from yesterday back to 28 days ago
                for days_ago in range(1, 29):  
                    completion_date = today - timedelta(days=days_ago)
                    
                    # Creating some patterns to show streaks and misses
                    if habit.name == "Workout":
                        # Workout we do it every day which is perfect streak
                        habit.completions.append(datetime(completion_date.year, completion_date.month, completion_date.day, 8, 0))
                    
                    elif habit.name == "Reading":
                        # Reading we do it most days, miss 3 random days
                        # if skiped 3 specific days
                        if days_ago not in [3, 10, 22]:  
                            habit.completions.append(datetime(completion_date.year, completion_date.month, completion_date.day, 20, 0))
                    
                    elif habit.name == "Meditate":
                        # Meditating also we do it most days, but say break streak on day 10
                        if days_ago != 10:  # miss day 10
                            habit.completions.append(datetime(completion_date.year, completion_date.month, completion_date.day, 7, 0))
            
            # Now For weekly habits
            else:  
                # Lets go back 4 weeks
                for weeks_ago in range(1, 5):
                    # We find Monday of that week
                    current_date = today - timedelta(weeks=weeks_ago)
                    # We go to Monday
                    start_of_week = current_date - timedelta(days=current_date.weekday())
                    
                    if habit.name == "Water plants":
                        # Water plants every Sunday
                        sunday = start_of_week + timedelta(days=6)
                        if sunday <= today:
                            habit.completions.append(datetime(sunday.year, sunday.month, sunday.day, 10, 0))
                    
                    elif habit.name == "Programming Skills":
                        # Practice programming 3 out of 4 weeks
                        # if we skip
                        if weeks_ago != 2:  
                            sunday = start_of_week + timedelta(days=6)
                            if sunday <= today:
                                habit.completions.append(datetime(sunday.year, sunday.month, sunday.day, 15, 0))
        
        print("Created 5 predefined habits with 4 weeks of example data")
        self.save()