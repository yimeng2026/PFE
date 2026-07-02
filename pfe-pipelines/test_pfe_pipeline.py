#!/usr/bin/env python3
"""
PFE Pipeline Tests
==================

Basic tests for PFE pipeline components.
Part of PFE Phase 2: CI/CD pipeline integration.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pfe_pipeline import LeanParser, PFEEngineeringPipeline
    HAS_PIPELINE = True
except ImportError:
    HAS_PIPELINE = False
    print("Warning: pfe_pipeline.py not available, skipping pipeline tests")

try:
    from report_generator import PFEReportGenerator
    HAS_REPORTER = True
except ImportError:
    HAS_REPORTER = False
    print("Warning: report_generator.py not available, skipping reporter tests")


def test_report_generator():
    """Test report generation with sample data."""
    if not HAS_REPORTER:
        print("SKIP: report_generator not available")
        return True
    
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
                    "theorems": 2, "lemmas": 1, "definitions": 1, "axioms": 0, "sorry": 1, "try_blocks": 1
                }
            }
        }
        
        # Test Markdown generation
        md_report = generator.generate_lean_report(sample_results)
        assert "PFE Lean Verification Report" in md_report
        assert "total_files" in md_report
        
        # Test file saving
        md_path = generator.save_report(md_report, "test_report.md")
        assert os.path.exists(md_path)
        
        # Test HTML generation
        html_report = generator.generate_html_report(sample_results)
        assert "<html>" in html_report
        
        print("PASS: report_generator tests")
        return True


def test_pipeline_basic():
    """Test basic pipeline functionality."""
    if not HAS_PIPELINE:
        print("SKIP: pfe_pipeline not available")
        return True
    
    # Create a temporary Lean file for testing
    test_lean = """
theorem test_theorem : True := by trivial

lemma test_lemma : 1 + 1 = 2 := by norm_num

def test_def : Nat := 42

axiom test_axiom : False

-- A sorry for testing
example : False := sorry
"""
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".lean", delete=False) as f:
        f.write(test_lean)
        tmp_path = f.name
    
    try:
        parser = LeanParser()
        results = parser.parse_file(tmp_path)
        
        assert results["file_name"] == os.path.basename(tmp_path)
        assert results["theorem_count"] == 1
        assert results["lemma_count"] == 1
        assert results["definition_count"] == 1
        assert results["axiom_count"] == 1
        assert results["sorry_count"] == 1
        
        print("PASS: pipeline basic tests")
        return True
    finally:
        os.unlink(tmp_path)


def main():
    """Run all tests."""
    print("=" * 60)
    print("PFE Pipeline Tests")
    print("=" * 60)
    
    tests = [
        ("Report Generator", test_report_generator),
        ("Pipeline Basic", test_pipeline_basic),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        print(f"\nRunning: {name}")
        try:
            if test_fn():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"FAIL: {name} - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
