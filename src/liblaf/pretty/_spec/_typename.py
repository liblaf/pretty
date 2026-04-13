from collections import defaultdict

_RUNG_COUNT: int = 4
_BUILTIN_TYPENAMES: dict[type, str] = {
    list: "",
    tuple: "",
    dict: "",
    set: "",
    frozenset: "frozenset",
}


def _typename_at_rung(cls: type, rung: int) -> str:
    match rung:
        case 1:
            return cls.__name__
        case 2:
            return cls.__qualname__
        case 3:
            return f"{cls.__module__}.{cls.__name__}"
        case 4:
            return f"{cls.__module__}.{cls.__qualname__}"
        case _:
            message = f"unsupported typename rung: {rung}"
            raise ValueError(message)


def disambiguate_typenames(types: set[type]) -> dict[type, str]:
    rungs: dict[type, int] = dict.fromkeys(types, 1)

    while True:
        groups: defaultdict[str, list[type]] = defaultdict(list)
        for cls in types:
            groups[_typename_at_rung(cls, rungs[cls])].append(cls)

        updates: dict[type, int] = {}
        for group in groups.values():
            if len(group) <= 1:
                continue
            target_rung: int = min(
                max(rungs[cls] for cls in group) + 1,
                _RUNG_COUNT,
            )
            for cls in group:
                if rungs[cls] < target_rung:
                    updates[cls] = target_rung

        if not updates:
            break

        rungs.update(updates)

    typenames: dict[type, str] = {
        cls: _typename_at_rung(cls, rungs[cls]) for cls in types
    }
    typenames.update(_BUILTIN_TYPENAMES)
    return typenames
