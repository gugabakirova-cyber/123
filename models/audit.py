from db import fetch_all


def get_audit_logs(location_id=None):
    query = '''
        SELECT
            a.*,
            l.name AS location_name
        FROM audit_logs a
        LEFT JOIN locations l ON l.id = a.location_id
        WHERE 1=1
    '''

    params = []

    if location_id:
        query += ' AND a.location_id = %s'
        params.append(location_id)

    query += ' ORDER BY a.created_at DESC'

    return fetch_all(query, tuple(params))