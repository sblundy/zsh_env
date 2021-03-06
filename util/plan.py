#!/usr/bin/env python3

import datetime
import shutil
import sys
import csv
import re
import math


class PlanDb:
    def __init__(self):
        self.plans = []

    def current(self, out, start=None, max_columns=None):
        if len(self.plans) > 0:
            plan = self.plans[len(self.plans) - 1]
            plan.current(out, start, max_columns=max_columns)

    def list(self, out, version=-1):
        if len(self.plans) > 0:
            plan_idx = version - 1 if version != -1 else len(self.plans) - 1
            self.plans[plan_idx].list(out)

    def set(self, time, action, cutoff=None):
        if len(self.plans) == 0:
            self.plans.append(Plan(1))
        plan = self.plans[len(self.plans) - 1]
        plan.set(time, action, cutoff)

    def replan(self, starting):
        if len(self.plans) > 0:
            old_plan = self.plans[len(self.plans) - 1]
            new_plan = Plan(len(self.plans) + 1)

            start_idx = to_time_index(starting.hour, starting.minute)
            for idx in range(start_idx, old_plan.max + 1):
                new_plan.set(to_time_str(idx), old_plan.get(to_time_str(idx)))
            self.plans.append(new_plan)

    def rm(self, time, cutoff=None):
        if len(self.plans) > 0:
            plan = self.plans[len(self.plans) - 1]
            plan.rm(time, cutoff)

    @staticmethod
    def from_tsv_string(tsvstr):
        plan_db = PlanDb()
        tsv = csv.reader(tsvstr, dialect=csv.excel_tab)
        for row in tsv:
            if len(row) > 1:
                time = row[0]
                if time != '':
                    for i in range(1, len(row)):
                        plan_idx = i - 1
                        if len(plan_db.plans) == plan_idx:
                            plan_db.plans.append(Plan(plan_idx + 1))
                        plan = plan_db.plans[plan_idx]
                        plan.set(time, row[i], None)
        return plan_db

    def to_tsv_string(self, out):
        tsv = csv.writer(out, dialect=csv.excel_tab)
        if len(self.plans) == 0:
            start_idx = 0
            end_idx = 47
        else:
            start_idx = self.plans[0].min
            end_idx = self.plans[0].max
            for plan in self.plans:
                start_idx = min(start_idx, plan.min)
                end_idx = max(end_idx, plan.max)

        for idx in range(start_idx, end_idx + 1):
            time = to_time_str(idx)
            row = [time]
            has_values = False
            for plan in self.plans:
                value = plan.get(time)
                row.append(value)
                if len(value) > 0:
                    has_values = True

            if has_values:
                tsv.writerow(row)

    @staticmethod
    def read(file_name):
        with open(file_name, newline='') as tsvfile:
            return PlanDb.from_tsv_string(tsvfile)

    def write(self, file_name):
        with open(file_name, newline='', mode='w') as tsvfile:
            self.to_tsv_string(tsvfile)


def ask_question(question):
    print(question)
    return sys.stdin.readline()


