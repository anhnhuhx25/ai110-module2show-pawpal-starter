import pytest
from datetime import date, timedelta, datetime
from pawpal_system import Task, Pet, Owner, Scheduler, ScheduleItem, Plan


def test_task_completion():
    """Test that marking a task as completed sets is_completed_today to True."""
    # Create a Task
    task = Task("Walk the dog", 30, 5)

    # Initially, task should not be completed
    assert task.is_completed_today is False

    # Call mark_completed()
    task.mark_completed()

    # Assert that is_completed_today is True
    assert task.is_completed_today is True


def test_pet_task_addition():
    """Test that adding a task to a pet increases the task list length."""
    # Create a Pet
    pet = Pet("Max", "Dog", "Golden Retriever")

    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0

    # Create and add a Task
    task = Task("Walk Max", 30, 5)
    pet.add_task(task)

    # Assert that the pet's task list now has 1 task
    assert len(pet.tasks) == 1


def test_sorting_preferred_time():
    """Verify tasks are sorted by preferred_time_window as time strings."""
    owner = Owner("Alex", "alex@example.com", available_time_hours=2)
    scheduler = Scheduler(owner)

    task_morning = Task("Morning Care", 30, 3, preferred_time_window="08:00")
    task_afternoon = Task("Afternoon Care", 30, 3, preferred_time_window="14:00")

    sorted_tasks = scheduler.sort_tasks_by_time([task_afternoon, task_morning])

    assert sorted_tasks[0] is task_morning
    assert sorted_tasks[1] is task_afternoon


def test_recurrence_mark_completed_daily():
    """Verify mark_completed increments next_due_date by 1 day for daily tasks."""
    task = Task("Feed", 10, 5, frequency="daily")
    initial_due = date.today()
    task.next_due_date = initial_due

    task.mark_completed()

    assert task.is_completed_today is True
    assert task.next_due_date == initial_due + timedelta(days=1)


def test_conflicts_overlapping_tasks():
    """Verify check_for_conflicts returns a warning on an overlap."""
    owner = Owner("Sam", "sam@example.com", available_time_hours=3)
    scheduler = Scheduler(owner)

    pet = Pet("Bella", "Dog", "Mixed")
    owner.add_pet(pet)

    task1 = Task("Brush", 30, 5)
    task2 = Task("Nail Trim", 30, 5)

    start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    item1 = ScheduleItem(task=task1, pet=pet, start_time=start, end_time=start + timedelta(minutes=30))
    item2 = ScheduleItem(task=task2, pet=pet, start_time=start + timedelta(minutes=15), end_time=start + timedelta(minutes=45))

    plan = Plan()
    plan.add_item(item1)
    plan.add_item(item2)

    conflicts = scheduler.check_for_conflicts(plan)

    assert len(conflicts) == 1
    assert "overlaps" in conflicts[0]
