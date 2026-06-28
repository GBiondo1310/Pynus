from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pynus.base import PynusBase, PynusMultiselect, callback


# ──────────────────────────────────────────────
# PynusBase — Constructor
# ──────────────────────────────────────────────


class TestPynusBaseInit:
    def test_does_not_mutate_original_options(self) -> None:
        original = ["A", "B"]
        PynusBase("Test", original)
        assert original == ["A", "B"], "Original list should not be mutated"

    def test_appends_back_to_options(self) -> None:
        menu = PynusBase("Test", ["A", "B"])
        assert "Back" in menu.options
        assert menu.options[-1] == "Back"

    def test_includes_all_original_options(self) -> None:
        menu = PynusBase("Test", ["A", "B"])
        assert "A" in menu.options
        assert "B" in menu.options

    def test_callbacks_is_empty_dict(self) -> None:
        menu = PynusBase("Test", ["A"])
        assert menu.callbacks == {}


# ──────────────────────────────────────────────
# PynusBase — add_callback / callback decorator
# ──────────────────────────────────────────────


class TestCallbackDecorator:
    def test_register_by_index(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, index=1)
        def my_func(**kwargs):
            return "called"

        assert 1 in menu.callbacks
        result = menu.callback(instance="B", index=1)
        assert result == "called"

    def test_register_by_obj(self) -> None:
        menu = PynusBase("Test", ["A", "B"])
        obj_key = "B"

        @callback(menu, obj=obj_key)
        def my_func(**kwargs):
            return "called_by_obj"

        assert obj_key in menu.callbacks
        result = menu.callback(instance="B", index=1)
        assert result == "called_by_obj"

    def test_register_all_callback(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu)
        def all_func(**kwargs):
            return "all_called"

        assert "all" in menu.callbacks
        result = menu.callback(instance="A", index=0)
        assert result == "all_called"

    def test_all_runs_for_side_effects_then_specific_returns(self) -> None:
        """'all' runs for side effects, but specific callback's return value wins"""
        menu = PynusBase("Test", ["A", "B"])
        side_effects: list[str] = []

        @callback(menu, index=0)
        def specific(**kwargs):
            return "specific"

        @callback(menu)
        def all_func(**kwargs):
            side_effects.append("all_ran")
            return "all"

        result = menu.callback(instance="A", index=0)
        assert result == "specific"
        assert side_effects == ["all_ran"]

    def test_all_result_fallback_when_no_specific_match(self) -> None:
        """When no specific callback matches, 'all' callback's return value is used"""
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu)
        def all_func(**kwargs):
            return "all_fallback"

        # No specific callback for index=1, falls back to "all"
        result = menu.callback(instance="B", index=1)
        assert result == "all_fallback"

    def test_raises_when_both_index_and_obj_provided(self) -> None:
        menu = PynusBase("Test", ["A"])

        with pytest.raises(Exception, match="Only one between index and obj can be defined"):

            @callback(menu, index=0, obj="A")
            def bad(**kwargs):
                pass

    def test_register_after_init(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, index=1)
        def later(**kwargs):
            return "later"

        result = menu.callback(instance="B", index=1)
        assert result == "later"


# ──────────────────────────────────────────────
# PynusBase — callback() dispatch
# ──────────────────────────────────────────────


class TestPynusBaseCallback:
    def test_callback_by_index(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, index=0)
        def handler(**kwargs):
            return f"handled {kwargs['instance']}"

        result = menu.callback(instance="A", index=0)
        assert result == "handled A"

    def test_callback_by_instance(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, obj="B")
        def handler(**kwargs):
            return f"handled {kwargs['instance']}"

        result = menu.callback(instance="B", index=1)
        assert result == "handled B"

    def test_all_callback_receives_kwargs(self) -> None:
        menu = PynusBase("Test", ["A"])

        @callback(menu)
        def handler(**kwargs):
            return (kwargs["instance"], kwargs["index"])

        result = menu.callback(instance="A", index=0)
        assert result == ("A", 0)

    def test_no_match_returns_none(self) -> None:
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, index=0)
        def handler(**kwargs):
            return "handled"

        # Index 1 has no registered callback
        result = menu.callback(instance="B", index=1)
        assert result is None


