:py:mod:`maha.cleaners.functions.normalize_fn`
==============================================

.. py:module:: maha.cleaners.functions.normalize_fn

.. autoapi-nested-parse::

   Special functions that convert similar characters into one common character
   (Characters that roughly have the same shape)



Module Contents
---------------


Functions
~~~~~~~~~

.. autosummary::

   normalize
   normalize_lam_alef
   normalize_small_alef



.. py:function:: normalize(text, lam_alef = None, alef = None, waw = None, yeh = None, teh_marbuta = None, ligatures = None, spaces = None, all = False)

   Normalizes characters in the given text

   :param text: Text to process
   :type text: str
   :param lam_alef: Normalize :data:`~.LAM_ALEF_VARIATIONS` characters to :data:`~.LAM` and
                    :data:`~.ALEF`, by default None
   :type lam_alef: bool, optional
   :param alef: Normalize :data:`~.ALEF_VARIATIONS` characters to :data:`~.ALEF`,
                by default None
   :type alef: bool, optional
   :param waw: Normalize :data:`~.WAW_VARIATIONS` characters to :data:`~.WAW`,
               by default None
   :type waw: bool, optional
   :param yeh: Normalize :data:`~.YEH_VARIATIONS` characters to :data:`~.YEH` and
               :data:`~.ALEF`, by default None
   :type yeh: bool, optional
   :param teh_marbuta: Normalize :data:`~.TEH_MARBUTA` characters to :data:`~.HEH`, by default None
   :type teh_marbuta: bool, optional
   :param ligatures: Normalize :data:`~.ARABIC_LIGATURES` characters to the corresponding indices
                     in :data:`~.ARABIC_LIGATURES_NORMALIZED`, by default None
   :type ligatures: bool, optional
   :param spaces: Normalize space variations using the expression :data:`~.EXPRESSION_ALL_SPACES`,
                  by default None
   :type spaces: bool, optional
   :param all: Do all normalization except the ones that are set to False, by default False
   :type all: bool, optional

   :returns: Processed text
   :rtype: str

   :raises ValueError: If no argument is set to True

   .. rubric:: Examples

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


.. py:function:: normalize_lam_alef(text, keep_hamza = True)

   Normalize :data:`~.LAM_ALEF_VARIATIONS` to
   :data:`~.LAM_ALEF_VARIATIONS_NORMALIZED` If ``keep_hamza`` is True. Otherwise,
   normalize to :data:`~.LAM` and :data:`~.ALEF`

   :param text: Text to process
   :type text: str
   :param keep_hamza: True to preserve hamza and madda characters, by default True
   :type keep_hamza: bool, optional

   :returns: Normalized text
   :rtype: str

   .. rubric:: Examples

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


.. py:function:: normalize_small_alef(text, keep_madda = True, normalize_end = False)

   Normalize :data:`~.ALEF_SUPERSCRIPT` to :data:`~.ALEF`. If ``keep_madda`` is True
   and :data:`~.ALEF_SUPERSCRIPT` is followed by :data:`HAMZA_ABOVE`, then normalize
   to :data:`~.ALEF_MADDA_ABOVE`

   :param text: Text to process
   :type text: str
   :param keep_madda: True to preserve madda character, by default True
   :type keep_madda: bool, optional
   :param normalize_end: True to normalize :data:`~.ALEF_SUPERSCRIPT` that appear at the end of a word,
                         by default False
   :type normalize_end: bool, optional

   :returns: Normalized text
   :rtype: str

   .. rubric:: Example

   .. code:: pycon

       >>> from maha.cleaners.functions import normalize_small_alef
       >>> text = "وَٱلصَّٰٓفَّٰتِ صَفّٗا"
       >>> normalize_small_alef(text)
       'وَٱلصَّآفَّاتِ صَفّٗا'


