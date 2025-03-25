import random
import smtplib
import time

import requests
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path

# This script generates some test emails using standalone greenmail.
# To use this script you must have installed python interpreter,
# then just invoke command: `python send_test_emails.py`


def create_test_email(n, m=0, add_attachments=False):
    msg = EmailMessage()
    cust_req_num = f'ТКЦ-2023-03-02-{str(m).zfill(7)}'
    msg['Subject'] = f'Test email {n}, #[{cust_req_num}] request number'
    msg['From'] = f'me.{m}@me.com'
    msg['To'] = 'test@example.com'
    msg.set_content(f"{n} - Это тестовое сообщение. Номер обращения: {cust_req_num}")

    if add_attachments:
        file_path = Path("тестовый файл 1.png")
        with file_path.open("rb") as fp:
            msg.add_attachment(fp.read(), maintype="image", subtype="png", filename=file_path.name)

        file_path = Path("тестовый файл 2.png")
        with file_path.open("rb") as fp:
            msg.add_attachment(fp.read(), maintype="image", subtype="png", filename=file_path.name)
    return msg


# To use these requests you need to install python lib 'requests'
new_user = {
    'email': 'test@example.com',
    'login': 'user',
    'password': 'pass'
}
users = list(requests.get('http://localhost:8080/api/user').json())
if len(users) > 0:
    user = users[0]
    if user['email'] != new_user['email'] or user['login'] != new_user['login']:
        requests.post('http://localhost:8080/api/user', json=new_user)
else:
    requests.post('http://localhost:8080/api/user', json=new_user)


s = smtplib.SMTP(host='localhost', port=3025)

for i in range(500):
    random_int = random.randrange(10)

    if random.randrange(100) < 30:
        s.send_message(create_test_email(i, m=random_int, add_attachments=True))
    else:
        s.send_message(create_test_email(i, m=random_int))

    print(f'{datetime.now()}: Email {i} sent')
    time.sleep(0.05)

s.quit()
print('done')
