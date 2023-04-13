import smtplib
from email.message import EmailMessage
from CREDENTIALS import email_id,email_pass

def send_mail(recipient_list, file_loc):
    # recipient_list = ['krimada1998@gmail.com'] ## testing account
    msg = EmailMessage()
    msg['Subject'] = 'FIRE DETECTED'
    msg['From'] = email_id
    msg['To'] = recipient_list
    msg.set_content('There might be fire in the given premise, refer attachement for photos')
    with open(file_loc, 'rb') as f:
        file_data = f.read()
        file_loc = file_loc.split('/')[-1]
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_loc)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
        print('email_send')