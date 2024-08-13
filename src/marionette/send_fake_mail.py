# Import smtplib for the actual sending function
import smtplib
import yaml

# Import the email modules we'll need
from email.message import EmailMessage

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost', port=2525)

with open("fake_mail.yaml") as fh:
    fake_mail_obj = yaml.safe_load(fh)

me = fake_mail_obj.get('me', 'me@example.org')
fake_mail = fake_mail_obj.get('mail', [])

for mail in fake_mail:
    msg = EmailMessage()
    msg.set_content(mail.get('message', 'Hello World!'))
    msg['Subject'] = mail.get('subject')
    msg['From'] = mail.get('from')
    msg['To'] = mail.get('to', me)
    msg['Message-ID'] = mail.get('mid')
    msg['References'] = mail.get('ref')

    s.send_message(msg)


s.quit()
print("Finished!")
