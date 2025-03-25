import random
import smtplib
import time

from email.message import EmailMessage
from datetime import datetime
from pathlib import Path


# This script generates some test emails and sends them through stage leroymerlin smtp server.
# To use this script you must have installed python interpreter,
# provide login and password of smtp server, list of recipients,
# then just invoke command: `python send_emails_by_STAGE_smtp.py`


def create_test_email(n, to, add_attachments=False):
    msg = EmailMessage()
    msg['Subject'] = f'{n} - Test email [ТКЦ-2023-03-02-{str(n).zfill(7)}]'
    msg['From'] = 'employee_notification_test@lemanapro.ru'
    msg['To'] = to
    html = f"""\
    <!DOCTYPE html>
    <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>
    
    <body>
    <p>&nbsp;</p>
    <div style="background-color: #ffffff;">
        <table width="100%" height="100%" cellspacing="0" cellpadding="0" border="0">
            <tbody>
            <tr>
                <td align="left" valign="top">
                    <table width="100%" cellspacing="0" cellpadding="0" border="0">
                        <tbody>
                        <tr>
                            <td width="100%">{n} - Это тестовое сообщение</td>
                        </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
    </body>
    </html>
    """
    msg.set_content(html, subtype='html')

    if add_attachments:
        file_path = Path("тестовый файл 1.png")
        with file_path.open("rb") as fp:
            msg.add_attachment(fp.read(), maintype="image", subtype="png", filename=file_path.name)

        file_path = Path("тестовый файл 2.png")
        with file_path.open("rb") as fp:
            msg.add_attachment(fp.read(), maintype="image", subtype="png", filename=file_path.name)
    return msg


s = smtplib.SMTP(host='owa.leroymerlin.ru', port=587)
s.starttls()
s.ehlo()
# TODO: change login and password
s.login('login', 'pass')

# TODO: change recipients
recipient = 'test@gmail.com'
s.send_message(create_test_email(1, recipient))
print(f'{datetime.now()}: Email 1 sent to Gmail.com through stage smtp server')
time.sleep(0.05)

recipient = 'test@mail.ru'
s.send_message(create_test_email(2, recipient))
print(f'{datetime.now()}: Email 2 sent to Mail.ru through stage smtp server')
time.sleep(0.05)

recipient = 'test@yandex.ru'
s.send_message(create_test_email(3, recipient))
print(f'{datetime.now()}: Email 3 sent to Yandex Mail through stage smtp server')
time.sleep(0.05)

recipient = 'test@exchange.ru'
s.send_message(create_test_email(4, recipient))
print(f'{datetime.now()}: Email 4 sent to MS Exchange through stage smtp server')
time.sleep(0.05)

s.quit()
print('done')
