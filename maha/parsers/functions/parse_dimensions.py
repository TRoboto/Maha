from __future__ import annotations

__all__ = ["parse_dimension"]


from maha.parsers.rules import (
    RULE_DURATION,
    RULE_NAME,
    RULE_NUMERAL,
    RULE_ORDINAL,
    RULE_TIME,
)
from maha.parsers.templates import Dimension, DimensionType
from maha.rexy import Expression


def parse_dimension(
    text: str,
    amount_of_money: bool | None = None,
    duration: bool | None = None,
    distance: bool | None = None,
    numeral: bool | None = None,
    ordinal: bool | None = None,
    quantity: bool | None = None,
    temperature: bool | None = None,
    time: bool | None = None,
    volume: bool | None = None,
    names: bool | None = None,
) -> list[Dimension]:
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

    if amount_of_money:
        raise NotImplementedError("amount_of_money is not implemented yet")
    if duration:
        output.extend(_get_dimensions(RULE_DURATION, text, DimensionType.DURATION))
    if distance:
        raise NotImplementedError("distance is not implemented yet")
    if numeral:
        output.extend(_get_dimensions(RULE_NUMERAL, text, DimensionType.NUMERAL))
    if ordinal:
        output.extend(_get_dimensions(RULE_ORDINAL, text, DimensionType.ORDINAL))
    if quantity:
        raise NotImplementedError("quantity is not implemented yet")
    if temperature:
        raise NotImplementedError("temperature is not implemented yet")
    if time:
        output.extend(_get_dimensions(RULE_TIME, text, DimensionType.TIME))
    if volume:
        raise NotImplementedError("volume is not implemented yet")
    if names:
        output.extend(_get_dimensions(RULE_NAME, text, DimensionType.NAME))

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
            names,
        ]
    ):
        raise ValueError("At least one argument should be True")

    return output


def _get_dimensions(
    rule: Expression, text: str, dimension_type: DimensionType
) -> list[Dimension]:
    output = []
    for result in rule(text):
        output.append(
            Dimension(
                result.expression,
                text[result.start : result.end],
                result.value,
                result.start,
                result.end,
                dimension_type,
            )
        )
    return output
