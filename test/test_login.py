import time

def test_login(app):
    app.session.login("administrator", "root")

    time.sleep(0)



    assert app.session.is_logged_in_as("administrator")