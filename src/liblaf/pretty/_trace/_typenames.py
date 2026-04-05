from __future__ import annotations

from collections import Counter
from collections.abc import Iterable


def disambiguate_typenames(types: Iterable[type]) -> dict[type, str]:
    unique_types: tuple[type, ...] = tuple(dict.fromkeys(types))
    counts: Counter[str] = Counter()
    candidates_by_type: dict[type, tuple[str, ...]] = {}
    for cls in unique_types:
        candidates: tuple[str, ...] = tuple(_candidates(cls))
        candidates_by_type[cls] = candidates
        counts.update(candidates)

    typenames: dict[type, str] = {}
    for cls in unique_types:
        for candidate in candidates_by_type[cls]:
            if counts[candidate] == 1:
                typenames[cls] = candidate
                break
        else:
            typenames[cls] = candidates_by_type[cls][-1]
    return typenames


def _candidates(cls: type) -> list[str]:
    module_raw = getattr(cls, "__module__", "<unknown>")
    module: str = module_raw if isinstance(module_raw, str) else "<unknown>"
    qualname_raw = getattr(cls, "__qualname__", cls.__name__)
    qualname: str = qualname_raw if isinstance(qualname_raw, str) else cls.__name__
    name: str = cls.__name__

    candidates: list[str] = [name]

    qual_parts: list[str] = qualname.split(".")
    for length in range(2, len(qual_parts) + 1):
        candidate = ".".join(qual_parts[-length:])
        if candidate not in candidates:
            candidates.append(candidate)

    module_parts: tuple[str, ...] = tuple(module.split("."))
    for length in range(1, len(module_parts) + 1):
        candidate = ".".join([*module_parts[-length:], *qual_parts])
        if candidate not in candidates:
            candidates.append(candidate)

    full_name: str = f"{module}.{qualname}"
    if full_name not in candidates:
        candidates.append(full_name)
    return candidates
