# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling
The PawPal+ system has been upgraded from a static list to an intelligent scheduling engine. Key features include:

- Chronological Sorting: Tasks are no longer scheduled in the order they were typed. The system uses lambda sorting to organize tasks by their preferred_time_window (e.g., 08:00 before 14:00).
- Intelligent Filtering: Owners can now query their dashboard for specific subsets of data, such as "Only Luna's tasks" or "Only uncompleted daily tasks."
- Automated Recurrence: Using Python's timedelta, the system automatically calculates and updates the due_date for Daily and Weekly tasks once they are marked complete.
- Conflict Detection: A lightweight safety check identifies overlapping task windows (e.g., two 30-minute walks starting at the same time) and issues a warning to the user.
- Constraint Management: The scheduler strictly respects the Owner's available_time_hours, prioritizing high-value tasks and cutting lower-priority items if the time budget is exceeded.

### Testing PawPal+
To ensure the reliability of the scheduling and recurrence logic, this project includes an automated test suite powered by `pytest`.
Confidence level: 5/5
How to Run tests
From the root directory, ensure your virtual environment is activated and run:
```bash
python -m pytest

