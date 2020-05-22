import json


def add_delete_filters(request, lookup):
    """Adding a delete filter by adding a where filter to the collection"""
    if 'where' in request.args and len(lookup) == 0:  # '_id' not in lookup:
        conditions = request.args.getlist('where')
        for cond_str in conditions:
            cond = json.loads(cond_str)
            for attrib in cond:
                lookup[attrib] = cond[attrib]
