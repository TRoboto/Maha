"""
Special functions that convert similar characters into one common character
(Characters that roughly have the same shape)
"""
from __future__ import annotations

__all__ = ["normalize", "normalize_lam_alef", "normalize_small_alef"]


import maha.cleaners.functions as functions
from maha.constants import (
    ALEF,
    ALEF_MADDA_ABOVE,
    ALEF_SUPERSCRIPT,
    ALEF_VARIATIONS,
    ARABIC_LIGATURES,
    ARABIC_LIGATURES_NORMALIZED,
    EMPTY,
    HEH,
    LAM,
    LAM_ALEF_VARIATIONS,
    LAM_ALEF_VARIATIONS_NORMALIZED,
    MADDAH_ABOVE,
    SPACE,
    TEH_MARBUTA,
    WAW,
    WAW_VARIATIONS,
    YEH,
    YEH_VARIATIONS,
)
from maha.expressions import EXPRESSION_ALL_SPACES


def normalize(
    text: str,
    lam_alef: bool | None = None,
    alef: bool | None = None,
    waw: bool | None = None,
    yeh: bool | None = None,
    teh_marbuta: bool | None = None,
    ligatures: bool | None = None,
    spaces: bool | None = None,
    all: bool = False,
) -> str:
    """Normalizes characters in the given text

    Parameters
    ----------
    text : str
        Text to process
    lam_alef : bool, optional
        Normalize :data:`~.LAM_ALEF_VARIATIONS` characters to :data:`~.LAM` and
        :data:`~.ALEF`, by default None
    alef : bool, optional
        Normalize :data:`~.ALEF_VARIATIONS` characters to :data:`~.ALEF`,
        by default None
    waw : bool, optional
        Normalize :data:`~.WAW_VARIATIONS` characters to :data:`~.WAW`,
        by default None
    yeh : bool, optional
        Normalize :data:`~.YEH_VARIATIONS` characters to :data:`~.YEH` and
        :data:`~.ALEF`, by default None
    teh_marbuta : bool, optional
        Normalize :data:`~.TEH_MARBUTA` characters to :data:`~.HEH`, by default None
    ligatures : bool, optional
        Normalize :data:`~.ARABIC_LIGATURES` characters to the corresponding indices
        in :data:`~.ARABIC_LIGATURES_NORMALIZED`, by default None
    spaces : bool, optional
        Normalize space variations using the expression :data:`~.EXPRESSION_ALL_SPACES`,
        by default None
    all : bool, optional
        Do all normalization except the ones that are set to False, by default False

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
    .. code:: pycon

        >>> from maha.cleaners.functions import normalize
        >>> text = "عن أبي هريرة"
        >>> normalize(text, alef=True, teh_marbuta=True)
        'عن ابي هريره'

    .. code:: pycon

        >>> from maha.cleaners.functions import normalize
        >>> text = "قال رسول الله ﷺ"
        >>> normalize(text, ligatures=True)
        'قال رسول الله صلى الله عليه وسلم'

    .. code:: pycon

        >>> from maha.cleaners.functions import normalize
        >>> text = "قال مؤمن: ﷽ قل هو ﷲ أحد"
        ... # For space
        >>> normalize(text, all=True, waw=False)
        'قال مؤمن: بسم الله الرحمن الرحيم قل هو الله احد'
    """
    if not text:
        return EMPTY

    if not (
        lam_alef or alef or waw or yeh or teh_marbuta or ligatures or spaces or all
    ):
        raise ValueError("At least one argument should be True")

    output = text
    if lam_alef or (all and lam_alef is not False) or (all and lam_alef is not False):
        output = functions.replace(output, LAM_ALEF_VARIATIONS, LAM + ALEF)
    if alef or (all and alef is not False):
        output = functions.replace(output, ALEF_VARIATIONS, ALEF)
    if waw or (all and waw is not False):
        output = functions.replace(output, WAW_VARIATIONS, WAW)
    if yeh or (all and yeh is not False):
        output = functions.replace(output, YEH_VARIATIONS, YEH)
    if teh_marbuta or (all and teh_marbuta is not False):
        output = functions.replace(output, TEH_MARBUTA, HEH)
    if ligatures or (all and ligatures is not False):
        output = functions.replace_pairs(
            output, ARABIC_LIGATURES, ARABIC_LIGATURES_NORMALIZED
        )
    if spaces or (all and spaces is not False):
        output = functions.replace_expression(output, EXPRESSION_ALL_SPACES, SPACE)

    return output


def normalize_lam_alef(text: str, keep_hamza: bool = True) -> str:
    """Normalize :data:`~.LAM_ALEF_VARIATIONS` to
    :data:`~.LAM_ALEF_VARIATIONS_NORMALIZED` If ``keep_hamza`` is True. Otherwise,
    normalize to :data:`~.LAM` and :data:`~.ALEF`

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
    .. code:: pycon

        >>> from maha.cleaners.functions import normalize_lam_alef
        >>> text = "السﻻم عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَﻷلأ وَجْهُه"
        >>> normalize_lam_alef(text)
        'السلام عليكم أحبتي، قالوا في صِفَةِ رَسُولِ الله يتَلألأ وَجْهُه'

    .. code:: pycon

        >>> from maha.cleaners.functions import normalize_lam_alef
        >>> text = "اﻵن يا أصحابي"
        >>> normalize_lam_alef(text, keep_hamza=False)
        'الان يا أصحابي'
    """
    if keep_hamza:
        output = functions.replace_pairs(
            text, LAM_ALEF_VARIATIONS, LAM_ALEF_VARIATIONS_NORMALIZED
        )
    else:
        output = functions.replace(text, LAM_ALEF_VARIATIONS, LAM + ALEF)

    return output


def normalize_small_alef(
    text: str, keep_madda: bool = True, normalize_end: bool = False
) -> str:
    """Normalize :data:`~.ALEF_SUPERSCRIPT` to :data:`~.ALEF`. If ``keep_madda`` is True
    and :data:`~.ALEF_SUPERSCRIPT` is followed by :data:`HAMZA_ABOVE`, then normalize
    to :data:`~.ALEF_MADDA_ABOVE`

    Parameters
    ----------
    text : str
        Text to process
    keep_madda : bool, optional
        True to preserve madda character, by default True
    normalize_end : bool, optional
        True to normalize :data:`~.ALEF_SUPERSCRIPT` that appear at the end of a word,
        by default False

    Returns
    -------
    str
        Normalized text

    Example
    -------
    .. code:: pycon

        >>> from maha.cleaners.functions import normalize_small_alef
        >>> text = "وَٱلصَّٰٓفَّٰتِ صَفّٗا"
        >>> normalize_small_alef(text)
        'وَٱلصَّآفَّاتِ صَفّٗا'
    """
    output = text
    if keep_madda:
        output = functions.replace_pairs(
            text, [ALEF_SUPERSCRIPT + MADDAH_ABOVE], [ALEF_MADDA_ABOVE]
        )
    if not normalize_end:
        output = functions.replace_expression(
            output, rf"{ALEF_SUPERSCRIPT}(?!\s|$)", ALEF
        )
    else:
        output = functions.replace(output, ALEF_SUPERSCRIPT, ALEF)

    return output


# def normalize_hamza(text: str):
#     ? Should this method be implemented?
#     * This method normalizes [HAMZA_WAW, HAMZA_YA, HAMZA] to HAMZA
#     raise NotImplementedError()
