"""
Functions that operate on a string and remove certain characters.
"""

__all__ = [
    "remove",
    "remove_strings",
    "remove_extra_spaces",
    "remove_punctuations",
    "remove_english",
    "remove_all_harakat",
    "remove_harakat",
    "remove_numbers",
    "remove_tatweel",
    "remove_patterns",
    "remove_emails",
    "remove_hashtags",
    "remove_links",
    "remove_mentions",
    "reduce_repeated_substring",
    "remove_arabic_letters_dots",
]

from typing import List, Union

import maha.cleaners.functions as functions
from maha.constants import (
    ALL_HARAKAT,
    ARABIC,
    ARABIC_LETTERS,
    ARABIC_LIGATURES,
    ARABIC_NUMBERS,
    ARABIC_PUNCTUATIONS,
    EMPTY,
    ENGLISH,
    ENGLISH_CAPITAL_LETTERS,
    ENGLISH_LETTERS,
    ENGLISH_NUMBERS,
    ENGLISH_PUNCTUATIONS,
    ENGLISH_SMALL_LETTERS,
    HARAKAT,
    NUMBERS,
    PATTERN_ARABIC_HASHTAGS,
    PATTERN_ARABIC_MENTIONS,
    PATTERN_EMAILS,
    PATTERN_EMOJIS,
    PATTERN_ENGLISH_HASHTAGS,
    PATTERN_ENGLISH_MENTIONS,
    PATTERN_HASHTAGS,
    PATTERN_LINKS,
    PATTERN_MENTIONS,
    PUNCTUATIONS,
    SPACE,
    TATWEEL,
    ARABIC_Dotless_Dictionary,
)
from maha.utils import check_positive_integer


def remove(
    text: str,
    arabic: bool = False,
    english: bool = False,
    arabic_letters: bool = False,
    english_letters: bool = False,
    english_small_letters: bool = False,
    english_capital_letters: bool = False,
    numbers: bool = False,
    harakat: bool = False,
    all_harakat: bool = False,
    tatweel: bool = False,
    punctuations: bool = False,
    arabic_numbers: bool = False,
    english_numbers: bool = False,
    arabic_punctuations: bool = False,
    english_punctuations: bool = False,
    arabic_ligatures: bool = False,
    arabic_hashtags: bool = False,
    arabic_mentions: bool = False,
    emails: bool = False,
    english_hashtags: bool = False,
    english_mentions: bool = False,
    hashtags: bool = False,
    links: bool = False,
    mentions: bool = False,
    emojis: bool = False,
    use_space: bool = True,
    custom_strings: Union[List[str], str] = None,
    custom_patterns: Union[List[str], str] = None,
):

    """Removes certain characters from the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix PATTERN_ from the parameter name

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Remove :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Remove :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Remove :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Remove :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Remove :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Remove :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Remove :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Remove :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Remove :data:`~.ALL_HARAKAT` characters, by default False
    tatweel : bool, optional
        Remove :data:`~.TATWEEL` character, by default False
    punctuations : bool, optional
        Remove :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Remove :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Remove :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Remove :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Remove :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
    arabic_ligatures : bool, optional
        Remove :data:`~.ARABIC_LIGATURES` words, by default False
    arabic_hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ARABIC_HASHTAGS`,
        by default False
    arabic_mentions : bool, optional
        Remove Arabic mentions using the pattern :data:`~.PATTERN_ARABIC_MENTIONS`,
        by default False
    emails : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_EMAILS`,
        by default False
    english_hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_HASHTAGS`,
        by default False
    english_mentions : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_ENGLISH_MENTIONS`,
        by default False
    hashtags : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_HASHTAGS`,
        by default False
    links : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_LINKS`,
        by default False
    mentions : bool, optional
        Remove Arabic hashtags using the pattern :data:`~.PATTERN_MENTIONS`,
        by default False
    emojis : bool, optional
        Remove emojis using the pattern :data:`~.PATTERN_EMOJIS`,
        by default False
    use_space : bool, optional
        False to not replace with space, check :func:`~.remove_strings`
        for more information, by default True
    custom_strings : Union[List[str], str], optional
        Include any other string(s), by default None
    custom_patterns , optional
        Include any other regular expression patterns, by default None

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        If no argument is set to True

    Examples
    --------
    .. code-block:: pycon

        >>> text = "ويندوز 11 سيدعم تطبيقات نظام أندرويد. #Windows11"
        >>> remove(text, hashtags=True)
        'ويندوز 11 سيدعم تطبيقات نظام أندرويد.'

    .. code-block:: pycon

        >>> text = "قَالَ رَبِّ اشْرَحْ لِي صَدْرِي.."
        >>> remove(text, all_harakat=True, punctuations=True)
        'قال رب اشرح لي صدري'
    """
    if not text:
        return EMPTY

    custom_strings = custom_strings or []
    custom_patterns = custom_patterns or []

    # current function arguments
    current_arguments = locals()
    constants = globals()

    # characters to remove
    chars_to_remove = []
    # patterns to remove
    patterns_to_remove = []

    if isinstance(custom_strings, str):
        custom_strings = [custom_strings]

    if isinstance(custom_patterns, str):
        custom_patterns = [custom_patterns]

    chars_to_remove.extend(custom_strings)
    patterns_to_remove.extend(custom_patterns)

    # Since each argument has the same name as the corresponding constant
    # (But, patterns should be prefixed with "PATTERN_" to match the actual pattern.)
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            chars_to_remove += const
            continue
        # check for pattern
        pattern = constants.get("PATTERN_" + arg.upper())
        if pattern and value is True:
            patterns_to_remove.append(pattern)

    if not (chars_to_remove or patterns_to_remove):
        raise ValueError("At least one argument should be True")

    output = text
    # remove using patterns
    if patterns_to_remove:
        output = remove_patterns(output, patterns_to_remove)

    if chars_to_remove:
        # check for constants that cannot be replaced with a space
        if all_harakat:
            output = remove_strings(output, ALL_HARAKAT, False)
        elif harakat:
            output = remove_strings(output, HARAKAT, False)
        if tatweel:
            output = remove_strings(output, TATWEEL, False)

        # remove duplicates
        chars_to_remove = list(set(chars_to_remove))
        output = remove_strings(output, chars_to_remove, use_space)

    return output


