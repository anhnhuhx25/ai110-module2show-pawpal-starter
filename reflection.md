# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Core logic: The Owners have Pets, and Pets have lists of Tasks.
- What classes did you include, and what responsibilities did you assign to each?
+ An Owner has name, email. They can add pet, get tasks.
+ A Pet has name, species, breed, task. It can add task, remove task.
+ A Task has description, duration, priority.
+ A Scheduler has max time. It can generate plan or explain logic.

**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
For step 1 phase 5, I asked copilot to detect any missing relationships. It said that my Scheduler lacks input data, my generate_plan() returns None, and task status tracking is missing.
After re-implementation, task now has id and status. There's a new Plan dataclass that represents a scheduled care plan with a list of scheduled tasks and total duration tracking. Schedule accepts Ownder, so it knows what pets to schedule. Generate_plan() now has parameters and returns Plan. Remove_task() is also improved.
Update: I realized I jumped straight into the instructions on Phase 1, instead of reading the overall picture of what I'm suppose to implement, as showed on GitHub repo when I re-opened the assignment the next day. Therefore, I decided to ask Copilot to re-generate an UML diagram based on those instructions, and got a more detailed description of what I needed to implement.

---

    ## 2. Scheduling Logic and Tradeoffs

    **a. Constraints and priorities**

    - What constraints does your scheduler consider (for example: time, priority, preferences)?
    My scheduler considers 2 constraints:
    + Time: all activities must fit the duration given - time is given priority
    + Priority: (5 - highest, 1 - lowest): after time, tasks are ordered by priority
    - How did you decide which constraints mattered most?
    I thought the the most important constraint was time. No matter how important the tasks are, if they don't satisfy the amount of time required, it cannot be done. In real-world scenarios, User availability is the most important factor.

    **b. Tradeoffs**

    - Describe one tradeoff your scheduler makes.
A tradeoff for my scheduler would be: all the tasks are ordered to maximize all the time_duration given. In real life, it might not be possible because the assistants would need break time in the middle, or rest time, even if just for 2-5 minutes to switch between each task instead of continuous work.
    - Why is that tradeoff reasonable for this scenario?
The tradeoff is reasonable because we are working with computers instead of real human here. The schedule will act as a baseline for assistants to set out goals for tasks needed to be done during the day.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
+ UML diagram: asked it to explain why Scheduler "uses" Owner, why toString() method is only in the ScheduleItem class and not Task/Plan.
- What kinds of prompts or questions were most helpful?
"Based on my ... file, write these functions."
"From this instruction guide [paste it], implement them."
I think being short and straightforward helps a lot. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
For Phase 2 step 3, I prompted "Generate tests" to Copilot, and it wrote a 337-line file for me. I suppose I had to be more specific about the 2 methods I needed to test, so I Undo the Copilot suggestions and re-wrote the prompt.
- How did you evaluate or verify what the AI suggested?
I prompted Gemini to explain if what Copilot suggested was reasonable, but I didn't specify this code is written by AI so Gemini wouldn't know if those were human's or AI's mistakes.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
