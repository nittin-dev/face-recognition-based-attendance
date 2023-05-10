import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Define sender and recipient email addresses
sender = '19epci021@skcet.ac.in'
recipient = 'knsbalan@skcet.ac.in'

# Define email subject
subject = 'Attendance Sheet'

# Define email body
body = 'No Proxies'

# Define CSV file name and location
csv_file = '/Users/nittin/Downloads/ATTENDANCE SYSTEM/Attendance.csv'

# Read the CSV file and create an attachment
with open(csv_file) as file:
    csv_data = file.read()
attachment = MIMEApplication(csv_data, Name='Attendance.csv')
attachment['Content-Disposition'] = f'attachment; filename="{csv_file}"'

# Create a multipart message and add the email body and attachment
message = MIMEMultipart()
message['From'] = sender
message['To'] = recipient
message['Subject'] = subject
message.attach(MIMEText(body))
message.attach(attachment)

# Connect to the SMTP server and send the email
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(sender, 'vimalaganesh21')
    smtp.send_message(message)
