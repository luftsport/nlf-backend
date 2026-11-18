from flask import g
from ext.scf import ACL_SUPERADMINS
def before_patch(request, response):
    
    #id == id!!
    if g._id != request._id:
        resp = Response(None, 401)
        abort(403, description="You can't edit someone else's account", response=resp)
        

def after_fetch(response):
    """ This is called after the GET request is processed in db layer
    """

    # If the user is not a superadmin, then they can only get their own account
    if g.id != response.get('id', None) and g.id not in ACL_SUPERADMINS:
        response.pop('settings', None)
        response.pop('acl', None)
        response.pop('default', None)
        response.pop('info', None)
        response.pop('statistics', None)
        response.pop('_version', None)
