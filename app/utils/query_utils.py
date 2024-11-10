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


def get_period(args: Dict[str, str]) -> Tuple[datetime, datetime]:
    if 'period' in args and args['period'] == 'daily':
        # if args['period'] == 'daily':
        if 'to' in args:
            return (get_query_date(args['to']).replace(hour=0, 
                                                     minute=0, 
                                                     second=0, 
                                                     microsecond=0), 
                    get_query_date(args['to']).replace(hour=23, 
                                                   minute=59, 
                                                   second=59, 
                                                   microsecond=59))
        else:
            return (datetime.datetime.now().replace(hour=0, 
                                                     minute=0, 
                                                     second=0, 
                                                     microsecond=0), 
                    datetime.datetime.now().replace(hour=23, 
                                                   minute=59, 
                                                   second=59, 
                                                   microsecond=59))
        
    return get_sum_period(args)

    

def get_transport_type(args: Dict[str, str]):
    if 'transport_type' in args:
        return args['transport_type']
    else:
        return None

def get_product_category(args: Dict[str, str]):
    if 'product_category' in args:
        return args['product_category']
    else:
        return None