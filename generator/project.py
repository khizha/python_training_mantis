# -*- coding: utf-8 -*-
from model.project import Project
import random
import string
import os.path
import jsonpickle
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of contacts", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/project.json"
status = (('development', 10, None), ('release', 30, None), ('stable', 50, 2), ('obsolete', 70, None))
inherit = ('yes', 'no')
viewstatus = (('public', 10, 2), ('private', 50, 3))

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a

def random_string_for_names_and_description(maxlen):
    # random string generating method

    # only letters
    symbols = string.ascii_letters

    # generate a random string with random length, but not longer than maxlen
    return "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

#    def __init__(self, name=None, status=None, inherit=None, view=None, description=None, id=None):
#        self.name = name
#        self.status = status
#        self.inherit = inherit
#        self.view = view
#        self.description = description
#        self.id = id


#testdata = [Project(name="", lastname="", address="", homephone="", mobilephone="", workphone="", phone2="", email="", email2="", email3="")] + [
testdata = [Project(name=random_string_for_names_and_description(20),
            status=random.choice(status),
            inherit=random.choice(inherit),
            view=random.choice(viewstatus),
            description=random_string_for_names_and_description(20))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))