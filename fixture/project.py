from selenium.webdriver.support.ui import Select
from model.project import Project

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        # if the current page address ends with "\manage_proj_page.php" and there is a button with name "new" on this page then
        # this is a correct page
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(wd.find_elements_by_xpath("//input[@value='Create New Project']")) > 0):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        # init project creation
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        # submit created project
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.open_projects_page()
        self.project_cache = None

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_dropdown_value("status", project.status)
        self.change_checkbox_value("inherit_global", project.inherit)
        self.change_dropdown_value("view_state", project.view)
        self.change_field_value("description", project.description)


    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_dropdown_value(self, field_name, value):
        wd = self.app.wd
        # select the chosen group from the drop-down list and click it
        Select(wd.find_element_by_name(field_name)).select_by_visible_text(value[0])
        wd.find_element_by_xpath("//option[@value='%s']" % value[1]).click()

    def change_checkbox_value(self, field_name, text):
        wd = self.app.wd
        # when new project dialog is opened the checkbox is set by default
        if text == "no":
            wd.find_element_by_name("inherit_global").click()

    def get_project_list(self):
        # check if project cache is empty
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_css_selector("span.group"):
                text = element.text
                # get attribute value from checkbox element residing inside span element
                id = element.find_element_by_name("selected[]").get_attribute("value")
                self.project_cache.append(Group(name=text, id=id))
        return list(self.project_cache)

    project_cache = None

    def get_project_list(self):
        # check if group cache is empty
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []

            #print("")
            #print("--------------- table length ---------------")
            #print(len(wd.find_elements_by_xpath("//*[@class= 'width100']/tbody/tr")))
            #print("")

            for element in wd.find_element_by_name("project_id").find_elements_by_tag_name("option"):
                #print(element.get_attribute("value") + ":" + (element.text))
                text = element.text
                id = element.get_attribute("value")
                if id != "0": # All Projects id=0
                    self.project_cache.append(Project(name=text, id=id))

            #print("")
            #print("--------------- self.project_cache ---------------")
            #print(self.project_cache)

        return list(self.project_cache)