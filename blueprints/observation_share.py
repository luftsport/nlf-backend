
from flask import g, Blueprint, current_app as app, request, Response, abort, jsonify
from bson import json_util
import json

from eve.methods.patch import patch_internal

# Need custom decorators
from ext.app.decorators import *
from datetime import datetime
from ext.notifications.email import Email  # , Sms
from ext.app.lungo import get_person_email

OrsShare = Blueprint('Observation Share', __name__, )

@OrsShare.route("/<int:observation_id>", methods=['POST'])
@require_token()
def share_observation(observation_id):
    
    args = request.get_json() #use force=True to do anyway!
    users = args.get('recepients')
    
    mail = Email()

    raise NotImplementedError
    recepients = get_person_email(users)
    status, action_by = get_person_email(g.user_id)
        
    subject = '%s har delt observasjon #%i' % (action_by, observation_id)
    
    message = {}
    message.update({'observation_id': observation_id})
    message.update({'action_by': action_by})
    message.update({'action': 'delt'})
    message.update({'title': args.get('title')})
    #message.update({'club': self.helper.get_melwin_club_name(self.db_wf.get('club'))})
    message.update({'date': datetime.today().strftime('%Y-%m-%d %H:%M')})
    message.update({'url': 'app/obs/#!/observation/report/%i\n' % observation_id})
    message.update({'url_root': request.url_root})
    message.update({'comment': args.get('comment')})
    message.update({'context': 'shared'})
    
    mail.add_message_html(message, 'ors')                                                                                                                                              
    mail.add_message_plain(message, 'ors') 
        
    mail.send(recepients, subject, 'OBSREG')
    
    return Response(json.dumps({'status': 'ok', 'code': 200}),  mimetype='application/json')
