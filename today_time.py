import datetime

def datetime_now():
    '''Method of defining current datetime'''
    return datetime.datetime.now().astimezone().strftime('%Y.%m.%d %H:%M:%S')