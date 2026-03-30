from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from uuid import uuid4
from datetime import datetime, timedelta, date
'''
Author: Anh Nhu
'''


@dataclass
class Task:
    """Represents a pet care task with scheduling properties."""
    description: str
    duration_minutes: int
    priority: int  # 1-5 scale, 5 being highest
    frequency: str = "daily"  # 'daily', 'weekly', etc.
    preferred_time_window: str = "any"  # 'morning', 'afternoon', 'evening', 'any'
    is_completed_today: bool = False
    next_due_date: date = field(default_factory=date.today)
    id: str = field(default_factory=lambda: str(uuid4()))
    
    def mark_completed(self) -> None:
        """Mark the task as completed and update next due date."""
        self.is_completed_today = True

        today = date.today()
        if self.frequency == 'daily':
            self.next_due_date = today + timedelta(days=1)
            print(f"Task scheduled for {self.next_due_date}")
        elif self.frequency == 'weekly':
            self.next_due_date = today + timedelta(days=7)
            print(f"Task scheduled for {self.next_due_date}")
        else:
            # Keep existing due date for other frequencies or set to tomorrow by default
            self.next_due_date = today + timedelta(days=1)
            print(f"Task scheduled for {self.next_due_date}")
    
    def reset_for_new_day(self) -> None:
        """Reset the task for a new day."""
        self.is_completed_today = False
    
    def get_emoji(self) -> str:
        """Return an emoji based on keywords in the task description."""
        desc = self.description.lower()
        if 'walk' in desc:
            return '🦮'
        elif 'feed' in desc:
            return '🥣'
        elif 'groom' in desc:
            return '✂️'
        elif 'play' in desc:
            return '🎾'
        else:
            return '🐾'


@dataclass
class Pet:
    """Represents a pet owned by an Owner."""
    name: str
    species: str
    breed: str
    age_years: float = 0.0
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the pet's task list by task ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
    
    def get_daily_tasks(self) -> List[Task]:
        """Get all tasks for this pet that are scheduled for today."""
        return [task for task in self.tasks if task.frequency == "daily" and not task.is_completed_today]


