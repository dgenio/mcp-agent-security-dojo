"""Tests for the offline Markdown link checker (``tools/check_doc_links.py``).

The checker gates the docs CI job, so its own logic needs coverage: a
resolvable repo-relative link must pass and a broken one must be reported.
``tools/`` is not an importable package, so the module is loaded by file path.
"""

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "tools" / "check_doc_links.py"
_spec = importlib.util.spec_from_file_location("check_doc_links", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
check_doc_links = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_doc_links)


def test_resolvable_repo_relative_link_passes(tmp_path):
    (tmp_path / "target.md").write_text("# Target\n", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text("See [the target](target.md) for details.\n", encoding="utf-8")
    assert check_doc_links._check_file(doc, tmp_path) == []


def test_broken_repo_relative_link_is_reported(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("See [missing](does_not_exist.md).\n", encoding="utf-8")
    errors = check_doc_links._check_file(doc, tmp_path)
    assert len(errors) == 1
    assert "does_not_exist.md" in errors[0]


def test_external_and_anchor_links_are_skipped(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text(
        "[web](https://example.com) [mail](mailto:a@b.com) [top](#section)\n",
        encoding="utf-8",
    )
    assert check_doc_links._check_file(doc, tmp_path) == []


def test_link_with_trailing_anchor_resolves_to_the_file(tmp_path):
    (tmp_path / "page.md").write_text("# Page\n", encoding="utf-8")
    doc = tmp_path / "doc.md"
    doc.write_text("[a heading](page.md#heading)\n", encoding="utf-8")
    assert check_doc_links._check_file(doc, tmp_path) == []


def test_is_external_classifies_schemes():
    assert check_doc_links._is_external("https://example.com")
    assert check_doc_links._is_external("mailto:a@b.com")
    assert not check_doc_links._is_external("docs/index.md")


def test_iter_markdown_walks_tree_and_skips_noise_dirs(tmp_path):
    (tmp_path / "a.md").write_text("ok\n", encoding="utf-8")
    nested = tmp_path / "docs"
    nested.mkdir()
    (nested / "b.md").write_text("ok\n", encoding="utf-8")
    skipped = tmp_path / "site"
    skipped.mkdir()
    (skipped / "generated.md").write_text("ok\n", encoding="utf-8")

    found = {p.name for p in check_doc_links._iter_markdown(tmp_path)}
    assert {"a.md", "b.md"} <= found
    assert "generated.md" not in found  # under a _SKIP_DIRS directory
