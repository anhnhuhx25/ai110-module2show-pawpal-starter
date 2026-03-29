from pawpal_system import Owner, Pet, Task, Scheduler, Plan, ScheduleItem
from datetime import datetime, timedelta

def run_demo():
    #Create owner
    owner = Owner('John', 'john@yahoo.com', available_time_hours=1.5)

    #Create pets
    buddy = Pet('Buddy', 'Dog', 'Golden Retriever')
    whiskers = Pet('Whiskers', 'Cat', 'Siamese')
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    
    #Create tasks for Buddy
    buddy.add_task(Task('Afternoon Walk Buddy', duration_minutes=30, priority=5, preferred_time_window='14:00'))
    buddy.add_task(Task('Morning Walk Buddy', duration_minutes=30, priority=4, preferred_time_window='08:00'))
    buddy.add_task(Task('Midday Play Buddy', duration_minutes=15, priority=3, preferred_time_window='11:00'))
    
    #Create task for Whiskers
    whiskers.add_task(Task('Brush Fur Whiskers', duration_minutes=15, priority=3))
    
    #Generate scheduler
    scheduler = Scheduler(owner)
    
    # Test sorting
    sorted_tasks = scheduler.sort_tasks_by_time(buddy.tasks)
    print("Sorted Buddy's tasks by time:")
    for task in sorted_tasks:
        print(f"{task.preferred_time_window}: {task.description}")
    
    # Add second pet Luna
    luna = Pet('Luna', 'Cat', 'Persian')
    owner.add_pet(luna)
    luna.add_task(Task('Groom Luna', duration_minutes=20, priority=2))
    
    # Test filtering
    luna_tasks = owner.filter_tasks(pet_name='Luna')
    print("\nLuna's tasks:")
    for task in luna_tasks:
        print(task.description)
    
    # Generate daily plan
    daily_plan = scheduler.generate_daily_plan()

    # Manually create overlapping items to test conflict detection
    conflict_plan = Plan()
    item1 = ScheduleItem(
        task=Task('Overlap Task 1', duration_minutes=30, priority=5),
        pet=buddy,
        start_time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
        end_time=datetime.now().replace(hour=9, minute=30, second=0, microsecond=0),
        priority_score=5.0,
    )
    item2 = ScheduleItem(
        task=Task('Overlap Task 2', duration_minutes=30, priority=4),
        pet=buddy,
        start_time=datetime.now().replace(hour=9, minute=15, second=0, microsecond=0),
        end_time=datetime.now().replace(hour=9, minute=45, second=0, microsecond=0),
        priority_score=4.0,
    )
    conflict_plan.add_item(item1)
    conflict_plan.add_item(item2)

    conflicts = scheduler.check_for_conflicts(conflict_plan)
    print("\nConflict check:")
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts found")

    #Output results to terminal
    print("\n--- PAWPAL DEMO ---")
    print(daily_plan.get_schedule_text())
    print("\n" + daily_plan.get_reasoning_text())
if __name__ == "__main__":
    run_demo()    