# ──────────────────────────────────────────────
# PynusBase — start() with mocked RainbowPicker
# ──────────────────────────────────────────────


class TestPynusBaseStart:
    def test_back_returns_none(self) -> None:
        """When user picks 'Back', start() should return None"""
        menu = PynusBase("Test", ["A", "B"])

        with patch("pynus.base.RainbowPicker.start", return_value=("Back", 2)):
            result = menu.start()

            assert result is None

    def test_start_invokes_callback(self) -> None:
        """When user picks a non-Back option, start() invokes the callback"""
        menu = PynusBase("Test", ["A", "B"])

        @callback(menu, index=0)
        def handler(**kwargs):
            return f"result_{kwargs['instance']}"

        with patch("pynus.base.RainbowPicker.start", return_value=("A", 0)):
            result = menu.start()
            assert result == "result_A"


# ──────────────────────────────────────────────
# PynusMultiselect
# ──────────────────────────────────────────────


class TestPynusMultiselectInit:
    def test_back_is_removed(self) -> None:
        menu = PynusMultiselect("Test", ["A", "B"])
        assert "Back" not in menu.options
        assert menu.options == ["A", "B"]

    def test_does_not_mutate_original_options(self) -> None:
        original = ["A", "B"]
        PynusMultiselect("Test", original)
        assert original == ["A", "B"]

    def test_multiselect_is_true(self) -> None:
        menu = PynusMultiselect("Test", ["A", "B"])
        assert menu.multiselect is True


class TestPynusMultiselectStart:
    def test_empty_picks_returns_none(self) -> None:
        """RainbowPicker can return an empty list (e.g. user quit with quit_keys)"""
        menu = PynusMultiselect("Test", ["A", "B"])

        # Start calls RainbowPicker.start(self) — it returns an empty list for multiselect with no selection
        with patch("pynus.base.RainbowPicker.start", return_value=[]):
            result = PynusMultiselect.start(menu)
            assert result is None

    def test_executes_all_callback(self) -> None:
        menu = PynusMultiselect("Test", ["A", "B"])
        calls: list[tuple] = []

        @callback(menu)
        def handler(**kwargs):
            calls.append((kwargs["instance"], kwargs["index"]))

        with patch("pynus.base.RainbowPicker.start", return_value=[("A", 0), ("B", 1)]):
            PynusMultiselect.start(menu)

        assert calls == [("A", 0), ("B", 1)]

    def test_executes_specific_callbacks(self) -> None:
        menu = PynusMultiselect("Test", ["A", "B", "C"])
        results: list[str] = []

        @callback(menu, index=0)
        def handler_a(**kwargs):
            results.append(f"a_{kwargs['instance']}")

        @callback(menu, obj="C")
        def handler_c(**kwargs):
            results.append(f"c_{kwargs['instance']}")

        with patch("pynus.base.RainbowPicker.start", return_value=[("A", 0), ("C", 2)]):
            PynusMultiselect.start(menu)

        assert "a_A" in results
        assert "c_C" in results

    def test_returns_picks(self) -> None:
        menu = PynusMultiselect("Test", ["A", "B"])
        expected = [("A", 0), ("B", 1)]

        with patch("pynus.base.RainbowPicker.start", return_value=expected):
            result = PynusMultiselect.start(menu)

        assert result == expected


# ──────────────────────────────────────────────
# Module-level callback alias
# ──────────────────────────────────────────────


def test_callback_is_add_callback_alias() -> None:
    """The module-level `callback` is an alias for PynusBase.add_callback"""
    from pynus.base import callback as cb
    from pynus.base import PynusBase

    assert cb is PynusBase.add_callback
