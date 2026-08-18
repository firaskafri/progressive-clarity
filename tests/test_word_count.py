"""Name: English word-count and lexical mechanics suite.

Description: Exercises included prose, every specified exclusion, compact
tokens, links, citations, headings, tables, fences, newline normalization,
lexical units, normative transformation precedence, and deterministic
property-style transformations.
Assumptions: Inputs use the English/Markdown subset made normative in SPEC.md.
Expectations: Counts match pc-core exactly across ordinary, edge, and corner
cases without making claims about non-English segmentation or semantics.
"""

from __future__ import annotations

import random
import unittest

from pc_core.word_count import (
    count_english_words,
    english_word_tokens,
    lexical_similarity,
    lexical_units,
    normalize_lexical_text,
)


class EnglishWordCountTests(unittest.TestCase):
    """Name: Normative English word-count scenarios.

    Description: Verifies reader-visible inclusion and Markdown exclusions at
    token, line, and block boundaries, including interactions whose result
    depends on the specification's ordered transformations.
    Assumptions: Whitespace separates counted tokens after deterministic
    Markdown preprocessing.
    Expectations: Every count is stable and follows the documented algorithm.
    """

    def test_counts_visible_links_inline_code_and_footnote_prose(self) -> None:
        """Name: Visible prose inclusion.

        Description: Counts link text, inline code, and explanatory footnote
        prose while excluding their syntax and reference marker.
        Assumptions: Link destinations and footnote markers are not prose.
        Expectations: Ten reader-visible tokens are counted.
        """
        markdown = (
            "# Excluded heading\n"
            "Direct **answer** with [visible link](https://example.test) and "
            '`client.write(mode="async")`. [1]\n'
            "[^note]: Extra footnote prose. ↩\n"
        )
        self.assertEqual(count_english_words(markdown), 10)

    def test_excludes_fences_tables_urls_images_and_citations(self) -> None:
        """Name: Block and citation exclusions.

        Description: Combines fenced code, a GFM table, bare URLs, an image,
        bracket citations, and author-date citations in one corner case.
        Assumptions: The table has a valid delimiter row and citations match the
        normative deterministic forms.
        Expectations: Only the two ordinary prose words remain.
        """
        markdown = """Useful prose. [Ops Memo 7] (Smith, 2025)

https://example.test/path
![diagram](https://example.test/image.svg)
![hidden alternate text][image-ref]
[image-ref]: https://example.test/hidden.svg
<!-- hidden state note words -->

| Metric | Value |
| --- | ---: |
| Pilot | 98.7% |

```python
print("not counted")
```
"""
        self.assertEqual(count_english_words(markdown), 2)

    def test_applies_block_exclusions_in_normative_order(self) -> None:
        """Name: Ordered block-transform precedence.

        Description: Places an unclosed fence inside an HTML comment and a
        pipe-containing ATX heading before a table-like delimiter.
        Assumptions: Fences precede comments, and headings precede tables, in
        the normative algorithm.
        Expectations: The unclosed fence excludes later prose while the row
        after the excluded heading remains countable.
        """
        comment_and_fence = "<!--\n```\nhidden\n-->\nVisible prose"
        heading_and_table = "# Heading | Cell\n--- | ---\nCounted | row"
        self.assertEqual(count_english_words(comment_and_fence), 0)
        self.assertEqual(count_english_words(heading_and_table), 2)

    def test_counts_compact_tokens_as_single_words(self) -> None:
        """Name: Compact token boundaries.

        Description: Covers contractions, hyphenated compounds, compact dates,
        times, currency, inequalities, and code-like values.
        Assumptions: None of the examples contains separating whitespace.
        Expectations: Each example contributes exactly one counted word.
        """
        text = "don't reader-first 2026-07-30 09:00 $120,000 ≤40 HTTP-409"
        self.assertEqual(count_english_words(text), 7)
        self.assertEqual(len(english_word_tokens(text)), 7)

    def test_excludes_ordered_markers_and_task_checkboxes(self) -> None:
        """Name: List syntax exclusions.

        Description: Counts ordered and task-list item text while excluding the
        numeric marker and checkbox state.
        Assumptions: Markers begin the Markdown line and are followed by
        whitespace.
        Expectations: Two two-word item bodies produce four counted words.
        """
        markdown = "1. First item\n- [x] Second item\n"
        self.assertEqual(count_english_words(markdown), 4)

    def test_excludes_atx_and_setext_headings(self) -> None:
        """Name: Heading-form exclusions.

        Description: Exercises ATX and Setext headings beside ordinary prose.
        Assumptions: A Setext underline immediately follows non-empty heading
        text.
        Expectations: Heading words are excluded and body words total four.
        """
        markdown = """## At a glance
First body.

Setext title
------------
Second body.
"""
        self.assertEqual(count_english_words(markdown), 4)

    def test_normalizes_newline_encodings(self) -> None:
        """Name: Newline normalization.

        Description: Compares LF, CRLF, and CR representations of identical
        visible prose.
        Assumptions: Newline encoding must not create or merge prose tokens.
        Expectations: All three representations produce the same count.
        """
        lf = "One two\nThree four\n"
        self.assertEqual(
            count_english_words(lf),
            count_english_words(lf.replace("\n", "\r\n")),
        )
        self.assertEqual(
            count_english_words(lf),
            count_english_words(lf.replace("\n", "\r")),
        )

    def test_property_punctuation_and_whitespace_preserve_token_count(self) -> None:
        """Name: Generated token-count invariance.

        Description: Uses a fixed seed to generate punctuation wrappers and
        variable whitespace around one hundred alphanumeric words.
        Assumptions: Added punctuation is Markdown syntax and added whitespace
        stays between, not inside, tokens.
        Expectations: Every generated case still counts one hundred words.
        """
        generator = random.Random(20260817)
        words = [f"word{index}" for index in range(100)]
        for _case in range(50):
            rendered = []
            for word in words:
                prefix = generator.choice(("", "**", "`", "["))
                suffix = {"": "", "**": "**", "`": "`", "[": "]"}[prefix]
                rendered.append(f"{prefix}{word}{suffix}")
            separator = generator.choice((" ", "  ", "\n", "\n\n"))
            self.assertEqual(count_english_words(separator.join(rendered)), 100)