class Owner:
    """Represents a pet owner with preferences and available time."""
    
    def __init__(self, name: str, email: str, available_time_hours: float = 2.0):
        """
        Initialize an owner.
        
        Args:
            name: Owner's name
            email: Owner's email
            available_time_hours: Hours available daily for pet care
        """
        self.name = name
        self.email = email
        self.available_time_hours = available_time_hours
        self.preferences: Dict[str, Any] = {}
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update owner preferences."""
        self.preferences.update(preferences)
    
    def get_available_time(self) -> float:
        """Get available time in hours."""
        return self.available_time_hours
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks across all owned pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks
    
    def filter_tasks(self, status=None, pet_name=None) -> List[Task]:
        """
        Filter tasks based on completion status and/or pet name.
        
        Args:
            status: If True/False, filter by is_completed_today
            pet_name: If provided, only include tasks from this pet
        
        Returns:
            List of filtered tasks
        """
        tasks = []
        for pet in self.pets:
            if pet_name is None or pet.name == pet_name:
                for task in pet.tasks:
                    if status is None or task.is_completed_today == status:
                        tasks.append(task)
        return tasks


@dataclass
class ScheduleItem:
    """Represents a single scheduled pet care task."""
    task: Task
    pet: Pet
    start_time: datetime
    end_time: datetime
    priority_score: float = 0.0
    
    def get_duration(self) -> int:
        """Get duration in minutes."""
        return self.task.duration_minutes
    
    def to_string(self) -> str:
        """Return a human-readable string representation of the scheduled item."""
        start_str = self.start_time.strftime("%I:%M %p")
        end_str = self.end_time.strftime("%I:%M %p")
        return (f"{start_str} - {end_str}: {self.task.get_emoji()} {self.task.description} "
                f"for {self.pet.name} ({self.get_duration()} minutes, Priority: {self.task.priority})")


class Plan:
    """Represents a daily pet care plan with scheduling and reasoning."""
    
    def __init__(self):
        """Initialize an empty plan."""
        self.scheduled_items: List[ScheduleItem] = []
        self.total_duration: int = 0
        self.reasoning: str = ""
    
    def add_item(self, item: ScheduleItem) -> None:
        """Add a scheduled item to the plan."""
        self.scheduled_items.append(item)
        self.total_duration += item.get_duration()
    
    def get_schedule_text(self) -> str:
        """Get formatted text of the schedule."""
        if not self.scheduled_items:
            return "No tasks scheduled for today."
        
        schedule_text = "Daily Pet Care Schedule:\n" + "=" * 50 + "\n"
        for item in self.scheduled_items:
            schedule_text += item.to_string() + "\n"
        schedule_text += "=" * 50 + f"\nTotal Duration: {self.total_duration} minutes"
        return schedule_text
    
    def get_reasoning_text(self) -> str:
        """Get formatted text explaining the scheduling reasoning."""
        return f"Scheduling Reasoning:\n{self.reasoning}"


class Scheduler:
    """Generates optimized daily pet care plans based on constraints and priorities."""
    
    def __init__(self, owner: Owner, constraints: Optional[Dict[str, Any]] = None):
        """
        Initialize scheduler.
        
        Args:
            owner: Owner whose pets to schedule
            constraints: Optional dict of scheduling constraints
        """
        self.owner = owner
        self.pets = owner.pets
        self.constraints = constraints or {}
    
    def generate_daily_plan(self) -> Plan:
        """
        Generate an optimized daily care plan for all owner's pets.
        
        Returns:
            Plan: A scheduled plan of tasks within constraints
        """
        plan = Plan()
        
        # Collect all daily tasks from all pets
        all_tasks = []
        for pet in self.pets:
            daily_tasks = pet.get_daily_tasks()
            all_tasks.extend([(task, pet) for task in daily_tasks])
        
        # Sort by priority (highest first)
        all_tasks.sort(key=lambda x: x[0].priority, reverse=True)
        
        # Schedule tasks starting from 9:00 AM
        current_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        max_minutes = int(self.owner.available_time_hours * 60)
        scheduled_count = 0
        
        for task, pet in all_tasks:
            duration_minutes = task.duration_minutes
            
            # Check if adding this task would exceed available time
            if plan.total_duration + duration_minutes > max_minutes:
                break  # Stop scheduling if we'd exceed time limit
            
            # Calculate end time
            end_time = current_time + timedelta(minutes=duration_minutes)
            
            # Create schedule item
            schedule_item = ScheduleItem(
                task=task,
                pet=pet,
                start_time=current_time,
                end_time=end_time,
                priority_score=float(task.priority)
            )
            
            # Add to plan
            plan.add_item(schedule_item)
            scheduled_count += 1
            
            # Update current time for next task (no gaps between tasks)
            current_time = end_time
        
        # Update reasoning
        plan.reasoning = (
            f"Scheduled {scheduled_count} out of {len(all_tasks)} tasks by priority "
            f"(highest first) within {self.owner.available_time_hours} hours available. "
            f"Started at 9:00 AM with no gaps between tasks. "
            f"{'All tasks scheduled.' if scheduled_count == len(all_tasks) else f'Stopped at {max_minutes} minutes limit.'}"
        )
        
        return plan
    
    def check_for_conflicts(self, plan: Plan) -> List[str]:
        """
        Check scheduled items for overlapping time windows.

        Args:
            plan: The plan to validate

        Returns:
            List[str]: warnings for detected conflicts or [] if none
        """
        conflicts = []
        previous_item = None

        for item in plan.scheduled_items:
            if previous_item is not None:
                if item.start_time < previous_item.end_time:
                    conflicts.append(
                        f"Conflict detected: [{previous_item.task.description}] overlaps with [{item.task.description}]"
                    )
            previous_item = item

        return conflicts
    
    def explain_plan(self, plan: Plan) -> str:
        """
        Explain the reasoning behind the generated plan.
        
        Args:
            plan: The plan to explain
        
        Returns:
            str: Explanation text
        """
        return plan.get_reasoning_text()
    
    def validate_constraints(self, plan: Plan) -> bool:
        """
        Validate that the plan meets all constraints.
        
        Args:
            plan: The plan to validate
        
        Returns:
            bool: True if plan is valid, False otherwise
        """
        max_minutes = int(self.owner.available_time_hours * 60)
        return plan.total_duration <= max_minutes
    
    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by their preferred time window chronologically.
        Tasks with 'any' time window are sorted last.
        
        Args:
            tasks: List of tasks to sort
        
        Returns:
            List of tasks sorted by preferred time
        """
        return sorted(tasks, key=lambda task: (
            task.preferred_time_window == 'any',
            int(task.preferred_time_window.split(':')[0]) * 60 + int(task.preferred_time_window.split(':')[1])
            if task.preferred_time_window != 'any' else 0
        ))
