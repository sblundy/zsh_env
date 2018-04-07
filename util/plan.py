#!/usr/bin/env python3

import datetime
import sys
import csv
import re
import math


class PlanDb:
    def __init__(self):
        self.plans = []

    def current(self, out, start=None):
        if len(self.plans) > 0:
            plan = self.plans[len(self.plans) - 1]
            plan.current(out, start)

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
                            plan_db.plans.append(Plan(plan_idx))
                        plan = plan_db.plans[plan_idx]
                        plan.set(time, row[i])
        return plan_db

    def to_tsv_string(self, out):
        tsv = csv.writer(out, dialect=csv.excel_tab)
        start_idx = self.plans[0].min
        end_idx = self.plans[0].max
        for plan in self.plans:
            start_idx = min(start_idx, plan.min)
            end_idx = max(end_idx, plan.max)

        for idx in range(start_idx, end_idx + 1):
            time = to_time_str(idx)
            row = [time]
            for plan in self.plans:
                row.append(plan.get(time))

            tsv.writerow(row)

    @staticmethod
    def read(file_name):
        with open(file_name, newline='') as tsvfile:
            return PlanDb.from_tsv_string(tsvfile)

    @staticmethod
    def init(file_name):
        with open(file_name, newline='', mode='w') as tsvfile:
            tsv = csv.writer(tsvfile, dialect=csv.excel_tab)
            for idx in range(0, 48):
                tsv.writerow([to_time_str(idx)])


class Plan:
    def __init__(self, version):
        self.plan = []
        for i in range(0, 48):
            self.plan.append('')
        self.version = version
        self.min = 48
        self.max = 0

    def set(self, time, action):
        idx = toindex(time)
        if idx < self.min:
            self.min = idx
        if idx > self.max:
            self.max = idx
        self.plan[idx] = action

    def get(self, time):
        return self.plan[toindex(time)]

    def current(self, out, start):
        # TODO respect COLUMNS env variable
        if start is None:
            start_idx = self.min
        else:
            idx = (start.hour * 2)
            if start.minute >= 30:
                idx = idx + 1
            start_idx = max(idx, self.min)

        print('Time  v' + str(self.version), file=out)
        for idx in range(start_idx, self.max + 1):
            print(to_time_str(idx) + ' ' + self.plan[idx], file=out)


TIME_REGEX = re.compile("([012]?\d):(\d\d)")


def toindex(time):
    result = TIME_REGEX.match(time)
    assert result is not None
    hour = int(result.group(1))
    minute = int(result.group(2))

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

    if action == 'current':
        plan = PlanDb.read(file)
        plan.current(sys.stdout, datetime.datetime.now().time())
    elif action == 'init':
        PlanDb.init(file)
    elif action == 'list':
        raise NotImplementedError
    elif action == 'replan':
        raise NotImplementedError
    elif action == 'set':
        raise NotImplementedError


if __name__ == "__main__":
    main()
