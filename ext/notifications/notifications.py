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
from ext.app.lungo import get_person_from_role, get_org_name, get_person_name

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
                        'full_name': person.get('full_name', ''),
                        'email': person.get('address', {}).get('email', [])[0]})
                except Exception as e:
                    print('Ugha', e)
                    pass

    return list({v['email']: v for v in result if len(v['email']) > 4}.values())


def get_recepients_from_roles(roles):
    persons = []

    try:
        for role in roles:
            resp = requests.get(
                '{}/{}?where={{"org_id": {}, "type_id": {}, "is_deleted": false, "is_passive": false }}&projection={{"person_id": 1}}'.format(
                    LUNGO_URL, 'functions', role.org, role.role),
                headers=LUNGO_HEADERS)

            if resp.status_code == 200:
                for item in resp.json().get('_items', []):
                    persons.append(item.get('person_id', 0))

        return get_recepients(list(set([i for i in persons if i > 0])))
    except:
        pass

    return persons


def get_org_name_text(org_id):

    status, result = get_org_name(org_id)
    if status is True:
        return result

    return 'Ukjent'


def get_person_name_text(person_id):
    status, result = get_person_name(person_id)
    if status is True:
        return result

    return 'Ukjent'


def notify(recepients, subject, message, prefix='NLF', subprefix='ORS'):
    ## TESTIONG
    recepients = list(set([301041]))

    msg = email.message.Message()
    msg['From'] = 'NLF Notifications <{}>'.format(EMAIL_CFG['from'])
    msg['Subject'] = '[{}.{}] {}'.format(prefix, app.config.get('APP_INSTANCE', '').upper(), subject)
    msg.add_header('Content-Type', 'text')
    msg.set_payload(message)

    send_async(recepients, msg)


# @async
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
