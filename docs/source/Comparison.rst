Comparison
==========

In this page, you will find a comparison in parsing functionality between `Maha <https://github.com/TRoboto/Maha>`_ and `duckling <https://github.com/facebook/duckling>`_.



This comparison considers the following points:

* Ease of use and integration.
* Parsing results.
* Time taken to get the results.

Ease of use and integration
---------------------------

The installation of Maha library is easier than the installation of duckling.

* Maha library is more user-friendly and you don't need much experience to use and install. In comparison, duckling is much difficult and it needs experience to build and install.
* Maha doesn't have build steps in comparison with duckling which has many build steps to run and use.
* Duckling needs a haskell for the building process.
* The installation of Maha is straight forward but duckling needs many steps to install.
* The integration of Maha is much easier in python projects in comparison with duckling.
* The contribution in Maha for Arabic language is easier than the contribution for Arabic langage in duckling.

.. note::
    Currently, the comaprison contains 4 dimensions which are: ordinal, time, duration and numeral.

Parsing results
---------------

Here, the results of comaprison will consider short and long examples to assessing the performance of maha and duckling.


For Maha, you need to import it as the following:

.. code:: pycon

  >>> import maha
  >>> from maha.parsers.functions import parse_dimension

For duckling, you need to run the server as the following:

.. code:: bash

  >>> stack exec duckling-example-exe


Short examples
--------------

The following examples show the performance of maha and duckling for short text, for example chatbot applications to parse the useful information.

Ordinal Dimension
-----------------

Ordinal dimension for Maha and duckling.

Example 1
^^^^^^^^^

.. code:: pycon

  >>> Example_1 = "المئة والخامس والسبعون من العصر الحجري"
  >>> parse_dimension(Example_1, ordinal=True)
  [Dimension(body=المئة والخامس والسبعون, value=175, start=0, end=22, dimension_type=DimensionType.ORDINAL)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_1, "locale": "ar_jo", "dims": '["ordinal"]'},
  ... ).text
  '[{"body":"الخامس والسبعون","start":7,"value":{"value":75,"type":"value"},"end":22,"dim":"ordinal","latent":false}]'


Example 2
^^^^^^^^^

.. code:: pycon

  >>> Example_2 = "الذكرى الرابعة لتخرج والدي"
  >>> parse_dimension(Example_2, ordinal=True)
  [Dimension(body=الرابعة, value=4, start=7, end=14, dimension_type=DimensionType.ORDINAL)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_2, "locale": "ar_jo", "dims": '["ordinal"]'},
  ... ).text
  '[{"body":"الرابعة","start":8,"value":{"value":4,"type":"value"},"end":15,"dim":"ordinal","latent":false},{"body":"العشرين","start":17,"value":{"value":20,"type":"value"},"end":24,"dim":"ordinal","latent":false}]'



Example 3
^^^^^^^^^

.. code:: pycon

  >>> Example_3 = "كنتُ في الثامنة والعشرين وكان والدي في الخامسة والستين عندتخرجي من الجامعة"
  >>> parse_dimension(Example_3, ordinal=True)
  [Dimension(body=الثامنة والعشرين, value=28, start=8, end=24, dimension_type=DimensionType.ORDINAL),
  Dimension(body=الخامسة والستين, value=65, start=39, end=54, dimension_type=DimensionType.ORDINAL)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_3, "locale": "ar_jo", "dims": '["ordinal"]'},
  ... ).text
  '[{"body":"الثامنة","start":8,"value":{"value":8,"type":"value"},"end":15,"dim":"ordinal","latent":false},{"body":"العشرين","start":17,"value":{"value":20,"type":"value"},"end":24,"dim":"ordinal","latent":false},{"body":"الخامسة","start":39,"value":{"value":5,"type":"value"},"end":46,"dim":"ordinal","latent":false},{"body":"الستين","start":48,"value":{"value":60,"type":"value"},"end":54,"dim":"ordinal","latent":false}]'


Example 4
^^^^^^^^^

.. code:: pycon

  >>> Example_4 = "كنت في المرتبة المئة والخامسة والسبعين في سباق الدراجات في السنة الماضية والآن أنا في المرتبة الأولى"
  >>> parse_dimension(Example_4, ordinal=True)
  [Dimension(body=المئة والخامسة والسبعين, value=175, start=15, end=38, dimension_type=DimensionType.ORDINAL),
  Dimension(body=الأولى, value=1, start=94, end=100, dimension_type=DimensionType.ORDINAL)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_4, "locale": "ar_jo", "dims": '["ordinal"]'},
  ... ).text
  '[{"body":"الخامسة","start":22,"value":{"value":5,"type":"value"},"end":29,"dim":"ordinal","latent":false},{"body":"السبعين","start":31,"value":{"value":70,"type":"value"},"end":38,"dim":"ordinal","latent":false},{"body":"الأولى","start":94,"value":{"value":1,"type":"value"},"end":100,"dim":"ordinal","latent":false}]'


