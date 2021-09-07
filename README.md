<hr />
<p align="center">
    <a href="#"><img src="images/logo.png" width= 400px></a>
    <br />
    <br />
    <img src="https://github.com/TRoboto/maha/actions/workflows/ci.yml/badge.svg", alt="CI">
    <img src="https://img.shields.io/badge/readme-tested-brightgreen.svg", alt="Examples are tested">
    <a href="https://codecov.io/gh/TRoboto/Maha"><img src="https://codecov.io/gh/TRoboto/Maha/branch/main/graph/badge.svg?token=9CBWXT8URA", alt="codecov"></a>
    <a href="https://discord.gg/WdNCU6yG"><img src="https://img.shields.io/discord/863503708385312769.svg?label=discord&logo=discord" alt="Discord"></a>
    <a href="https://opensource.org/licenses/BSD-3-Clause"><img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg" alt="License"></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <br />
    <br />
    An Arabic text processing library intended for use in NLP applications.

</p>
<hr />

Maha is a text processing library specially developed to deal with Arabic text. The beta version can be used to clean and parse text, files, and folders with or without streaming capability.

## Table of Content

- [Installation](#installation)
- [Quick start](#quick-start)
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

Cleaners module contains a set of functions that operate on texts. It can be used to [keep](), [remove](), or [replace]() specific characters as well as [normalize]() characters and check if the text [contains]() specific characters.

**Examples**

```py
>>> from maha.cleaners.functions import keep, remove, contains, replace
>>> text = """
... 1. بِسْمِ اللَّـهِ الرَّحْمَـٰـــنِ الرَّحِيمِ
... 2. In the name of God, the most gracious, the most merciful
... """
>>> keep(text, arabic=True)
'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ'
>>> keep(text, arabic_letters=True)
'بسم الله الرحمن الرحيم'
>>> keep(text, arabic_letters=True, harakat=True)
'بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ'
>>> remove(text, numbers=True, punctuations=True)
'بِسْمِ اللَّـهِ الرَّحْمَـٰـــنِ الرَّحِيمِ\n In the name of God the most gracious the most merciful'
>>> contains(text, numbers=True)
True
>>> contains(text, hashtags=True, arabic=True, emails=True)
{'arabic': True, 'emails': False, 'hashtags': False}
>>> replace(keep(text, english_letters=True), "God", "Allah")
'In the name of Allah the most gracious the most merciful'

```

```py
>>> from maha.cleaners.functions import keep, normalize
>>> text = "وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ"
>>> keep(text, arabic_letters=True)
'وما أرسلناك إلا رحمة للعالمين'
>>> normalize(keep(text, arabic_letters=True), alef=True, teh_marbuta=True)
'وما ارسلناك الا رحمه للعالمين'

>>> text = 'ﷺ'

>>> normalize(text, ligatures=True)
'صلى الله عليه وسلم'

```

<!--
Maha contains few samples for testing.

```py
from pathlib import Path

resource_path = Path(__file__).parent / "templates"
data = resource_path.joinpath("temp_file").read_bytes()
``` -->

## Documentation

Documentation are hosted at [ReadTheDocs](https://maha.readthedocs.io).

## Contributing

Maha welcomes and encourages everyone to contribute. Contributions are always appreciated. Feel free to take a look at our contribution guidelines in the [documentation](#).

## License

Maha is BSD-licensed.
