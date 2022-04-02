from __future__ import annotations

__all__ = ["TimeValue", "TimeInterval"]


from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta
from hijri_converter import Gregorian, Hijri

from . import constants


class TimeValue(relativedelta):
    def __init__(
        self,
        dt1=None,
        dt2=None,
        years=None,
        months=None,
        days=None,
        leapdays=None,
        weeks=None,
        hours=None,
        minutes=None,
        seconds=None,
        microseconds=None,
        year=None,
        month=None,
        day=None,
        weekday=None,
        yearday=None,
        nlyearday=None,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
        am_pm=None,
        next_month=None,
        prev_month=None,
        hijri=None,
    ):

        super().__init__(
            dt1=dt1,
            dt2=dt2,
            years=years if years is not None else 0,
            months=months if months is not None else 0,
            days=days if days is not None else 0,
            leapdays=leapdays if leapdays is not None else 0,
            hours=hours if hours is not None else 0,
            minutes=minutes if minutes is not None else 0,
            seconds=seconds if seconds is not None else 0,
            microseconds=microseconds if microseconds is not None else 0,
            year=year,
            month=month,
            day=day,
            weekday=weekday,
            yearday=yearday,
            nlyearday=nlyearday,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
        )
        self._years = years
        self._months = months
        self._days = days
        self._leapdays = leapdays
        self._weeks = weeks
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        self._microseconds = microseconds
        self.next_month = next_month
        self.prev_month = prev_month
        self.am_pm = am_pm
        self.hijri = hijri

    @property
    def am_pm(self):
        return self._am_pm

    @am_pm.setter
    def am_pm(self, am_pm):
        self._am_pm = am_pm
        # handle hour am pm
        if am_pm == "PM" and self.hour is not None and self.hour < 12:
            self.hour += 12

    @property
    def weeks(self):
        return self._weeks

    @weeks.setter
    def weeks(self, value):
        self._weeks = value

    def is_years_set(self):
        return self._years is not None or self.year is not None

    def is_months_set(self):
        return self._months is not None or self.month is not None

    def is_days_set(self):
        return self._days is not None or self.day is not None

    def is_leapdays_set(self):
        return self._leapdays is not None

    def is_weeks_set(self):
        return self.weeks is not None or self.weekday is not None

    def is_hours_set(self):
        return self._hours is not None or self.hour is not None

    def is_minutes_set(self):
        return self._minutes is not None or self.minute is not None

    def is_seconds_set(self):
        return self._seconds is not None or self.second is not None

    def is_microseconds_set(self):
        return self._microseconds is not None or self.microsecond is not None

    def is_am_pm_set(self):
        return self.am_pm is not None

    def is_hijri_set(self):
        return self.hijri is not None

    def _add(self, value1, value2):
        if value1 is not None and value2 is not None:
            return value1 + value2
        if value1 is None:
            return value2
        if value2 is None:
            return value1

    def __add__(self, other):
        if isinstance(other, TimeValue):
            return self.__class__(
                years=self._add(other._years, self._years),
                months=self._add(other._months, self._months),
                days=self._add(other._days, self._days),
                leapdays=self._add(other._leapdays, self._leapdays),
                weeks=self._add(other._weeks, self.weeks),
                hours=self._add(other._hours, self._hours),
                minutes=self._add(other._minutes, self._minutes),
                seconds=self._add(other._seconds, self._seconds),
                microseconds=self._add(other._microseconds, self._microseconds),
                year=(other.year if other.year is not None else self.year),
                month=(other.month if other.month is not None else self.month),
                day=(other.day if other.day is not None else self.day),
                weekday=(other.weekday if other.weekday is not None else self.weekday),
                hour=(other.hour if other.hour is not None else self.hour),
                minute=(other.minute if other.minute is not None else self.minute),
                second=(other.second if other.second is not None else self.second),
                microsecond=(
                    other.microsecond
                    if other.microsecond is not None
                    else self.microsecond
                ),
                am_pm=other.am_pm or self.am_pm,
                next_month=(
                    other.next_month
                    if other.next_month is not None
                    else self.next_month
                ),
                prev_month=(
                    other.prev_month
                    if other.prev_month is not None
                    else self.prev_month
                ),
                hijri=other.hijri or self.hijri,
            )

        old_values = self.__dict__.copy()

        # Handle next/prev week
        if isinstance(other, datetime) and self.weeks:
            self.days = self._days or 0
            current_day = other.weekday()
            if self._days is not None:
                self.days += self.weeks * 7
            else:
                start_of_week = (current_day + 7 - constants.START_OF_WEEK) % 7
                # next week(s)
                if self.weeks > 0:
                    self.days += 7 - start_of_week + (self.weeks - 1) * 7
                # prev week(s)
                elif self.weeks < 0:
                    self.days -= start_of_week - 7 * self.weeks

        # Handle hijri date
        if isinstance(other, datetime) and self.hijri:
            current_hijri = Gregorian.fromdate(other.date()).to_hijri()
            hijri_year = self.year or current_hijri.year
            hijri_month = self.month or current_hijri.month
            hijri_day = self.day or current_hijri.day
            month_lengths = [0] + [
                Hijri(hijri_year, i, 1).month_length() for i in range(1, 13)
            ]
            hijri_day = min(hijri_day, month_lengths[hijri_month])
            hijri_year += self.years
            hijri_month += self.months
            hijri_day += self.days

            while hijri_day > month_lengths[hijri_month]:
                if hijri_month > 12:
                    hijri_year += self.months // 12
                    hijri_month = self.months % 12
                hijri_day -= month_lengths[hijri_month]
                hijri_month += 1

            if self.next_month:
                hijri_year += 1 if self.next_month <= current_hijri.month else 0
                hijri_month = self.next_month
            elif self.prev_month:
                hijri_year += 0 if self.prev_month <= current_hijri.month else -1
                hijri_month = self.prev_month

            new_date = Hijri(hijri_year, hijri_month, hijri_day).to_gregorian()
            self.year = new_date.year
            self.month = new_date.month
            self.day = new_date.day
            self.years = 0
            self.months = 0
            self.days = 0
        elif isinstance(other, datetime):
            current_month = other.month
            if self.next_month:
                self.years += 1 if self.next_month <= current_month else 0
                self.month = self.next_month
            elif self.prev_month:
                self.years += 0 if self.prev_month <= current_month else -1
                self.month = self.prev_month

        output = super().__add__(other)
        self.__dict__ = old_values
        return output

    def __repr__(self):
        l = []
        for attr in [
            "_years",
            "_months",
            "_weeks",
            "_days",
            "_leapdays",
            "_hours",
            "_minutes",
            "_seconds",
            "_microseconds",
            "_am_pm",
            "next_month",
            "prev_month",
            "year",
            "month",
            "day",
            "weekday",
            "hour",
            "minute",
            "second",
            "microsecond",
            "hijri",
        ]:
            value = getattr(self, attr)
            if value is not None:
                l.append(
                    "{attr}={value}".format(attr=attr.strip("_"), value=repr(value))
                )
        return "{classname}({attrs})".format(
            classname=self.__class__.__name__, attrs=", ".join(l)
        )

    def __eq__(self, other):
        if not isinstance(other, TimeValue):
            return NotImplemented
        if self.weekday or other.weekday:
            if not self.weekday or not other.weekday:
                return False
            if self.weekday.weekday != other.weekday.weekday:
                return False
            n1, n2 = self.weekday.n, other.weekday.n
            if n1 != n2 and not ((not n1 or n1 == 1) and (not n2 or n2 == 1)):
                return False
        return (
            self._years == other._years
            and self._months == other._months
            and self._days == other._days
            and self._hours == other._hours
            and self._minutes == other._minutes
            and self._seconds == other._seconds
            and self._microseconds == other._microseconds
            and self._leapdays == other._leapdays
            and self.year == other.year
            and self.month == other.month
            and self.day == other.day
            and self.hour == other.hour
            and self.minute == other.minute
            and self.second == other.second
            and self.microsecond == other.microsecond
            and self.weekday == other.weekday
            and self.am_pm == other.am_pm
            and self.weeks == other.weeks
            and self.hijri == other.hijri
        )


@dataclass
class TimeInterval:
    start: TimeValue | None = None
    end: TimeValue | None = None
