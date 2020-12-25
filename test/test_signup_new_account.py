import string
import random

def random_username(prefix, maxlen):
    # random string generating method

    # all the symbols, punctuation symbols and 10 whitespaces
    symbols = string.ascii_letters

    # generate a random string with random length, but not longer than maxlen
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

def test_signup_new_account(app):
    # verify that the user id registered on the mail server
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    # veriify that the user exists on the mail server
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    # try to login as the user above to verify that signup was successful
    #app.session.login(username, password)
    #assert app.session.is_logged_in_as(username)
    #app.session.logout()

    #using soap
    assert app.soap.can_login(username, password)