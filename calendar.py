"""
This is the Calendar Module. 
We gave you some basic methods.
Please implement all the methods that says FIX ME!

author: Ziyad Alsaeed
email: zalsaeed@qu.edu.sa
"""

from appointment import Appointment


class Calendar:

    def __init__(self):
        """
        We initialize a Calendar by having an empty list.
        It is already done for you!
        """
        self.appointments = []

    def append(self, element: "Appointment"):
        """
        Adding a new appointment to our Calendar!

        :param element: A instant of an Appointment class or any of its children.
        """
        self.appointments.append(element)

    def __str__(self) -> str:
        """
        We print a Calendar by having each appointment in a new line
        :return: A long list of appointments!
        """
        lines = [str(app) for app in self.appointments]
        return '\n'.join(lines)

    def __len__(self) -> int:
        """
        By implementing __len__ we then can say len(calendar) which should
        return the number of items in our list. Thus, you should 'delegate'
        the len of appointment list to this method.
        :return: The number of elements in our list of appointments.
        """
        return len(self.appointments)

    def sort(self):
        """
        Sort the element of the list based on their start time!
        You need this to be efficient in calculating the intersections.
        """
        self.appointments.sort(key=lambda app: app.start_time)

    def total_intersections(self) -> float:
        """
        For all the appointments this calendar has.
        It should go over all of them checking for conflict.
        If there is one, then it should keep track of the intersection total.
        Intersections as defined in the Appointment class are the duration of overlap in hour.
        This intersection value should be calculated in the Appointment class itself.
        This method main goal is to find the total intersection value in an efficient time.
        Your algorithm must run in time O(n lg n) where n is max(number of appointments, number of conflicts).

        :return: Total intersection time in hours.
        """
        total_intersection = 0.0
        self.sort()  # sort appointments by start time
        for i, app1 in enumerate(self.appointments):
            for app2 in self.appointments[i + 1:]:
                if app2.start_time >= app1.end_time:
                    break  # no more overlaps
                total_intersection += app1.intersect(app2)
        return total_intersection
