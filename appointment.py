
"""
This is a skeleton of the Appointment module. 
Most of your implementations should be in the Appointment
class. Only the ones that are special for each subtype 
will be implemented in the subtype.

author: Ziyad Alsaeed
email: zalsaeed@qu.edu.sa
"""

import datetime
import utility


class Appointment:

    def __init__(self, title: str, start_time: datetime, end_time: datetime):
        if type(self) is Appointment:
            raise NotImplementedError("I'm an abstract class!")
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def priority(self) -> int:
        raise NotImplementedError("I'm an abstract class!")

    def __str__(self):
        return f"{self.start_time} - {self.end_time} | {self.title}"

    def __lt__(self, other):
        return self.end_time <= other.start_time

    def __gt__(self, other):
        return self.start_time >= other.end_time

    def __eq__(self, other):
        return self.start_time == other.start_time and self.end_time == other.end_time

    def overlap(self, other):
        if self < other or self > other:
            return False
        else:
            return True

    def intersect(self, other) -> float:
        if self.start_time == other.start_time and self.end_time == other.end_time:
            return utility.convert_timedelta_to_hours(self.end_time - self.start_time)
        else:
            if self.overlap(other):
                start_overlap = max(self.start_time, other.start_time)
                end_overlap = min(self.end_time, other.end_time)
                return utility.convert_timedelta_to_hours(end_overlap - start_overlap)
            else:
                return 0  # If there's no overlap, it returns 0.


class WorkAppointment(Appointment):
        def __init__(self, title: str, start_time: datetime, end_time: datetime):
            if end_time <= start_time:
                raise ValueError("End time must be after start time")
            super().__init__(title, start_time, end_time)

        def priority(self) -> int:
            return 1  # Work appointments have priority 1


class PersonalAppointment(Appointment):
    def __init__(self, title: str, start_time: datetime, end_time: datetime):
        if end_time <= start_time:
            raise ValueError("End time must be after start time")
        super().__init__(title, start_time, end_time)

    def priority(self) -> int:
        return 2  # Personal appointments have priority 2
