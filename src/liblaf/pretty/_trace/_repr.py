import reprlib

from rich.text import Text

from liblaf.pretty._prelude._helpers._builder import PrettyBuilder
from liblaf.pretty._prelude._helpers._specs import LeafSpec


def repr_text(obj: object, builder: PrettyBuilder) -> Text:
    arepr = reprlib.Repr(
        maxlevel=builder.options.max_level,
        maxtuple=builder.options.max_list,
        maxlist=builder.options.max_list,
        maxarray=builder.options.max_array,
        maxdict=builder.options.max_dict,
        maxset=builder.options.max_list,
        maxfrozenset=builder.options.max_list,
        maxdeque=builder.options.max_list,
        maxstring=builder.options.max_string,
        maxlong=builder.options.max_long,
        maxother=builder.options.max_other,
        indent=builder.options.indent.plain,
    )
    return builder.highlight(arepr.repr1(obj, builder.options.max_level))


def trace_repr(obj: object, builder: PrettyBuilder) -> LeafSpec:
    return LeafSpec(repr_text(obj, builder))
