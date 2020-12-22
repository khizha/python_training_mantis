class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.app.wd
        wd.implicitly_wait(3)
        wd.find_element_by_link_text("Logout").click()
        # wait the login page to appear
        #wd.find_element_by_name("user")

    def ensure_logout(self):
        wd = self.app.wd
        #check if the current page contains "Logout" reference. If not then this is already login page
        # if the length of "Logout" references list on the current page is non-zero, i.e there is at list one "Logout"
        if self.is_logged_in():
            # perform logout
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        wd.implicitly_wait(3)
        #return wd.find_element_by_xpath("//div[@id='top']/form/b").text == "(" + username + ")"
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                # we are logged in as wrong user
                self.logout()
        self.login(username, password)




