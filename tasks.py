"""
tasks.py – Break down peer-feedback into actionable daily tasks.

Each review can be converted into one or more Task records.  A task has the
shape:
    {
        "id": "<uuid>",
        "review_id": "<uuid of the parent review>",
        "reviewee": "<name>",
        "description": "<what to do today>",
        "due_date": "<ISO-8601 date>",
        "status": "pending | in_progress | done",
        "created_date": "<ISO-8601 date>"
    }

Tasks are stored in tasks.json.
"""

import json
import uuid
from datetime import date, timedelta
from pathlib import Path

TASKS_FILE = Path("tasks.json")

# A simple keyword → suggested action mapping used by generate_tasks().
# In a real deployment this would be replaced by an LLM call or a richer
# rules engine.
_KEYWORD_ACTIONS: list[tuple[tuple[str, ...], str]] = [
    (
        ("communication", "communicate", "clarity", "clear", "explain"),
        "Write a concise summary of your current project status and share it with your team.",
    ),
    (
        ("technical", "code", "quality", "review", "refactor", "test"),
        "Spend 30 minutes reviewing and refactoring a section of code you own, focusing on readability.",
    ),
    (
        ("teamwork", "collaborate", "help", "support", "team"),
        "Pair with a colleague on a task today and offer / ask for help proactively.",
    ),
    (
        ("leadership", "lead", "mentor", "initiative", "decision"),
        "Identify one decision you can own end-to-end today and drive it to completion.",
    ),
    (
        ("deadline", "time", "punctual", "late", "delivery", "deliver"),
        "Block 90 minutes in your calendar today to work uninterrupted on your highest-priority item.",
    ),
    (
        ("feedback", "listen", "receptive", "open"),
        "Ask a colleague for one specific piece of feedback on recent work and document it.",
    ),
]
_DEFAULT_ACTION = "Reflect on the feedback you received and write down one concrete improvement for tomorrow."


def _load() -> list[dict]:
    """Return the persisted list of tasks (empty list if file doesn't exist)."""
    if TASKS_FILE.exists():
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    return []


def _save(tasks: list[dict]) -> None:
    """Persist the list of tasks to disk."""
    TASKS_FILE.write_text(json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8")


def _suggest_actions(feedback: str, category: str) -> list[str]:
    """Derive a short list of actionable descriptions from *feedback* text.

    The heuristic checks for keyword overlap between the feedback and a
    built-in keyword→action table.  It always returns at least one item.
    """
    feedback_lower = f"{feedback} {category}".lower()
    actions: list[str] = []
    for keywords, action in _KEYWORD_ACTIONS:
        if any(kw in feedback_lower for kw in keywords):
            actions.append(action)
    if not actions:
        actions.append(_DEFAULT_ACTION)
    return actions


def generate_tasks(review: dict, days_ahead: int = 1) -> list[dict]:
    """Convert a review record into one or more daily Task records.

    Generated tasks are persisted to *tasks.json* and also returned.

    Args:
        review: A review dict as produced by ``review.add_review()``.
        days_ahead: How many days from today to set as the due date
                    (default: 1 – due tomorrow).

    Returns:
        List of newly created task dicts.
    """
    due = date.today() + timedelta(days=days_ahead)
    actions = _suggest_actions(review["feedback"], review.get("category", "other"))

    new_tasks = [
        {
            "id": str(uuid.uuid4()),
            "review_id": review["id"],
            "reviewee": review["reviewee"],
            "description": action,
            "due_date": due.isoformat(),
            "status": "pending",
            "created_date": date.today().isoformat(),
        }
        for action in actions
    ]

    tasks = _load()
    tasks.extend(new_tasks)
    _save(tasks)
    return new_tasks


def list_tasks(reviewee: str | None = None, status: str | None = None) -> list[dict]:
    """Return tasks, optionally filtered by *reviewee* and/or *status*.

    Args:
        reviewee: When given, only tasks for this person are returned
                  (case-insensitive match).
        status: One of ``pending``, ``in_progress``, or ``done``.

    Returns:
        List of task dicts sorted by due date (earliest first).
    """
    tasks = _load()
    if reviewee:
        tasks = [t for t in tasks if t["reviewee"].lower() == reviewee.lower()]
    if status:
        tasks = [t for t in tasks if t["status"] == status.lower()]
    return sorted(tasks, key=lambda t: t["due_date"])


def update_task_status(task_id: str, new_status: str) -> dict | None:
    """Update the status of a task identified by *task_id*.

    Args:
        task_id: UUID of the task to update.
        new_status: One of ``pending``, ``in_progress``, or ``done``.

    Returns:
        The updated task dict, or *None* if no task with that id was found.

    Raises:
        ValueError: If *new_status* is not a recognised status value.
    """
    valid_statuses = {"pending", "in_progress", "done"}
    new_status = new_status.lower().strip()
    if new_status not in valid_statuses:
        raise ValueError(
            f"Invalid status '{new_status}'. Must be one of: {', '.join(sorted(valid_statuses))}"
        )

    tasks = _load()
    updated = None
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            updated = task
            break

    if updated:
        _save(tasks)
    return updated
