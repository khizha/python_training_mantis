def test_signup_new_account(app):
    # verify that the user id registered on the mail server
    username = "user1111"
    password = "test"
    app.james.ensure_user_exists(username, password)
