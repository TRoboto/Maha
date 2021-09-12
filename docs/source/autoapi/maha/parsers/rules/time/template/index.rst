:py:mod:`maha.parsers.rules.time.template`
==========================================

.. py:module:: maha.parsers.rules.time.template


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   maha.parsers.rules.time.template.TimeValue




.. py:class:: TimeValue(dt1=None, dt2=None, years=None, months=None, days=None, leapdays=None, weeks=None, hours=None, minutes=None, seconds=None, microseconds=None, year=None, month=None, day=None, weekday=None, yearday=None, nlyearday=None, hour=None, minute=None, second=None, microsecond=None, am_pm=None)

   Bases: :py:obj:`dateutil.relativedelta.relativedelta`

   The relativedelta type is designed to be applied to an existing datetime and
   can replace specific components of that datetime, or represents an interval
   of time.

   It is based on the specification of the excellent work done by M.-A. Lemburg
   in his
   `mx.DateTime <https://www.egenix.com/products/python/mxBase/mxDateTime/>`_ extension.
   However, notice that this type does *NOT* implement the same algorithm as
   his work. Do *NOT* expect it to behave like mx.DateTime's counterpart.

   There are two different ways to build a relativedelta instance. The
   first one is passing it two date/datetime classes::

       relativedelta(datetime1, datetime2)

   The second one is passing it any number of the following keyword arguments::

       relativedelta(arg1=x,arg2=y,arg3=z...)

       year, month, day, hour, minute, second, microsecond:
           Absolute information (argument is singular); adding or subtracting a
           relativedelta with absolute information does not perform an arithmetic
           operation, but rather REPLACES the corresponding value in the
           original datetime with the value(s) in relativedelta.

       years, months, weeks, days, hours, minutes, seconds, microseconds:
           Relative information, may be negative (argument is plural); adding
           or subtracting a relativedelta with relative information performs
           the corresponding arithmetic operation on the original datetime value
           with the information in the relativedelta.

       weekday:
           One of the weekday instances (MO, TU, etc) available in the
           relativedelta module. These instances may receive a parameter N,
           specifying the Nth weekday, which could be positive or negative
           (like MO(+1) or MO(-2)). Not specifying it is the same as specifying
           +1. You can also use an integer, where 0=MO. This argument is always
           relative e.g. if the calculated date is already Monday, using MO(1)
           or MO(-1) won't change the day. To effectively make it absolute, use
           it in combination with the day argument (e.g. day=1, MO(1) for first
           Monday of the month).

       leapdays:
           Will add given days to the date found, if year is a leap
           year, and the date found is post 28 of february.

       yearday, nlyearday:
           Set the yearday or the non-leap year day (jump leap days).
           These are converted to day/month/leapdays information.

   There are relative and absolute forms of the keyword
   arguments. The plural is relative, and the singular is
   absolute. For each argument in the order below, the absolute form
   is applied first (by setting each attribute to that value) and
   then the relative form (by adding the value to the attribute).

   The order of attributes considered when this relativedelta is
   added to a datetime is:

   1. Year
   2. Month
   3. Day
   4. Hours
   5. Minutes
   6. Seconds
   7. Microseconds

   Finally, weekday is applied, using the rule described above.

   For example

   >>> from datetime import datetime
   >>> from dateutil.relativedelta import relativedelta, MO
   >>> dt = datetime(2018, 4, 9, 13, 37, 0)
   >>> delta = relativedelta(hours=25, day=1, weekday=MO(1))
   >>> dt + delta
   datetime.datetime(2018, 4, 2, 14, 37)

   First, the day is set to 1 (the first of the month), then 25 hours
   are added, to get to the 2nd day and 14th hour, finally the
   weekday is applied, but since the 2nd is already a Monday there is
   no effect.


   .. py:method:: is_years_set(self)


   .. py:method:: is_months_set(self)


   .. py:method:: is_days_set(self)


   .. py:method:: is_leapdays_set(self)


   .. py:method:: is_weeks_set(self)


   .. py:method:: is_hours_set(self)


   .. py:method:: is_minutes_set(self)


   .. py:method:: is_seconds_set(self)


   .. py:method:: is_microseconds_set(self)



