import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to read the CSV file
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to compose email
def compose_email(sender, receiver, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach resume PDF
    filename = attachment_path.split('/')[-1]
    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    return msg

# Function to send email
def send_email(sender_email, receiver_email, password, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Email credentials
SENDER_EMAIL = 'provide senders mail id'
SENDER_PASSWORD = 'password' # if the 537 errors occurs make sure to create APP password and add it here

# Read CSV file
csv_data = read_csv('your local drive resume path')

# Loop through each recipient in the CSV file and send email
for row in csv_data:
    receiver_email = row['Receiver Email']
    subject = row['Subject']
    body = row['Body']
    attachment_path = row['Attachment Path']
    
    # Compose email message
    email = compose_email(SENDER_EMAIL, receiver_email, subject, body, attachment_path)
    
    # Send email
    send_email(SENDER_EMAIL, receiver_email, SENDER_PASSWORD, email)
