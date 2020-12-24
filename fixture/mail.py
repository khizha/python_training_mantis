import poplib
import email
import time

class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        # the email can arrive with some delay, so we will do several (5) attempts to read the email from server
        for i in range(5):
            # establish connection
            pop = poplib.POP3(self.app.config['james']['host'])
            # set user credentials
            pop.user(username)
            pop.pass_(password)
            # get the number of letters on the server. pop.stat() returns  tuple and the first element of it returns the
            #number of letters
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # go through the letters
                    msglines = pop.retr(n+1)[1] # +1 as the numeration starts from 1; letters' body is in the second element of the returned tuple
                    # text body is retrieved as a list of byte lines and we have to decode and "glue" them together before trying to retrieve the registration link
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    msg = email.message_from_string(msgtext)
                    if msg.get("Subject") == subject:
                        # mark the email for deletion
                        pop.dele(n+1)
                        # close the connection with deletion of emails marked to delete
                        pop.quit()
                        # return the body of the e-mail
                        #print("\n\n\n msg found, steps passed %s", str(i))
                        return msg.get_payload()

                    # if there are no letters on the server, close session without deletion of emails and wait for 3 seconds
            pop.close()
            time.sleep(3)
        #print("\n\n\n steps passed %s", str(i))
        return None # if confirmation letter was not found in 5 attempts



