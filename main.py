"""
main.py – Command-line interface for the Performance Review System.

Usage examples
--------------
Add a review:
    python main.py add-review --reviewee "Alice" --reviewer "Bob" \\
        --feedback "Alice communicates well but should improve code review quality." \\
        --category technical

List reviews for a person:
    python main.py list-reviews --reviewee "Alice"

Generate tasks from a review:
    python main.py generate-tasks --review-id <uuid>

List tasks (optionally filter by person / status):
    python main.py list-tasks --reviewee "Alice" --status pending

Update a task's status:
    python main.py update-task --task-id <uuid> --status in_progress

Show progress report:
    python main.py report --reviewee "Alice"
"""

import argparse
import json
import sys

import review as review_module
import tasks as tasks_module
import tracker as tracker_module


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _print_json(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _abort(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Command handlers
# ──────────────────────────────────────────────────────────────────────────────

def cmd_add_review(args: argparse.Namespace) -> None:
    try:
        record = review_module.add_review(
            reviewee=args.reviewee,
            reviewer=args.reviewer,
            feedback=args.feedback,
            category=args.category,
        )
    except ValueError as exc:
        _abort(str(exc))
    print(f"Review added (id: {record['id']})")
    _print_json(record)


def cmd_list_reviews(args: argparse.Namespace) -> None:
    reviews = review_module.list_reviews(reviewee=args.reviewee)
    if not reviews:
        print("No reviews found.")
        return
    _print_json(reviews)


def cmd_generate_tasks(args: argparse.Namespace) -> None:
    rec = review_module.get_review(args.review_id)
    if rec is None:
        _abort(f"No review with id '{args.review_id}' found.")
    new_tasks = tasks_module.generate_tasks(rec, days_ahead=args.days_ahead)
    print(f"{len(new_tasks)} task(s) generated:")
    _print_json(new_tasks)


def cmd_list_tasks(args: argparse.Namespace) -> None:
    task_list = tasks_module.list_tasks(reviewee=args.reviewee, status=args.status)
    if not task_list:
        print("No tasks found.")
        return
    _print_json(task_list)


def cmd_update_task(args: argparse.Namespace) -> None:
    try:
        updated = tasks_module.update_task_status(args.task_id, args.status)
    except ValueError as exc:
        _abort(str(exc))
    if updated is None:
        _abort(f"No task with id '{args.task_id}' found.")
    print(f"Task updated (id: {updated['id']}, status: {updated['status']})")


def cmd_report(args: argparse.Namespace) -> None:
    report = tracker_module.progress_report(args.reviewee)
    print(tracker_module.format_report(report))


# ──────────────────────────────────────────────────────────────────────────────
# Argument parser
# ──────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="performance-review",
        description="Peer Performance Review System – turn feedback into daily actions.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-review
    p_add = sub.add_parser("add-review", help="Record a new piece of peer feedback.")
    p_add.add_argument("--reviewee", required=True, help="Name of the person being reviewed.")
    p_add.add_argument("--reviewer", required=True, help="Name of the person giving feedback.")
    p_add.add_argument("--feedback", required=True, help="Free-text feedback.")
    p_add.add_argument(
        "--category",
        default="other",
        choices=sorted(review_module.VALID_CATEGORIES),
        help="Feedback category (default: other).",
    )

    # list-reviews
    p_lr = sub.add_parser("list-reviews", help="List recorded reviews.")
    p_lr.add_argument("--reviewee", default=None, help="Filter by reviewee name.")

    # generate-tasks
    p_gt = sub.add_parser("generate-tasks", help="Generate daily tasks from a review.")
    p_gt.add_argument("--review-id", required=True, dest="review_id", help="UUID of the review.")
    p_gt.add_argument(
        "--days-ahead",
        type=int,
        default=1,
        dest="days_ahead",
        help="Days until the tasks are due (default: 1).",
    )

    # list-tasks
    p_lt = sub.add_parser("list-tasks", help="List tasks.")
    p_lt.add_argument("--reviewee", default=None, help="Filter by reviewee name.")
    p_lt.add_argument(
        "--status",
        default=None,
        choices=["pending", "in_progress", "done"],
        help="Filter by task status.",
    )

    # update-task
    p_ut = sub.add_parser("update-task", help="Update the status of a task.")
    p_ut.add_argument("--task-id", required=True, dest="task_id", help="UUID of the task.")
    p_ut.add_argument(
        "--status",
        required=True,
        choices=["pending", "in_progress", "done"],
        help="New status.",
    )

    # report
    p_rep = sub.add_parser("report", help="Display a progress report for a person.")
    p_rep.add_argument("--reviewee", required=True, help="Name of the person.")

    return parser


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

_COMMAND_MAP = {
    "add-review": cmd_add_review,
    "list-reviews": cmd_list_reviews,
    "generate-tasks": cmd_generate_tasks,
    "list-tasks": cmd_list_tasks,
    "update-task": cmd_update_task,
    "report": cmd_report,
}


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handler = _COMMAND_MAP.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)
    handler(args)


if __name__ == "__main__":
    main()
