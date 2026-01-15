"""ASN Memo TUI Application using Textual."""

from typing import Optional

from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import (
    Header,
    Footer,
    Button,
    Static,
    Label,
    ListView,
    ListItem,
    DataTable,
    ProgressBar,
)
from textual.containers import Container, Vertical, Horizontal, Center
from textual.binding import Binding

from data import NETWORKS, Network, Tier, get_networks_by_tier
from spaced_repetition import Scheduler, Rating, CardState
from progress import ProgressManager


class MainMenuScreen(Screen):
    """Main menu with navigation options."""

    BINDINGS = [
        Binding("s", "study", "Study"),
        Binding("b", "browse", "Browse"),
        Binding("t", "stats", "Statistics"),
        Binding("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("ASN Memo", id="title"),
            Static("Master Network AS Numbers", id="subtitle"),
            Vertical(
                Button("Study Due Cards [S]", id="study", variant="primary"),
                Button("Browse All Cards [B]", id="browse", variant="default"),
                Button("View Statistics [T]", id="stats", variant="default"),
                Button("Reset Progress", id="reset", variant="warning"),
                Button("Quit [Q]", id="quit", variant="error"),
                id="menu-buttons",
            ),
            id="main-container",
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "study":
            self.action_study()
        elif event.button.id == "browse":
            self.action_browse()
        elif event.button.id == "stats":
            self.action_stats()
        elif event.button.id == "reset":
            self.app.push_screen(ResetConfirmScreen())
        elif event.button.id == "quit":
            self.app.exit()

    def action_study(self) -> None:
        self.app.push_screen(StudyScreen())

    def action_browse(self) -> None:
        self.app.push_screen(BrowseScreen())

    def action_stats(self) -> None:
        self.app.push_screen(StatisticsScreen())

    def action_quit(self) -> None:
        self.app.exit()


class StudyScreen(Screen):
    """Flash card study session screen."""

    BINDINGS = [
        Binding("space", "reveal", "Reveal Answer", show=True),
        Binding("1", "rate_again", "Again", show=True),
        Binding("2", "rate_hard", "Hard", show=True),
        Binding("3", "rate_good", "Good", show=True),
        Binding("4", "rate_easy", "Easy", show=True),
        Binding("escape", "back", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.current_card: Optional[Network] = None
        self.cards_to_study: list[Network] = []
        self.cards_completed = 0
        self.total_cards = 0
        self.revealed = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Study Session", id="study-title"),
            ProgressBar(total=100, show_eta=False, id="progress"),
            Static("Loading...", id="progress-text"),
            Container(
                Static("", id="card-tier", classes="card-tier"),
                Static("", id="card-name", classes="card-name"),
                Static("", id="card-hq", classes="card-hq"),
                Static("What is the AS Number?", id="card-question"),
                Container(
                    Static("", id="card-answer", classes="card-answer"),
                    Static("", id="card-specialization"),
                    Static("", id="card-facts"),
                    id="answer-container",
                    classes="hidden",
                ),
                id="card-container",
            ),
            Container(
                Button("Reveal Answer [Space]", id="reveal-btn", variant="primary"),
                id="action-buttons",
            ),
            Horizontal(
                Button("Again [1]", id="again-btn", variant="error"),
                Button("Hard [2]", id="hard-btn", variant="warning"),
                Button("Good [3]", id="good-btn", variant="success"),
                Button("Easy [4]", id="easy-btn", variant="primary"),
                id="rating-buttons",
                classes="hidden",
            ),
            id="study-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        self._load_study_session()
        self._show_next_card()

    def _load_study_session(self) -> None:
        """Load cards due for review plus new cards."""
        scheduler = self.app.scheduler

        # Get due cards
        due_ids = scheduler.get_due_cards()
        due_networks = [n for n in NETWORKS if str(n.asn) in due_ids]

        # Get new cards (limit 10 per session)
        all_ids = [str(n.asn) for n in NETWORKS]
        new_ids = scheduler.get_new_cards(all_ids, limit=10)
        new_networks = [n for n in NETWORKS if str(n.asn) in new_ids]

        self.cards_to_study = due_networks + new_networks
        self.total_cards = len(self.cards_to_study)

    def _show_next_card(self) -> None:
        """Display the next card in the study session."""
        if not self.cards_to_study:
            self._end_session()
            return

        self.current_card = self.cards_to_study.pop(0)
        self.revealed = False

        # Update card display
        self.query_one("#card-tier", Static).update(f"[{self.current_card.tier.value}]")
        self.query_one("#card-name", Static).update(self.current_card.name)
        self.query_one("#card-hq", Static).update(self.current_card.headquarters)
        self.query_one("#card-answer", Static).update(f"AS{self.current_card.asn}")
        self.query_one("#card-specialization", Static).update(
            self.current_card.specialization or ""
        )

        facts_text = "\n".join(f"  - {fact}" for fact in self.current_card.facts)
        self.query_one("#card-facts", Static).update(facts_text)

        # Hide answer, show reveal button
        self.query_one("#answer-container").add_class("hidden")
        self.query_one("#rating-buttons").add_class("hidden")
        self.query_one("#action-buttons").remove_class("hidden")

        # Update progress
        if self.total_cards > 0:
            progress = (self.cards_completed / self.total_cards) * 100
            self.query_one("#progress", ProgressBar).update(progress=progress)
            self.query_one("#progress-text", Static).update(
                f"Card {self.cards_completed + 1} of {self.total_cards}"
            )

    def action_reveal(self) -> None:
        """Reveal the answer."""
        if self.revealed or not self.current_card:
            return

        self.revealed = True
        self.query_one("#answer-container").remove_class("hidden")
        self.query_one("#rating-buttons").remove_class("hidden")
        self.query_one("#action-buttons").add_class("hidden")

    def _rate_card(self, rating: Rating) -> None:
        """Process user rating and move to next card."""
        if not self.current_card or not self.revealed:
            return

        # Update spaced repetition state
        card_id = str(self.current_card.asn)
        self.app.scheduler.review_card(card_id, rating)
        self.app.save_progress()

        self.cards_completed += 1
        self._show_next_card()

    def action_rate_again(self) -> None:
        if self.revealed:
            self._rate_card(Rating.AGAIN)

    def action_rate_hard(self) -> None:
        if self.revealed:
            self._rate_card(Rating.HARD)

    def action_rate_good(self) -> None:
        if self.revealed:
            self._rate_card(Rating.GOOD)

    def action_rate_easy(self) -> None:
        if self.revealed:
            self._rate_card(Rating.EASY)

    def _end_session(self) -> None:
        """Display session complete message."""
        # Hide card elements
        try:
            self.query_one("#card-container").add_class("hidden")
            self.query_one("#action-buttons").add_class("hidden")
            self.query_one("#rating-buttons").add_class("hidden")
            self.query_one("#progress").add_class("hidden")
        except Exception:
            pass

        self.query_one("#progress-text", Static).update("")
        self.query_one("#study-title", Static).update("Session Complete!")

        # Mount completion message
        container = self.query_one("#study-container")
        container.mount(
            Container(
                Static(f"Cards reviewed: {self.cards_completed}", id="complete-stats"),
                Static("Great work! Keep practicing.", id="complete-message"),
                Button("Return to Menu", id="return-btn", variant="primary"),
                id="complete-container",
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "reveal-btn":
            self.action_reveal()
        elif button_id == "again-btn":
            self.action_rate_again()
        elif button_id == "hard-btn":
            self.action_rate_hard()
        elif button_id == "good-btn":
            self.action_rate_good()
        elif button_id == "easy-btn":
            self.action_rate_easy()
        elif button_id == "return-btn":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()


class BrowseScreen(Screen):
    """Browse all cards grouped by tier."""

    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("1", "tier1", "Tier 1"),
        Binding("2", "tier2", "Tier 2"),
        Binding("3", "tier3", "Tier 3"),
        Binding("4", "cdn", "CDN"),
        Binding("5", "cloud", "Cloud"),
        Binding("6", "ixp", "IXP"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Browse Networks", id="browse-title"),
            Horizontal(
                ListView(
                    ListItem(Label("Tier 1 Networks [1]"), id="tier1"),
                    ListItem(Label("Tier 2 Networks [2]"), id="tier2"),
                    ListItem(Label("Tier 3 Networks [3]"), id="tier3"),
                    ListItem(Label("CDN Providers [4]"), id="cdn"),
                    ListItem(Label("Cloud Providers [5]"), id="cloud"),
                    ListItem(Label("Internet Exchanges [6]"), id="ixp"),
                    id="tier-list",
                ),
                Container(
                    DataTable(id="network-table"),
                    id="network-container",
                ),
                id="browse-layout",
            ),
            id="browse-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#network-table", DataTable)
        table.add_columns("ASN", "Name", "Headquarters", "Specialization")
        table.cursor_type = "row"
        self._show_tier(Tier.TIER_1)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        tier_map = {
            "tier1": Tier.TIER_1,
            "tier2": Tier.TIER_2,
            "tier3": Tier.TIER_3,
            "cdn": Tier.CDN,
            "cloud": Tier.CLOUD,
            "ixp": Tier.IXP,
        }
        tier = tier_map.get(event.item.id)
        if tier:
            self._show_tier(tier)

    def _show_tier(self, tier: Tier) -> None:
        """Display networks for selected tier."""
        table = self.query_one("#network-table", DataTable)
        table.clear()

        networks = get_networks_by_tier(tier)
        for network in networks:
            table.add_row(
                f"AS{network.asn}",
                network.name,
                network.headquarters or "-",
                network.specialization or "-",
            )

    def action_tier1(self) -> None:
        self._show_tier(Tier.TIER_1)

    def action_tier2(self) -> None:
        self._show_tier(Tier.TIER_2)

    def action_tier3(self) -> None:
        self._show_tier(Tier.TIER_3)

    def action_cdn(self) -> None:
        self._show_tier(Tier.CDN)

    def action_cloud(self) -> None:
        self._show_tier(Tier.CLOUD)

    def action_ixp(self) -> None:
        self._show_tier(Tier.IXP)

    def action_back(self) -> None:
        self.app.pop_screen()


class StatisticsScreen(Screen):
    """Display learning statistics."""

    BINDINGS = [
        Binding("escape", "back", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Learning Statistics", id="stats-title"),
            Container(
                Static("", id="total-networks"),
                Static("", id="total-studied"),
                Static("", id="due-today"),
                Static("", id="mastered"),
                Static("", id="learning"),
                Static("", id="avg-ease"),
                id="stats-box",
            ),
            Button("Back to Menu", id="back-btn", variant="primary"),
            id="statistics-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        stats = self.app.scheduler.get_statistics()
        total_networks = len(NETWORKS)

        self.query_one("#total-networks", Static).update(
            f"Total Networks in Database: {total_networks}"
        )
        self.query_one("#total-studied", Static).update(
            f"Cards Studied: {stats['total_studied']} / {total_networks}"
        )
        self.query_one("#due-today", Static).update(
            f"Due for Review: {stats['due_today']}"
        )
        self.query_one("#mastered", Static).update(
            f"Mastered (3+ correct reviews): {stats['mastered']}"
        )
        self.query_one("#learning", Static).update(
            f"Still Learning: {stats['learning']}"
        )
        self.query_one("#avg-ease", Static).update(
            f"Average Ease Factor: {stats['average_ease']}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()

    def action_back(self) -> None:
        self.app.pop_screen()


class ResetConfirmScreen(ModalScreen):
    """Confirmation dialog for resetting progress."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("y", "confirm", "Confirm"),
        Binding("n", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Reset Progress?", id="reset-title"),
            Static(
                "This will delete ALL your learning progress.\nThis action cannot be undone.",
                id="reset-warning",
            ),
            Horizontal(
                Button("Cancel [N]", id="cancel-btn", variant="default"),
                Button("Reset [Y]", id="confirm-btn", variant="error"),
                id="reset-buttons",
            ),
            id="reset-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-btn":
            self.action_cancel()
        elif event.button.id == "confirm-btn":
            self.action_confirm()

    def action_cancel(self) -> None:
        self.app.pop_screen()

    def action_confirm(self) -> None:
        self.app.progress_manager.reset()
        self.app.card_states = {}
        self.app.scheduler = Scheduler({})
        self.app.pop_screen()
        self.app.notify("Progress reset successfully", severity="warning")


class ASNMemoApp(App):
    """ASN Memorization Flash Card Application."""

    CSS_PATH = "asn_memo.tcss"
    TITLE = "ASN Memo"
    SUB_TITLE = "Network AS Number Flash Cards"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("?", "help", "Help"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.progress_manager = ProgressManager()
        self.card_states = self.progress_manager.load()
        self.scheduler = Scheduler(self.card_states)

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

    def save_progress(self) -> None:
        """Save current progress to disk."""
        self.progress_manager.save(self.scheduler.card_states)

    def action_quit(self) -> None:
        self.save_progress()
        self.exit()

    def action_help(self) -> None:
        self.notify(
            "Space: Reveal | 1-4: Rate | Esc: Back | Q: Quit",
            title="Keyboard Shortcuts",
        )
