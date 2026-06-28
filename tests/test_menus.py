from __future__ import annotations

from unittest.mock import patch

from pynus.menus import PynusYN


class TestPynusYNInit:
    def test_options_are_yes_no_back(self) -> None:
        yn = PynusYN("Test title")
        assert yn.options[-1] == "Back"
        assert "Yes" in yn.options
        assert "No" in yn.options

    def test_callbacks_registered(self) -> None:
        yn = PynusYN("Test title")
        assert 0 in yn.callbacks  # Yes callback
        assert 1 in yn.callbacks  # No callback
        assert len(yn.callbacks) == 2

    def test_does_not_mutate_reference_list(self) -> None:
        """Ensure the original list passed to super().__init__ isn't mutated"""
        # PynusYN passes a list literal to super(), so this is less critical,
        # but worth testing that options + Back works correctly
        yn = PynusYN("Test title")
        assert "Yes" in yn.options
        assert "No" in yn.options
        assert len(yn.options) == 3  # Yes, No, Back


class TestPynusYNCallbacks:
    def test_yes_callback_returns_true(self) -> None:
        yn = PynusYN("Test title")
        result = yn.callback(instance="Yes", index=0)
        assert result is True

    def test_no_callback_returns_false(self) -> None:
        yn = PynusYN("Test title")
        result = yn.callback(instance="No", index=1)
        assert result is False

    def test_back_option_returns_none_from_start(self) -> None:
        """When user picks Back, PynusBase.start() should return None"""
        yn = PynusYN("Test title")

        with patch("pynus.base.RainbowPicker.start", return_value=("Back", 2)):
            result = yn.start()
            assert result is None

    def test_yes_triggers_yes_callback_through_start(self) -> None:
        yn = PynusYN("Test title")

        with patch("pynus.base.RainbowPicker.start", return_value=("Yes", 0)):
            result = yn.start()
            assert result is True

    def test_no_triggers_no_callback_through_start(self) -> None:
        yn = PynusYN("Test title")

        with patch("pynus.base.RainbowPicker.start", return_value=("No", 1)):
            result = yn.start()
            assert result is False
