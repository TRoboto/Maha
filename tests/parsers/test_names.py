from maha.parsers.functions import parse_dimension

BOYS = [
    "محمد",
    "أحمد",
    "يوسف",
    "عمر",
    "علي",
    "عبد الله",
    "آدم",
    "ياسين",
    "عبد الرحمن",
    "إياد",
    "نوح",
    "عرفان",
    "وليام",
    "جاك",
    "توماس",
    "بول",
    "لوكاس",
    "يونس",
    "ليون",
    "ديفيد (داوود)",
    "دانيال",
    "رافاييل",
    "ريان",
    "حمود",
]
GIRLS = [
    "لمار",
    "تالا",
    "دانة/",
    "فرح/ردينة",
    "ريتال",
    "ريم",
    "زينب",
    "ليان",
    "فريدة",
    "هنا/جودي/ريماس",
    "شهد،زهراء",
    "آنا",
    "ماري",
    "ميا",
    "إيما",
    "لارا",
    "سارة",
    "لورا",
    "فالنتينا",
    "ليا",
    "جوليا",
]


def test_names_of_boys():
    output = parse_dimension(" ".join(BOYS), names=True)
    assert len(output) == 25
    assert output[0].value == "محمد"


def test_names_of_girls():
    output = parse_dimension(" ".join(GIRLS), names=True)
    assert len(output) == 25
    assert output[-1].value == "جوليا"
