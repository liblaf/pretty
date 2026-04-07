from collections import Counter


def disambiguate_typenames(types: set[type]) -> dict[type, str]:
    counts: Counter[str] = Counter(cls.__name__ for cls in types)
    typenames: dict[type, str] = {}
    for cls in types:
        if counts[cls.__name__] > 1:
            typenames[cls] = f"{cls.__module__}.{cls.__name__}"
        else:
            typenames[cls] = cls.__name__
    typenames.update({list: "", tuple: "", dict: "", set: "", frozenset: "frozenset"})
    return typenames
