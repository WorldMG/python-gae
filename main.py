from flask import Flask, request
from google.appengine.api import mail

app = Flask(__name__)
app.config['DEBUG'] = False

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello Lawyer"

@app.route('/sendout',methods=['GET', 'POST'])
def sendout():
    """Return an email sending result."""
    emailto = request.form.get('emailto') if request.form.get('emailto') else ""
    subject = request.form.get('subject') if request.form.get('subject') else ""
    format = request.form.get('format') if request.form.get('format') else ""
    emailcc = request.form.get('emailcc') if request.form.get('emailcc') else ""
    emailbcc = request.form.get('emailbcc') if request.form.get('emailbcc') else ""
    emailcontent = request.form.get('content') if request.form.get('content') else ""
    
    error = False
    errormessage = ''
    if not error and len(emailto) < 2:
        error = True
        errormessage = "Missing Email to"
    if not error and len(subject) < 2:
        error = True
        errormessage = "Missing Subject"
    if not error and len(emailcontent) < 5:
        error = True
        errormessage = "Missing Email content"
    if not error and len(format) < 1:
        error = True
        errormessage = "Missing Email Format"
    if not error:
        message = mail.EmailMessage(sender="Lawyer.com Referrals <referrals@corp.lawyer.com>", subject = subject)
        message.reply_to = "Lawyer.com Referrals <referrals@corp.lawyer.com>"
        if not mail.is_email_valid(emailto):
            pass

        message.to = emailto
        if len(emailcc) > 0:
            message.cc = emailcc
        if len(emailbcc) > 0:
            message.bcc = emailbcc
        if format == "html":
            message.html = emailcontent
        elif format == "txt":
            message.body = emailcontent
        
        try:
            message.send()
            return 'sent'
        except:
            return errormessage
    return "New World"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == '__main__':
    app.run()