from rich.text import Text

from liblaf.pretty._prelude import LiteralSpec

TRUE = LiteralSpec(Text("True", "repr.bool_true"))
FALSE = LiteralSpec(Text("False", "repr.bool_false"))
ELLIPSIS = LiteralSpec(Text("...", "repr.ellipsis"))
NONE = LiteralSpec(Text("None", "repr.none"))
