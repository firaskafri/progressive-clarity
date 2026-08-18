"""Name: Conversation-state persistence suite.

Description: Exercises initial defaults, strict parsing, atomic replacement,
fact-ledger and host-session round trips, malformed input, valid and dangling
symlink refusal, and temporary-file cleanup.
Assumptions: Tests run on a filesystem supporting same-directory os.replace.
Expectations: Only complete valid state becomes visible and failed loads or
unsafe paths never silently reset committed history.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pc_core.model import ConversationState, SchemaError, StoredFact
from pc_core.state import FileStateStore, StateError


class FileStateStoreTests(unittest.TestCase):
    """Name: Atomic file-state transactions.

    Description: Validates state loading and commits over missing, valid,
    malformed, replaced, host-session-bearing, and both valid and dangling
    unsafe filesystem paths.
    Assumptions: A single wrapper process owns a given state file at a time.
    Expectations: Commits are atomic and invalid prior state fails closed.
    """

    def test_missing_state_returns_v02_initial_defaults(self) -> None:
        """Name: Missing-state initialization.

        Description: Loads a path that has never been committed.
        Assumptions: A missing file denotes a new conversation, not corruption.
        Expectations: Topic and branch are unset and counters are empty.
        """
        with tempfile.TemporaryDirectory() as directory:
            state = FileStateStore(Path(directory) / "state.json").load()
        self.assertIsNone(state.active_topic_id)
        self.assertIsNone(state.branch)
        self.assertEqual(state.turn, 0)
        self.assertEqual(state.facts, {})
        self.assertEqual(state.host_sessions, {})

    def test_atomic_commit_round_trips_fact_state(self) -> None:
        """Name: Complete state round trip.

        Description: Commits a populated topic and reloads every deterministic
        field.
        Assumptions: JSON serialization preserves Unicode and sorted fact keys.
        Expectations: Reloaded state equals the immutable committed value.
        """
        state = ConversationState(
            active_topic_id="atlas",
            branch="rollback",
            turn=3,
            facts={
                "ATLAS-F1": StoredFact(
                    text="Atlas saves money.",
                    allocation="at_a_glance",
                    first_turn=1,
                )
            },
            host_sessions={"cursor": "cursor-session-1"},
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "state.json"
            store = FileStateStore(path)
            store.commit(state)
            loaded = store.load()
            temporary_files = list(path.parent.glob("*.tmp"))
        self.assertEqual(loaded, state)
        self.assertEqual(temporary_files, [])

    def test_second_commit_atomically_replaces_prior_document(self) -> None:
        """Name: Atomic replacement.

        Description: Commits two complete states to the same path.
        Assumptions: os.replace exposes either old or new bytes, never partial
        JSON.
        Expectations: The second complete state is the only state subsequently
        loaded.
        """
        first = ConversationState(active_topic_id="atlas", turn=1)
        second = ConversationState(active_topic_id="retention", turn=2)
        with tempfile.TemporaryDirectory() as directory:
            store = FileStateStore(Path(directory) / "state.json")
            store.commit(first)
            store.commit(second)
            loaded = store.load()
        self.assertEqual(loaded, second)

    def test_malformed_state_fails_closed(self) -> None:
        """Name: Malformed-state refusal.

        Description: Writes truncated JSON at an existing state path.
        Assumptions: Existing malformed bytes indicate corruption, not a new
        conversation.
        Expectations: Loading raises StateError instead of resetting state.
        """
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text('{"active_topic_id":', encoding="utf-8")
            with self.assertRaises(StateError):
                FileStateStore(path).load()

    def test_symlink_state_path_is_rejected(self) -> None:
        """Name: Symlink-state refusal.

        Description: Points the configured state path at another regular file.
        Assumptions: Following a mutable symlink would weaken path ownership.
        Expectations: Both load and commit reject the symlink.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target.json"
            target.write_text(
                json.dumps(ConversationState.initial().to_dict()),
                encoding="utf-8",
            )
            link = root / "state.json"
            link.symlink_to(target)
            store = FileStateStore(link)
            with self.assertRaises(StateError):
                store.load()
            with self.assertRaises(StateError):
                store.commit(ConversationState.initial())

    def test_dangling_symlink_state_path_is_rejected(self) -> None:
        """Name: Dangling-symlink state refusal.

        Description: Points the configured state path at a missing target.
        Assumptions: Path.exists is false for a dangling symlink even though
        the configured path remains an unsafe link.
        Expectations: Load and commit fail closed rather than treating the path
        as absent or replacing the link.
        """
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = root / "state.json"
            link.symlink_to(root / "missing-target.json")
            store = FileStateStore(link)
            with self.assertRaises(StateError):
                store.load()
            with self.assertRaises(StateError):
                store.commit(ConversationState.initial())


class ConversationStateSchemaTests(unittest.TestCase):
    """Name: Persisted state schema strictness.

    Description: Checks unknown-field rejection independently of filesystem I/O.
    Assumptions: State schema changes require an explicit version migration.
    Expectations: Unrecognized fields cannot be silently retained or dropped.
    """

    def test_unknown_state_field_is_rejected(self) -> None:
        """Name: Unknown state field.

        Description: Adds one field to an otherwise valid initial document.
        Assumptions: The current state schema is closed.
        Expectations: Strict parsing raises SchemaError.
        """
        data = ConversationState.initial().to_dict()
        data["future_field"] = "unsupported"
        with self.assertRaises(SchemaError):
            ConversationState.from_dict(data)


if __name__ == "__main__":
    unittest.main()
