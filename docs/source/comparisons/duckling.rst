Duckling
========

`Duckling <https://github.com/facebook/duckling>`_ is an open-source parsing library
developed by Facebook. It supports many languages including Arabic. In this comparison,
the latest version of Duckling (0.2.0.0) is used.

Summary
-------

The following table provides a summary of the comparison.

.. list-table::
   :header-rows: 1
   :widths: 15 30 30

   * -
     - Maha
     - Duckling
   * - Installing
     - Easy
     - Needs Haskell and compilation
   * - Language
     - Python
     - Haskell
   * - Speed
     - Fast
     - Normal
   * - Ease of use
     - User-friendly
     - Difficult
   * - Parsing Results
     - Rich and more detailed
     - Good
   * - Python Integration
     - Integrated with Python
     - Easy integration with Duckling server
   * - Dimensions
     - Time, numeral, ordinal and duration
     - Time, numeral, ordinal, duration, quantity, temperature, volume, and amount of money
   * - Parsing Engine
     - Regex
     - Regex

Conditions
-----------

The following points are considered for the comparison:

* Both libraries are used in a **Python** environment.
* For a fair comparison, duckling server is run locally.
* Only ``time``, ``numeral``, ``ordinal`` and ``duration`` dimensions are compared.
* Long and short texts are compared.

The hardware specifications used to run both libraries are as follows:

* CPU: Intel(R) Core(TM) i5-6200U CPU @ 2.30GHz, 4 cores
* Memory: 12GiB SODIMM DDR3 Synchronous 1600 MHz (0.6 ns)
* OS: Ubuntu 20.04.3 LTS, 64-bit

Speed and results
-----------------

Short texts
***********

Short texts are compared in terms of the results obtained and the time taken to get them.
Whereas the long text is only compared in terms of the time taken to obtain the results.

For each dimension, 4 examples are considered for comparison. The results
are summarized in the following table:

.. flat-table::
   :header-rows: 2
   :stub-columns: 0
   :widths: 1 2 2 3 1 1

   * - :rspan:`1` Dimension
     - :rspan:`1` Example
     - :cspan:`1` Result
     - :cspan:`1` Mean time (ms)

   * - Maha
     - Duckling
     - Maha
     - Duckling

   * - :rspan:`3` Time (06/11/2021)
     - بدي إياك هسه
     - 2021-11-06
     - None
     - 4.78
     - 3.84

   * - قبل خمس سنوات أربعة ونص مساء يوم الجمعة
     - 2016-11-11 16:30:00
     -
        * 2021-10-31 16:30:00 (أربعة ونص مساء)
        * 2021-11-06 00:00:00 (مساء يوم الجمعة)
     - 2.37
     - 5.54

   * - بعد سنتين يوم السبت والساعة الخامسة وسبع دقائق في المساء
     - 2023-11-11 17:07:00
     -
        * 2023-10-07 00:00:00 (بعد سنتين يوم السبت)
        * 2021-11-06 17:07:00 (الساعة الخامسة وسبع دقائق في المساء)
     - 4.26
     - 6.82

   * - السادس عشر من شهر حزيران والساعة الواحدة بعد الظهر
     - 2021-06-16 13:00:00
     -
        * 2022-06-16 00:00:00 (السادس عشر من شهر حزيران)
        * 2021-11-06 13:00:00 (واحدة بعد الظهر)
     - 3.88
     - 7.62

   * - :rspan:`3` Numeral
     - ثلاثين مليون وواحد وعشرين الف وخمسة
     - 30021005
     -
        * 30000000 (ثلاثين مليون)
        * 21000 (واحد وعشرين الف)
        * 5 (خمسة)
     - 0.19
     - 3.55

   * - الف وخمسمية واربعطاشر
     - 1514
     -
        * 1000 (الف)
        * 500 (خمسمية)
     - 0.18
     - 4.15

   * - 16 ألف و10
     - 16010
     -
        * 16000 (16 الف)
        * 10 (10)
     - 0.17
     - 3.40

   * - سبعطاشر ألف وخمسمية واربعة فاصلة أربعة وخمسين
     - 17504.54
     -
        * 1000 (ألف)
        * 504.54 (خمسمية واربعة فاصلة أربعة وخمسين)
        * 504.4 (خمسية واربعة فاصلة أربعة وخمسين)
     - 0.24
     - 4.64

   * - :rspan:`3` Ordinal
     - المئة والخامس والسبعون من العصر الحجري
     - 175
     - 75 (الخامس والسبعون)
     - 0.29
     - 4.44

   * - الذكرى الرابعة لتخرج والدي
     - 4
     - 4 (الرابعة)
     - 0.20
     - 4.21

   * - كنتُ في الثامنة والعشرين وكان والدي في الخامسة والستين عند تخرجي من الجامعة
     -
        * 28 (الثامنة والعشرين)
        * 65 (الخامسة والستين)
     -
        * 8 (الثامنة)
        * 20 (العشرين)
        * 5 (الخامسة)
        * 60 (الستين)

     - 0.36
     - 4.02

   * - تعدت ثروته المليون
     - 1000000
     - None
     - 0.13
     - 3.75

   * - :rspan:`3` Duration
     - سأبقى في الأردن لمدة خمس سنوات وأربع أشهر و15 يوما و3 ساعات وخمس دقائق
     -
        * 5 Years
        * 4 Months
        * 15 Days
        * 3 Hours
        * 5 Minutes
     -
        * 5 Years
        * 4 Months
        * 15 Days
        * 3 Hours
        * 5 Minutes
     - 1.54
     - 4.04

   * - لقد قضيت فيه هذا البلد ما مدته خمسة عشرة سنة
     - 15 Years
     - 15 Years (خمسة عشر سنة)
     - 0.63
     - 3.58

   * - مئة وخمسة واربعين سنة
     - 145
     - None
     - 0.30
     - 5.16

   * - بقينا في الجامعة لمدة عامين
     - 2 Years
     - 2 Years
     - 0.51
     - 3.47

Speed is measured in a jupyter notebook using the magic command ``%%timeit -n 1000 -r 5``.
The notebook used for the comparison is available
`here <https://colab.research.google.com/drive/1hGINXWidFrfjO3gpj1wcu_yTAewd1Bqb?usp=sharing>`_.

For the time dimension, date ``06/11/2021`` is taken as reference.

Long text
*********

The long text is taken from `here <https://surahquran.com/tafsir-mokhtasar/altafsir.html>`_.

The text file is cleaned with :func:`~.keep_arabic_letters` and is available `here <https://drive.google.com/drive/folders/1ZCRDEuWtQlk9IMYRC3_h4JA2oEvQ7pPv?usp=sharing>`_.
The following are details of the cleaned text file:

* File size: 2.8 MB (Duckling timeouts after ~2.8 MB of text)
* File encoding: UTF-8 Unicode text
* Lines counts: 10364
* Words counts: 292074
* Characters counts: 1565476

Speed is measured using the magic command ``%%timeit -n 10 -r 5`` and the results are as follows:

.. list-table::
   :header-rows: 1
   :widths: 10 10 10

   * - Dimension
     - Maha
     - Duckling
   * - Ordinal
     - 246 ms ± 3.34 ms
     - 872 ms ± 7.85 ms
   * - Time
     - 28.9 s ± 66.5 ms
     - 28 s ± 13.6 ms
   * - Duration
     - 1.77 s ± 4.58 ms
     - 1.7 s ± 6.36 ms
   * - Numeral
     - 767 ms ± 3.52 ms
     - 914 ms ± 3.52 ms
   * - All
     - 32.8 s ± 2.28 s
     - 32.6 s ± 263 ms
