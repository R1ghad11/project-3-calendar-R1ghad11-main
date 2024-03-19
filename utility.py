
"""
This is a utility module. 
It only has helper methods that you might find useful.

author: Ziyad Alsaeed
email: zalsaeed@qu.edu.sa
"""

from datetime import timedelta


def convert_timedelta_to_hours(td: timedelta) -> float:
    """
    A method that takes a timedelta (a timedelta is duration
    representation that you would get if you subtract two 
    times from each other), and return the duration given 
    in hours. 

    :param td: A duration (for example 11 days!)
    :return: The duration given in hours. 
    """
    sec_per_hour = 60 * 60  # minutes * seconds
    return td.total_seconds()/sec_per_hour
