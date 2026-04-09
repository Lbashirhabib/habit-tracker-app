# test_habit_tracker.py
# Simple unit tests to check if everything works

import unittest
from datetime import datetime, timedelta, date
from habit import Habit
from habit_tracker import HabitTracker
from analytics import (
    longest_streak_for_habit,
    longest_streak_all,
    current_streak_for_habit,
    list_all_habits,
    filter_by_periodicity
)


class TestHabitTracker(unittest.TestCase):
    """Testinge habit tracker functionality"""
    
    def setUp(self):
        """This runs before each test - set up what we need"""
        self.tracker = HabitTracker("test_habits.json")
        self.tracker.habits = []  
    
    def test_add_habit(self):
        """Testingat we can add a habit"""
        habit = self.tracker.add_habit("Test Habit", "Testing", "daily")
        self.assertIsNotNone(habit)
        self.assertEqual(len(self.tracker.habits), 1)
        self.assertEqual(self.tracker.habits[0].name, "Test Habit")
        print(" test_add_habit passed")
    
    def test_remove_habit(self):
        """Testing that we can remove a habit """
        self.tracker.add_habit("Test Habit", "Testing", "daily")
        result = self.tracker.remove_habit("Test Habit")
        self.assertEqual(len(self.tracker.habits), 0)
        self.assertTrue(result)
        print(" test_remove_habit passed")
    
    def test_complete_habit(self):
        """Test that completing a habit adds a timestamp"""
        habit = self.tracker.add_habit("Test Habit", "Testing", "daily")
        result = habit.complete_task()
        self.assertEqual(len(habit.completions), 1)
        self.assertTrue(result)
        print("test_complete_habit passed")
    
    def test_longest_streak(self):
        """Test streak calculation works with consecutive days"""
        # Create a habit
        habit = Habit("Test", "Testing", "daily")
        # Set creation date to 3 days ago so periods start before completions
        habit.creation_date = datetime.now() - timedelta(days=3)
        
        # Create dates for 3 consecutive days
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        # Add completions for 3 consecutive days
        habit.complete_task(two_days_ago)
        habit.complete_task(yesterday)
        habit.complete_task(today)
        
        # Calculate the streak
        streak = longest_streak_for_habit(habit)
        
        # Should be 3 if all three days are consecutive
        self.assertEqual(streak, 3)
        print(f"✓ test_longest_streak passed (streak = {streak})")
    
    def test_longest_streak_with_break(self):
        """Test streak calculation with a break in between"""
        # Create a habit
        habit = Habit("Test", "Testing", "daily")
        # Set creation date to 5 days ago so periods start before completions
        habit.creation_date = datetime.now() - timedelta(days=5)
        
        # Create dates
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        three_days_ago = today - timedelta(days=3)
        four_days_ago = today - timedelta(days=4)
        
        # days 1-2, break day 3, then days 4-5
        # 2 days and 2 days, longest should be 2
        habit.complete_task(four_days_ago)  
        habit.complete_task(three_days_ago)
        # day 3 is MISSED (no completion)
        habit.complete_task(yesterday)      
        habit.complete_task(today)          
        
        streak = longest_streak_for_habit(habit)
        
        # Longest streak should be 2 (either first 2 days or last 2 days)
        self.assertEqual(streak, 2)
        print(f" test_longest_streak_with_break passed (streak = {streak})")
    
    def test_get_habit_by_name(self):
        """Test finding a habit by name"""
        self.tracker.add_habit("Morning Run", "Run 5km", "daily")
        habit = self.tracker.get_habit_by_name("Morning Run")
        self.assertIsNotNone(habit)
        self.assertEqual(habit.name, "Morning Run")
        
        # Test case insensitive
        habit = self.tracker.get_habit_by_name("morning run")
        self.assertIsNotNone(habit)
        print(" test_get_habit_by_name passed")
    
    def test_filter_by_periodicity(self):
        """Test filtering habits"""
        self.tracker.add_habit("Daily Habit", "Do this daily", "daily")
        self.tracker.add_habit("Weekly Habit", "Do this weekly", "weekly")
        
        daily_habits = self.tracker.get_habits_by_periodicity("daily")
        weekly_habits = self.tracker.get_habits_by_periodicity("weekly")
        
        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(daily_habits[0].name, "Daily Habit")
        self.assertEqual(weekly_habits[0].name, "Weekly Habit")
        print(" test_filter_by_periodicity passed")
    
    def test_analytics_list_all_habits(self):
        """Test the list_all_habits function from analytics"""
        self.tracker.add_habit("Habit 1", "First", "daily")
        self.tracker.add_habit("Habit 2", "Second", "weekly")
        
        all_habits = list_all_habits(self.tracker.get_all_habits())
        self.assertEqual(len(all_habits), 2)
        print(" test_analytics_list_all_habits passed")
    
    def test_analytics_filter_by_periodicity(self):
        """Test the filter_by_periodicity function from analytics"""
        self.tracker.add_habit("Daily 1", "First daily", "daily")
        self.tracker.add_habit("Daily 2", "Second daily", "daily")
        self.tracker.add_habit("Weekly 1", "First weekly", "weekly")
        
        daily_habits = filter_by_periodicity(self.tracker.get_all_habits(), "daily")
        weekly_habits = filter_by_periodicity(self.tracker.get_all_habits(), "weekly")
        
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(len(weekly_habits), 1)
        print("✓ test_analytics_filter_by_periodicity passed")
    
    def test_save_and_load(self):
        """Test that saving and loading works"""
        # Add a habit
        self.tracker.add_habit("Save Test", "Testing save", "daily")
        
        # Complete it once
        habit = self.tracker.get_habit_by_name("Save Test")
        habit.complete_task()
        
        # Save to file
        self.tracker.save()
        
        # Create new tracker and load
        new_tracker = HabitTracker("test_habits.json")
        new_tracker.load()
        
        # Check that habit exists
        loaded_habit = new_tracker.get_habit_by_name("Save Test")
        self.assertIsNotNone(loaded_habit)
        self.assertEqual(len(loaded_habit.completions), 1)
        print("✓ test_save_and_load passed")
    
    def test_current_streak(self):
        """Test current streak calculation"""
        habit = Habit("Test", "Testing", "daily")
        # Set creation date to 3 days ago so periods start before completions
        habit.creation_date = datetime.now() - timedelta(days=3)
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        # Complete last 2 days, but not today
        habit.complete_task(two_days_ago)
        habit.complete_task(yesterday)
        
        streak = current_streak_for_habit(habit)
        # Current streak should be 2 (yesterday and two days ago)
        self.assertEqual(streak, 2)
        print(f" test_current_streak passed (current streak = {streak})")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("RUNNING HABIT TRACKER TESTS")
    print("=" * 50 + "\n")
    unittest.main()