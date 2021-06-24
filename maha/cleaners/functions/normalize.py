"""
Special functions that convert similar characters into one common character
(Characters that roughly have the same shape)
"""

__all__ = ["normalize", "normalize_lam_alef"]


from maha.constants import (
    ALEF,
    ALEF_VARIATIONS,
    ARABIC_LIGATURES,
    ARABIC_LIGATURES_NORMALIZED,
    HEH,
    LAM,
    LAM_ALEF_VARIATIONS,
    LAM_ALEF_VARIATIONS_NORMALIZED,
    PATTERN_SPACES,
    SPACE,
    TEH_MARBUTA,
    WAW,
    WAW_VARIATIONS,
    YEH,
    YEH_VARIATIONS,
)

from .replace import replace, replace_pairs, replace_pattern


def normalize(
    text: str,
    lam_alef: bool = False,
    alef: bool = False,
    waw: bool = False,
    yeh: bool = False,
    teh_marbuta: bool = False,
    ligatures: bool = False,
    spaces: bool = False,
) -> str:
    """Normalizes characters in the given text

    Parameters
    ----------
    text : str
        Text to process
    lam_alef : bool, optional
        Normalize :data:`~.LAM_ALEF_VARIATIONS` characters to :data:`~.LAM` and
        :data:`~.ALEF`, by default False
    alef : bool, optional
        Normalize :data:`~.ALEF_VARIATIONS` characters to :data:`~.ALEF`,
        by default False
    waw : bool, optional
        Normalize :data:`~.WAW_VARIATIONS` characters to :data:`~.WAW`,
        by default False
    yeh : bool, optional
        Normalize :data:`~.YEH_VARIATIONS` characters to :data:`~.YEH` and
        :data:`~.ALEF`, by default False
    teh_marbuta : bool, optional
        Normalize :data:`~.TEH_MARBUTA` characters to :data:`~.HEH`, by default False
    ligatures : bool, optional
        Normalize :data:`~.ARABIC_LIGATURES` characters to the corresponding indices
        in :data:`~.ARABIC_LIGATURES_NORMALIZED`, by default False
    spaces : bool, optional
        Normalize space variations using the pattern :data:`~.PATTERN_SPACES`,
        by default False

    Returns
    -------
    str
        Processed text

    Raises
    ------
    ValueError
        If input text is empty or no argument is set to True

    Examples
    --------
    .. code-block:: python

        >>> text = "عن أبي هريرة"
        >>> normalize(text, alef=True, teh_marbuta=True)
        'عن ابي هريره'

    .. code-block:: python

        >>> text = "قال رسول الله ﷺ"
        >>> normalize(text, ligatures=True)
        'قال رسول الله صلى الله عليه وسلم'
    """
    if not text:
        raise ValueError("Text cannot be empty")

    if not (lam_alef or alef or waw or yeh or teh_marbuta or ligatures or spaces):
        raise ValueError("At least one argument should be True")

    output = text
    if lam_alef:
        output = replace(output, LAM_ALEF_VARIATIONS, LAM + ALEF)
    if alef:
        output = replace(output, ALEF_VARIATIONS, ALEF)
    if waw:
        output = replace(output, WAW_VARIATIONS, WAW)
    if yeh:
        output = replace(output, YEH_VARIATIONS, YEH)
    if teh_marbuta:
        output = replace(output, TEH_MARBUTA, HEH)
    if ligatures:
        output = replace_pairs(output, ARABIC_LIGATURES, ARABIC_LIGATURES_NORMALIZED)
    if spaces:
        output = replace_pattern(output, PATTERN_SPACES, SPACE)

    return output


def normalize_lam_alef(text: str, keep_hamza: bool = True) -> str:
    """Normalize :data:`~.LAM_ALEF_VARIATIONS` to
    :data:`~.LAM_ALEF_VARIATIONS_NORMALIZED` If ``keep_hamza`` is True. Otherwise,
    normalize to to :data:`~.LAM` and :data:`~.ALEF`

    Parameters
    ----------
    text : str
        Text to process
    keep_hamza : bool, optional
        True to preserve hamza and madda characters, by default True

    Returns
    -------
    str
        Normalized text

    Examples
    --------
    .. code-block:: python

        >>> text = "السﻻم عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَﻷلأ وَجْهُه"
        >>> normalize_lam_alef(text)
        'السلام عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَلألأ وَجْهُه'

    .. code-block:: python

        >>> text = "اﻵن يا أصحابي"
        >>> normalize_lam_alef(text, keep_hamza=False)
        'الان يا أصحابي'
    """
    if keep_hamza:
        output = replace_pairs(
            text, LAM_ALEF_VARIATIONS, LAM_ALEF_VARIATIONS_NORMALIZED
        )
    else:
        output = replace(text, LAM_ALEF_VARIATIONS, LAM + ALEF)

    return output


# def normalize_hamza(text: str):
#     ? Should this method be implemented?
#     * This method normalizes [HAMZA_WAW, HAMZA_YA, HAMZA] to HAMZA
#     raise NotImplementedError()
