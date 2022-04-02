Overview
========

What is Maha?
-------------

Maha is a Python library that provides simple, yet powerful, functions for dealing with Arabic text.
It can be used to clean and parse text, files, and folders with or without streaming capability.

Cleaners
--------

This module provides a number of functions for cleaning Arabic text. These functions are
summarized into the following categories:

* :mod:`~.keep_fn`: Functions that keep only specific characters in a text.
* :mod:`~.remove_fn`: Functions that remove specific characters from a text.
* :mod:`~.normalize_fn`: Functions that converts similar characters into one common character.
* :mod:`~.replace_fn`: Functions that replace specific characters with other characters.
* :mod:`~.contains_fn`: Functions that check if a text contains specific characters.
* :mod:`~.num2text`: Contains the logic for converting numbers to text.

These modules expose a simple interface that is used in conjunction with the defined
:mod:`constants<maha.constants>` as well as the available :mod:`expressions <maha.expressions>`.
Custom constants/expressions are also supported and can be easily used.

Examples
********

* To keep :data:`~.ARABIC_LETTERS` and :data:`~.HARAKAT` only,
  you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import keep
    >>> sample_text = "البسملة : ( بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ )"
    >>> keep(sample_text, arabic_letters=True, harakat=True)
    'البسملة بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ'

* To remove :data:`~.PUNCTUATIONS`, you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import remove
    >>> sample_text = "البسملة : ( بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ )"
    >>> remove(sample_text, punctuations=True)
    'البسملة بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ'

* To normalize :data:`~.ALEF_VARIATIONS`, you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import normalize
    >>> sample_text = "أنا وأخي علي في المكتبةِ نَطلعُ على موضوع البرمجه"
    >>> normalize(sample_text, alef=True)
    'انا واخي علي في المكتبةِ نَطلعُ على موضوع البرمجه'

* To normalize all but :data:`~.ALEF_VARIATIONS`, you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import normalize
    >>> sample_text = "أنا وأخي علي في المكتبةِ نَطلعُ على موضوع البرمجه"
    >>> normalize(sample_text, alef=False, all=True)
    'أنا وأخي علي في المكتبهِ نَطلعُ علي موضوع البرمجه'

* To check if text contains :data:`~.ARABIC_LETTERS`, you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import contains
    >>> sample_text = "أنا وأخي علي في المكتبةِ نَدرسُ البرمجه"
    >>> contains(sample_text, arabic_letters=True)
    True

* To check if text contains :data:`~.ARABIC_LETTERS` and :data:`~.ENGLISH_LETTERS`,
  you can do the following:

.. code:: pycon

    >>> from maha.cleaners.functions import contains
    >>> sample_text = "أنا وأخي علي في المكتبةِ نَدرسُ البرمجه"
    >>> contains(sample_text, arabic_letters=True, english_letters=True)
    {'arabic_letters': True, 'english_letters': False}

Cleaners are robust against most real case scenarios and can output clean text.
Check the following example:

.. code:: pycon

    >>> from maha.cleaners.functions import remove
    >>> sample_text = "#بسم_الله_الرحمن_الرحيم"
    >>> remove(sample_text, punctuations=True)
    'بسم الله الرحمن الرحيم'

Cleaners also support the first robust **numbers to text** conversion. Check below examples:

.. code:: pycon

    >>> from maha.cleaners.functions import numbers_to_text
    >>> numbers_to_text("في المكتبة 152 كتاب")
    'في المكتبة مائة وإثنان وخمسون كتاب'
    >>> numbers_to_text("في المكتبة 152 كتاب", accusative=True)
    'في المكتبة مائة وإثنين وخمسين كتاب'
    >>> numbers_to_text("يقدر عدد سكان العالم حوالي 7.9 مليار خلال عام 2022")
    'يقدر عدد سكان العالم حوالي سبعة فاصلة تسعة مليار خلال عام ألفان وإثنان وعشرون'
    >>> numbers_to_text("يقدر عدد سكان العالم حوالي 7.9 مليار خلال عام 2022", accusative=True)
    'يقدر عدد سكان العالم حوالي سبعة فاصلة تسعة مليار خلال عام ألفين وإثنين وعشرين'
    >>> numbers_to_text("1,111,111")
    'مليون ومائة وأحد عشر ألف ومائة وأحد عشر'
    >>> numbers_to_text("0.5")
    'خمسة من عشرة'
    >>> numbers_to_text("0.0033")
    'ثلاثة وثلاثون من عشرة آلاف'
    >>> numbers_to_text("101.00102")
    'مائة وواحد فاصلة مائة وإثنان من مائة ألف'

