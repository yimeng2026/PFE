#!/usr/bin/env python3
"""
PFE Pipeline Tests
==================

Basic tests for PFE pipeline components.
Part of PFE Phase 2: CI/CD pipeline integration.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Allow both `pytest pfe-pipelines/test_pfe_pipeline.py` and direct execution.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pfe_pipeline import LeanParser
from report_generator import PFEReportGenerator


def test_report_generator():
    """Test report generation with explicitly synthetic input data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        generator = PFEReportGenerator(output_dir=tmpdir)
        sample_results = {
            "total_files": 5,
            "total_theorems": 42,
            "total_sorry": 36,
            "proven_count": 9,
            "try_block_count": 31,
            "file_stats": {
                "Test.lean": {
                    "theorems": 2,
                    "lemmas": 1,
                    "definitions": 1,
                    "axioms": 0,
                    "sorry": 1,
                    "try_blocks": 1,
                }
            },
        }

        md_report = generator.generate_lean_report(sample_results)
        assert "PFE Lean Text Scan Report" in md_report
        assert "not Lean compilation" in md_report
        assert "Hodge symmetry" not in md_report

        md_path = generator.save_report(md_report, "test_report.md")
        assert os.path.exists(md_path)
        html_report = generator.generate_html_report(sample_results)
        assert "<html>" in html_report


def test_pipeline_basic():
    """Parse declarations without hiding comments, strings or import errors."""
    test_lean = """
theorem test_theorem : True := by trivial

lemma test_lemma : 1 + 1 = 2 := by norm_num

theorem with_parameters (n : Nat) : n = n := by rfl

def test_def : Nat := 42

def text_literal : String := "sorry"

axiom test_axiom : False

/- A block comment with sorry and a fake declaration:
theorem hidden_in_comment : False
-/

-- A line comment with sorry
example : False := sorry
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "Test.lean"
        tmp_path.write_text(test_lean, encoding="utf-8")
        parser = LeanParser(tmpdir)
        results = parser.parse_file(tmp_path)

        assert results["file_name"] == tmp_path.name
        assert len(results["theorems"]) == 3
        assert len(results["definitions"]) == 2
        assert len(results["axioms"]) == 1
        assert results["sorry_count"] == 1
        expected_line = test_lean.splitlines().index("example : False := sorry") + 1
        assert results["sorry_lines"] == [expected_line]
        assert results["axioms"][0]["has_sorry"] is False
        assert results["analysis_mode"] == "text_only_not_compiled"
        assert len(parser.parse_all()) == 1
        assert len(parser.parse_all()) == 1  # repeated scans must not duplicate modules


def test_parser_rejects_missing_or_empty_input():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        with pytest.raises(FileNotFoundError):
            LeanParser(str(root / "missing")).parse_all()
        with pytest.raises(ValueError):
            LeanParser(tmpdir).parse_all()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
