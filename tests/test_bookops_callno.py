from bookops_callno import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_BplCallNo_top_import():
    try:
        from bookops_callno import BplCallNo
    except ImportError:
        pytest.fail("Top level CallNo import failed.")


def test_NyplCallNo_top_import():
    try:
        from bookops_callno import NyplCallNo
    except ImportError:
        pytest.fail("Top level CallNo import failed.")
