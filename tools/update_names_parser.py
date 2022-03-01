import datasets
from tqdm import tqdm

from maha.cleaners.functions import keep
from maha.parsers.rules.common import EXPRESSION_END, EXPRESSION_START
from maha.rexy import Expression, capture_group

names = datasets.load_dataset("TRoboto/names")["train"]
cleaned_names = []
for name in tqdm(names, desc="Loading names"):
    name = keep(name["name"], arabic_letters=True)
    if name not in cleaned_names:
        cleaned_names.append(name)

print("Number of total cleaned names:", len(cleaned_names))

# cache the cleaned names
Expression(
    EXPRESSION_START + capture_group(*cleaned_names) + EXPRESSION_END, pickle=True
).compile()
