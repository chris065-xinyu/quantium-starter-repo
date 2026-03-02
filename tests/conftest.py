import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(autouse=True)
def _force_matching_chromedriver(monkeypatch):
    """
    Force dash.testing (dash_duo) to use a ChromeDriver that matches the local Chrome version
    instead of relying on PATH (brew chromedriver).
    """

    # webdriver-manager 会下载一个合适的 chromedriver（通常会匹配本机 Chrome major 版本）
    driver_path = ChromeDriverManager().install()

    # 保存原始 Chrome 构造器，避免递归调用
    _orig_chrome = selenium_webdriver.Chrome

    def _patched_chrome(*args, **kwargs):
        # dash.testing.browser 里通常是 webdriver.Chrome(options=options) 这样调用
        options = kwargs.get("options", None)
        return _orig_chrome(service=Service(driver_path), options=options)

    # 关键：patch dash.testing.browser 内部引用的 webdriver.Chrome
    monkeypatch.setattr("dash.testing.browser.webdriver.Chrome", _patched_chrome)