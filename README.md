# PerformanceReviewSystem

A lightweight, command-line **peer-performance review system** that turns free-text feedback into concrete, day-by-day improvement tasks and lets you track progress over time.

---

## Table of Contents

1. [Overview](#overview)
2. [How It Works](#how-it-works)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [Quick Start](#quick-start)
6. [Usage](#usage)
   - [Add a Review](#add-a-review)
   - [List Reviews](#list-reviews)
   - [Generate Daily Tasks](#generate-daily-tasks)
   - [List Tasks](#list-tasks)
   - [Update a Task's Status](#update-a-tasks-status)
   - [Progress Report](#progress-report)
7. [Data Storage](#data-storage)
8. [Feedback Categories](#feedback-categories)
9. [Task Statuses](#task-statuses)
10. [End-to-End Example](#end-to-end-example)

---

## Overview

Getting peer feedback is valuable — but feedback alone rarely changes behaviour.
The **PerformanceReviewSystem** bridges the gap between *receiving* feedback and
*acting on it* by:

1. **Storing** structured peer reviews (who gave feedback, about whom, on which topic).
2. **Analysing** the free-text feedback to identify the most relevant improvement
   actions using a keyword-based rules engine.
3. **Generating** one or more small, achievable daily tasks from each review so that
   the reviewee has a clear to-do list rather than vague advice.
4. **Tracking** task completion and surfacing overdue items in a plain-English
   progress report.

---

## How It Works

```
Peer gives feedback
        │
        ▼
  add-review command
  ─────────────────
  Stores a review record in reviews.json
  (reviewee, reviewer, date, feedback text, category)
        │
        ▼
  generate-tasks command
  ──────────────────────
  Analyses the feedback text for keywords
  (e.g. "communicate", "refactor", "deadline")
  Maps keywords → concrete daily actions
  Writes task records to tasks.json with a due date
        │
        ▼
  reviewee works through their tasks
  ───────────────────────────────────
  update-task --status in_progress / done
        │
        ▼
  report command
  ──────────────
  Displays totals (pending / in-progress / done),
  completion percentage, and any overdue tasks
```

---

## Project Structure

```
PerformanceReviewSystem/
├── main.py       # CLI entry point – parses arguments and dispatches commands
├── review.py     # Add, list, retrieve, and delete peer-review records
├── tasks.py      # Generate daily tasks from a review; list and update tasks
├── tracker.py    # Build and format progress reports for a reviewee
├── reviews.json  # Auto-created at runtime – stores review records
└── tasks.json    # Auto-created at runtime – stores task records
```

| File | Responsibility |
|------|---------------|
| `review.py` | CRUD operations on review records persisted to `reviews.json` |
| `tasks.py` | Keyword-based task generation; task status management in `tasks.json` |
| `tracker.py` | Aggregation and formatting of task progress for a given reviewee |
| `main.py` | `argparse`-based CLI that ties all three modules together |

---

## Requirements

- Python **3.10** or later (uses the `X | Y` union type hint syntax)
- No third-party dependencies – the standard library is sufficient

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/davidmukiibi/PerformanceReviewSystem.git
cd PerformanceReviewSystem

# Run the help menu
python main.py --help
```

---

## Usage

All commands are run through `main.py`.

```
python main.py <command> [options]
```

### Add a Review

Record a piece of peer feedback about someone.

```bash
python main.py add-review \
  --reviewee "Alice" \
  --reviewer "Bob" \
  --feedback "Alice communicates clearly in stand-ups but her pull requests lack inline comments." \
  --category technical
```

**Options**

| Flag | Required | Description |
|------|----------|-------------|
| `--reviewee` | ✔ | Name of the person being reviewed |
| `--reviewer` | ✔ | Name of the person giving the feedback |
| `--feedback` | ✔ | Free-text feedback |
| `--category` | optional | One of the [feedback categories](#feedback-categories) (default: `other`) |

The command prints the new review's UUID — keep it for the `generate-tasks` step.

---

### List Reviews

```bash
# All reviews
python main.py list-reviews

# Only reviews about Alice
python main.py list-reviews --reviewee "Alice"
```

---

### Generate Daily Tasks

Convert a review into one or more actionable tasks due tomorrow (or in N days).

```bash
python main.py generate-tasks --review-id <uuid>

# Set tasks due in 3 days instead
python main.py generate-tasks --review-id <uuid> --days-ahead 3
```

The system analyses the feedback text for keywords and maps them to specific,
time-boxed actions (e.g. *"Spend 30 minutes reviewing and refactoring a section of
code you own"*).  At least one task is always generated.

---

### List Tasks

```bash
# All tasks
python main.py list-tasks

# Pending tasks for Alice
python main.py list-tasks --reviewee "Alice" --status pending
```

**Status filter values:** `pending`, `in_progress`, `done`

---

### Update a Task's Status

```bash
python main.py update-task --task-id <uuid> --status in_progress
python main.py update-task --task-id <uuid> --status done
```

---

### Progress Report

Display a summary of all tasks for a person, including completion rate and
any overdue items.

```bash
python main.py report --reviewee "Alice"
```

**Sample output**

```
Progress Report – Alice
Date            : 2026-04-08
────────────────────────────────────────
Total tasks     : 3
  Pending       : 1
  In progress   : 1
  Done          : 1
Completion      : 33.3%

⚠  Overdue tasks (1):
   • [2026-04-07] Ask a colleague for one specific piece of feedback on recent work and document it.
```

---

## Data Storage

Reviews and tasks are stored as plain JSON files in the working directory:

| File | Contents |
|------|----------|
| `reviews.json` | Array of review objects (id, reviewee, reviewer, date, feedback, category) |
| `tasks.json` | Array of task objects (id, review_id, reviewee, description, due_date, status, created_date) |

These files are created automatically on first use.  They can be committed to
version control, backed up, or migrated to a database without changing the
application logic.

---

## Feedback Categories

| Category | Typical focus area |
|----------|--------------------|
| `communication` | Clarity, written/verbal communication, active listening |
| `technical` | Code quality, testing, architecture, documentation |
| `teamwork` | Collaboration, helping colleagues, cross-functional work |
| `leadership` | Initiative, decision-making, mentoring, ownership |
| `other` | Anything that doesn't fit the above buckets |

---

## Task Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Task created but not yet started |
| `in_progress` | Reviewee is actively working on it |
| `done` | Task completed |

---

## End-to-End Example

```bash
# 1. Bob gives Alice feedback on her technical skills
python main.py add-review \
  --reviewee "Alice" \
  --reviewer "Bob" \
  --feedback "Alice writes clean code but rarely adds inline comments or tests." \
  --category technical
# → Review added (id: a1b2c3d4-...)

# 2. Generate daily tasks from that review
python main.py generate-tasks --review-id a1b2c3d4-...
# → 1 task(s) generated:
#   [{
#     "description": "Spend 30 minutes reviewing and refactoring a section of code...",
#     "due_date": "2026-04-09",
#     "status": "pending",
#     ...
#   }]

# 3. Alice starts working on the task
python main.py update-task --task-id <task-uuid> --status in_progress

# 4. Alice finishes the task
python main.py update-task --task-id <task-uuid> --status done

# 5. Check Alice's overall progress
python main.py report --reviewee "Alice"
# → Progress Report – Alice
#   Date            : 2026-04-09
#   ────────────────────────────────────────
#   Total tasks     : 1
#     Pending       : 0
#     In progress   : 0
#     Done          : 1
#   Completion      : 100.0%
```
