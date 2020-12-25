# -*- coding: utf-8 -*-
from model.project import Project

# load test data from groups.json file which resides in data package (see data_groups argument)
def test_add_project(app, json_project):
        project = json_project

        username = app.session.get_logged_user()
        password = app.config['webadmin']['password']

        old_projects = app.soap.get_project_list(username, password)

        app.project.create(project)
        old_projects.append(project)

        new_projects = app.soap.get_project_list(username, password)

        assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
