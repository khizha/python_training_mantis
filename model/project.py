from sys import maxsize

class Project:

    def __init__(self, name=None, status=('development', 10), inherit="yes", view=('public', 10), description=None, id=None):
        self.name = name
        self.status = status
        self.inherit = inherit
        self.view = view
        self.description = description
        self.id = id

    def __repr__(self):
        # representation of the object in Console
        return "id %s; \nProjName %s; \nStatus %s; \nInherit  %s; \nView  %s; \nDescription  %s" % (self.id, self.name, self.status, self.inherit, self.view, self.description)

    def __eq__(self, other):
        # comparison of two objects
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
