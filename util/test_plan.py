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

    def test_get(self):
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        output = sut.get('6:00')
        self.assertEqual(output, 'test')

    def test_get_invalid(self):
        sut = plan.Plan(1)
        sut.set('6:00', 'test')
        with self.assertRaises(plan.TimeFormatException):
            sut.get('xxxx')

    def test_set_range(self):
        sut = plan.Plan(1)
        sut.set('6:00-6:30', 'test')
        output = sut.get('6:00')
        self.assertEqual(output, 'test')
        output = sut.get('6:30')
        self.assertEqual(output, 'test')
        output = sut.get('7:00')
        self.assertEqual(output, '')


class TestPlanDb(unittest.TestCase):
    def test_from_tsv_string(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2\ta2.2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.current(buf)
        self.assertEqual(buf.getvalue(), 'Time  v2\n06:30 a2.2\n')

    def test_to_tsv_string(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2\ta2.2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.to_tsv_string(buf)
        self.assertEqual(buf.getvalue(), '06:00\ta1\t\r\n06:30\ta2\ta2.2\r\n')

    def test_updates_current_plan(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2\ta2.2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.set('6:30', 'a2.3')
        sut.current(buf)
        self.assertEqual(buf.getvalue(), 'Time  v2\n06:30 a2.3\n')

    def test_replan(self):
        tsv = io.StringIO('6:00\ta1\r\n6:30\ta2')
        buf = io.StringIO()
        sut = plan.PlanDb.from_tsv_string(tsv)
        sut.replan(datetime.time(6, 30))
        sut.current(buf, start=datetime.time(6, 30))
        self.assertEqual(buf.getvalue(), 'Time  v2\n06:30 a2\n')

    def test_set_on_empty_plan(self):
        buf = io.StringIO()
        sut = plan.PlanDb()
        sut.set('12:00', 'test')
        sut.current(buf, start=datetime.time(12, 00))
        self.assertEqual(buf.getvalue(), 'Time  v1\n12:00 test\n')

    def test_to_tsv_string_on_empty_plan(self):
        buf = io.StringIO()
        sut = plan.PlanDb()
        sut.to_tsv_string(buf)
        self.assertGreater(len(buf.getvalue()), len("00:00\r\n"))
        self.assertEqual(buf.getvalue()[0:7], "00:00\r\n")


class TestTimeStringParsing(unittest.TestCase):
    def test_simple(self):
        output = plan.toindex('6:00')
        self.assertEqual(output, 12)

    def test_hour_only(self):
        output = plan.toindex('6')
        self.assertEqual(output, 12)

    def test_range_single_time(self):
        output = plan.parse_range('6:00')
        self.assertEqual(output, (12, None))

    def test_range(self):
        output = plan.parse_range('6:00-7:00')
        self.assertEqual(output, (12, 14))


if __name__ == '__main__':
    unittest.main()