def reduce_repeated_substring(
    text: str, min_repeated: int = 3, reduce_to: int = 2
) -> str:
    """Reduces consecutive substrings that are repeated at least ``min_repeated`` times
    to `reduce_to`` times. For example with the default arguments, 'hhhhhh' is
    reduced to 'hh'

    TODO: Maybe change the implemention for 50x speed
    https://stackoverflow.com/questions/29481088/how-can-i-tell-if-a-string-repeats-itself-in-python/29489919#29489919

    Parameters
    ----------
    text : str
        Text to process
    min_repeated : int, optional
        Minimum number of consecutive repeated substring to consider, by default 3
    reduce_to : int, optional
        Number of substring to keep, by default 2

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        If non positive integer is passed or ``reduce_to`` is greater than
        ``min_repeated``

    Examples
    --------

    ..code-block:: python

        >>> text = "ههههههههههههههه"
        >>> reduce_repeated_substring(text)
        'هه'

    ..code-block:: python

        >>> text = "ويييييييييين راححححححححححححوا"
        >>> reduce_repeated_substring(text, reduce_to=1)
        'وين راحوا'
    """
    check_positive_integer(min_repeated, "min_repeated")
    check_positive_integer(reduce_to, "reduce_to")

    # * This might be unnecessary but for consistency with the function description
    if reduce_to > min_repeated:
        raise ValueError("`reduce_to` cannot be greater than `min_repeated`")

    pattern = r"(.+?)\1{}".format(f"{{{min_repeated-1},}}")
    return functions.replace_pattern(text, pattern, r"\1" * reduce_to)


def remove_hash_keep_tag(text: str):
    # TODO: Add function that removes only the hash sign from the hashtag
    pass


def remove_hashtags_at_end(text: str):
    # TODO: Add function that removes only hashtags that appear at the end of a text
    pass


def remove_tatweel(text: str) -> str:
    """Removes tatweel symbol :data:`~.TATWEEL` from the given text.

    Parameters
    ----------
    text : str
        Text to process

    Returns
    -------
    str
        Text with tatweel symbol removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "الحمــــــــد لله رب العــــــــــــالمـــــــيـــــن"
        >>> remove_tatweel(text)
        'الحمد لله رب العالمين'
    """
    return remove_strings(text, TATWEEL, False)


def remove_emails(text: str) -> str:
    """Removes emails using pattern :data:`~.PATTERN_EMAILS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with emails removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "يمكن استخدام الإيميل الشخصي، كمثال user1998@gmail.com"
        >>> remove_emails(text)
        'يمكن استخدام الإيميل الشخصي، كمثال'
    """
    return remove_patterns(text, PATTERN_EMAILS)


