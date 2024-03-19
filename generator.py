
"""
This is a generator module. 
You don't have to understand it. 
It is used for generating test data.

author: Ziyad Alsaeed
email: zalsaeed@qu.edu.sa
"""

from random import randint
from datetime import datetime, timedelta

from appointment import WorkAppointment
from calendar import Calendar


def deterministic_generator(number_of_appointments: int) -> Calendar:

    start_date = datetime(2022, 9, 1, 0, 0)
    end_date = datetime(2022, 9, 1, 0, 59)

    c = Calendar()
    for i in range(number_of_appointments):
        app = WorkAppointment(f"Sample {i+1}", start_date + timedelta(hours=i), end_date + timedelta(hours=i))
        c.append(app)
    return c


def non_deterministic_generator(number_of_appointments: int) -> Calendar:
    c = Calendar()
    for i in range(number_of_appointments):
        # get a random date
        start_date = datetime(2022, randint(9, 10), randint(1, 28), randint(0, 23), randint(0, 59))
        end_date = start_date + timedelta(hours=randint(1, 5))
        app = WorkAppointment(f"Sample {i+1}", start_date, end_date)
        c.append(app)
    return c
