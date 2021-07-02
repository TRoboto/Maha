import pytest


@pytest.fixture()
def simple_text_input():
    return " 1. بِسْمِ،اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ In the name of Allah,Most Gracious, Most Merciful. "


@pytest.fixture()
def multiple_tweets():
    return """
 الساعة الآن 12:00 في اسبانيا 🇪🇸, انتهى بشكل رسمي عقد الأسطورة ليو ميسي مع برشلونة . .
 طبعا بكونو حاطين المكيف ع٣ مئوية وخود تقلبات وبرد وحر وCNS وزعيق المراقب وألف نيلة وقر فتحت اشوف درجة الحرارة هتبقي كام يو الامتحان لقيتها ٤٢ والامتحان الساعه ١ فعايز انورماليز اننا ننزل بالفالنه الحمالات Hot fac
 يسعدلي مساكم ❤🌹 شرح كلمة zwa هالمنشور رح تلاقو (zwar) سهل و لذيذ (aber) ناقصو شوية ملح وكزبر #منقو
 مـعلش استحملوني ب الاصفر هالفتره 💛 #ريشـه
 لما حد يسالني بتختفي كتير لية =..
 زيِّنوا ليلة الجمع بالصلاة على النَّبِيِّ ﷺ" ❤
 #Windows11 is on the horizon. What feature are you looking forward to
 Get vaccinate #savethesaviour
 Today I am beginning project on 10 days duratio #30daysofcod #DEVCommunit
"""
