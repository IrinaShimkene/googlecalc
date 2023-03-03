import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(autouse=True)
def open_site():
    pytest.driver = webdriver.Chrome('..\\chromedriver.exe')
    pytest.driver.set_window_size(1024, 600)
    pytest.driver.maximize_window()
    pytest.driver.get('https://www.google.com/search?q=%D0%BA%D0%B0%D0%BB%D1%8C%D0%BA%D1%83%D0%BB%D1%8F%D1%82%D0%BE%D1%80')
    pytest.driver.implicitly_wait(10)

    yield

    pytest.driver.quit()