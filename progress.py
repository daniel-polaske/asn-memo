"""Persistence layer for saving and loading user progress."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from spaced_repetition import CardState

DEFAULT_PROGRESS_DIR = Path.home() / ".asn-memo"
DEFAULT_PROGRESS_FILE = DEFAULT_PROGRESS_DIR / "progress.json"


class ProgressManager:
    """Manages persistence of learning progress to JSON file."""

    def __init__(self, filepath: Optional[Path] = None):
        """
        Initialize the progress manager.

        Args:
            filepath: Optional custom path for progress file.
                     Defaults to ~/.asn-memo/progress.json
        """
        self.filepath = filepath or DEFAULT_PROGRESS_FILE
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, CardState]:
        """
        Load progress from JSON file.

        Returns:
            Dictionary mapping card IDs to CardState objects
        """
        if not self.filepath.exists():
            return {}

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

        card_states = {}
        for card_id, state_data in data.get("cards", {}).items():
            try:
                state_data["card_id"] = card_id
                card_states[card_id] = CardState.from_dict(state_data)
            except (KeyError, ValueError):
                # Skip invalid entries
                continue

        return card_states

    def save(self, card_states: dict[str, CardState]) -> None:
        """
        Save progress to JSON file.

        Args:
            card_states: Dictionary mapping card IDs to CardState objects
        """
        data = {
            "version": 1,
            "last_saved": datetime.now().isoformat(),
            "cards": {},
        }

        for card_id, state in card_states.items():
            state_dict = state.to_dict()
            # Remove card_id from nested dict since it's the key
            del state_dict["card_id"]
            data["cards"][card_id] = state_dict

        # Write to temp file first, then rename for atomicity
        temp_file = self.filepath.with_suffix(".tmp")
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=2)
        temp_file.rename(self.filepath)

    def reset(self) -> None:
        """Delete all progress."""
        if self.filepath.exists():
            self.filepath.unlink()

    def exists(self) -> bool:
        """Check if progress file exists."""
        return self.filepath.exists()
