"""
tracker.py – Progress tracking and summary reporting.

Aggregates task data for a given reviewee and produces a plain-text or
dict-based progress report so that both humans (via the CLI) and automated
pipelines can consume it.
"""

from datetime import date

from tasks import list_tasks


def progress_report(reviewee: str) -> dict:
    """Build a progress summary for *reviewee*.

    Returns a dict with the following keys:
        reviewee    – name of the person
        report_date – today's ISO date
        total       – total number of tasks
        pending     – number of tasks with status "pending"
        in_progress – number of tasks with status "in_progress"
        done        – number of tasks with status "done"
        completion  – completion percentage (done / total * 100), or 0 if no tasks
        overdue     – tasks whose due_date is in the past and status != "done"
    """
    all_tasks = list_tasks(reviewee=reviewee)
    today = date.today().isoformat()

    pending = [t for t in all_tasks if t["status"] == "pending"]
    in_progress = [t for t in all_tasks if t["status"] == "in_progress"]
    done = [t for t in all_tasks if t["status"] == "done"]
    overdue = [
        t for t in all_tasks if t["due_date"] < today and t["status"] != "done"
    ]

    total = len(all_tasks)
    completion = round(len(done) / total * 100, 1) if total else 0.0

    return {
        "reviewee": reviewee,
        "report_date": today,
        "total": total,
        "pending": len(pending),
        "in_progress": len(in_progress),
        "done": len(done),
        "completion": completion,
        "overdue": overdue,
    }


def format_report(report: dict) -> str:
    """Render a progress *report* dict as a human-readable string."""
    lines = [
        f"Progress Report – {report['reviewee']}",
        f"Date            : {report['report_date']}",
        "─" * 40,
        f"Total tasks     : {report['total']}",
        f"  Pending       : {report['pending']}",
        f"  In progress   : {report['in_progress']}",
        f"  Done          : {report['done']}",
        f"Completion      : {report['completion']}%",
    ]
    if report["overdue"]:
        lines.append(f"\n⚠  Overdue tasks ({len(report['overdue'])}):")
        for task in report["overdue"]:
            lines.append(f"   • [{task['due_date']}] {task['description']}")
    return "\n".join(lines)
