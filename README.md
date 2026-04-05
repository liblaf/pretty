# Pretty

`liblaf.pretty` is a small pretty-printing library built around three stages:

1. `describe`: user code implements `__pretty__(options) -> Spec`
2. `trace`: the library resolves shared references with a stable breadth-first walk
3. `lower`: the library turns traced nodes into a Rich renderable with width-aware layout

## Public API

```python
from liblaf.pretty import (
    PrettyOptions,
    Spec,
    SpecContainer,
    SpecField,
    SpecKeyValue,
    SpecLeaf,
    SpecValue,
    pdoc,
    pformat,
    pprint,
)
```

Top-level formatters accept a `PrettyOptions` object:

```python
from rich.text import Text

from liblaf.pretty import PrettyOptions, pformat

text = pformat(
    {"a": [1, 2, 3]},
    options=PrettyOptions(max_width=13, indent=Text("│   ", "repr.indent")),
)
```

Custom objects participate by returning immutable specs:

```python
import attrs
from rich.text import Text

from liblaf.pretty import PrettyOptions, SpecContainer, SpecField, SpecLeaf


@attrs.frozen(slots=True, kw_only=True)
class GreetingSpec(SpecContainer):
    child: SpecLeaf

    def iter_children(self):
        yield SpecField(name="message", value=self.child)


class Greeting:
    def __pretty__(self, _options: PrettyOptions):
        return GreetingSpec(
            cls=type(self),
            id_=id(self),
            referable=True,
            begin=Text.assemble(("Greeting", "repr.tag_name"), ("(", "repr.tag_start")),
            end=Text(")", "repr.tag_end"),
            child=SpecLeaf(
                cls=str,
                referable=False,
                text=Text("'hello'", "repr.str"),
            ),
        )
```
