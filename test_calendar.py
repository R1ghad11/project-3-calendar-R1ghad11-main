
"""
A test module to validate the Calendar functionalities.

Author: Ziyad Alsaeed
Email: zalsaeed@qu.edu.sa
"""

import time
import unittest
from datetime import datetime

import generator
from calendar import Calendar
from appointment import WorkAppointment


class TestCalendar(unittest.TestCase):
    """
    A calendar unittest class.
    """

    def setUp(self):
        """
        Setting up the common test data for each test case
        """
        self.work_app1 = WorkAppointment("IT315 Lecture",
                                         datetime(2022, 9, 25, 10, 15),
                                         datetime(2022, 9, 25, 12, 25))
        self.work_app2 = WorkAppointment("IT315 Lab1",
                                         datetime(2022, 9, 27, 8, 0),
                                         datetime(2022, 9, 27, 10, 10))
        self.work_app3 = WorkAppointment("IT315 Lab2",
                                         datetime(2022, 9, 27, 12, 30),
                                         datetime(2022, 9, 27, 14, 40))

    def test_append(self):
        """
        Validate that we implement the same list append behaviour
        by adding the same elements to a local list.
        """
        c1 = Calendar()
        my_list = []
        c1.append(self.work_app1)
        my_list.append(self.work_app1)
        c1.append(self.work_app2)
        my_list.append(self.work_app2)
        c1.append(self.work_app3)
        my_list.append(self.work_app3)
        self.assertEqual(c1.appointments, my_list)

    def test_len(self):
        """
        Validate the length (len) function is implemented
        for the Calendar class even though it doesn't extend the
        list class.
        """
        c1 = Calendar()
        self.assertEqual(0, len(c1))
        c1.append(self.work_app1)
        c1.append(self.work_app2)
        c1.append(self.work_app3)
        self.assertEqual(3, len(c1))

    def test_sort(self):
        """
        Validate the sort functionality of the calendar.
        Appointments in the calendar should be sorted based
        on their start time.
        """
        my_list = [self.work_app1, self.work_app2, self.work_app3]
        c1 = Calendar()
        c1.append(self.work_app3)
        c1.append(self.work_app2)
        c1.append(self.work_app1)
        c1.sort()
        self.assertEqual(my_list, c1.appointments)

    def test_intersect_total(self):
        """
        Validate the correctness of the calculating the
        total intersection duration. Intersect duration is
        calculated within the Appointment class.
        However, we need to find the total intersect time in
        whole calendar.
        """
        # overlapping appointment with a total of 1.5 hours of intersection
        # 1:00AM ----        2:00AM first    (overlaps with second) + 0.5 = 0.5
        # 1:30AM   ----      2:30AM second   (overlaps with third; first already counted) + 0.5 = 1.0
        # 2:00AM     ----    3:00AM third    (overlaps with third; second already counted) + 0.5 = 1.5
        # 2:30AM       ----  3:30AM fourth   (nothing starts after it)
        app1 = WorkAppointment("First", datetime(2022, 1, 1, 1, 0), datetime(2022, 1, 1, 2, 0))
        app2 = WorkAppointment("second", datetime(2022, 1, 1, 1, 30), datetime(2022, 1, 1, 2, 30))
        app3 = WorkAppointment("third", datetime(2022, 1, 1, 2, 0), datetime(2022, 1, 1, 3, 0))
        app4 = WorkAppointment("fourth", datetime(2022, 1, 1, 2, 30), datetime(2022, 1, 1, 3, 30))

        # try them sorted already
        c1 = Calendar()
        c1.append(app1)
        c1.append(app2)
        c1.append(app3)
        c1.append(app4)
        self.assertEqual(1.5, c1.total_intersections())

        # now change the sorting
        c1 = Calendar()
        c1.append(app3)
        c1.append(app1)
        c1.append(app4)
        c1.append(app2)
        self.assertEqual(1.5, c1.total_intersections())

        # three overlapping appointments (total intersect = 2.0)
        # 1:00AM ---------------- 3:00AM fifth   (overlaps with sixth and seventh) + 1.5 = 1.5
        # 2:00AM        --------- 3:00AM sixth   (overlaps  with seventh; fifth is already counted) + 0.5 = 2.0
        # 2:30AM             ---- 3:00AM seventh (nothing starts after it) + 0.0 = 2.0
        app5 = WorkAppointment("fifth", datetime(2022, 1, 1, 1, 0), datetime(2022, 1, 1, 3, 0))
        app6 = WorkAppointment("sixth", datetime(2022, 1, 1, 2, 0), datetime(2022, 1, 1, 3, 0))
        app7 = WorkAppointment("seventh", datetime(2022, 1, 1, 2, 30), datetime(2022, 1, 1, 3, 0))

        # try them sorted already
        c1 = Calendar()
        c1.append(app5)
        c1.append(app6)
        c1.append(app7)
        self.assertEqual(2.0, c1.total_intersections())

        # what about if we try them all?
        # overlapping appointment with a total of 1.5 hours of intersection
        # 1:00AM -------            2:00AM first    (overlaps with second and fifth) + 1.5 = 1.5
        # 1:30AM   -------          2:30AM second   (overlaps with third, fifth, and sixth; first already counted) + 2.0 = 3.5
        # 2:00AM        -------     3:00AM third    (overlaps with fourth, fifth, sixth, and seventh; second already counted) + 3.0 = 6.5
        # 2:30AM           -------  3:30AM fourth   (overlaps with fifth, sixth and seventh, third already counted) + 1.5 = 8.0
        # 1:00AM ----------------   3:00AM fifth    (overlaps with sixth and seventh, everything else already counted) + 1.5 = 9.5
        # 2:00AM        ---------   3:00AM sixth    (overlaps  with seventh; everything else already counted) + 0.5 = 10.0
        # 2:30AM            -----   3:00AM seventh  (nothing starts after it) + 0.0 = 10.0
        c1 = Calendar()
        c1.append(app1)
        c1.append(app2)
        c1.append(app3)
        c1.append(app4)
        c1.append(app5)
        c1.append(app6)
        c1.append(app7)
        self.assertEqual(10.0, c1.total_intersections())

    def test_intersect_speed(self):
        """
        In addition to validity, we need to test performance of the
        intersection calculation. Hints are given in the handouts.
        This test case assume validate intersect calculation where
        appointments are sorted and actually have no overlaps at all.
        In this case we expect you to check 10,000 appointments
        in less than 2 seconds.
        """
        # get a calendar with 10,000 appointments
        big_calender = generator.deterministic_generator(10_000)
        assert len(big_calender) == 10_000  # sanity check

        time_before = time.perf_counter()
        _ = big_calender.total_intersections()  # we don't care about the value, _ means we throw it away
        time_after = time.perf_counter()
        elapsed_seconds = time_after - time_before
        self.assertLess(elapsed_seconds, 2, f"Are you sure your algorithm is fast enough ({elapsed_seconds} >= 2)?")
        print(f"Good work! It took you {elapsed_seconds} seconds.")

    def test_intersect_speed_random_data(self):
        """
        Again validate the performance if calculating the intersections total.
        But now we know nothing about the data we are getting.
        """
        # get a calendar with 10,000 random appointments
        big_calender = generator.non_deterministic_generator(10_000)
        assert len(big_calender) == 10_000  # sanity check

        time_before = time.perf_counter()
        _ = big_calender.total_intersections()  # we don't care about the value, _ means we throw it away
        time_after = time.perf_counter()
        elapsed_seconds = time_after - time_before
        self.assertLess(elapsed_seconds, 2, f"Are you sure your algorithm is fast enough ({elapsed_seconds} >= 2)?")
        print(f"Good work! It took you {elapsed_seconds} seconds.")


if __name__ == '__main__':
    unittest.main()
