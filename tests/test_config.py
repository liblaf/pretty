from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from rich.text import Text

from liblaf.pretty import PrettyOptions
from liblaf.pretty.common import ObjectIdentifier


def test_pretty_options_preserves_text_indent_objects() -> None:
    indent = Text("> ", "repr.indent")

    options = PrettyOptions(
        max_level=1,
        max_list=2,
        max_array=3,
        max_dict=4,
        max_string=5,
        max_long=6,
        max_other=7,
        indent=indent,
        hide_defaults=True,
    )

    assert options.indent is indent


def test_pretty_options_accept_markup_indent() -> None:
    expected_indent = Text.from_markup("[bold]>>[/] ")

    options = PrettyOptions(
        max_level=1,
        max_list=2,
        max_array=3,
        max_dict=4,
        max_string=5,
        max_long=6,
        max_other=7,
        indent="[bold]>>[/] ",
        hide_defaults=True,
    )

    assert options.indent.plain == ">> "
    assert options.indent.spans == expected_indent.spans


def test_pretty_options_accept_ansi_indent() -> None:
    options = PrettyOptions(
        max_level=1,
        max_list=2,
        max_array=3,
        max_dict=4,
        max_string=5,
        max_long=6,
        max_other=7,
        indent="\x1b[31m> \x1b[0m",
        hide_defaults=True,
    )

    assert options.indent.plain == "> "
    assert bool(options.indent.spans)


def test_pretty_config_dump_reads_environment_overrides() -> None:
    root = Path(__file__).resolve().parents[1]
    script = """
import json
import sys
sys.path.insert(0, 'src')
from liblaf.pretty import PrettyConfig
dumped = PrettyConfig().dump()
print(json.dumps({
    'max_list': dumped.max_list,
    'hide_defaults': dumped.hide_defaults,
    'indent_plain': dumped.indent.plain,
    'has_indent_spans': bool(dumped.indent.spans),
}))
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=True,
        cwd=root,
        env={
            **os.environ,
            "PRETTY_MAX_LIST": "2",
            "PRETTY_HIDE_DEFAULTS": "false",
            "PRETTY_INDENT": "[bold]>>[/] ",
        },
        text=True,
    )
    dumped = json.loads(result.stdout)

    assert dumped["max_list"] == 2
    assert dumped["hide_defaults"] is False
    assert dumped["indent_plain"] == ">> "
    assert dumped["has_indent_spans"] is True


def test_object_identifier_tracks_real_and_missing_objects() -> None:
    obj = object()

    identifier = ObjectIdentifier.from_obj(obj)

    assert identifier.cls is object
    assert identifier.id_ == id(obj)
    assert ObjectIdentifier.missing() == ObjectIdentifier(cls=None, id=None)