class Plan:
    def __init__(self, version, ask_question_func=ask_question):
        self.plan = []
        for _ in range(0, 48):
            self.plan.append('')
        self.version = version
        self.min = 48
        self.max = 0
        self.ask_question = ask_question_func

    def set(self, time, action, cutoff=None):
        curr = -1 if cutoff is None else to_time_index(cutoff.hour, cutoff.minute)
        for idx in parse_time(time):
            if idx < curr and idx < 24:
                answer = self.ask_question('Did you mean PM? [Y/n]')
                if answer.lower() != "n\n":
                    idx += 24
            if idx < self.min:
                self.min = idx
            if idx > self.max:
                self.max = idx
            self.plan[idx] = action

        while self.min < len(self.plan) and (self.plan[self.min] == '' or self.plan[self.min] is None):
            self.min += 1

        while self.max >= 0 and (self.plan[self.max] == '' or self.plan[self.max] is None):
            self.max -= 1

    def rm(self, time, cutoff=None):
        self.set(time, '', cutoff)

    def get(self, time):
        return self.plan[to_time_index_from_string(time)]

    def current(self, out, start, max_columns=None):
        if start is None:
            start_idx = self.min
        else:
            idx = to_time_index(start.hour, start.minute)
            start_idx = max(idx, self.min)
        self._print_list(out, start_idx, max_columns)

    def _print_list(self, out, start_idx, max_columns=None):
        print('\x1B[1mTime  v' + str(self.version) + '\x1B[0m', file=out)
        for idx in range(start_idx, self.max + 1):
            line = to_time_str(idx) + ' ' + ('' if self.plan[idx] is None else self.plan[idx])
            if max_columns is not None and len(line) > max_columns:
                line = line[0:max_columns - 1] + '…'
            print(line, file=out)

    def list(self, out):
        self._print_list(out, self.min)


class TimeFormatException(Exception):
    def __init__(self, message):
        self.message = message


TIME_REGEX = re.compile(r"([012]?\d)(?::(\d\d))?")
TIME_RANGE = re.compile(r"([0-9:]{1,5})-([0-9:]{1,5})")
TIME_RANGE_EXCLUSIVE = re.compile(r"(1?\d:[0-5]\d [AP]M) - (1?\d:[0-5]\d [AP]M)")
TIME_RANGE_EXCLUSIVE_FORMAT = '%I:%M %p'


def parse_time(time):
    exclusive_result = TIME_RANGE_EXCLUSIVE.match(time)
    if exclusive_result is not None:
        start = datetime.datetime.strptime(exclusive_result.group(1), TIME_RANGE_EXCLUSIVE_FORMAT)
        end = datetime.datetime.strptime(exclusive_result.group(2), TIME_RANGE_EXCLUSIVE_FORMAT)
        return range(to_time_index(start.hour, start.minute), to_time_index(end.hour, end.minute))
    times = []
    for segment in time.split(','):
        (start, end) = parse_range(segment)
        if end is None:
            times.append(start)
        else:
            times.extend(range(start, end + 1))
    return times


def parse_range(time):
    result = TIME_RANGE.match(time)
    if result is None:
        return to_time_index_from_string(time), None
    start = result.group(1)
    end = result.group(2)
    return to_time_index_from_string(start), to_time_index_from_string(end)


def to_time_index_from_string(time):
    result = TIME_REGEX.match(time)
    if result is None:
        raise TimeFormatException('"' + time + '" is not a valid time')
    hour = int(result.group(1))
    minute = 0 if result.group(2) is None else int(result.group(2))

    return to_time_index(hour, minute)


def to_time_index(hour, minute):
    if minute < 30:
        return hour * 2
    else:
        return (hour * 2) + 1


def to_time_str(idx):
    hour: int = math.floor(idx / 2)
    minute = 0 if idx % 2 == 0 else 30
    t = datetime.time(hour, minute)
    return t.strftime('%H:%M')


def main():
    file = sys.argv[1]
    action = sys.argv[2]

    plan = PlanDb.read(file)
    try:
        if action == 'current':
            size = shutil.get_terminal_size((-1, -1))
            max_columns = size.columns if size.columns != -1 else None
            plan.current(sys.stdout, datetime.datetime.now().time(), max_columns=max_columns)
        elif action == 'list':
            version = -1 if len(sys.argv) < 4 else int(sys.argv[3])
            plan.list(sys.stdout, version)
        elif action == 'replan':
            plan.replan(datetime.datetime.now().time())
            plan.write(file)
        elif action == 'set':
            plan.set(sys.argv[3], sys.argv[4], datetime.datetime.now().time())
            plan.write(file)
        elif action == 'rm':
            plan.rm(sys.argv[3], datetime.datetime.now().time())
            plan.write(file)
    except TimeFormatException as err:
        print(err.message, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
