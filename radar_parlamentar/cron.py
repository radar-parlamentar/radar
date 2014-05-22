from django_cron import cronScheduler, Job

# This is a function I wrote to check a feedback email address and add it to our database. Replace with your own imports
from MyMailFunctions import check_feedback_mailbox

class CheckMail(Job):
        """
                Cron Job that checks the lgr users mailbox and adds any approved senders' attachments to the db
        """

        # run every 300 seconds (5 minutes)
        run_every = 30
                
        def job(self):
                # This will be executed every 5 minutes
                check_feedback_mailbox()
                

cronScheduler.register(CheckMail)

