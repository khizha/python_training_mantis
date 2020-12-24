import re

class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector('input[type="submit"]').click()
        # a confirmation email is sent to the email server after the step above

        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration") # parameter is the letter title
        # get the confirmation url from the email text
        url = self.extract_confirmation_url(mail)

        # follow the extracted url
        wd.get(url)

        # complete the registration process
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector('input[value="Update User"]').click()

    def extract_confirmation_url(self, text): # text - is the body of the letter
        t=  re.search("http://.*$", text, re.MULTILINE).group(0)
        return re.search("http://.*$", text, re.MULTILINE).group(0) # string that begins with http:// and has a number of symbols till the end of string ($ stands for the end of string)