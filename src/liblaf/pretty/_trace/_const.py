from rich.text import Text

from liblaf.pretty._lower import TracedLeaf

TRUE = TracedLeaf(Text("True", "repr.bool_true"))
FALSE = TracedLeaf(Text("False", "repr.bool_false"))
ELLIPSIS = TracedLeaf(Text("...", "repr.ellipsis"))
NONE = TracedLeaf(Text("None", "repr.none"))
