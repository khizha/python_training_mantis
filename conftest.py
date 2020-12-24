
from fixture.application import Application
import pytest
import json
import os.path
import jsonpickle
import ftputil

# global variable containing fixture
fixture = None

# global variable containing configuration file data
target = None

def load_config(file):
    global target

    if target is None:
        # get path to the configuration file
        #if request.config.getoption("--targetpath") is None:
            # if the path to the configuration file is not provided in the command line then it is located in the current directory
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        #else:
            # if the path to the configuration file is provided
        #   config_file = os.path.join(request.config.getoption("--targetpath"), file)

        with open(config_file) as f:
            target = json.load(f)

    return target

@pytest.fixture(scope="session")
def config(request):
    #this fixture will be used by other fixtures
    return load_config(request.config.getoption("--target"))

@pytest.fixture()
def app(request, config):
    # use the global variable "fixture"
    global fixture

    browser = request.config.getoption("--browser")

    # check if fixture does not exist or is corrupted/invalid
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    webadmin_config = load_config(request.config.getoption("--target"))['webadmin']
    return fixture

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    # using ftp protocol put the configuration file to the server
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    #create new connection to ftp server
    with ftputil.FTPHost(host, username, password) as remote:
        # if config file.bak exists on the remote server, remove it
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        # if config file exists on the remote server, rename it
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        # upload the configuration file to the server
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")

def restore_server_configuration(host, username, password):
    #create new connection to ftp server
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--targetpath", action="store", default=None)

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())