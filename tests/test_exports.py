from __future__ import annotations


class TestExports:
    """Verify that all expected names are importable from pynus"""

    def test_import_PynusBase(self) -> None:
        from pynus import PynusBase

        assert PynusBase.__name__ == "PynusBase"

    def test_import_PynusMultiselect(self) -> None:
        from pynus import PynusMultiselect

        assert PynusMultiselect.__name__ == "PynusMultiselect"

    def test_import_PynusYN(self) -> None:
        from pynus import PynusYN

        assert PynusYN.__name__ == "PynusYN"

    def test_import_Stack(self) -> None:
        from pynus import Stack

        assert Stack.__name__ == "Stack"

    def test_import_stack_instance(self) -> None:
        from pynus import stack

        from pynus.stack import Stack

        assert isinstance(stack, Stack)

    def test_import_callback(self) -> None:
        from pynus import callback

        from pynus.base import PynusBase

        assert callback is PynusBase.add_callback

    def test_import_version(self) -> None:
        from pynus import __version__

        assert isinstance(__version__, str)
        assert __version__ == "1.2.1.dev1"
