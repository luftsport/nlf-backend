from ext.app.responseless_decorators import async
from flask import current_app as app
from jinja2 import Environment, FileSystemLoader
from ext.notifications.jinja2_filters import nl2br
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email.message
import email.utils

import requests
from ext.scf import LUNGO_HEADERS, LUNGO_URL, EMAIL_CFG



def get_recepients(recepients):

    result = []
    query = 'where={{"id": {{"$in": {} }}}}&projection={{"full_name": 1, "address.email": 1}}'.format(recepients)
    print('{}/{}?{}'.format(LUNGO_URL, 'persons', query))
    resp = requests.get('{}/{}?{}'.format(LUNGO_URL, 'persons', query), headers=LUNGO_HEADERS)

    if resp.status_code == 200:

        for person in resp.json()['_items']:
            if not '_merged_to' in person:
                try:
                    result.append({
                        'full_name': person.get('full_name',''),
                        'email': person.get('address',{}).get('email',[])[0]})
                except Exception as e:
                    print('Ugha', e)
                    pass

    return list({v['email']: v for v in result if len(v['email'])>4}.values())


def notify(recepients, subject, message, prefix='NLF', subprefix='ORS'):

    ## TESTIONG
    recepients = list(set([301041]))

    msg = email.message.Message()
    msg['From'] = 'NLF Notifications <{}>'.format(EMAIL_CFG['from'])
    msg['Subject'] = '[{}.{}] {}'.format(prefix, app.config.get('APP_INSTANCE', '').upper(), subject)
    msg.add_header('Content-Type', 'text')
    msg.set_payload(message)

    send_async(recepients, msg)




#@async
def send_async(recepients, message):

    s = smtplib.SMTP(EMAIL_CFG['smtp'], EMAIL_CFG['smtp_port'])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(EMAIL_CFG['username'], EMAIL_CFG['password'])

    for recepient in get_recepients(recepients):
        print(recepient)
        message['To'] = '{} <{}>'.format(recepient['full_name'], recepient['email'])
        try:
            s.send_message(message)
        except:
            print('Error sending message')
            pass

    s.quit()

