from selenium import webdriver
from fixture.session import SessionHelper

class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %" % browser)
        self.session = SessionHelper(self)
        self.base_url=base_url

    def is_valid(self):
        try:
            # try to get the current opened page url from the browser
            self.wd.current_url
            # if the url retrieved successfully then the fixture is considered to be valid
            return True
        except:
            # the fixture is not valid
            return False

    def open_home_page(self):
        wd = self.wd
        # check if we are not already on the home page
        #if not (wd.current_url.endswith("localhost/addressbook/") and len(wd.find_elements_by_xpath("//input[@value='Send e-Mail']")) > 0):
        #    wd.get("http://localhost/addressbook/")
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()