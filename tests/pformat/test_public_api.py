from liblaf import pretty
from liblaf.pretty import PrettyDoc, PrettyOptions, config, pdoc


def test_public_api_exports() -> None:
    assert hasattr(pretty, "PrettyBuilder")
    assert hasattr(pretty, "PrettyRegistry")
    assert not hasattr(pretty, "TracedLeaf")
    assert not hasattr(pretty, "TraceContext")
    assert not hasattr(pretty, "LoweredLeaf")


def test_pretty_options_replace() -> None:
    options = PrettyOptions(max_width=10)
    replaced = options.replace(max_width=20)
    assert options.max_width == 10
    assert replaced.max_width == 20


def test_config_override() -> None:
    before = config.get()
    with config.override(max_width=13) as overridden:
        assert overridden.max_width == 13
        assert config.get().max_width == 13
    assert config.get() == before


def test_pdoc_returns_pretty_doc() -> None:
    assert isinstance(pdoc([1, 2, 3]), PrettyDoc)
