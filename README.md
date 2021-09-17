<hr />
<p align="center">
    <a href="#"><img src="https://github.com/TRoboto/Maha/raw/main/images/logo.png" width= 400px></a>
    <br />
    <br />
    <img src="https://github.com/TRoboto/maha/actions/workflows/ci.yml/badge.svg", alt="CI">
    <img src="https://img.shields.io/badge/readme-tested-brightgreen.svg", alt="Examples are tested">
    <a href="https://codecov.io/gh/TRoboto/Maha"><img src="https://codecov.io/gh/TRoboto/Maha/branch/main/graph/badge.svg?token=9CBWXT8URA", alt="codecov"></a>
    <a href="https://discord.gg/6W2tRFE7k4"><img src="https://img.shields.io/discord/863503708385312769.svg?label=discord&logo=discord" alt="Discord"></a>
    <a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <a href="http://mypy-lang.org/"><img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy"></a>
    <br />
    <br />
    An Arabic text processing library intended for use in NLP applications.

</p>
<hr />

Maha is a text processing library specially developed to deal with Arabic text. The beta version can be used to clean and parse text, files, and folders with or without streaming capability.

If you need help or want to discuss topics related to Maha, feel free to reach out to our [Discord](https://discord.gg/6W2tRFE7k4) server. If you would like to submit a bug report or feature request, please open an issue.

## Table of Content

- [Installation](#installation)
- [Quick start](#quick-start)
  - [Cleaners](#cleaners)
  - [Parsers](#parsers)
  - [Processors](#processors)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Installation

Simply run the following to install Maha:

```bash
pip install mahad # pronounced maha d
```

For source installation, check the [documentation](#).

## Quick start

As of now, Maha supports three main modules: cleaners, parsers and processors.

### Cleaners

Cleaners, from its name, contain a set of functions for cleaning texts. They can be used to [keep](), [remove](), or [replace]() specific characters as well as [normalize]() characters and check if the text [contains]() specific characters.

**Examples**

```py
>>> from maha.cleaners.functions import keep, remove, contains, replace
>>> sample_text = """
... 1. بِسْمِ اللَّـهِ الرَّحْمَـٰـــنِ الرَّحِيمِ
... 2. In the name of God, the most gracious, the most merciful
... """
>>> keep(sample_text, arabic=True)
'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ'
>>> keep(sample_text, arabic_letters=True)
'بسم الله الرحمن الرحيم'
>>> keep(sample_text, arabic_letters=True, harakat=True)
'بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ'
>>> remove(sample_text, numbers=True, punctuations=True)
'بِسْمِ اللَّـهِ الرَّحْمَـٰـــنِ الرَّحِيمِ\n In the name of God the most gracious the most merciful'
>>> contains(sample_text, numbers=True)
True
>>> contains(sample_text, hashtags=True, arabic=True, emails=True)
{'arabic': True, 'emails': False, 'hashtags': False}
>>> replace(keep(sample_text, english_letters=True), "God", "Allah")
'In the name of Allah the most gracious the most merciful'

```

```py
>>> from maha.cleaners.functions import keep, normalize
>>> sample_text = "وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ"
>>> keep(sample_text, arabic_letters=True)
'وما أرسلناك إلا رحمة للعالمين'
>>> normalize(keep(sample_text, arabic_letters=True), alef=True, teh_marbuta=True)
'وما ارسلناك الا رحمه للعالمين'
>>> sample_text = 'ﷺ'
>>> normalize(sample_text, ligatures=True)
'صلى الله عليه وسلم'

```

```py
>>> from maha.cleaners.functions import reduce_repeated_substring, remove_arabic_letter_dots, connect_single_letter_word
>>> sample_text = "ههههههههههه أضحكني"
>>> reduce_repeated_substring(sample_text)
'هه أضحكني'
>>> remove_arabic_letter_dots(sample_text)
'ههههههههههه أصحكٮى'
>>> connect_single_letter_word('محمد و احمد', waw=True)
'محمد واحمد'

```

### Parsers

Parsers include a set of rules for extracting values from text. All rules can be accessed and utilized by two main functions, [parse]() and [parse_dimension]().

**Examples**

Parse character and simple expressions.

```py
>>> from maha.parsers.functions import parse
>>> sample_text = '@Maha مها هي مكتبة لمساعدتك في التعامل مع النص العربي @مها test@example.com'
>>> parse(sample_text, emails=True)
[Dimension(body=test@example.com, value=test@example.com, start=59, end=75, dimension_type=DimensionType.EMAILS)]
>>> parse(sample_text, english_mentions=True)
[Dimension(body=@Maha, value=@Maha, start=0, end=5, dimension_type=DimensionType.ENGLISH_MENTIONS)]
>>> parse(sample_text, mentions=True, emails=True)
[Dimension(body=test@example.com, value=test@example.com, start=59, end=75, dimension_type=DimensionType.EMAILS), Dimension(body=@Maha, value=@Maha, start=0, end=5, dimension_type=DimensionType.MENTIONS), Dimension(body=@مها, value=@مها, start=54, end=58, dimension_type=DimensionType.MENTIONS)]

```

Parse time.

```py
>>> from maha.parsers.functions import parse_dimension
>>> from datetime import datetime
>>> now = datetime(2021, 9, 1)
>>> sample_text = 'الثالث من شباط بعد ثلاث سنين يوم السبت الساعة خمسة واثنين واربعين دقيقة العصر'
>>> output_time = parse_dimension(sample_text, time=True)[0]
>>> output_time
Dimension(body=الثالث من شباط بعد ثلاث سنين يوم السبت الساعة خمسة واثنين واربعين دقيقة العصر, value=TimeValue(years=3, am_pm='PM', month=2, day=3, weekday=SA, hour=17, minute=42, second=0, microsecond=0), start=0, end=77, dimension_type=DimensionType.TIME)
>>> output_time.value.is_hours_set()
True
>>> output_time.value + now
datetime.datetime(2024, 2, 3, 17, 42)

```

```py
>>> from maha.parsers.functions import parse_dimension
>>> from datetime import datetime
>>> now = datetime(2021, 9, 1)
>>> now + parse_dimension('غدا الساعة الحادية عشر', time=True)[0].value
datetime.datetime(2021, 9, 2, 11, 0)
>>> now + parse_dimension('الخميس الأسبوع الجاي عالوحدة ونص المسا', time=True)[0].value
datetime.datetime(2021, 9, 9, 13, 30)
>>> now + parse_dimension('عام الفين وواحد', time=True)[0].value
datetime.datetime(2001, 9, 1, 0, 0)

```

Parse duration.

```py
>>> from maha.parsers.functions import parse_dimension
>>> output = parse_dimension('شهرين واربعين يوم', duration=True)[0].value
>>> output
DurationValue(values=[ValueUnit(value=2, unit=<DurationUnit.MONTHS: 6>), ValueUnit(value=40, unit=<DurationUnit.DAYS: 4>)], normalized_unit=<DurationUnit.SECONDS: 1>)
>>> print('2 months and 40 days in seconds:', output.normalized_value.value)
2 months and 40 days in seconds: 8640000
>>> parse_dimension('الف وخمسمية دقيقة وساعة', duration=True)[0].value
DurationValue(values=[ValueUnit(value=1, unit=<DurationUnit.HOURS: 3>), ValueUnit(value=1500, unit=<DurationUnit.MINUTES: 2>)], normalized_unit=<DurationUnit.SECONDS: 1>)
>>> parse_dimension('30 مليون ثانية', duration=True)[0].value
DurationValue(values=[ValueUnit(value=30000000, unit=<DurationUnit.SECONDS: 1>)], normalized_unit=<DurationUnit.SECONDS: 1>)

```

Parse numeral.

```py
>>> from maha.parsers.functions import parse_dimension
>>> parse_dimension('عشرة', numeral=True)
[Dimension(body=عشرة, value=10, start=0, end=4, dimension_type=DimensionType.NUMERAL)]
>>> parse_dimension('عشرين الف وخمسمية وثلاثة واربعين', numeral=True)[0].value
20543
>>> parse_dimension('حدعشر', numeral=True)[0].value
11
>>> parse_dimension('200 وعشرين', numeral=True)[0].value
220
>>> parse_dimension('عشرين فاصلة اربعة', numeral=True)[0].value
20.4
>>> parse_dimension('10.5 الف', numeral=True)[0].value
10500.0
>>> parse_dimension('مليون وستمية وعشرة', numeral=True)[0].value
1000610
>>> parse_dimension('اطنعش', numeral=True)[0].value
12
>>> parse_dimension('عشرة وعشرين', numeral=True)[0].value
30

```

Parse ordinal.

```py
>>> from maha.parsers.functions import parse_dimension
>>> parse_dimension('الأول', ordinal=True)
[Dimension(body=الأول, value=1, start=0, end=5, dimension_type=DimensionType.ORDINAL)]
>>> parse_dimension('العاشر', ordinal=True)[0].value
10
>>> parse_dimension('التاسع والخمسين', ordinal=True)[0].value
59
>>> parse_dimension('المئة والثالث والثلاثون', ordinal=True)[0].value
133
>>> parse_dimension('المليون', ordinal=True)[0].value
1000000

```

### Processors

Processors are wrappers for cleaners to clean text files and folders. There are two types of processors, the simple [TextProcessor]() and [FileProcessor]() processors, and the [StreamTextProcessor]() and [StreamFileProcessor]() processors.

**Examples**

We can use the sample data that comes with Maha.

```py
>>> from pathlib import Path
>>> import maha

>>> resource_path = Path(maha.__file__).parents[1] / "sample_data/surah_al-ala.txt"
>>> data = resource_path.read_text()
>>> print(data)
﷽
   سَبِّحِ اسْمَ رَبِّكَ الْأَعْلَى ﴿1﴾
الَّذِي خَلَقَ فَسَوَّىٰ ﴿2﴾
وَالَّذِي قَدَّرَ فَهَدَىٰ ﴿3﴾
وَالَّذِي أَخْرَجَ الْمَرْعَىٰ ﴿4﴾
فَجَعَلَهُ غُثَاءً أَحْوَىٰ ﴿5﴾
سَنُقْرِئُكَ فَلَا تَنْسَىٰ ﴿6﴾
إِلَّا مَا شَاءَ اللَّهُ ۚ إِنَّهُ يَعْلَمُ الْجَهْرَ وَمَا يَخْفَىٰ ﴿7﴾
وَنُيَسِّرُكَ لِلْيُسْرَىٰ ﴿8﴾
فَذَكِّرْ إِنْ نَفَعَتِ الذِّكْرَىٰ ﴿9﴾
سَيَذَّكَّرُ مَنْ يَخْشَىٰ ﴿10﴾
وَيَتَجَنَّبُهَا الْأَشْقَى ﴿11﴾
الَّذِي يَصْلَى النَّارَ الْكُبْرَىٰ ﴿12﴾
ثُمَّ لَا يَمُوتُ فِيهَا وَلَا يَحْيَىٰ ﴿13﴾
قَدْ أَفْلَحَ مَنْ تَزَكَّىٰ ﴿14﴾
وَذَكَرَ اسْمَ رَبِّهِ فَصَلَّىٰ ﴿15﴾
بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا ﴿16﴾
وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ ﴿17﴾
إِنَّ هَٰذَا لَفِي الصُّحُفِ الْأُولَىٰ ﴿18﴾
صُحُفِ إِبْرَاهِيمَ وَمُوسَىٰ ﴿19﴾
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>

>>> from maha.processors import FileProcessor
>>> proc = FileProcessor(resource_path)
>>> cleaned = proc.normalize(all=True).keep(arabic_letters=True).drop_empty_lines()
>>> print(cleaned.text)
بسم الله الرحمن الرحيم
سبح اسم ربك الاعلي
الذي خلق فسوي
والذي قدر فهدي
والذي اخرج المرعي
فجعله غثاء احوي
سنقريك فلا تنسي
الا ما شاء الله انه يعلم الجهر وما يخفي
ونيسرك لليسري
فذكر ان نفعت الذكري
سيذكر من يخشي
ويتجنبها الاشقي
الذي يصلي النار الكبري
ثم لا يموت فيها ولا يحيي
قد افلح من تزكي
وذكر اسم ربه فصلي
بل توثرون الحياه الدنيا
والاخره خير وابقي
ان هذا لفي الصحف الاولي
صحف ابراهيم وموسي

>>> unique_char = cleaned.get(unique_characters=True)
>>> unique_char.sort()
>>> unique_char
[' ', 'ء', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']

```

Additional step is required for stream processors. You need to call `~.process_and_save` function after calling at least one clean function

```py
...
from maha.processors import StreamFileProcessor

proc = StreamFileProcessor(resource_path)
cleaned = proc.normalize(all=True).keep(arabic_letters=True).drop_empty_lines()
# ----------------
cleaned.process_and_save('output_file.txt')
# ----------------
...
```

## Documentation

Documentation are hosted at [ReadTheDocs](https://maha.readthedocs.io).

## Contributing

Maha welcomes and encourages everyone to contribute. Contributions are always appreciated. Feel free to take a look at our contribution guidelines in the [documentation](#).

## License

Maha is BSD-licensed.
