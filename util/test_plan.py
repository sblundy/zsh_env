import unittest
import io
import datetime
import plan


class TestPlan(unittest.TestCase):
    def test_current(self):
        buf = io.StringIO()
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        sut.set('6:30', 'test2')
        sut.current(buf, None)
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:00 test\n06:30 test2\n')

    def test_current_multiple(self):
        buf = io.StringIO()
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        sut.current(buf, None)
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:00 test\n')

    def test_current_gap(self):
        buf = io.StringIO()
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        sut.set('7:00', 'test3')
        sut.current(buf, None)
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:00 test\n06:30 \n07:00 test3\n')

    def test_current_with_start(self):
        buf = io.StringIO()
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        sut.set('6:30', 'test2')
        sut.current(buf, datetime.time(6, 30))
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:30 test2\n')

    def test_current_columns_env(self):
        buf = io.StringIO()
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        sut.set('6:30', 'test2')
        sut.current(buf, None, max_columns=10)
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:00 test\n06:30 tes…\n')


class TestPlanDb(unittest.TestCase):
    def test_from_tsv_string(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2\ta2.2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.current(buf)
        self.assertEqual(buf.getvalue(), 'Time  v1\n06:30 a2.2\n')

    def test_to_tsv_string(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2\ta2.2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.to_tsv_string(buf)
        self.assertEqual(buf.getvalue(), '06:00\ta1\t\r\n06:30\ta2\ta2.2\r\n')


if __name__ == '__main__':
    unittest.main()