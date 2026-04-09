# This is the main program where the users can see the menu to use

from habit_tracker import HabitTracker
from analytics import (
    list_all_habits,
    filter_by_periodicity,
    longest_streak_all,
    longest_streak_for_habit,
    current_streak_for_habit
)


def print_menu():
    """Here we display the main menu options for the user select option"""
    print("\n" + "=" * 40)
    print("        HABIT TRACKER APP")
    print("=" * 40)
    print("1. Add a new habit")
    print("2. Complete a habit (check it off)")
    print("3. Delete a habit")
    print("4. View all habits")
    print("5. View daily habits only")
    print("6. View weekly habits only")
    print("7. Show longest streak (all habits)")
    print("8. Show longest streak for one habit")
    print("9. Show current streak for a habit")
    print("10. Save and Exit")
    print("=" * 40)


def view_all_habits(tracker):
    """Show all habits"""
    habits = list_all_habits(tracker.get_all_habits())
    if not habits:
        print("No habits yet. Add one!")
        return
    
    print("\n--- ALL HABITS ---")
    for habit in habits:
        completions_count = len(habit.completions)
        print(f"• {habit.name} ({habit.periodicity})")
        print(f"  {habit.description}")
        print(f"  Completed {completions_count} times")
        print()


def view_habits_by_periodicity(tracker, periodicity):
    """Showing habits filtered by daily or weekly"""
    habits = filter_by_periodicity(tracker.get_all_habits(), periodicity)
    if not habits:
        print(f"No {periodicity} habits yet.")
        return
    
    print(f"\n--- {periodicity.upper()} HABITS ---")
    for habit in habits:
        print(f"• {habit.name}: {habit.description}")


def show_longest_streak_all(tracker):
    """Showing the longest streak across all habits"""
    name, streak = longest_streak_all(tracker.get_all_habits())
    if name:
        print(f"\n Longest streak overall: {name} with {streak} periods!")
    else:
        print("No habits yet!")


def show_longest_streak_one(tracker):
    """Showing longest streak for a specific habit"""
    name = input("Enter habit name: ")
    habit = tracker.get_habit_by_name(name)
    
    if not habit:
        print(f"Habit '{name}' not found!")
        return
    
    streak = longest_streak_for_habit(habit)
    print(f"\n Longest streak for '{habit.name}': {streak} periods")


def show_current_streak(tracker):
    """Show current ongoing streak for a habit"""
    name = input("Enter habit name: ")
    habit = tracker.get_habit_by_name(name)
    
    if not habit:
        print(f"Habit '{name}' not found!")
        return
    
    streak = current_streak_for_habit(habit)
    print(f"\n Current streak for '{habit.name}': {streak} periods (and counting!)")


def add_habit(tracker):
    """Add a new habit"""
    print("\n--- ADD NEW HABIT ---")
    name = input("Habit name (e.g., Workout): ")
    description = input("Description (e.g., 30 min run): ")
    
    print("Periodicity:")
    print("1. Daily")
    print("2. Weekly")
    choice = input("Choose 1 or 2: ")
    
    if choice == "1":
        periodicity = "daily"
    elif choice == "2":
        periodicity = "weekly"
    else:
        print("Invalid choice!")
        return
    
    tracker.add_habit(name, description, periodicity)
    # We save after adding
    tracker.save()  


def complete_habit(tracker):
    """Mark a habit as completed"""
    name = input("Enter habit name to complete: ")
    habit = tracker.get_habit_by_name(name)
    
    if not habit:
        print(f"Habit '{name}' not found!")
        return
    
    habit.complete_task()
    # we save after completing
    tracker.save()  
    print("Great job! Keep going!")


def delete_habit(tracker):
    """Delete a habit"""
    name = input("Enter habit name to delete: ")
    tracker.remove_habit(name)
    tracker.save()  


def main():
    """Main program loop"""
    print("\n Welcome to Habit Tracker!")
    
    # Creating tracker and load saved data
    tracker = HabitTracker()
    tracker.load()
    
    # Main menu loop
    while True:
        print_menu()
        choice = input("Choose an option (1-10): ")
        
        if choice == "1":
            add_habit(tracker)
        
        elif choice == "2":
            complete_habit(tracker)
        
        elif choice == "3":
            delete_habit(tracker)
        
        elif choice == "4":
            view_all_habits(tracker)
        
        elif choice == "5":
            view_habits_by_periodicity(tracker, "daily")
        
        elif choice == "6":
            view_habits_by_periodicity(tracker, "weekly")
        
        elif choice == "7":
            show_longest_streak_all(tracker)
        
        elif choice == "8":
            show_longest_streak_one(tracker)
        
        elif choice == "9":
            show_current_streak(tracker)
        
        elif choice == "10":
            tracker.save()
            print("\n Habits saved.")
            break
        
        else:
            print("Invalid choice! Please enter 1-10")


# Now we Run the program
if __name__ == "__main__":
    main()