In addition, :func:`~.numbers_to_text` function is compatible with
:func:`~.parse_dimension` numeral parsing. Check the following examples:

.. code:: pycon

    >>> from maha.cleaners.functions import numbers_to_text
    >>> from maha.parsers.functions import parse_dimension
    >>> parse_dimension(numbers_to_text("في المكتبة 152 كتاب"), numeral=True)[0].value
    152
    >>> parse_dimension(numbers_to_text("في المكتبة 152 كتاب", accusative=True), numeral=True)[
    ...     0
    ... ].value
    152
    >>> parse_dimension(
    ...     numbers_to_text("يقدر عدد سكان العالم حوالي 7.9 مليار خلال عام 2022"), numeral=True
    ... )[0].value
    7900000000
    >>> parse_dimension(numbers_to_text("1,111,111"), numeral=True)[0].value
    1111111
    >>> parse_dimension(numbers_to_text("0.5"), numeral=True)[0].value
    0.5
    >>> parse_dimension(numbers_to_text("0.0033"), numeral=True)[0].value
    0.0033
    >>> parse_dimension(numbers_to_text("101.00102"), numeral=True)[0].value
    101.00102

In general all cleaners provide the same interface.
Check the full list of functions :mod:`here <maha.cleaners.functions>`

How cleaners work
*****************

Cleaners rely on `regular expressions <https://en.wikipedia.org/wiki/Regular_expression>`_
to clean text. All regular expressions are constructed from your inputs on the fly. They
are efficient and fast. We use `regex library <https://pypi.org/project/regex/>`_
instead of the built-in `re <https://docs.python.org/3/library/re.html>`_ module.

.. note::
    If you need to clean a large amount of text or files, it is recommended to use
    :mod:`processors <maha.processors>` instead.


Parsers
-------

This module provides a number of rules for extracting useful values from Arabic text.
This includes extracting :mod:`constants<maha.constants>` and :mod:`expressions <maha.expressions>`
in addition to extracting specific dimensions such as extracting duration, numeral, or time.

.. tip::
    Before parsing a text, it is recommended to either remove all harakat
    using :func:`~.remove` or keep arabic letters only using :func:`~.keep`.

The module provides the following simple interfaces to parse text.

* The :func:`~.parse` function is used to parse any of the available
  :mod:`constants<maha.constants>` and :mod:`expressions <maha.expressions>`. It is also
  possible to use custom constants/expressions.

* The :func:`~.parse_dimension` function is used to parse any of the available dimensions.
  The available dimensions are ``duration``,  ``time``, ``numeral``, ``ordinal`` and ``names``.
  To create your own dimension, check out :doc:`custom dimension<development/custom_dimension>`.
  If you would like to contribute your custom dimension to the project, check
  :doc:`contribution guidelines<contributing>`.

Examples
********

* To extract all :data:`~.ARABIC` characters, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse
    >>> sample_text = "أنا وأخي في المكتبةِ نَدرسُ برمجه Python "
    >>> parse(sample_text, arabic=True, include_space=True)
    [Dimension(body=أنا وأخي في المكتبةِ نَدرسُ برمجه , value=أنا وأخي في المكتبةِ نَدرسُ برمجه , start=0, end=34, dimension_type=DimensionType.ARABIC)]

* To extract emails, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse
    >>> sample_text = "الإيميل: test@example.com أو test2@example.com"
    >>> parse(sample_text, emails=True)
    [Dimension(body=test@example.com, value=test@example.com, start=9, end=25, dimension_type=DimensionType.EMAILS), Dimension(body=test2@example.com, value=test2@example.com, start=29, end=46, dimension_type=DimensionType.EMAILS)]

