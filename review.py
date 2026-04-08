"""
review.py – Collect and persist peer-performance feedback.

A "review" is a JSON record stored in reviews.json with the shape:
    {
        "id": "<uuid>",
        "reviewee": "<name>",
        "reviewer": "<name>",
        "date": "<ISO-8601 date>",
        "feedback": "<free-text feedback>",
        "category": "<one of: communication | technical | teamwork | leadership | other>"
    }
"""

import json
import uuid
from datetime import date
from pathlib import Path

REVIEWS_FILE = Path("reviews.json")
VALID_CATEGORIES = {"communication", "technical", "teamwork", "leadership", "other"}


def _load() -> list[dict]:
    """Return the persisted list of reviews (empty list if file doesn't exist)."""
    if REVIEWS_FILE.exists():
        return json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
    return []


def _save(reviews: list[dict]) -> None:
    """Persist the list of reviews to disk."""
    REVIEWS_FILE.write_text(json.dumps(reviews, indent=2, ensure_ascii=False), encoding="utf-8")


def add_review(reviewee: str, reviewer: str, feedback: str, category: str = "other") -> dict:
    """Create a new feedback record and append it to the data store.

    Args:
        reviewee: Name of the person being reviewed.
        reviewer: Name of the person giving the review.
        feedback: Free-text performance feedback.
        category: One of the VALID_CATEGORIES; defaults to "other".

    Returns:
        The newly created review record (dict).

    Raises:
        ValueError: If *category* is not one of the accepted values.
    """
    category = category.lower().strip()
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category '{category}'. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    record = {
        "id": str(uuid.uuid4()),
        "reviewee": reviewee.strip(),
        "reviewer": reviewer.strip(),
        "date": date.today().isoformat(),
        "feedback": feedback.strip(),
        "category": category,
    }

    reviews = _load()
    reviews.append(record)
    _save(reviews)
    return record


def list_reviews(reviewee: str | None = None) -> list[dict]:
    """Return all reviews, optionally filtered by *reviewee* name.

    Args:
        reviewee: When given, only reviews for this person are returned
                  (case-insensitive match).

    Returns:
        List of review dicts, sorted by date (oldest first).
    """
    reviews = _load()
    if reviewee:
        reviewee_lower = reviewee.lower()
        reviews = [r for r in reviews if r["reviewee"].lower() == reviewee_lower]
    return sorted(reviews, key=lambda r: r["date"])


def get_review(review_id: str) -> dict | None:
    """Return a single review by its UUID, or *None* if not found."""
    for review in _load():
        if review["id"] == review_id:
            return review
    return None


def delete_review(review_id: str) -> bool:
    """Remove a review by its UUID.

    Returns:
        True if the review was found and deleted; False otherwise.
    """
    reviews = _load()
    new_reviews = [r for r in reviews if r["id"] != review_id]
    if len(new_reviews) == len(reviews):
        return False
    _save(new_reviews)
    return True
