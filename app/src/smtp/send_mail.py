import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(subject, results, sender_email, sender_password, recipient_emails, cc_email=None, job_title="N/A", top_n=10):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails) if isinstance(recipient_emails, list) else recipient_emails
    msg['Subject'] = subject
    if cc_email:
        msg['Cc'] = ", ".join(cc_email) if isinstance(cc_email, list) else cc_email
    
    email_body = f"Here are the top {top_n} sorted resumes based on the final score for the job of an {job_title} \n\n"
    attachments = {}
    
    for result in results:
        email_body += f"Name: {result[3]}\n"
        email_body += f"Email: {result[2]}\n"
        email_body += f"Final Score: {result[14]}\n"
        email_body += f"Summary: {result[8]}\n"
        email_body += f"Experience Score: {result[9]}\n"
        email_body += f"Skills Score: {result[10]}\n"
        email_body += f"Responsibilities Score: {result[11]}\n"
        email_body += f"Requirements Score: {result[12]}\n"
        email_body += f"Soft Skills Score: {result[13]}\n"
        email_body += f"Technical Skills: {result[5]}\n"
        email_body += "-------------------------\n"
        
        resume = result[-1]
        if resume:
            attachments[f"{result[3]}_resume.pdf"] = resume
    
    msg.attach(MIMEText(email_body, 'plain'))
    
    for filename, content in attachments.items():
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)
    
    recipients = [recipient_emails]
    if cc_email:
        recipients.append(cc_email)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, recipients, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
           
def send_email_test(subject, body, sender_email, sender_password, recipient_emails, cc_email=None, job_title="N?A"):
    msg = MIMEMultipart()
    msg['FROM'] = sender_email
    msg['TO'] = recipient_emails
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
     
    with smtplib.SMTP('smtp.gmail.com', 587) as smpt_server:
        smpt_server.starttls()
        smpt_server.login(sender_email, sender_password)
        smpt_server.sendmail(sender_email, recipient_emails, msg.as_string())
    
    print('Message Sent!')
    
    
if __name__ == '__main__':
    subject = "test Email"
    body = "tet body"
    SENDER_EMAIL="moiz.ahmed@ecoedgeai.com"
    SENDER_PASSWORD="kjnq abcr scak lnre"
    RECEIVER_EMAIL="moiz.ahmed@ecoedgeai.com"
    CC_EMAIL="ahmedmoiz962@gmail.com"
    JOB_TITLE="AI Engineer"
    send_email(subject, 
               body,
               SENDER_EMAIL,
               SENDER_PASSWORD,
               RECEIVER_EMAIL,
               CC_EMAIL,
               JOB_TITLE)