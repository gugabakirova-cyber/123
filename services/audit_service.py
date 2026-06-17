from db import execute_query


def add_audit_log(username, location_id, action_type, object_name, details=''):

    execute_query(
        '''
        INSERT INTO audit_logs (
            username,
            location_id,
            action_type,
            object_name,
            details
        )
        VALUES (%s,%s,%s,%s,%s)
        ''',
        (
            username,
            location_id,
            action_type,
            object_name,
            details
        )
    )