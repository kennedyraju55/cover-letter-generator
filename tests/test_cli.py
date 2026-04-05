"""Tests for Cover Letter Generator CLI."""

import pytest
from click.testing import CliRunner
from cover_letter_gen.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

class TestCLI:
    def test_tones_command(self, runner):
        result = runner.invoke(cli, ["tones"])
        assert result.exit_code == 0

    def test_revisions_command(self, runner):
        result = runner.invoke(cli, ["revisions"])
        assert result.exit_code == 0