* To extract arabic hashtags and all mentions, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse
    >>> sample_text = "#مها #maha @Maha @مها"
    >>> parse(sample_text, arabic_hashtags=True, mentions=True)
    [Dimension(body=#مها, value=#مها, start=0, end=4, dimension_type=DimensionType.ARABIC_HASHTAGS), Dimension(body=@Maha, value=@Maha, start=11, end=16, dimension_type=DimensionType.MENTIONS), Dimension(body=@مها, value=@مها, start=17, end=21, dimension_type=DimensionType.MENTIONS)]

* To extract arabic hashtags and all mentions, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse
    >>> sample_text = "#مها #maha @Maha @مها"
    >>> parse(sample_text, arabic_hashtags=True, mentions=True)
    [Dimension(body=#مها, value=#مها, start=0, end=4, dimension_type=DimensionType.ARABIC_HASHTAGS), Dimension(body=@Maha, value=@Maha, start=11, end=16, dimension_type=DimensionType.MENTIONS), Dimension(body=@مها, value=@مها, start=17, end=21, dimension_type=DimensionType.MENTIONS)]

* To extract numerals, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> parse_dimension("العام ثلاثمئة وستة وخمسون يوما او 12 شهرا", numeral=True)
    [Dimension(body=ثلاثمئة وستة وخمسون, value=356, start=6, end=25, dimension_type=DimensionType.NUMERAL), Dimension(body=12, value=12, start=34, end=36, dimension_type=DimensionType.NUMERAL)]
    >>> parse_dimension("مليون واربعمية وستة عشر", numeral=True)[0].value
    1000416
    >>> parse_dimension("خمسين فاصلة ثلاثة واربعين", numeral=True)[0].value
    50.43
    >>> parse_dimension("تسعة عشر الف ومئة", numeral=True)[0].value
    19100
    >>> parse_dimension(
    ...     "تسع وتسعين مليار وتسعة وتسعين الف وتسع مائة وتسع وتسعين ", numeral=True
    ... )[0].value
    99000099999
    >>> parse_dimension("100 وخمسين", numeral=True)[0].value
    150
    >>> parse_dimension("100 و1", numeral=True)[0].value
    101


* To extract duration, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> parse_dimension("العام ثلاثمئة وستة وخمسون يوما او 12 شهرا", duration=True)
    [Dimension(body=ثلاثمئة وستة وخمسون يوما, value=DurationValue(values=[ValueUnit(value=356, unit=<DurationUnit.DAYS: 4>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=6, end=30, dimension_type=DimensionType.DURATION), Dimension(body=12 شهرا, value=DurationValue(values=[ValueUnit(value=12, unit=<DurationUnit.MONTHS: 6>)], normalized_unit=<DurationUnit.SECONDS: 1>), start=34, end=41, dimension_type=DimensionType.DURATION)]
    >>> parse_dimension("مليون ثانية ودقيقة", duration=True)[0].value
    DurationValue(values=[ValueUnit(value=1, unit=<DurationUnit.MINUTES: 2>), ValueUnit(value=1000000, unit=<DurationUnit.SECONDS: 1>)], normalized_unit=<DurationUnit.SECONDS: 1>)
    >>> parse_dimension("مليون ثانية ودقيقة", duration=True)[0].value.normalized_value
    ValueUnit(value=1000060, unit=<DurationUnit.SECONDS: 1>)
    >>> parse_dimension("يوم ونصف دقيقة", duration=True)[0].value
    DurationValue(values=[ValueUnit(value=1, unit=<DurationUnit.DAYS: 4>), ValueUnit(value=0.5, unit=<DurationUnit.MINUTES: 2>)], normalized_unit=<DurationUnit.SECONDS: 1>)
    >>> parse_dimension("ساعة الا ثلث", duration=True)[0].value.normalized_value
    ValueUnit(value=2400, unit=<DurationUnit.SECONDS: 1>)
    >>> parse_dimension("يومين و10 ساعات", duration=True)[0].value.values
    [ValueUnit(value=2, unit=<DurationUnit.DAYS: 4>), ValueUnit(value=10, unit=<DurationUnit.HOURS: 3>)]

* To extract ordinal, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> parse_dimension("الأول", ordinal=True)
    [Dimension(body=الأول, value=1, start=0, end=5, dimension_type=DimensionType.ORDINAL)]
    >>> parse_dimension("الثالث والرابع", ordinal=True)
    [Dimension(body=الثالث, value=3, start=0, end=6, dimension_type=DimensionType.ORDINAL), Dimension(body=الرابع, value=4, start=8, end=14, dimension_type=DimensionType.ORDINAL)]
    >>> parse_dimension("الخمسين", ordinal=True)[0].value
    50
    >>> parse_dimension("الثاني والمئة", ordinal=True)
    [Dimension(body=الثاني, value=2, start=0, end=6, dimension_type=DimensionType.ORDINAL), Dimension(body=المئة, value=100, start=8, end=13, dimension_type=DimensionType.ORDINAL)]
    >>> parse_dimension("المليون والعشرين", ordinal=True)
    [Dimension(body=المليون, value=1000000, start=0, end=7, dimension_type=DimensionType.ORDINAL), Dimension(body=العشرين, value=20, start=9, end=16, dimension_type=DimensionType.ORDINAL)]
    >>> parse_dimension("الألف والمئتين", ordinal=True)
    [Dimension(body=الألف, value=1000, start=0, end=5, dimension_type=DimensionType.ORDINAL), Dimension(body=المئتين, value=200, start=7, end=14, dimension_type=DimensionType.ORDINAL)]

* To extract time, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> from datetime import datetime
    >>> now = datetime(2021, 9, 15)
    >>> parse_dimension("غدا", time=True)
    [Dimension(body=غدا, value=TimeValue(days=1), start=0, end=3, dimension_type=DimensionType.TIME)]
    >>> parse_dimension("غدا الساعة الرابعة مساء", time=True)[0].value + now
    datetime.datetime(2021, 9, 16, 16, 0)
    >>> parse_dimension("السنة القادمة الموافق 15/9", time=True)[0].value + now
    datetime.datetime(2022, 9, 15, 0, 0)
    >>> parse_dimension("عام الفين وواحد وعشرين", time=True)[0].value
    TimeValue(year=2021)
    >>> (
    ...     parse_dimension("الأسبوع الماضي يوم السبت الساعة 11 و30 دقيقة", time=True)[0].value
    ...     + now
    ... )
    datetime.datetime(2021, 9, 11, 11, 30)
    >>> output = parse_dimension("الشهر القادم", time=True)[0].value
    >>> output.is_months_set()
    True

* Hijri date parsing is supported as well:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> from datetime import datetime
    >>> now = datetime(2021, 9, 15)
    >>> output = parse_dimension("أول اثنين من شهر جمادى الأول من عام 1443", time=True)[0]
    >>> output
    Dimension(body=أول اثنين من شهر جمادى الأول من عام 1443, value=TimeValue(year=1443, month=5, day=1, weekday=MO(+1), hijri=True), start=0, end=40, dimension_type=DimensionType.TIME)
    >>> output.value + now
    datetime.datetime(2021, 12, 6, 0, 0)
    >>> parse_dimension("بداية رمضان القادم", time=True)[0].value + now
    datetime.datetime(2022, 4, 2, 0, 0)
    >>> parse_dimension("عام الف واربعمئة وعشرين هجري", time=True)[0].value
    TimeValue(year=1420, hijri=True)
    >>> parse_dimension("العيد يبدأ اول شوال", time=True)[0].value + now
    datetime.datetime(2022, 5, 2, 0, 0)
    >>> output.value.is_months_set()
    True
    >>> output.value.is_days_set()
    True
    >>> output.value.is_hijri_set()
    True

* It is also possible to extract time intervals as follows:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> from datetime import datetime
    >>> now = datetime(2021, 9, 15)
    >>> parse_dimension("من الساعة 9 الى 11 صباحا", time=True)
    [Dimension(body=من الساعة 9 الى 11 صباحا, value=TimeInterval(start=TimeValue(am_pm='AM', hour=9, minute=0, second=0, microsecond=0), end=TimeValue(am_pm='AM', hour=11, minute=0, second=0, microsecond=0)), start=0, end=24, dimension_type=DimensionType.TIME)]
    >>> interval = parse_dimension("من 13 هذا الشهر الى 20 الشهر القادم", time=True)[0].value
    >>> interval
    TimeInterval(start=TimeValue(months=0, day=13), end=TimeValue(months=1, day=20))
    >>> interval.start + now
    datetime.datetime(2021, 9, 13, 0, 0)
    >>> interval.end + now
    datetime.datetime(2021, 10, 20, 0, 0)
    >>> parse_dimension("الساعة ثلاثة الا ثلث للساعة 4 ونص", time=True)[0].value
    TimeInterval(start=TimeValue(hour=2, minute=40, second=0, microsecond=0), end=TimeValue(hour=4, minute=30, second=0, microsecond=0))
    >>> parse_dimension("من 6 اكتوبر", time=True)[0].value
    TimeInterval(start=TimeValue(month=10, day=6), end=None)
    >>> parse_dimension("حتى الرابعة وربع بعد العصر", time=True)[0].value
    TimeInterval(start=None, end=TimeValue(am_pm='PM', hour=16, minute=15, second=0, microsecond=0))


* To extract names, you can do the following:

.. code:: pycon

    >>> from maha.parsers.functions import parse_dimension
    >>> parse_dimension("محمد", names=True)
    [Dimension(body=محمد, value=محمد, start=0, end=4, dimension_type=DimensionType.NAME)]
    >>> parse_dimension("مريم", names=True)
    [Dimension(body=مريم, value=مريم, start=0, end=4, dimension_type=DimensionType.NAME)]
    >>> parse_dimension("اسمي فاطمة", names=True)
    [Dimension(body=فاطمة, value=فاطمة, start=5, end=10, dimension_type=DimensionType.NAME)]
    >>> parse_dimension("انا آنا", names=True)
    [Dimension(body=آنا, value=آنا, start=4, end=7, dimension_type=DimensionType.NAME)]
    >>> parse_dimension("ادهم في المكتبة", names=True)
    [Dimension(body=ادهم, value=ادهم, start=0, end=4, dimension_type=DimensionType.NAME)]
    >>> parse_dimension("جاك", names=True)
    [Dimension(body=جاك, value=جاك, start=0, end=3, dimension_type=DimensionType.NAME)]

How parsers work
*****************

Parsers also rely on `regular expressions <https://en.wikipedia.org/wiki/Regular_expression>`_
to extract values from text. Dimension parsers use very sophisticated regular expressions,
which we call Rules. Rules are defined in :mod:`maha.parsers.rules`. All rules are
optimized, compiled and cached to ensure best performance possible.

Rules can be easily extended, check :doc:`custom dimension<development/custom_dimension>`.


Processors
----------

This module extends the functionality of cleaners to work on files and folders. It
provides a way to process files in a streaming fashion, which is useful for large
files. Processors are developed to extend any future classes that can work on files
and folders.

The available processors are:

* :class:`~.TextProcessor`: Processes simple texts.
* :class:`~.FileProcessor`: Processes small files.
* :class:`~.StreamTextProcessor`: Processes stream of texts.
* :class:`~.StreamFileProcessor`: Processes files in a streaming fashion.


Examples
********

* To process a simple text, you can do the following:

.. code:: pycon

    >>> from maha.processors import TextProcessor
    >>> sample_text = """
    ...  بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ
    ... الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
    ... الرَّحْمَنِ الرَّحِيمِ
    ... مَالِكِ يَوْمِ الدِّينِ
    ... إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
    ... اهدِنَا الصِّرَاطَ الْمُسْتَقِيمَ
    ... صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلاَ الضَّالِّينَ
    ... """
    >>> processor = TextProcessor.from_text(sample_text, sep="\n")
    >>> cleaned_text = (
    ...     processor.normalize(alef=True).keep(arabic_letters=True).drop_empty_lines().text
    ... )
    >>> print(cleaned_text)
    بسم الله الرحمن الرحيم
    الحمد لله رب العالمين
    الرحمن الرحيم
    مالك يوم الدين
    اياك نعبد واياك نستعين
    اهدنا الصراط المستقيم
    صراط الذين انعمت عليهم غير المغضوب عليهم ولا الضالين
    >>> # To print the unique characters
    >>> unique_char = processor.get(unique_characters=True)
    >>> unique_char.sort()
    >>> unique_char
    [' ', 'ا', 'ب', 'ت', 'ح', 'د', 'ذ', 'ر', 'س', 'ص', 'ض', 'ط', 'ع', 'غ', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']

* To streamly process a file, you can do the following:

.. code:: pycon

    >>> from pathlib import Path
    >>> import maha
    >>> # This is a sample file that comes with Maha.
    >>> resource_path = Path(maha.__file__).parents[1] / "sample_data/surah_al-ala.txt"
    >>> from maha.processors import StreamFileProcessor
    >>> proc = StreamFileProcessor(resource_path)
    >>> proc = proc.normalize(all=True).keep(arabic_letters=True).drop_empty_lines()
    >>> # To start processing the file, run the following commented code.
    >>> # proc.process_and_save(Path("output.txt"))