Time Dimension
--------------

Time dimension for Maha and duckling.


Example 1
^^^^^^^^^

.. code:: pycon

  >>> Example_1 = "بدي إياك هسه"
  >>> parse_dimension(Example_1, time=True)
  [Dimension(body=هسه, value=TimeValue(years=0, months=0, days=0, hours=0, minutes=0, seconds=0), start=9, end=12, dimension_type=DimensionType.TIME)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_1, "locale": "ar_jo", "dims": '["time"]'},
  ... ).text
  '[]'



Example 2
^^^^^^^^^

.. code:: pycon

  >>> Example_2 = "قبل خمس سنوات الساعة أربعة ونصف صباحا يوم الجمعة"
  >>> parse_dimension(Example_2, time=True)
  [Dimension(body=قبل خمس سنوات الساعة أربعة ونصف صباحا يوم الجمعة, value=TimeValue(years=-5, am_pm='AM', weekday=FR, hour=4, minute=15, second=0, microsecond=0), start=0, end=48, dimension_type=DimensionType.TIME)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_2, "locale": "ar_jo", "dims": '["time"]'},
  ... ).text
  '[{"body":"الساعة أربعة ونصف صباحا يوم الجمعة","start":14,"value":{"values":[{"value":"2021-10-22T04:30:00.000-07:00","grain":"minute","type":"value"},{"value":"2021-10-29T04:30:00.000-07:00","grain":"minute","type":"value"},{"value":"2021-11-05T04:30:00.000-07:00","grain":"minute","type":"value"}],"value":"2021-10-22T04:30:00.000-07:00","grain":"minute","type":"value"},"end":48,"dim":"time","latent":false}]'



Example 3
^^^^^^^^^

.. code:: pycon

  >>> Example_3 = "بعد سنتين يوم السبت والساعة الخامسة وسبع دقائق في المساء"
  >>> parse_dimension(Example_3, time=True)
  [Dimension(body=بعد سنتين يوم السبت والساعة الخامسة وسبع دقائق في المساء, value=TimeValue(years=2, am_pm='PM', weekday=SA, hour=17, minute=7, second=0, microsecond=0), start=0, end=56, dimension_type=DimensionType.TIME)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_3, "locale": "ar_jo", "dims": '["time"]'},
  ... ).text
  '[{"body":"بعد سنتين يوم السبت","start":0,"value":{"values":[{"from":{"value":"2023-10-07T00:00:00.000-07:00","grain":"day"},"type":"interval"},{"from":{"value":"2023-10-14T00:00:00.000-07:00","grain":"day"},"type":"interval"},{"from":{"value":"2023-10-21T00:00:00.000-07:00","grain":"day"},"type":"interval"}],"from":{"value":"2023-10-07T00:00:00.000-07:00","grain":"day"},"type":"interval"},"end":19,"dim":"time","latent":false},{"body":"الساعة الخامسة وسبع دقائق في المساء","start":21,"value":{"values":[{"value":"2021-10-19T17:07:00.000-07:00","grain":"minute","type":"value"},{"value":"2021-10-20T17:07:00.000-07:00","grain":"minute","type":"value"},{"value":"2021-10-21T17:07:00.000-07:00","grain":"minute","type":"value"}],"value":"2021-10-19T17:07:00.000-07:00","grain":"minute","type":"value"},"end":56,"dim":"time","latent":false}]'



Example 4
^^^^^^^^^

.. code:: pycon

  >>> Example_4 = "السادس عشر من شهر حزيران والساعة الواحدة بعد الظهر"
  >>> parse_dimension(Example_4, time=True)
  [Dimension(body=السادس عشر من شهر حزيران والساعة الواحدة بعد الظهر, value=TimeValue(am_pm='PM', month=6, day=16, hour=13, minute=0, second=0, microsecond=0), start=0, end=50, dimension_type=DimensionType.TIME)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_4, "locale": "ar_jo", "dims": '["time"]'},
  ... ).text
  '[{"body":"السادس عشر من شهر حزيران","start":0,"value":{"values":[{"value":"2022-06-16T00:00:00.000-07:00","grain":"day","type":"value"},{"value":"2023-06-16T00:00:00.000-07:00","grain":"day","type":"value"},{"value":"2024-06-16T00:00:00.000-07:00","grain":"day","type":"value"}],"value":"2022-06-16T00:00:00.000-07:00","grain":"day","type":"value"},"end":24,"dim":"time","latent":false},{"body":"واحدة بعد الظهر","start":35,"value":{"values":[{"value":"2021-10-20T13:00:00.000-07:00","grain":"hour","type":"value"},{"value":"2021-10-21T13:00:00.000-07:00","grain":"hour","type":"value"},{"value":"2021-10-22T13:00:00.000-07:00","grain":"hour","type":"value"}],"value":"2021-10-20T13:00:00.000-07:00","grain":"hour","type":"value"},"end":50,"dim":"time","latent":false}]'




