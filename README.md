# Habit Tracker: A Simple Python Habit Tracking App

This is a simple habit tracker that runs in the terminal. You can create daily or weekly habits, And check them off when you complete them, and see your streaks. All your data is saved to a file, so it is still there when you reopen the app.
You need Python 3.7 or above to run it, No extra libraries are needed, it uses only built-in Python modules.

## How to install and use it
1. Download all the files into one folder:
   - `habit.py`
   - `habit_tracker.py`
   - `analytics.py`
   - `main.py`
   - `test_habit_tracker.py` (this is for testing only)
2. Open a terminal or command prompt in that folder.
3. Run the app: by typing "python main.py"

The app shows a menu with numbers. Just type the number of what you want to do from number 1 to number 10.

- Add a habit: You will be asked for a name, a description, and if it is daily or weekly.
- Complete a habit: Type the name of the habit you completed, then It will record the current date and time.
- View habits: You can see all habits, or only daily/weekly ones.
- Streaks: The app can show you your longest streak (ever) and your current streak (ongoing).

All changes are saved automatically when you add, complete, or delete a habit.

## Predefined habits
The first time you run the app, it creates five habits with example data (4 weeks of completions) so you can see how streaks work right away. You can delete or add your own anytime.

## Testing
If you want to check that everything works correctly, run:
python test_habit_tracker.py
All tests should pass.

