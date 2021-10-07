from tqdm import tqdm

from maha.datasets import load_dataset
from maha.parsers.rules.common import EXPRESSION_END, EXPRESSION_START
from maha.rexy import Expression, capture_group

names = load_dataset("names")
cleaned_names = []
for name in tqdm(names, desc="Loading names"):
    if name.cleaned_name not in cleaned_names:
        cleaned_names.append(name.cleaned_name)

print("Number of total cleaned names:", len(cleaned_names))

# cache the cleaned names
Expression(
    EXPRESSION_START + capture_group(*cleaned_names) + EXPRESSION_END, pickle=True
).compile()