def remove_hashtags(text: str) -> str:
    """Removes hashtags (strings that start with # symbol) using pattern
    :data:`~.PATTERN_HASHTAGS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with hashtags removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "ويمكن القول أن مكة المكرمة من أجمل المناطق على وجه الأرض #السعودية"
        >>> remove_hashtags(text)
        'ويمكن القول أن مكة المكرمة من أجمل المناطق على وجه الأرض'
    """
    return remove_patterns(text, PATTERN_HASHTAGS)


def remove_links(text: str) -> str:
    """Removes links using pattern :data:`~.PATTERN_LINKS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with links removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "لمشاهدة آخر التطورات يرجى زيارة الموقع التالي: https://github.com/TRoboto/Maha"
        >>> remove_links(text)
        'لمشاهدة آخر التطورات يرجى زيارة الموقع التالي:'
    """
    return remove_patterns(text, PATTERN_LINKS)


def remove_mentions(text: str) -> str:
    """Removes mentions (strings that start with @ symbol) using pattern
    :data:`~.PATTERN_MENTIONS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with mentions removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "@test لو سمحت صديقنا تزورنا على المعرض لاستلام الجائزة"
        >>> remove_mentions(text)
        'لو سمحت صديقنا تزورنا على المعرض لاستلام الجائزة'
    """
    return remove_patterns(text, PATTERN_MENTIONS)


def remove_punctuations(text: str) -> str:
    """Removes all punctuations :data:`~.PUNCTUATIONS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with punctuations removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "مثال على الرموز الخاصة كالتالي $ ^ & * ( ) ! @"
        >>> remove_punctuations(text)
        'مثال على الرموز الخاصة كالتالي'
    """
    return remove_strings(text, PUNCTUATIONS)


def remove_english(text: str) -> str:
    """Removes all english characters :data:`~.ENGLISH` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with english removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "ومن أفضل الجامعات هي جامعة إكسفورد (Oxford University)"
        >>> remove_english(text)
        'ومن أفضل الجامعات هي جامعة إكسفورد'
    """
    return remove_strings(text, ENGLISH)


def remove_all_harakat(text: str) -> str:
    """Removes all harakat :data:`~.ALL_HARAKAT` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with all harakat removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "وَٱلصَّٰٓفَّٰتِ صَفّٗا (1) فَٱلزَّٰجِرَٰتِ زَجۡرٗا"
        >>> remove_all_harakat(text)
        'وٱلصفت صفا (1) فٱلزجرت زجرا'
    """
    return remove_strings(text, ALL_HARAKAT, False)


def remove_harakat(text: str) -> str:
    """Removes common harakat :data:`~.HARAKAT` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with common harakat removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "ألا تَرَى: كلَّ مَنْ تَرجو وتَأمَلُهُ مِنَ البَرِيَّةِ (مسكينُ بْنُ مسكينِ)"
        >>> remove_harakat(text)
        'ألا ترى: كل من ترجو وتأمله من البرية (مسكين بن مسكين)'
    """
    return remove_strings(text, HARAKAT, False)


def remove_numbers(text: str) -> str:
    """Removes all numbers :data:`~.NUMBERS` from the given text.

    Parameters
    ----------
    text : str
        Text to be processed

    Returns
    -------
    str
        Text with numbers removed.

    Example
    -------

    .. code-block:: pycon

        >>> text = "ورقم أبو تريكة في نادي الأهلي هو إثنين وعشرين (22)"
        >>> remove_numbers(text)
        'ورقم أبو تريكة في نادي الأهلي هو إثنين وعشرين ( )'
    """
    return remove_strings(text, NUMBERS)


def remove_patterns(
    text: str, patterns: Union[List[str], str], remove_spaces: bool = True
) -> str:
    r"""Removes matched characters from the given text ``text`` using input
    patterns ``patterns``

    .. note::
        Use lookahead/lookbehind when substrings should not be captured or removed.

    Parameters
    ----------
    text : str
        Text to process
    patterns : Union[List[str], str]
        Pattern(s) to use
    remove_spaces : bool, optional
        False to keep extra spaces, defaults to True

    Returns
    -------
    str
        Text with matched characters removed.

    Raises
    ------
    ValueError
        If no ``patterns`` are provided

    Example
    -------

    .. code-block:: pycon

        >>> text = "الأميرُ الغازي أرطُغرُل، أو اختصارًا أرطغرل (بالتركية: Ertuğrul)"
        >>> remove_patterns(text, r"\(.*\)")
        'الأميرُ الغازي أرطُغرُل، أو اختصارًا أرطغرل'
    """

    if not patterns:
        raise ValueError("'chars' cannot be empty.")

    # convert list to str
    if isinstance(patterns, list):
        patterns = "|".join(patterns)

    output_text = functions.replace_pattern(text, patterns, EMPTY)

    if remove_spaces:
        output_text = remove_extra_spaces(output_text)

    return output_text.strip()


