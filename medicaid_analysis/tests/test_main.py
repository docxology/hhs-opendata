"""Tests for the main.py orchestrator module."""

import pytest
import subprocess
import sys


class TestOrchestrator:
    """Test main.py CLI behavior."""

    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True, text=True, cwd="."
        )
        assert result.returncode == 0
        assert "--sections" in result.stdout
        assert "--skip-fraud" in result.stdout
        assert "--sample" in result.stdout

    def test_parse_args_defaults(self):
        from main import parse_args
        import sys
        old_argv = sys.argv
        sys.argv = ["main.py"]
        args = parse_args()
        sys.argv = old_argv
        assert args.sections is None
        assert args.skip_fraud is False
        assert args.sample is False

    def test_should_run_all(self):
        from main import should_run
        import argparse
        args = argparse.Namespace(sections=None, skip_fraud=False)
        for i in range(1, 41):
            assert should_run(i, args) is True

    def test_should_run_skip_fraud(self):
        from main import should_run
        import argparse
        args = argparse.Namespace(sections=None, skip_fraud=True)
        assert should_run(1, args) is True
        assert should_run(32, args) is True
        assert should_run(33, args) is False
        assert should_run(40, args) is False

    def test_should_run_specific_sections(self):
        from main import should_run
        import argparse
        args = argparse.Namespace(sections=[1, 5, 32], skip_fraud=False)
        assert should_run(1, args) is True
        assert should_run(5, args) is True
        assert should_run(32, args) is True
        assert should_run(2, args) is False
        assert should_run(33, args) is False

    def test_run_section_error_handling(self):
        from main import run_section

        def failing_func(*args):
            raise ValueError("Test error")

        result = run_section(99, failing_func, "a", "b")
        assert result is None  # Should catch error and return None
