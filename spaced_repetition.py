"""SM-2 Spaced Repetition Algorithm implementation."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Optional


class Rating(IntEnum):
    """User self-assessment ratings for card reviews."""
    AGAIN = 0   # Complete blackout, need to relearn
    HARD = 2    # Incorrect response, but upon seeing answer, remembered
    GOOD = 3    # Correct response with some difficulty
    EASY = 5    # Perfect response with no hesitation


@dataclass
class CardState:
    """Tracks the learning state of a single flash card."""
    card_id: str
    ease_factor: float = 2.5  # Initial ease factor (2.5 is SM-2 default)
    interval: int = 0         # Days until next review
    repetitions: int = 0      # Count of consecutive correct responses
    next_review: datetime = field(default_factory=datetime.now)
    last_reviewed: Optional[datetime] = None

    def is_due(self) -> bool:
        """Check if this card is due for review."""
        return datetime.now() >= self.next_review

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "card_id": self.card_id,
            "ease_factor": self.ease_factor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review": self.next_review.isoformat(),
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CardState":
        """Create CardState from dictionary."""
        return cls(
            card_id=data["card_id"],
            ease_factor=data["ease_factor"],
            interval=data["interval"],
            repetitions=data["repetitions"],
            next_review=datetime.fromisoformat(data["next_review"]),
            last_reviewed=datetime.fromisoformat(data["last_reviewed"]) if data.get("last_reviewed") else None,
        )


def sm2_algorithm(state: CardState, rating: Rating) -> CardState:
    """
    Apply the SM-2 algorithm to update card state based on user rating.

    The SM-2 algorithm works as follows:
    1. If rating >= 3 (correct response):
       - If repetitions == 0: interval = 1 day
       - If repetitions == 1: interval = 6 days
       - If repetitions > 1: interval = interval * ease_factor
       - Increment repetitions
    2. If rating < 3 (incorrect response):
       - Reset repetitions to 0
       - Set interval to 1 day (relearn from start)
    3. Update ease factor:
       EF' = EF + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
       Minimum ease factor is 1.3

    Args:
        state: Current card state
        rating: User's self-assessment rating

    Returns:
        New CardState with updated values
    """
    # Calculate new ease factor
    # Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    rating_value = int(rating)
    new_ease = state.ease_factor + (0.1 - (5 - rating_value) * (0.08 + (5 - rating_value) * 0.02))
    new_ease = max(1.3, new_ease)  # Minimum ease factor is 1.3

    if rating >= Rating.GOOD:  # Correct response (3+)
        if state.repetitions == 0:
            new_interval = 1
        elif state.repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(state.interval * state.ease_factor)
        new_repetitions = state.repetitions + 1
    else:  # Incorrect response (0-2)
        new_repetitions = 0
        new_interval = 1

    new_next_review = datetime.now() + timedelta(days=new_interval)

    return CardState(
        card_id=state.card_id,
        ease_factor=new_ease,
        interval=new_interval,
        repetitions=new_repetitions,
        next_review=new_next_review,
        last_reviewed=datetime.now(),
    )


class Scheduler:
    """Manages card scheduling for study sessions."""

    def __init__(self, card_states: dict[str, CardState]):
        """
        Initialize scheduler with existing card states.

        Args:
            card_states: Dictionary mapping card IDs to their states
        """
        self.card_states = card_states

    def get_due_cards(self) -> list[str]:
        """
        Get list of card IDs that are due for review.

        Returns:
            List of card IDs due for review, sorted by next_review date
        """
        due = [
            (card_id, state)
            for card_id, state in self.card_states.items()
            if state.is_due()
        ]
        # Sort by next_review date (oldest first)
        due.sort(key=lambda x: x[1].next_review)
        return [card_id for card_id, _ in due]

    def get_new_cards(self, all_card_ids: list[str], limit: int = 10) -> list[str]:
        """
        Get new cards that haven't been studied yet.

        Args:
            all_card_ids: List of all available card IDs
            limit: Maximum number of new cards to return

        Returns:
            List of new card IDs (up to limit)
        """
        studied = set(self.card_states.keys())
        new_cards = [cid for cid in all_card_ids if cid not in studied]
        return new_cards[:limit]

    def review_card(self, card_id: str, rating: Rating) -> CardState:
        """
        Process a card review and update its state.

        Args:
            card_id: The card ID being reviewed
            rating: User's self-assessment rating

        Returns:
            Updated CardState
        """
        current_state = self.card_states.get(
            card_id,
            CardState(card_id=card_id)
        )
        new_state = sm2_algorithm(current_state, rating)
        self.card_states[card_id] = new_state
        return new_state

    def get_state(self, card_id: str) -> Optional[CardState]:
        """Get the current state of a card."""
        return self.card_states.get(card_id)

    def get_statistics(self) -> dict:
        """
        Calculate study statistics.

        Returns:
            Dictionary with statistics about learning progress
        """
        if not self.card_states:
            return {
                "total_studied": 0,
                "due_today": 0,
                "mastered": 0,
                "learning": 0,
                "average_ease": 0.0,
            }

        due_count = sum(1 for s in self.card_states.values() if s.is_due())
        mastered = sum(1 for s in self.card_states.values() if s.repetitions >= 3)
        learning = len(self.card_states) - mastered
        avg_ease = sum(s.ease_factor for s in self.card_states.values()) / len(self.card_states)

        return {
            "total_studied": len(self.card_states),
            "due_today": due_count,
            "mastered": mastered,
            "learning": learning,
            "average_ease": round(avg_ease, 2),
        }
