from model.project import Project
import random

def test_del_project(app):
    # if groups list is empty
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="Test"))

    username = app.session.get_logged_user()
    password = app.config['webadmin']['password']

    old_projects = app.soap.get_project_list(username, password)
    #old_projects = app.project.get_project_list()

    # select random project for deletion
    project = random.choice(old_projects)

    #print("")
    #print("--------------- project for deletion ---------------")
    #print(project.name)

    app.project.delete_project_by_id(project.id)

    assert len(old_projects) - 1 == app.project.count()
    #new_projects = app.project.get_project_list()
    new_projects = app.soap.get_project_list(username, password)

    # remove project element that is equal to the given parameter
    old_projects.remove(project)

    assert old_projects == new_projects
