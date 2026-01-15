#!/usr/bin/env python3
"""ASN Memo - Network AS Number Flash Card Application.

A TUI flash card application for memorizing Autonomous System (AS) numbers
and facts about major Internet networks, grouped by tier.

Usage:
    python main.py

Controls:
    - Space: Reveal answer
    - 1-4: Rate difficulty (Again/Hard/Good/Easy)
    - Escape: Go back
    - Q: Quit
"""

from app import ASNMemoApp


def main() -> None:
    """Run the ASN Memo application."""
    app = ASNMemoApp()
    app.run()


if __name__ == "__main__":
    main()
