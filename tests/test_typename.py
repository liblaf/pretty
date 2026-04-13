from liblaf.pretty._spec._typename import disambiguate_typenames


def test_same_name_in_different_modules_climbs_to_module_name() -> None:
    first = type("Thing", (), {"__module__": "pkg_a"})
    second = type("Thing", (), {"__module__": "pkg_b"})

    typenames = disambiguate_typenames({first, second})

    assert typenames[first] == "pkg_a.Thing"
    assert typenames[second] == "pkg_b.Thing"


def test_same_name_in_same_module_uses_qualname_when_available() -> None:
    top_level = type("Thing", (), {"__module__": "pkg"})
    nested = type("Thing", (), {"__module__": "pkg", "__qualname__": "Outer.Thing"})

    typenames = disambiguate_typenames({top_level, nested})

    assert typenames[top_level] == "Thing"
    assert typenames[nested] == "Outer.Thing"


def test_cross_level_collisions_advance_every_conflicting_type_to_same_rung() -> None:
    plain = type("X", (), {"__module__": "pkg_a"})
    colliding = type("Thing", (), {"__module__": "pkg_b", "__qualname__": "X"})
    companion = type("Thing", (), {"__module__": "pkg_c"})

    typenames = disambiguate_typenames({plain, colliding, companion})

    assert typenames[plain] == "pkg_a.X"
    assert typenames[colliding] == "pkg_b.Thing"
    assert typenames[companion] == "Thing"


def test_impossible_collisions_stop_at_module_qualname() -> None:
    first = type("Thing", (), {"__module__": "pkg", "__qualname__": "Outer.Thing"})
    second = type("Thing", (), {"__module__": "pkg", "__qualname__": "Outer.Thing"})

    typenames = disambiguate_typenames({first, second})

    assert typenames[first] == "pkg.Outer.Thing"
    assert typenames[second] == "pkg.Outer.Thing"


def test_disambiguation_is_independent_of_input_set_construction() -> None:
    first = type("Thing", (), {"__module__": "pkg_a"})
    second = type("Thing", (), {"__module__": "pkg_b"})
    third = type("Thing", (), {"__module__": "pkg_a", "__qualname__": "Outer.Thing"})

    forward = {first, second, third}
    reverse: set[type] = set()
    for cls in (third, second, first):
        reverse.add(cls)

    assert disambiguate_typenames(forward) == disambiguate_typenames(reverse)
