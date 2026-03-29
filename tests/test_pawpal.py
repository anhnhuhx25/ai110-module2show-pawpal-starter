import pytest
from pawpal_system import Task, Pet


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