from bookops_callno import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_CallNo_top_import():
    try:
        from bookops_callno import CallNo
    except ImportError:
        pytest.fail("Top level CallNo import failed.")
