# -*- coding: utf-8 -*-
from model.project import Project

# load test data from groups.json file which resides in data package (see data_groups argument)
def test_add_project(app, json_project):
        project = json_project
        old_projects = app.project.get_project_list()
        app.project.create(project)
        new_projects = app.project.get_project_list()
        old_projects.append(project)

        #print("")
        #print("--------------- old_projects ---------------")
        #print(old_projects)

        #print("")
        #print("--------------- new_projects ---------------")
        #print(new_projects)


        assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
