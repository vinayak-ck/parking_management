# parking/utils.py
from django.utils.dateformat import format as dj_format

def owner_to_dict(o):
    return {'id': o.id, 'name': o.name}

def vehicle_to_dict(v):
    return {
        'id': v.id,
        'owner': owner_to_dict(v.owner),
        'vehicle_number': v.vehicle_number,
        'vehicle_type': v.vehicle_type,
    }

def pass_to_dict(p):
    return {
        'id': p.id,
        'vehicle': vehicle_to_dict(p.vehicle),
        'pass_type': p.pass_type,
        'issue_date': p.issue_date.isoformat(),
        'expiry_date': p.expiry_date.isoformat(),
    }

def tx_to_dict(t):
    return {
        'id': t.id,
        'vehicle': vehicle_to_dict(t.vehicle),
        'entry_time': t.entry_time.isoformat(),
        'exit_time': t.exit_time.isoformat() if t.exit_time else None,
        'fees_paid': float(t.fees_paid) if t.fees_paid is not None else None,
    }
