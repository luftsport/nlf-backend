from flask import current_app as app


def increment(counter):
    seq = app.data.driver.db['seq']

    try:
        result = seq.update_one({'c': counter}, {'$inc': {'i': int(1)}}, True)

        if result.matched_count > 0:
            seq_r = seq.find_one({'c': counter}, {'i': 1, '_id': 0})

            if seq_r:
                return int(seq_r.get('i'))
        raise Exception('Could not increment {}'.format(counter))
    except Exception as e:
        pass

    return False
