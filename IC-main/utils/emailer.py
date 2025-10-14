import smtplib
from email.mime.text import MIMEText

def send_email(to_addr, subject, body):
    host = "smtp.gmail.com"
    port = 587
    user = "gmaeagendamentos@gmail.com"
    pwd = "whtt djil vuif alex"
    frm = user
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = frm
    msg["To"] = to_addr
    try:
        with smtplib.SMTP(host, port,) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(user, pwd)
            s.send_message(msg)
        return True, ""
    except Exception as e:
        return False, str(e)