def remove_strings(
    text: str, strings: Union[List[str], str], use_space: bool = True
) -> str:

    """Removes the input strings ``strings`` in the given text ``text``

    This works by replacing all input strings ``strings`` with a space,
    which means space cannot be removed. This is to help separate texts when unwanted
    strings are present without spaces. For example, 'end.start' will be converted
    to 'end start' if dot :data:`~.DOT` is passed to ``strings``.
    To disable this behavior, set ``use_space`` to False.

    .. note::
        Extra spaces (more than one space) are removed by default if ``use_space`` is
        set to True.

    Parameters
    ----------
    text : str
        Text to be processed
    strings : Union[List[str], str]
        list of strings to remove
    use_space :
        False to not replace with space, defaults to True

    Returns
    -------
    str
        Text with input strings removed.

    Raises
    ------
    ValueError
        If no ``strings`` are provided

    Example
    -------

    .. code-block:: pycon

        >>> text = "ومن الكلمات المحظورة السلاح"
        >>> remove_strings(text, "السلاح")
        'ومن الكلمات المحظورة'
    """

    if not strings:
        raise ValueError("'strings' cannot be empty.")

    # convert str to list
    if isinstance(strings, str):
        strings = [strings]

    if use_space:
        output_text = functions.replace(text, strings, SPACE)
        output_text = remove_extra_spaces(output_text)
    else:
        output_text = functions.replace(text, strings, EMPTY)

    return output_text.strip()


def remove_extra_spaces(text: str, max_spaces: int = 1) -> str:
    """Keeps a maximum of ``max_spaces`` number of spaces when extra spaces are present
    (more than one space)

    Parameters
    ----------
    text : str
        Text to be processed
    max_spaces : int, optional
        Maximum number of spaces to keep, by default 1

    Returns
    -------
    str
        Text with extra spaces removed

    Raises
    ------
    ValueError
        When a negative or float value is assigned to ``max_spaces``

    Example
    -------

    .. code-block:: pycon

        >>> text = "وكان صديقنا    العزيز   محمد من أفضل   الأشخاص الذين قابلتهم"
        >>> remove_extra_spaces(text)
        'وكان صديقنا العزيز محمد من أفضل الأشخاص الذين قابلتهم'
    """

    check_positive_integer(max_spaces, "max_spaces")

    return functions.replace_pattern(text, SPACE * max_spaces + "+", SPACE * max_spaces)


def remove_arabic_letters_dots(text: str) -> str:
    """remove the dots from ``ARABIC_LETTERS`` in the given ``text``

    Args:
        text (str): Text to be processed

    Returns:
        str: Text with dotless Arabic letters

    Example
    -------

    .. code-block:: pycon

        >>> text = "الحَمدُ للهِ الَّذي بنِعمتِه تَتمُّ الصَّالحاتُ"
        >>> remove_arabic_letters_dots(text)
        'الحَمدُ للهِ الَّدى ٮٮِعمٮِه ٮَٮمُّ الصَّالحاٮُ'

    """

    text_after = functions.keep_strings(text, ARABIC_LETTERS)

    output = []

    for index, char in enumerate(text_after):

        if char in ARABIC_Dotless_Dictionary:
            if (index + 1) < (len(text_after)):
                if char == "\u0646" and text_after[index + 1] in ARABIC_LETTERS:
                    output.append("\u066E")
                else:
                    output.append(ARABIC_Dotless_Dictionary[char])
            else:
                output.append(ARABIC_Dotless_Dictionary[char])
        else:
            if char in ARABIC_LETTERS:
                output.append(char)

    indx = 0
    Edited_text = ""

    for char in text:

        if char in ARABIC_LETTERS:
            # if char in ARABIC_LETTERS:
            Edited_text += output[indx]
            indx += 1

        else:
            Edited_text += char

    return Edited_text
