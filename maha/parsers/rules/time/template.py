__all__ = ["TimeValue"]

from dateutil.relativedelta import relativedelta


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
    ):
        self._years = years
        self._months = months
        self._days = days
        self._leapdays = leapdays
        self._weeks = weeks
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        self._microseconds = microseconds
        self._am_pm = am_pm

        # handle hour am pm
        if am_pm == "PM" and hour is not None and hour < 12:
            hour += 12

        super().__init__(
            dt1=dt1,
            dt2=dt2,
            years=years if years is not None else 0,
            months=months if months is not None else 0,
            days=days if days is not None else 0,
            leapdays=leapdays if leapdays is not None else 0,
            weeks=weeks if weeks is not None else 0,
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

    def is_years_set(self):
        return self._years is not None or self.year is not None

    def is_months_set(self):
        return self._months is not None or self.month is not None

    def is_days_set(self):
        return self._days is not None or self.day is not None

    def is_leapdays_set(self):
        return self._leapdays is not None

    def is_weeks_set(self):
        return self._weeks is not None

    def is_hours_set(self):
        return self._hours is not None or self.hour is not None

    def is_minutes_set(self):
        return self._minutes is not None or self.minute is not None

    def is_seconds_set(self):
        return self._seconds is not None or self.second is not None

    def is_microseconds_set(self):
        return self._microseconds is not None or self.microsecond is not None

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
                weeks=self._add(other._weeks, self._weeks),
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
                am_pm=other._am_pm or self._am_pm,
            )
        return super().__add__(other)

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
            "year",
            "month",
            "day",
            "weekday",
            "hour",
            "minute",
            "second",
            "microsecond",
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
        )
