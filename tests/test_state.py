"""Name: Conversation-state persistence suite.

Description: Exercises initial defaults, strict parsing, atomic replacement,
fact-ledger and host-session round trips, malformed or ambiguous input, valid
and dangling symlink refusal, v0.3 protocol-state rejection, immutable
snapshots, and temporary-file cleanup.
Assumptions: Tests run on a filesystem supporting same-directory os.replace.
Expectations: Only complete valid state becomes visible and failed loads or
unsafe paths never silently reset committed history.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pc_core.model import ConversationState, SchemaError, StoredFact, TopicState
from pc_core.state import FileStateStore, MemoryStateStore, StateError


class FileStateStoreTests(unittest.TestCase):
    """Name: Atomic file-state transactions.

    Description: Validates state loading and commits over missing, valid,
    malformed, duplicate-key, non-UTF-8, replaced, host-session-bearing, and
    both valid and dangling unsafe filesystem paths, including old-protocol
    state that retains the current schema number.
    Assumptions: A single wrapper process owns a given state file at a time.
    Expectations: Commits are atomic and invalid prior state fails closed.
    """

    def test_missing_state_returns_v04_initial_defaults(self) -> None:
        """Name: Missing-state v0.4 initialization.

        Description: Loads a path that has never been committed.
        Assumptions: A missing file denotes a new conversation, not corruption.
        Expectations: Active topic is unset and the topic map is empty.
        """
        with tempfile.TemporaryDirectory() as directory:
            state = FileStateStore(Path(directory) / "state.json").load()
        self.assertIsNone(state.active_topic_id)
        self.assertEqual(state.turn, 0)
        self.assertEqual(state.topics, {})

    def test_atomic_commit_round_trips_fact_state(self) -> None:
        """Name: Complete state round trip.

        Description: Commits a populated topic and reloads every deterministic
        field.
        Assumptions: JSON serialization preserves Unicode and sorted fact keys.
        Expectations: Reloaded state equals the immutable committed value.
        """
        state = ConversationState(
            active_topic_id="atlas",
            turn=3,
            topics={
                "atlas": TopicState(
                    branch="rollback",
                    facts={
                        "ATLAS-F1": StoredFact(
                            text="Atlas saves money.",
                            first_turn=1,
                        )
                    },
                    host_sessions={"cursor": "cursor-session-1"},
                    has_committed_overview=True,
                ),
                "beacon": TopicState(
                    facts={
                        "BEACON-F1": StoredFact(
                            text="Beacon remains in discovery.",
                            first_turn=2,
                        )
                    },
                    host_sessions={"cursor": "cursor-session-2"},
                ),
            },
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
        first = ConversationState(
            active_topic_id="atlas",
            turn=1,
            topics={"atlas": TopicState()},
        )
        second = ConversationState(
            active_topic_id="retention",
            turn=2,
            topics={"retention": TopicState()},
        )
        with tempfile.TemporaryDirectory() as directory:
            store = FileStateStore(Path(directory) / "state.json")
            store.commit(first)
            store.commit(second)
            loaded = store.load()
        self.assertEqual(loaded, second)

    def test_stores_reject_incompatible_state_before_commit(self) -> None:
        """Name: Incompatible state commit refusal.

        Description: Supplies an old schema and old protocol through direct
        dataclass construction.
        Assumptions: Embedders can bypass JSON parsing when using state stores.
        Expectations: File and memory stores reject both without recording a
        commit.
        """
        incompatible_states = (
            (
                ConversationState(schema_version="2.1.0"),
                "unsupported state schema",
            ),
            (
                ConversationState(protocol_version="0.3"),
                "state protocol",
            ),
        )
        for incompatible, message in incompatible_states:
            with self.subTest(message=message):
                with tempfile.TemporaryDirectory() as directory:
                    store = FileStateStore(Path(directory) / "state.json")
                    with self.assertRaisesRegex(StateError, message):
                        store.commit(incompatible)
                with self.assertRaisesRegex(StateError, message):
                    MemoryStateStore(incompatible)

    def test_v03_state_file_is_rejected_without_migration(self) -> None:
        """Name: Persisted v0.3 protocol-state rejection.

        Description: Writes a schema-3.0.0 state that declares protocol 0.3.
        Assumptions: Protocol 0.4 changes semantics without changing state shape.
        Expectations: Loading fails closed instead of silently reinterpreting it.
        """
        old_state = ConversationState.initial().to_dict()
        old_state["protocol_version"] = "0.3"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps(old_state), encoding="utf-8")
            with self.assertRaisesRegex(StateError, "state protocol"):
                FileStateStore(path).load()

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

    def test_ambiguous_or_non_utf8_state_fails_closed(self) -> None:
        """Name: Strict persisted JSON boundary.

        Description: Supplies duplicate object members and invalid UTF-8 bytes.
        Assumptions: State files are standards-compliant UTF-8 JSON documents.
        Expectations: Both inputs raise StateError without loading partial state.
        """
        state_json = json.dumps(ConversationState.initial().to_dict())
        duplicate_turn = state_json.replace(
            '"turn": 0',
            '"turn": 7, "turn": 0',
        ).encode("utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            store = FileStateStore(path)
            for payload in (duplicate_turn, b"\xff"):
                with self.subTest(payload=payload):
                    path.write_bytes(payload)
                    with self.assertRaises(StateError):
                        store.load()

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

    Description: Checks unknown fields, direct nested invariants, chronology,
    and read-only mapping snapshots independently of filesystem I/O.
    Assumptions: State schema changes require an explicit version migration,
    and callers may retain mutable dictionaries used during construction.
    Expectations: Unrecognized fields and alias mutations cannot alter state.
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

    def test_direct_state_rejects_invalid_nested_values(self) -> None:
        """Name: Direct nested state invariants.

        Description: Constructs negative turns, unsafe fact IDs, empty host keys,
        and facts committed after the conversation turn.
        Assumptions: Direct state objects must round-trip through persisted schema.
        Expectations: Every invalid state is rejected before storage.
        """
        invalid_constructors = (
            lambda: ConversationState(turn=-1),
            lambda: TopicState(
                facts={
                    "unsafe fact id": StoredFact(
                        text="Fact.",
                        first_turn=1,
                    )
                }
            ),
            lambda: TopicState(host_sessions={"": "session"}),
            lambda: ConversationState(
                active_topic_id="atlas",
                turn=0,
                topics={
                    "atlas": TopicState(
                        facts={
                            "ATLAS-F1": StoredFact(
                                text="Fact.",
                                first_turn=1,
                            )
                        }
                    )
                },
            ),
        )
        for construct in invalid_constructors:
            with self.subTest(construct=construct):
                with self.assertRaises(SchemaError):
                    construct()

    def test_state_snapshots_mapping_inputs_as_read_only(self) -> None:
        """Name: Immutable state mapping snapshot.

        Description: Mutates constructor inputs and then attempts direct writes.
        Assumptions: Frozen state must not alias caller-owned dictionaries.
        Expectations: Input changes are isolated and mapping writes raise.
        """
        facts = {
            "ATLAS-F1": StoredFact(
                text="Atlas saves money.",
                first_turn=1,
            )
        }
        sessions = {"cursor": "session-1"}
        topic = TopicState(facts=facts, host_sessions=sessions)
        topics = {"atlas": topic}
        state = ConversationState(
            active_topic_id="atlas",
            turn=1,
            topics=topics,
        )

        facts.clear()
        sessions.clear()
        topics.clear()
        self.assertIn("atlas", state.topics)
        self.assertIn("ATLAS-F1", state.topics["atlas"].facts)
        self.assertEqual(
            state.topics["atlas"].host_sessions["cursor"],
            "session-1",
        )
        with self.assertRaises(TypeError):
            state.topics["atlas"].facts["ATLAS-F2"] = StoredFact(
                text="Atlas needs review.",
                first_turn=1,
            )
        with self.assertRaises(TypeError):
            state.topics["atlas"].host_sessions["cursor"] = "session-2"


if __name__ == "__main__":
    unittest.main()
