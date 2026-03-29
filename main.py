from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    #Create owner
    owner = Owner('John', 'john@yahoo.com', available_time_hours=1.5)

    #Create pets
    dog = Pet('Max', 'Dog', 'Golden Retriever')
    cat = Pet('Whiskers', 'Cat', 'Siamese')
    owner.add_pet(dog)
    owner.add_pet(cat)
    #Create tasks
    dog.add_task(Task('Morning Walk Max', duration_minutes= 30, priority=5))
    cat.add_task(Task('Brush Fur Whiskers', duration_minutes= 15, priority=3))
    dog.add_task(Task('Training Sessions Max', duration_minutes= 60, priority=4))
    #Generate scheduler
    scheduler = Scheduler(owner)
    daily_plan = scheduler.generate_daily_plan()

    #Output results to terminal
    print("\n--- PAWPAL DEMO ---")
    print(daily_plan.get_schedule_text())
    print("\n" + daily_plan.get_reasoning_text())
if __name__ == "__main__":
    run_demo()    