class LexicalMechanicsTests(unittest.TestCase):
    """Name: Lexical duplicate primitives.

    Description: Covers normalized exact units and deterministic similarity
    used by duplicate diagnostics.
    Assumptions: Lexical signals are mechanical proxies, not semantic identity.
    Expectations: Exact normalization is stable and near overlap is measurable.
    """

    def test_normalizes_markdown_case_and_sentence_units(self) -> None:
        """Name: Lexical normalization.

        Description: Removes Markdown syntax, folds case, and splits two
        sentences into normalized units.
        Assumptions: Sentence punctuation ends each supplied sentence.
        Expectations: The normalized units retain only visible lexical tokens.
        """
        text = "**Atlas** saves money. Migration takes two weekends."
        self.assertEqual(
            normalize_lexical_text(text),
            "atlas saves money migration takes two weekends",
        )
        self.assertEqual(
            lexical_units(text),
            ("atlas saves money", "migration takes two weekends"),
        )

    def test_similarity_is_symmetric_and_bounded(self) -> None:
        """Name: Similarity property bounds.

        Description: Checks symmetry, identity, disjointness, and numeric bounds
        over generated lexical unit pairs.
        Assumptions: Jaccard token-set similarity defines the advisory signal.
        Expectations: Scores stay within zero and one and are order independent.
        """
        units = [
            "alpha beta gamma",
            "alpha beta delta",
            "one two three",
            "",
        ]
        for left in units:
            for right in units:
                score = lexical_similarity(left, right)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)
                self.assertEqual(score, lexical_similarity(right, left))
        self.assertEqual(lexical_similarity("a b", "a b"), 1.0)
        self.assertEqual(lexical_similarity("a", "b"), 0.0)


if __name__ == "__main__":
    unittest.main()
