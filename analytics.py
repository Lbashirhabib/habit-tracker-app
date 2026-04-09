# in this file, it contains functions for analysing the habits Using functional programming style.

from datetime import datetime, timedelta, date
from typing import List
from habit import Habit


def list_all_habits(habits):
    """this return list of all habits."""
    return [habit for habit in habits]


def filter_by_periodicity(habits, periodicity):
    """here it return habits with given periodicity daily or weekly."""
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def _get_periods(habit, end_date=None, include_today=True):
    """
    we generate a list of start, end tuples for each period day or week
    from habit creation up to end_date.
    
    If include_today is True, periods include today; otherwise, they stop at yesterday.
    """
    if end_date is None:
        end_date = date.today()
        if include_today:
            # Include todays period
            end_date = end_date + timedelta(days=1)
    
    start_date = habit.creation_date.date()
    periods = []

    if habit.periodicity == "daily":
        current = start_date
        while current < end_date:
            periods.append((current, current))
            current += timedelta(days=1)
    else:  # if weekly
        # Find the Monday of the week containing creation date
        days_to_monday = start_date.weekday() 
        first_monday = start_date - timedelta(days=days_to_monday)
        current = first_monday
        while current < end_date:
            week_start = current
            week_end = current + timedelta(days=6)
            periods.append((week_start, week_end))
            current += timedelta(days=7)

    return periods


def _was_completed_in_period(habit, period_start, period_end):
    """here it check if habit was completed for at least once between period_start and period_end."""
    for completion in habit.completions:
        comp_date = completion.date()
        if period_start <= comp_date <= period_end:
            return True
    return False


def longest_streak_for_habit(habit):
    """here we return the longest consecutive periods streak for a single habit including today if it is completed."""
    periods = _get_periods(habit, include_today=True)  # this line Include todays period
    longest = 0
    current = 0

    for start, end in periods:
        if _was_completed_in_period(habit, start, end):
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0

    return longest


def longest_streak_all(habits):
    """return habit_name, longest_streak across all habits."""
    best_habit = None
    best_streak = 0
    for habit in habits:
        streak = longest_streak_for_habit(habit)
        if streak > best_streak:
            best_streak = streak
            best_habit = habit
    if best_habit:
        return best_habit.name, best_streak
    return None, 0


def current_streak_for_habit(habit):
    """we return current ongoing streak (number of consecutive completed periods up to yesterday)."""
    periods = _get_periods(habit, include_today=False)  # Exclude today's period
    current_streak = 0
    # Walk backwards from the most recent period
    for start, end in reversed(periods):
        if _was_completed_in_period(habit, start, end):
            current_streak += 1
        else:
            break
    return current_streak