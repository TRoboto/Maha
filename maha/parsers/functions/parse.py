"""Functions that extracts values from text"""

__all__ = ["parse", "parse_expression"]

from typing import Dict, List, Optional, Union

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
    PUNCTUATIONS,
    SPACE,
    TATWEEL,
)
from maha.expressions import (
    EXPRESSION_ARABIC_HASHTAGS,
    EXPRESSION_ARABIC_MENTIONS,
    EXPRESSION_EMAILS,
    EXPRESSION_EMOJIS,
    EXPRESSION_ENGLISH_HASHTAGS,
    EXPRESSION_ENGLISH_MENTIONS,
    EXPRESSION_HASHTAGS,
    EXPRESSION_LINKS,
    EXPRESSION_MENTIONS,
)
from maha.parsers.templates import Dimension, DimensionType, TextExpression
from maha.rexy import Expression, ExpressionGroup


def parse(
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
    custom_expressions: Union[ExpressionGroup, Expression] = None,
) -> Union[List[Dimension], Dict[str, List[Dimension]]]:

    """Extracts certain characters/patterns from the given text.

    To add a new parameter, make sure that its name is the same as the corresponding
    constant. For the patterns, only remove the prefix EXPRESSION_ from the parameter name

    Parameters
    ----------
    text : str
        Text to be processed
    arabic : bool, optional
        Extract :data:`~.ARABIC` characters, by default False
    english : bool, optional
        Extract :data:`~.ENGLISH` characters, by default False
    arabic_letters : bool, optional
        Extract :data:`~.ARABIC_LETTERS` characters, by default False
    english_letters : bool, optional
        Extract :data:`~.ENGLISH_LETTERS` characters, by default False
    english_small_letters : bool, optional
        Extract :data:`~.ENGLISH_SMALL_LETTERS` characters, by default False
    english_capital_letters : bool, optional
        Extract :data:`~.ENGLISH_CAPITAL_LETTERS` characters, by default False
    numbers : bool, optional
        Extract :data:`~.NUMBERS` characters, by default False
    harakat : bool, optional
        Extract :data:`~.HARAKAT` characters, by default False
    all_harakat : bool, optional
        Extract :data:`~.ALL_HARAKAT` characters, by default False
    tatweel : bool, optional
        Extract :data:`~.TATWEEL` character, by default False
    punctuations : bool, optional
        Extract :data:`~.PUNCTUATIONS` characters, by default False
    arabic_numbers : bool, optional
        Extract :data:`~.ARABIC_NUMBERS` characters, by default False
    english_numbers : bool, optional
        Extract :data:`~.ENGLISH_NUMBERS` characters, by default False
    arabic_punctuations : bool, optional
        Extract :data:`~.ARABIC_PUNCTUATIONS` characters, by default False
    english_punctuations : bool, optional
        Extract :data:`~.ENGLISH_PUNCTUATIONS` characters, by default False
    arabic_ligatures : bool, optional
        Extract :data:`~.ARABIC_LIGATURES` words, by default False
    arabic_hashtags : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ARABIC_HASHTAGS`,
        by default False
    arabic_mentions : bool, optional
        Extract Arabic mentions using the expression :data:`~.EXPRESSION_ARABIC_MENTIONS`,
        by default False
    emails : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_EMAILS`,
        by default False
    english_hashtags : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_HASHTAGS`,
        by default False
    english_mentions : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_ENGLISH_MENTIONS`,
        by default False
    hashtags : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_HASHTAGS`,
        by default False
    links : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_LINKS`,
        by default False
    mentions : bool, optional
        Extract Arabic hashtags using the expression :data:`~.EXPRESSION_MENTIONS`,
        by default False
    emojis : bool, optional
        Extract emojis using the expression :data:`~.EXPRESSION_EMOJIS`,
        by default False
    custom_expressions : Union[:class:`~.ExpressionGroup`, :class:`~.Expression`],
        optional. Include any other string(s), by default None

    Returns
    -------
    Union[List[:class:`~.Dimension`], Dict[str, List[:class:`~.Dimension`]]]
        * If one argument is set to True, a list of dimensions is returned. Can be
        empty if no match found.
        * If more than one argument is set to True, a dictionary is returned where
        keys are the True passed arguments and the corresponding values are
        list of dimensions, any of which can be empty if no match found.

    Raises
    ------
    ValueError
        If no argument is set to True
    """

    # TODO: Maybe add `include_space` option to allow including spaces in the expressions
    # TODO: Maybe add `merge` option to allow merging of the expressions
    if not text:
        return []

    # current function arguments
    current_arguments = locals()
    constants = globals()

    output = {}

    # Since each argument has the same name as the corresponding constant
    # (But, expressions should be prefixed with "EXPRESSION_" to match the actual expression.)
    # Looping through all arguments and appending constants that correspond to the
    # True arguments can work
    # TODO: Maybe find a good pythonic way to do this
    for arg, value in current_arguments.items():
        const = constants.get(arg.upper())
        if const and value is True:
            text_exp = TextExpression(f"[{''.join(const)}]+")
            parsed = parse_expression(text, text_exp, DimensionType[arg.upper()])
            output[arg] = parsed
            continue
        # check for expression
        expression: Optional[Expression] = constants.get("EXPRESSION_" + arg.upper())
        if expression and value is True:
            text_exp = TextExpression(str(expression))
            parsed = parse_expression(text, text_exp, DimensionType[arg.upper()])
            output[arg] = parsed

    if custom_expressions:
        output["custom_expressions"] = parse_expression(text, custom_expressions)

    if not output:
        raise ValueError("At least one argument should be True")

    if len(output) == 1:
        return list(output.values())[0]

    return output


def parse_expression(
    text: str,
    expressions: Union[ExpressionGroup, Expression],
    dimension_type: DimensionType = DimensionType.GENERAL,
) -> List[Dimension]:
    """
    Extract matched strings in the given ``text`` using the input ``patterns``

    Parameters
    ----------
    text : str
        Text to check
    expressions : Union[:class:`~ExpressionGroup`, :class:`~Expression`]
        Expression(s) to use
    dimension_type : DimensionType
        Dimension type of the input ``expressions``,
        by default :attribute:`~.DimensionType.GENERAL`

    Returns
    -------
    List[:class:`~.Dimension`]
        List of extracted dimensions

    Raises
    ------
    ValueError
        If ``expressions`` are invalid
    """

    if (
        not expressions
        or (isinstance(expressions, Expression) and not expressions.pattern)
        or (isinstance(expressions, ExpressionGroup) and not expressions.expressions)
    ):
        raise ValueError("'expressions' cannot be empty.")

    # convert to ExpressionGroup
    if isinstance(expressions, Expression):
        expressions = ExpressionGroup(expressions)

    output = []
    for result in expressions.parse(text):
        start = result.start
        end = result.end
        value = result.value
        body = text[start:end]
        output.append(
            Dimension(result.expression, body, value, start, end, dimension_type)
        )

    return output
