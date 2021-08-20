__all__ = ["parse_dimension"]

from typing import List

from maha.parsers.templates import Dimension, DimensionType, Rule


def parse_dimension(
    text: str,
    amount_of_money: bool = None,
    duration: bool = None,
    distance: bool = None,
    numeral: bool = None,
    ordinal: bool = None,
    quantity: bool = None,
    temperature: bool = None,
    time: bool = None,
    volume: bool = None,
) -> List[Dimension]:
    """Extract dimensions from a given text.

    Parameters
    ----------
    text : str
        Text to extract dimensions from
    amount_of_money : bool, optional
        Extract amount of money using the rule :data:`~.RULE_AMOUNT_OF_MONEY`,
        by default None
    duration : bool, optional
        Extract duration using the rule :data:`~.RULE_DURATION`,
        by default None
    distance : bool, optional
        Extract distance using the rule :data:`~.RULE_DISTANCE`,
        by default None
    numeral : bool, optional
        Extract numeral using the rule :data:`~.RULE_NUMERAL`,
        by default None
    ordinal : bool, optional
        Extract ordinal using the rule :data:`~.RULE_ORDINAL`,
        by default None
    quantity : bool, optional
        Extract quantity using the rule :data:`~.RULE_QUANTITY`,
        by default None
    temperature : bool, optional
        Extract temperature using the rule :data:`~.RULE_TEMPERATURE`,
        by default None
    time : bool, optional
        Extract time using the rule :data:`~.RULE_TIME`,
        by default None
    volume : bool, optional
        Extract volume using the rule :data:`~.RULE_VOLUME`,
        by default None

    Returns
    -------
    List[:class:`~.Dimension`]
        List of :class:`~.Dimension` objects extracted from the text

    Raises
    ------
    ValueError
        If no argument is set to True
    """
    output = []

    if duration:
        output.extend(_get_dimensions(Rule.get("duration"), text))
    if numeral:
        output.extend(_get_dimensions(Rule.get("numeral"), text))
    if ordinal:
        output.extend(_get_dimensions(Rule.get("ordinal"), text))

    if not any(
        [
            amount_of_money,
            duration,
            distance,
            numeral,
            ordinal,
            quantity,
            temperature,
            time,
            volume,
        ]
    ):
        raise ValueError("At least one argument should be True")

    return output


def _get_dimensions(rule: Rule, text: str) -> List[Dimension]:
    output = []
    for result in rule.apply(text):
        output.append(
            Dimension(
                result.expression,
                text[result.start : result.end],
                result.value,
                result.start,
                result.end,
                DimensionType[rule.name.upper()],
            )
        )
    return output
