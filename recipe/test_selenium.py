
import os
import importlib
import importlib.metadata as ilmd
import pytest

# Core import should succeed quickly and without side effects
def test_core_imports():
    import selenium
    assert hasattr(selenium, "__version__")

    # Commonly used submodules should be importable
    import selenium.webdriver
    import selenium.webdriver.common
    import selenium.webdriver.remote

    # These are present in Selenium 4.x
    import selenium.webdriver.chrome
    import selenium.webdriver.firefox
    import selenium.webdriver.edge
    import selenium.webdriver.safari


def test_package_version_matches_env_or_metadata():
    """
    Fast sanity check that the installed distribution metadata is consistent.
    If EXPECTED_VERSION is provided in env, ensure it matches.
    Otherwise, just assert that version is a non-empty string.
    """
    dist_version = ilmd.version("selenium")
    assert isinstance(dist_version, str) and dist_version

    expected = os.environ.get("EXPECTED_VERSION")
    if expected:
        assert dist_version == expected, f"{dist_version=} != {expected=}"


def test_capabilities_build_chrome():
    """
    Build Chrome options and convert to capabilities without launching anything.
    """
    from selenium.webdriver.chrome.options import Options as ChromeOptions

    opts = ChromeOptions()
    # Adding arguments must only mutate internal state; no process is spawned
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")

    caps = opts.to_capabilities()
    assert isinstance(caps, dict)
    # W3C capability key should be present
    assert "browserName" in caps
    assert caps["browserName"].lower() in {"chrome", "chromium"}


def test_capabilities_build_firefox():
    from selenium.webdriver.firefox.options import Options as FirefoxOptions

    opts = FirefoxOptions()
    opts.headless = True

    caps = opts.to_capabilities()
    assert isinstance(caps, dict)
    assert "browserName" in caps
    assert caps["browserName"].lower() == "firefox"


def test_capabilities_build_edge():
    from selenium.webdriver.edge.options import Options as EdgeOptions

    opts = EdgeOptions()
    opts.add_argument("--headless=new")

    caps = opts.to_capabilities()
    assert isinstance(caps, dict)
    assert "browserName" in caps
    # Browser name can be "MicrosoftEdge" or "msedge" depending on Selenium
    assert caps["browserName"].lower() in {"microsoftedge", "msedge", "edge"}


def test_capabilities_build_safari():
    """
    Safari has an Options class but no headless support.
    This test only validates capability dict building.
    """
    from selenium.webdriver.safari.options import Options as SafariOptions

    opts = SafariOptions()
    caps = opts.to_capabilities()
    assert isinstance(caps, dict)
    assert "browserName" in caps
    assert caps["browserName"].lower() == "safari"