Duration Dimension
------------------

Duration dimension for Maha and duckling.


Example 1
^^^^^^^^^

.. code:: pycon

  >>> sample_text = "سأبقى في الأردن لمدة خمس سنوات وأربع أشهر و15 يوما و3 ساعات وخمس دقائق"
  >>> parse_dimension(Example_1, duration=True)
  [Dimension(body=خمس سنوات وأربع أشهر و15 يوما و3 ساعات وخمس دقائق, value=DurationValue(values=[ValueUnit(value=5, unit=<DurationUnit.YEARS: 7>), ValueUnit(value=4, unit=<DurationUnit.MONTHS: 6>), ValueUnit(value=15, unit=<DurationUnit.DAYS: 4>), ValueUnit(value=3, unit=<DurationUnit.HOURS: 3>), ValueUnit(value=5, unit=<DurationUnit.MINUTES: 2>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=21, end=70, dimension_type=DimensionType.DURATION)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_1, "locale": "ar_jo", "dims": '["duration"]'},
  ... ).text
  '[{"body":"أربع أشهر","start":32,"value":{"value":4,"month":4,"type":"value","unit":"month","normalized":{"value":10368000,"unit":"second"}},"end":41,"dim":"duration","latent":false},{"body":"3 ساعات","start":52,"value":{"value":3,"hour":3,"type":"value","unit":"hour","normalized":{"value":10800,"unit":"second"}},"end":59,"dim":"duration","latent":false},{"body":"خمس دقائق","start":61,"value":{"value":5,"type":"value","minute":5,"unit":"minute","normalized":{"value":300,"unit":"second"}},"end":70,"dim":"duration","latent":false}]'


Example 2
^^^^^^^^^

.. code:: pycon

  >>> Example_2 = "لقد قضيت فيه هذا البلد ما مدته خمسة عشرة سنة و11 شهر و28 يوم وخمس عشرة دقيقة و15 ساعة وخمسة عشر ثانية"
  >>> parse_dimension(Example_2, duration=True)
  [Dimension(body=خمسة عشرة سنة و11 شهر و28 يوم وخمس عشرة دقيقة و15 ساعة وخمسة عشر ثانية, value=DurationValue(values=[ValueUnit(value=15, unit=<DurationUnit.YEARS: 7>), ValueUnit(value=11, unit=<DurationUnit.MONTHS: 6>), ValueUnit(value=28, unit=<DurationUnit.DAYS: 4>), ValueUnit(value=15, unit=<DurationUnit.HOURS: 3>), ValueUnit(value=15, unit=<DurationUnit.MINUTES: 2>), ValueUnit(value=15, unit=<DurationUnit.SECONDS: 1>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=31, end=101, dimension_type=DimensionType.DURATION)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_2, "locale": "ar_jo", "dims": '["duration"]'},
  ... ).text
  '[{"body":"خمسة عشرة سنة","start":31,"value":{"value":15,"year":15,"type":"value","unit":"year","normalized":{"value":473040000,"unit":"second"}},"end":44,"dim":"duration","latent":false},{"body":"11 شهر","start":46,"value":{"value":11,"month":11,"type":"value","unit":"month","normalized":{"value":28512000,"unit":"second"}},"end":52,"dim":"duration","latent":false},{"body":"28 يوم","start":54,"value":{"value":28,"day":28,"type":"value","unit":"day","normalized":{"value":2419200,"unit":"second"}},"end":60,"dim":"duration","latent":false},{"body":"خمس عشرة دقيقة","start":62,"value":{"value":15,"type":"value","minute":15,"unit":"minute","normalized":{"value":900,"unit":"second"}},"end":76,"dim":"duration","latent":false},{"body":"15 ساعة","start":78,"value":{"value":15,"hour":15,"type":"value","unit":"hour","normalized":{"value":54000,"unit":"second"}},"end":85,"dim":"duration","latent":false},{"body":"خمسة عشر ثانية","start":87,"value":{"second":15,"value":15,"type":"value","unit":"second","normalized":{"value":15,"unit":"second"}},"end":101,"dim":"duration","latent":false}]'



Example 3
^^^^^^^^^

.. code:: pycon

  >>> Example_3 = "10 ثواني و5 ساعات وخمس سنوات و6 أشهر"
  >>> parse_dimension(sample_text, duration=True)
  [Dimension(body=10 ثواني و5 ساعات وخمس سنوات و6 أشهر, value=DurationValue(values=[ValueUnit(value=5, unit=<DurationUnit.YEARS: 7>), ValueUnit(value=6, unit=<DurationUnit.MONTHS: 6>), ValueUnit(value=5, unit=<DurationUnit.HOURS: 3>), ValueUnit(value=10, unit=<DurationUnit.SECONDS: 1>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=0, end=36, dimension_type=DimensionType.DURATION)]
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": sample_text, "locale": "ar_jo", "dims": '["duration"]'},
  ... ).text
  '[{"body":"10 ثواني","start":0,"value":{"second":10,"value":10,"type":"value","unit":"second","normalized":{"value":10,"unit":"second"}},"end":8,"dim":"duration","latent":false},{"body":"5 ساعات","start":10,"value":{"value":5,"hour":5,"type":"value","unit":"hour","normalized":{"value":18000,"unit":"second"}},"end":17,"dim":"duration","latent":false},{"body":"6 أشهر","start":30,"value":{"value":6,"month":6,"type":"value","unit":"month","normalized":{"value":15552000,"unit":"second"}},"end":36,"dim":"duration","latent":false}]'



Example 4
^^^^^^^^^

.. code:: pycon

  >>> Example_4 = "بقينا في الجامعة لمدة عامين"
  >>> parse_dimension(Example_4, duration=True)
  [Dimension(body=عامين, value=DurationValue(values=[ValueUnit(value=2, unit=<DurationUnit.YEARS: 7>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=22, end=27, dimension_type=DimensionType.DURATION)]
  requests.post('http://0.0.0.0:8000/parse' , data={'text':Example_4, 'locale':'ar_jo','dims':'["duration"]'}).text
  '[{"body":"عامين","start":22,"value":{"value":2,"year":2,"type":"value","unit":"year","normalized":{"value":63072000,"unit":"second"}},"end":27,"dim":"duration","latent":false}]'


Numeral Dimension
-----------------

Numeral dimension for Maha and duckling.

Example 1
^^^^^^^^^

.. code:: pycon

  >>> Example_1 = "عشرة آلاف وخمسمئة وثلاثون فاصلة عشرة"
  >>> parse_dimension(Example_1, numeral=True)[0].value
  Dimension(body=عشرة آلاف وخمسمئة وثلاثون فاصلة عشرة, value=10530.1, start=0, end=36, dimension_type=DimensionType.NUMERAL)
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": sample_text, "locale": "ar_jo", "dims": '["numeral"]'},
  ... ).text
  '[{"body":"عشرة آلاف","start":0,"value":{"value":10000,"type":"value"},"end":9,"dim":"number","latent":false},{"body":"خمسمئة وثلاثون فاصلة عشرة","start":11,"value":{"value":530.1,"type":"value"},"end":36,"dim":"number","latent":false}]'


Example 2
^^^^^^^^^

.. code:: pycon

  >>> Example_2 = "الف وخمسمية واربعطاشر"
  >>> parse_dimension(Example_2, numeral=True)
  Dimension(body=الف وخمسمية واربعطاشر, value=1514, start=0, end=21, dimension_type=DimensionType.NUMERAL)
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_2, "locale": "ar_jo", "dims": '["numeral"]'},
  ... ).text
  '[{"body":"الف","start":0,"value":{"value":1000,"type":"value"},"end":3,"dim":"number","latent":false},{"body":"الف","start":0,"value":{"values":[{"value":"1000-01-01T00:00:00.000-07:53","grain":"year","type":"value"}],"value":"1000-01-01T00:00:00.000-07:53","grain":"year","type":"value"},"end":3,"dim":"time","latent":false},{"body":"خمسمية","start":5,"value":{"value":500,"type":"value"},"end":11,"dim":"number","latent":false}]'


Example 3
^^^^^^^^^

.. code:: pycon

  >>> sample_text = "16 ألف و10 "
  >>> parse_dimension(sample_text, numeral=True)[0]
  Dimension(body=10, value=10, start=0, end=2, dimension_type=DimensionType.NUMERAL)
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_3, "locale": "ar_jo", "dims": '["numeral"]'},
  ... ).text
  '[{"body":"16 ألف","start":0,"value":{"value":16000,"type":"value"},"end":6,"dim":"number","latent":false},{"body":"10","start":8,"value":{"value":10,"type":"value"},"end":10,"dim":"number","latent":false}]'


Example 4
^^^^^^^^^


.. code:: pycon

  >>> Example_4 = "سبعطاشر ألف وخمسمية واربعة فاصلة أربعة وخمسين"
  >>> parse_dimension(sample_text, numeral=True)[0]
  Dimension(body=سبعطاشر ألف وخمسمية واربعة فاصلة أربعة وخمسين, value=17504.54, start=0, end=45, dimension_type=DimensionType.NUMERAL)
  >>> requests.post(
  ...     "http://0.0.0.0:8000/parse",
  ...     data={"text": Example_4, "locale": "ar_jo", "dims": '["numeral"]'},
  ... ).text
  '[{"body":"ألف","start":8,"value":{"value":1000,"type":"value"},"end":11,"dim":"number","latent":false},{"body":"خمسمية واربعة فاصلة أربعة وخمسين","start":13,"value":{"value":504.54,"type":"value"},"end":45,"dim":"number","latent":false},{"body":"خمسمية واربعة فاصلة أربعة وخمسين","start":13,"value":{"value":554.4,"type":"value"},"end":45,"dim":"number","latent":false}]'


The following table describes the time of parsing for Maha in comparison of duckling.


.. list-table::
   :header-rows: 1
   :widths: 15 10 75 75

   * - Dimension
     - Example #
     - Time
     - Time
   * - _
     - _
     - Maha
     - Duckling
   * - Ordinal
     - 1
     - 166 µs ± 27.9 µs
     - 4.26 ms ± 706 µs
   * - _
     - 2
     - 141 µs ± 11.3 µs
     - 3.96 ms ± 61.2 µs
   * - _
     - 3
     - 3.76 ms ± 158 µs
     - 5.76 ms ± 285 µs
   * - _
     - 4
     - 2.99 ms ± 127 µs
     - 5.34 ms ± 301 µs
   * - Duration
     - 1
     - 10.8 ms ± 877 µs
     - 4.53 ms ± 462 µs
   * - _
     - 2
     - 12.9 ms ± 836 µs
     - 5.06 ms ± 435 µs
   * - _
     - 3
     - 2.95 ms ± 81.6 µs
     - 3.53 ms ± 107 µs
   * - _
     - 4
     - 9.02 ms ± 1.05 ms
     - 4.1 ms ± 456 µs
   * - Numeral
     - 1
     - 245 µs ± 40.8 µs
     - 5.57 ms ± 127 µs
   * - _
     - 2
     - 206 µs ± 17.2 µs
     - 5.01 ms ± 470 µs
   * - _
     - 3
     - 815 µs ± 37.8 µs
     - 5.76 ms ± 477 µs
   * - _
     - 4
     - 256 µs ± 16.7 µs
     - 5.62 ms ± 208 µs


Notes
*****
1. The parsing time in Maha is longer that the parsing time duckling in duration dimension, and the reason of this that Maha parse more complex patterns than duckling.
2. The time format is calculated by this criteria: (mean ± std. dev. of 5 runs, 1000 loops each).
3. As we see from the results and the previous table, we can conculde that Maha is better than duckling in parsing for Arabic language.



Long examples
-------------

The following is a describtin of the file that used for the comparison.

* File size: 2.8 MB (2,838,878 bytes)

* File encoding: UTF-8 Unicode text, with very long lines

* Lines counts: 10364

* Words counts: 292074

* Characters counts: 1565476


The time is calculated for Maha and duckling for each dimension separetly and for all available dimensions at the same time.

.. list-table::
   :header-rows: 1
   :widths: 10 10 10

   * - Dimension
     - Maha
     - Duckling
   * - Ordinal
     - 266 ms ± 6.43 ms
     - 1.06 s ± 35 ms
   * - Time
     - 32.4 s ± 67.7 ms
     - 28.3 s ± 84.5 ms
   * - Duration
     - 33.9 s ± 4.88 s
     - 1.77 s ± 24.9 ms
   * - Numeral
     - 756 ms ± 13.2 ms
     - 1.08 s ± 55.6 ms
   * - All
     - 1min 3s ± 26.5 ms
     - 32.3 s ± 640 ms



Notes:

We have reduced the file size to about 2.8 MB since duckling doesn't deal with size more than this. On the hand, maha works with original fiel smoothly
without any problem.

We have tried to increase the timeout but it have not worked

The file is pre-processed with keeping Arabic letters only.