from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a task that a pet needs to complete."""
    description: str
    duration: int  # in minutes
    priority: int  # higher number = higher priority


@dataclass
class Pet:
    """Represents a pet owned by an Owner."""
    name: str
    species: str
    breed: str
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's task list."""
        self.tasks.remove(task)


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks across all owned pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Scheduler for generating and explaining pet care plans."""
    
    def __init__(self, max_time: int):
        """
        Initialize scheduler.
        
        Args:
            max_time: Maximum time available (in minutes)
        """
        self.max_time = max_time
    
    def generate_plan(self):
        """Generate an optimized care plan for pets."""
        pass
    
    def explain_logic(self) -> str:
        """Explain the logic behind the scheduling decisions."""
        pass
