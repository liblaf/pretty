_DEFAULT_TYPENAMES: dict[type, str] = {dict: "", list: "", set: "", tuple: ""}


class TypeNameResolver:
    def resolve(self, types: set[type]) -> dict[type, str]:
        counter: dict[str, int] = {}
        typenames: dict[type, str] = {**_DEFAULT_TYPENAMES}
        for cls in types:
            if cls in typenames:
                continue
            for name in typenames_for(cls):
                counter[name] = counter.get(name, 0) + 1
        for cls in types:
            if cls in typenames:
                continue
            names: list[str] = typenames_for(cls)
            typenames[cls] = next(
                (name for name in names if counter[name] == 1), names[-1]
            )
        return typenames


def typenames_for(cls: type) -> list[str]:
    module: str = getattr(cls, "__module__", "<unknown>")
    name: str = cls.__name__
    qualname: str | None = getattr(cls, "__qualname__", name)
    if qualname != name:
        return [name, qualname, f"{module}.{name}", f"{module}.{qualname}"]
    return [name, f"{module}.{name}"]
