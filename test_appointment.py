"""
A test module to go over all the appointment classes.

Author: Ziyad Alsaeed
Email: zalsaeed@qu.edu.sa
"""

import unittest
from datetime import datetime

from appointment import Appointment, WorkAppointment, PersonalAppointment


class TestAppointment(unittest.TestCase):
    """
    An appointments unittest class.
    """

    def setUp(self):
        """
        Setting up common data for each test case.
        """
        self.personal_app1 = PersonalAppointment("Coffee with family",
                                                 datetime(2022, 9, 25, 17, 20),
                                                 datetime(2022, 9, 25, 18, 20))
        self.personal_app2 = PersonalAppointment("Hangout with friends",
                                                 datetime(2022, 9, 25, 19, 30),
                                                 datetime(2022, 9, 25, 23, 30))
        self.work_app1 = WorkAppointment("IT315 Lecture",
                                         datetime(2022, 9, 25, 10, 15),
                                         datetime(2022, 9, 25, 12, 25))
        self.work_app2 = WorkAppointment("IT315 Lab1",
                                         datetime(2022, 9, 27, 8, 0),
                                         datetime(2022, 9, 27, 10, 10))
        self.work_app3 = WorkAppointment("IT315 Lab2",
                                         datetime(2022, 9, 27, 12, 30),
                                         datetime(2022, 9, 27, 14, 40))

        self.time_x1 = datetime(2022, 9, 25, 10, 15)
        self.time_x2 = datetime(2022, 9, 25, 9, 15)
        self.time_x3 = datetime(2022, 9, 25, 10, 15)

    def test_init_abstract_class(self):
        """
        The abstract class should never be initialized.
        In this test we make sure that the correct
        exception is thrown when someone tries to create
        an instance of our abstract class.
        """
        self.assertRaises(NotImplementedError, lambda: Appointment("dummy appointment", self.time_x2, self.time_x1))

    def test_init_appointments_with_negative_period(self):
        """
        When creating an appointment, the end (date, time)
        should never be smaller than the start (date, time).
        If someone tries it, the class should trow a ValueError exception.

        In this test case, we try to check if the correct exception is thrown.
        """
        # time_x2 comes before time_x1, this shouldn't be possible.
        self.assertRaises(ValueError, lambda: WorkAppointment("Wrongly timed", self.time_x1, self.time_x2))


        # time_x3 equal time_x1, which means the appointment is for zero seconds! This also shouldn't be possible.
        self.assertRaises(ValueError, lambda: WorkAppointment("Wrongly timed", self.time_x1, self.time_x3))

        # the same with the Personal Appointment
        self.assertRaises(ValueError, lambda: PersonalAppointment("Wrongly timed", self.time_x1, self.time_x2))
        self.assertRaises(ValueError, lambda: PersonalAppointment("Wrongly timed", self.time_x1, self.time_x3))

    def test_prints(self):
        """
        Are appointments printed as we want (hint: __str__)?
        """
        self.assertEqual("2022-09-25 10:15:00 - 2022-09-25 12:25:00 | IT315 Lecture", str(self.work_app1))
        self.assertEqual("2022-09-27 08:00:00 - 2022-09-27 10:10:00 | IT315 Lab1", str(self.work_app2))
        self.assertEqual("2022-09-27 12:30:00 - 2022-09-27 14:40:00 | IT315 Lab2", str(self.work_app3))
        self.assertEqual("2022-09-25 17:20:00 - 2022-09-25 18:20:00 | Coffee with family", str(self.personal_app1))
        self.assertEqual("2022-09-25 19:30:00 - 2022-09-25 23:30:00 | Hangout with friends", str(self.personal_app2))

    def test_priority(self):
        """
        Each subtype of the abstract class, has it own priority code.
        Here we check if the right code is returned based on each type.
        """
        self.assertEqual(1, self.work_app1.priority())
        self.assertEqual(2, self.personal_app1.priority())

    def test_order(self):
        """
        Using __lt__ and __gt__ we should be able to check if an appointment
        comes before or after the other.
        """
        self.assertTrue(self.work_app1 < self.work_app2)
        self.assertFalse(self.work_app1 > self.work_app2)
        self.assertTrue(self.work_app2 > self.work_app1)
        self.assertFalse(self.work_app2 < self.work_app1)

        self.assertTrue(self.work_app2 < self.work_app3)
        self.assertFalse(self.work_app2 > self.work_app3)

        self.assertTrue(self.work_app1 < self.personal_app1)
        self.assertFalse(self.work_app1 > self.personal_app1)

        # an example of an appointment that starts after the other immediately
        personal1 = PersonalAppointment('first', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        personal2 = PersonalAppointment('second', datetime(2022, 10, 1, 1, 0), datetime(2022, 10, 1, 2, 0))

        self.assertEqual(datetime(2022, 10, 1, 1, 0), datetime(2022, 10, 1, 1, 0))
        self.assertTrue(personal1 < personal2)
        self.assertFalse(personal1 > personal2)
        self.assertTrue(personal2 > personal1)
        self.assertFalse(personal2 < personal1)

    def test_equality(self):
        """
        Two appointments are equal to each other if they
        have the same start_time and end_time.
        The tite doesn't matter in this case.
        """
        persona1 = PersonalAppointment('Not Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        work = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        self.assertEqual(persona1, work)

    def test_inequality(self):
        """
        If you applied the equality correctly this test case should
        pass by default.
        """
        persona1 = PersonalAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 2, 0))
        work = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        self.assertNotEqual(persona1, work)

    def test_overlap(self):
        """
        Two appointments are overlapping if they have occurred during
        the same time for any portion of their durations.
        """
        # These two overlap!
        app1 = PersonalAppointment('Not Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 2, 0))
        app2 = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))

        # This one doesn't overlap with any of them! It is NEXT YEAR
        diff_app = WorkAppointment('Working', datetime(2023, 10, 1, 0, 0), datetime(2023, 10, 1, 1, 0))

        self.assertTrue(app1.overlap(app2))
        self.assertTrue(app2.overlap(app1))
        self.assertFalse(app1.overlap(diff_app))
        self.assertFalse(app2.overlap(diff_app))

    def test_interest(self):
        """
        If methods overlap, then we should know how
        long they overlap (in hours).
        """
        # These two intersect for a duration of exactly one hour
        same1 = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        same2 = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        self.assertEqual(1.0, same1.intersect(same2))

        # one is much longer than the other
        starts_first_ends_second = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 3, 0))
        starts_second_ends_first = WorkAppointment('Working', datetime(2022, 10, 1, 1, 0), datetime(2022, 10, 1, 2, 0))
        self.assertEqual(1.0, starts_first_ends_second.intersect(starts_second_ends_first))

        # opposite of the above but ends overlap for half-an-hour
        start_second_ends_first = WorkAppointment('Working', datetime(2022, 10, 1, 1, 0), datetime(2022, 10, 1, 1, 30))
        starts_first_ends_second = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 3, 0))
        self.assertEqual(0.5, start_second_ends_first.intersect(starts_first_ends_second))

        # one starts before the other starts and ends before the other ends
        starts_first_ends_first = WorkAppointment('Working', datetime(2022, 10, 1, 0, 0), datetime(2022, 10, 1, 1, 0))
        starts_second_ends_second = WorkAppointment('Working', datetime(2022, 10, 1, 0, 30),
                                                    datetime(2022, 10, 1, 2, 0))
        self.assertEqual(0.5, starts_first_ends_first.intersect(starts_second_ends_second))
        self.assertEqual(0.5, starts_second_ends_second.intersect(starts_first_ends_first))


if __name__ == '__main__':
    unittest.main()
