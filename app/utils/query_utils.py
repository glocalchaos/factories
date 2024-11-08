from datetime import datetime
from typing import Dict, Tuple

QUERY_DATE_FORMAT = '%d.%m.%Y'

def get_query_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, QUERY_DATE_FORMAT)

def validate_period(): # TODO
    pass

def get_sum_period(args: Dict[str, str]) -> Tuple[datetime, datetime]:
    if 'to' in args:
        to_date = get_query_date(args['to'])
    else:
        to_date = datetime.now()
    
    if 'from' in args:
        from_date = get_query_date(args['from'])
    else:
        from_date = to_date.replace(day=1, hour=0, minute=0, microsecond=0)

    return from_date, to_date

    
