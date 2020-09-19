import datetime

def stamp_to_dt(timestamp):
    '''Transfer timestamp to date time
    Use example: stamp_to_dt(1590988249)

    :param timestamp: timestamp to be transformed
    :type timestamp: timestamp

    :returns: transformed date time
    :rtype: datetime
    '''

    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt

def str_to_dt(dt_str):
    '''Transfer string format date time to date time
    Use example: str_to_dt('2020-09-01 11:15:50')

    :param dt_str: date time in string format, such as '2020-09-01 11:15:49' (%Y-%m-%d %H:%M:%S)
    :type dt_str: str

    :returns: transformed date time
    :rtype: datetime
    '''
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    return dt

def dt_to_stamp(dt):
    '''Transfer date time to timestamp
    Use example: dt_to_stamp(datetime.now())

    :param dt_str: date time, such as '2020-09-01 11:15:49' (%Y-%m-%d %H:%M:%S)
    :type dt_str: str

    :returns: transformed timestamp
    :rtype: timestamp
    '''

    timestamp = datetime.datetime.timestamp(dt)
    return timestamp

def str_to_stamp(dt_str):
    '''Transfer string to timestamp
    Use example: str_to_stamp('2020-09-01 11:15:50')

    :param dt_str: string date time, such as '2020-09-01 11:15:49' (%Y-%m-%d %H:%M:%S)
    :type dt_str: str

    :returns: transformed timestamp
    :rtype: timestamp
    '''
    timestamp = dt_to_stamp(str_to_dt(dt_str))
    return timestamp
