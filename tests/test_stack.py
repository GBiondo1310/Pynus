from __future__ import annotations

from unittest.mock import Mock, MagicMock

import pytest

from pynus.stack import Stack


class TestStackInit:
    """Stack constructor behavior"""

    def test_empty_on_creation(self) -> None:
        stack = Stack()
        assert len(stack) == 0
        assert list(stack) == []


class TestStackPop:
    """Stack.pop() method"""

    def test_pop_from_empty_returns_none(self) -> None:
        stack = Stack()
        assert stack.pop() is None

    def test_pop_with_index_from_empty_returns_none(self) -> None:
        stack = Stack()
        assert stack.pop(0) is None

    def test_pop_returns_last_pushed(self) -> None:
        stack = Stack()
        stack.push("first")
        stack.push("second")
        assert stack.pop() == "second"

    def test_pop_maintains_lifo_order(self) -> None:
        stack = Stack()
        stack.push("a")
        stack.push("b")
        stack.push("c")
        assert stack.pop() == "c"
        assert stack.pop() == "b"
        assert stack.pop() == "a"
        assert stack.pop() is None

    def test_pop_with_index_returns_correct_item(self) -> None:
        stack = Stack()
        stack.push("a")
        stack.push("b")
        stack.push("c")
        # index 0 is the first element (bottom of stack)
        assert stack.pop(0) == "a"
        assert stack.pop(0) == "b"
        assert stack.pop(0) == "c"
        assert stack.pop(0) is None

    def test_pop_reduces_length(self) -> None:
        stack = Stack()
        stack.push("a")
        stack.push("b")
        assert len(stack) == 2
        stack.pop()
        assert len(stack) == 1
        stack.pop()
        assert len(stack) == 0


class TestStackPush:
    """Stack.push() method"""

    def test_push_adds_to_stack(self) -> None:
        stack = Stack()
        stack.push("item")
        assert len(stack) == 1
        assert stack[0] == "item"

    def test_push_increases_length(self) -> None:
        stack = Stack()
        stack.push("a")
        assert len(stack) == 1
        stack.push("b")
        assert len(stack) == 2

    def test_push_returns_none(self) -> None:
        stack = Stack()
        result = stack.push("item")
        assert result is None  # list.append() returns None

    def test_push_none_value(self) -> None:
        stack = Stack()
        stack.push(None)
        assert len(stack) == 1
        assert stack[0] is None


class TestStackMainloop:
    """Stack.mainloop() method"""

    def test_empty_stack_exits_immediately(self) -> None:
        stack = Stack()
        # Should not raise or loop infinitely
        stack.mainloop()

    def test_single_menu_calls_start_once(self) -> None:
        stack = Stack()
        menu = MagicMock()
        menu.start.return_value = None  # Returning None stops the loop

        stack.push(menu)
        stack.mainloop()

        menu.start.assert_called_once()

    def test_menu_returning_none_pops_next(self) -> None:
        stack = Stack()
        menu1 = MagicMock()
        menu1.start.return_value = None

        menu2 = MagicMock()
        menu2.start.return_value = None

        stack.push(menu1)
        stack.push(menu2)
        stack.mainloop()

        # menu2 was popped first (LIFO), then when it returns None,
        # menu1 is popped and its start() is called
        menu2.start.assert_called_once()
        menu1.start.assert_called_once()

    def test_menu_returning_menu_chains_correctly(self) -> None:
        stack = Stack()
        menu1 = MagicMock()
        menu2 = MagicMock()
        menu2.start.return_value = None

        # menu1.start() returns menu2, so mainloop should call menu2.start()
        menu1.start.return_value = menu2

        stack.push(menu1)
        stack.mainloop()

        menu1.start.assert_called_once()
        menu2.start.assert_called_once()

    def test_chain_then_pop_back(self) -> None:
        stack = Stack()
        menu1 = MagicMock()
        menu2 = MagicMock()
        menu2.start.return_value = None

        # menu1.start() returns menu2, which returns None
        menu1.start.return_value = menu2

        stack.push(menu1)
        stack.mainloop()

        menu1.start.assert_called_once()
        menu2.start.assert_called_once()

    def test_push_within_callback(self) -> None:
        """When a callback pushes to stack and returns None, stack should pop next"""
        stack = Stack()
        menu1 = MagicMock()
        menu1.start.return_value = None

        menu2 = MagicMock()
        # Simulates: callback pushes current menu and returns None
        menu2.start.side_effect = lambda: stack.push(menu1) or None

        stack.push(menu2)
        stack.mainloop()

        menu2.start.assert_called_once()
        # After menu2 returns None, menu1 should be popped from stack
        menu1.start.assert_called_once()

    def test_no_infinite_loop_with_chained_returns(self) -> None:
        """Returning self should work but not cause infinite loop"""
        stack = Stack()
        menu = MagicMock()
        # Return self first time, then None
        menu.start.side_effect = [menu, None]

        stack.push(menu)
        stack.mainloop()

        assert menu.start.call_count == 2


class TestStackInheritance:
    """Stack inherits from list"""

    def test_is_list_subclass(self) -> None:
        stack = Stack()
        assert isinstance(stack, list)

    def test_len_and_bool(self) -> None:
        stack = Stack()
        assert len(stack) == 0
        assert not stack

        stack.push("item")
        assert len(stack) == 1
        assert stack  # truthy when non-empty
