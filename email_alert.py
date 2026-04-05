import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email Configuration
EMAIL_CONFIG = {
    'from_email': 'jitesh@avissupport.com',
    'to_email': ['rahul.upadhyay@cogenteservices.com'],
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'jitesh@avissupport.com',
    'password': 'wlfh jfbp czhu kutg'
}

# Jenkins Configuration: Last build console log
JENKINS_LOG_URL = 'http://192.168.160.60:8080/job/Tataplayfiber_recording/lastBuild/consoleText'

def fetch_jenkins_log(url):
    """Fetch Jenkins console log via HTTP."""
    try:
        response = requests.get(url, timeout=30)  # Add auth=('user','APIToken') if needed
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch log. Status code: {response.status_code}"
    except Exception as e:
        return f"Error fetching Jenkins log: {e}"

def send_email(log_content):
    """Send Jenkins logs via email."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['from_email']
        msg['To'] = ', '.join(EMAIL_CONFIG['to_email'])
        msg['Subject'] = f'Jenkins Pipeline Log - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

        # Attach log content
        msg.attach(MIMEText(log_content, 'plain'))

        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['username'], EMAIL_CONFIG['password'])
        server.send_message(msg)
        server.quit()

        print("Latest Jenkins log email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    log_content = fetch_jenkins_log(JENKINS_LOG_URL)
    send_email(log_content)

if __name__ == "__main__":
    main()
