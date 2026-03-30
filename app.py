import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="Unknown")
age = st.number_input("Age (years)", min_value=0.0, max_value=30.0, value=0.0, step=0.5)
available_hours = st.slider("Available hours per day", min_value=0.5, max_value=12.0, value=2.0, step=0.5)

# Initialize Owner in session state if not already present
if "owner" not in st.session_state:
    #1. create owner
    new_owner = Owner(owner_name, f"{owner_name.lower()}@example.com", available_time_hours=2)
    #2. create pet and add to owner
    new_pet = Pet(pet_name, species, breed, age)
    new_owner.add_pet(new_pet)
    #3. save owner to session state
    st.session_state.owner = new_owner
owner = st.session_state.owner
owner.available_time_hours = available_hours
if owner.pets:
    owner.pets[0].name = pet_name
    owner.pets[0].species = species
    owner.pets[0].breed = breed
    owner.pets[0].age_years = age

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium low", "medium", "medium high", "high"], index=2)
with col4:
    task_time = st.text_input("Preferred Time (HH:MM)", value="09:00")
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly"], index=0)

if st.button("Add task"):
    #map UI text to numeric priorities
    priority_map = {"low": 1, "medium low": 2, "medium": 3, "medium high": 4, "high": 5}

    #create task object
    new_task = Task(task_title, duration, priority_map[priority], frequency=frequency, preferred_time_window=task_time)

    #add it to first pet in owner's list
    if owner.pets:
        owner.pets[0].add_task(new_task)
        st.success(f"Added task '{task_title}' to pet '{owner.pets[0].name}'")

# Show tasks for the first pet
if owner.pets and owner.pets[0].tasks:
    st.write(f"Current tasks for {owner.pets[0].name}:")
    # This turns our objects into a simple list so st.table can read them
    display_data = [
        {"Description": f"{t.get_emoji()} {t.description}", "Mins": t.duration_minutes, "Priority": t.priority, "Preferred Time": t.preferred_time_window, "Frequency": t.frequency} 
        for t in owner.pets[0].tasks
    ]
    st.table(display_data)
else:
    st.info("No tasks yet. Add one above.")
st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    #intialize scheduler with vault owner
    scheduler = Scheduler(owner)

    #generate plan
    daily_plan = scheduler.generate_daily_plan()

    # check for conflicts and show warnings above schedule output
    warnings = scheduler.check_for_conflicts(daily_plan)
    if warnings:
        for warning in warnings:
            st.warning(warning)

    #display results
    st.markdown("### Generated Schedule")
    st.write(daily_plan.get_schedule_text())
    st.info(daily_plan.get_reasoning_text())
