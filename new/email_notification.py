#Version = 3.0
#Updated Date = 04-SEP-2025
#Updated by = Hari



import boto3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


class EmailNotification():
    def send_email(self,subject,message,smtp_host,smtp_port,sender_email,recipient_email,is_attachment=False,s3_bucket='',var_directory='',file_name=''):

        body = f"Hi All,\n\n{message}\n\nNote: This is an auto-generated email. Please do not respond to this email.\n\nThanks"

        try:
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            if is_attachment:
                if s3_bucket:
                    s3_client = boto3.client('s3')
                    s3_object = s3_client.get_object(Bucket=s3_bucket, Key=f'{var_directory}/{file_name}')
                    attachment_data = s3_object['Body'].read()
                    
                else:
                    local_file_path = os.path.join(var_directory, file_name) if var_directory else None
                    if local_file_path and os.path.isfile(local_file_path):
                        with open(local_file_path, 'rb') as f:
                            attachment_data = f.read()
                    

                # Add Attachment
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(attachment_data)
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename={file_name}'
                )
                message.attach(attachment)
            recipient_email_list = [email.strip() for email in recipient_email.split(",")]

            with smtplib.SMTP(smtp_host,smtp_port) as server:
                server.starttls()
                server.sendmail(sender_email, recipient_email_list, message.as_string())
        except Exception as e:
            print(f'ERROR DETAILS: Failed to send email {e}')
            raise