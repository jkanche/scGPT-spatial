import pytest

def test_package_load():
    try:
        import scgpt_spatial
        assert True
    except Exception as e:
        assert False